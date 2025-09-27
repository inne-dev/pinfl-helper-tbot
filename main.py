"""Module providing receiving requests from users in a telegram bot."""

import datetime
import os
import random
from functools import wraps
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
)
from pinfl_utilities_generator import PinflUtilitiesGenerator
from pinfl_utilities_parser import PinflUtilitiesParser
from database import Database
from translations import get_text, get_month_name, LANGUAGES

# Initialize database
db = Database()

# Statistics are available to all users for transparency and interest


def with_user_context(log_request_type=None):
    """
    Decorator for automatic user registration and context retrieval.
    Similar to before_action in Rails.

    Args:
        log_request_type: Request type for logging ('generate', 'analyze', None)
    """

    def decorator(func):
        @wraps(func)
        def wrapper(update, context):
            # Get user
            user = update.effective_user
            if not user:
                return

            user_id = user.id

            # Register or update user
            user_data = db.get_user(user_id)
            if not user_data:
                # New user
                db.add_user(
                    user_id=user_id,
                    username=user.username,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    language_code=user.language_code or "ru",
                )
                user_lang = user.language_code or "ru"
                is_new_user = True
            else:
                # Update existing user activity
                db.update_last_activity(user_id)
                user_lang = user_data["language_code"]
                is_new_user = False

            # Log request if needed
            if log_request_type:
                db.add_request(user_id, log_request_type)

            # Add context to context object
            context.user_data.update(
                {"user_id": user_id, "user_lang": user_lang, "is_new_user": is_new_user}
            )

            # Call original function
            return func(update, context)

        return wrapper

    return decorator


def get_user_context(context):
    """Get user context from context."""
    return (
        context.user_data.get("user_id"),
        context.user_data.get("user_lang", "ru"),
        context.user_data.get("is_new_user", False),
    )


@with_user_context()
def start(update, context):
    """Handle the start command."""
    user_id, user_lang, is_new_user = get_user_context(context)

    if is_new_user:
        # For new users, show language selection first
        show_language_selection(update, context, is_initial=True)
    else:
        # For existing users, show start message immediately
        send_start_message(update, user_lang)


def show_language_selection(update, context, is_initial=False):
    """Show language selection."""
    user_id, user_lang, _ = get_user_context(context)

    keyboard = []
    for code, name in LANGUAGES.items():
        callback_data = f"lang_{code}_initial" if is_initial else f"lang_{code}"
        keyboard.append([InlineKeyboardButton(name, callback_data=callback_data)])

    reply_markup = InlineKeyboardMarkup(keyboard)
    message_key = "initial_language_selection" if is_initial else "language_selection"
    message = get_text(message_key, user_lang)

    if update.message:
        update.message.reply_text(message, reply_markup=reply_markup)
    elif update.callback_query:
        update.callback_query.message.edit_text(message, reply_markup=reply_markup)


def send_start_message(update, user_lang):
    """Send start message."""
    message = get_text("start_message", user_lang)
    if update.message:
        update.message.reply_text(message)
    elif update.callback_query:
        update.callback_query.message.edit_text(message)


@with_user_context()
def language_command(update, context):
    """Handle language selection command."""
    show_language_selection(update, context, is_initial=False)


def language_callback(update, context):
    """Handle language selection callback."""
    query = update.callback_query
    query.answer()

    user_id = query.from_user.id
    callback_data = query.data

    # Check if this is initial language selection
    is_initial = callback_data.endswith("_initial")
    if is_initial:
        lang_code = callback_data.replace("_initial", "").split("_")[1]
    else:
        lang_code = callback_data.split("_")[1]

    if lang_code in LANGUAGES:
        # Update language in database
        db.update_user_language(user_id, lang_code)

        if is_initial:
            # For initial selection, show start message
            message = get_text("start_message", lang_code)
            query.edit_message_text(message)
        else:
            # For regular language change, show confirmation
            message = get_text("language_changed", lang_code)
            query.edit_message_text(message)


@with_user_context(log_request_type="analyze")
def echo(update, context):
    """Handle PINFL analysis."""
    user_id, user_lang, _ = get_user_context(context)

    pinfl_text = update.message.text.strip()

    if pinfl_text.isdigit() and len(pinfl_text) >= 14:
        parser = PinflUtilitiesParser(pinfl_text)

        if parser.is_valid():
            response = get_text("pinfl_valid", user_lang, birth_date=parser.birth_date)
        else:
            response = get_text("pinfl_invalid_header", user_lang)

            if not parser.is_valid_date():
                response += get_text("invalid_date", user_lang)
            if not parser.validate_check_digit():
                correct_check_digit = parser.calculate_check_digit()
                response += get_text(
                    "invalid_check_digit", user_lang, correct_digit=correct_check_digit
                )
            if not parser.validate_area_code():
                response += get_text("invalid_area_code", user_lang)
            if not parser.validate_citizen_serial_number():
                response += get_text("invalid_serial_number", user_lang)
    else:
        response = get_text("pinfl_format_error", user_lang)

    update.message.reply_text(response)


@with_user_context(log_request_type="generate")
def generate_pinfl(update, context):
    """Handle PINFL generation."""
    user_id, user_lang, _ = get_user_context(context)

    generator = PinflUtilitiesGenerator()
    gender = random.choice(["male", "female"])
    birth_date = datetime.date(
        random.randint(1900, datetime.date.today().year - 19),
        random.randint(1, 12),
        random.randint(1, 28),
    )

    pinfl = generator.generate(gender, birth_date)

    # Translate gender
    gender_text = get_text(f"gender_{gender}", user_lang)

    info_text = get_text(
        "generated_pinfl", user_lang, birth_date=birth_date, gender=gender_text
    )

    update.message.reply_text(
        f"<pre>{pinfl}</pre>\n{info_text}",
        parse_mode="HTML",
    )


@with_user_context()
def stats(update, context):
    """Handle statistics command (available to all users)."""
    user_id, user_lang, _ = get_user_context(context)

    # Stats are available to all users to show bot popularity and usage

    # Get current month stats
    now = datetime.datetime.now()
    stats_data = db.get_monthly_stats(now.year, now.month)

    month_name = get_month_name(now.month, user_lang)

    # Format statistics message
    title = get_text("stats_title", user_lang, month=month_name, year=now.year)
    generate_line = get_text(
        "stats_generate_requests", user_lang, count=stats_data["generate_requests"]
    )
    analyze_line = get_text(
        "stats_analyze_requests", user_lang, count=stats_data["analyze_requests"]
    )
    new_users_line = get_text(
        "stats_new_users", user_lang, count=stats_data["new_users"]
    )
    total_users_line = get_text(
        "stats_total_users", user_lang, count=stats_data["total_users"]
    )

    message = f"{title}\n\n{generate_line}\n{analyze_line}\n{new_users_line}\n{total_users_line}"

    update.message.reply_text(message)


@with_user_context()
def issues(update, context):
    """Handle issues command."""
    user_id, user_lang, _ = get_user_context(context)

    issue_link = os.environ.get("ISSUE_LINK", "")
    message = get_text("issues_message", user_lang, issue_link=issue_link)

    update.message.reply_text(message, parse_mode="HTML")


def error_handler(update, context):
    """Handle errors."""
    import traceback

    print(f"Update {update} caused error {context.error}")
    print(f"Traceback: {traceback.format_exc()}")


def main():
    """Entry point."""
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        print("Error: TELEGRAM_BOT_TOKEN environment variable is not set")
        return

    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    # Command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("generate", generate_pinfl))
    dp.add_handler(CommandHandler("language", language_command))
    dp.add_handler(CommandHandler("stats", stats))
    dp.add_handler(CommandHandler("issues", issues))

    # Callback query handler for language selection
    dp.add_handler(CallbackQueryHandler(language_callback, pattern="^lang_.*"))

    # Message handler for PINFL analysis
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Error handler
    dp.add_error_handler(error_handler)

    print("Bot launched successfully")

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
