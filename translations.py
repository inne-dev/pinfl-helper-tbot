"""Translations and localization for the PINFL Helper Telegram Bot."""

from typing import Any

# Available languages
LANGUAGES = {"uz": "O'zbekcha", "ru": "Русский", "en": "English"}

# Translation dictionary
TRANSLATIONS = {
    "start_message": {
        "uz": (
            "Salom! PINFL tahlil qilish uchun menga yuboring va men uning to'g'ri yoki noto'g'ri ekanligini aytaman.\n"
            "Mavjud buyruqlar:\n"
            "/start - Bot bilan ishlashni boshlash\n"
            "/generate - Tasodifiy PINFL yaratish\n"
            "/language - Tilni tanlash\n"
            "/stats - Oylik statistika (shaffoflik uchun)\n"
            "/issues - Muammo haqida xabar berish\n"
            "Yoki tahlil qilish uchun oddiy xabar sifatida PINFL yuborishingiz mumkin."
        ),
        "ru": (
            "Привет! Отправь мне PINFL для анализа и я скажу валидный он или нет.\n"
            "Доступные команды:\n"
            "/start - Начать работу с ботом\n"
            "/generate - Сгенерировать случайный PINFL\n"
            "/language - Выбрать язык\n"
            "/stats - Месячная статистика (для прозрачности)\n"
            "/issues - Сообщить о проблеме\n"
            "Или вы можете отправить мне PINFL для анализа обычным сообщением."
        ),
        "en": (
            "Hello! Send me a PINFL for analysis and I'll tell you if it's valid or not.\n"
            "Available commands:\n"
            "/start - Start working with the bot\n"
            "/generate - Generate random PINFL\n"
            "/language - Choose language\n"
            "/stats - Monthly statistics (for transparency)\n"
            "/issues - Report an issue\n"
            "Or you can send me PINFL as a regular message for analysis."
        ),
    },
    "language_selection": {
        "uz": "Tilni tanlang:",
        "ru": "Выберите язык:",
        "en": "Choose language:",
    },
    "initial_language_selection": {
        "uz": "Xush kelibsiz! Bot bilan ishlashni boshlash uchun tilni tanlang:",
        "ru": "Добро пожаловать! Выберите язык для работы с ботом:",
        "en": "Welcome! Choose a language to work with the bot:",
    },
    "language_changed": {
        "uz": "Til muvaffaqiyatli o'zgartirildi!",
        "ru": "Язык успешно изменен!",
        "en": "Language changed successfully!",
    },
    "pinfl_valid": {
        "uz": "PINFL to'g'ri.\nTug'ilgan sana: {birth_date}",
        "ru": "PINFL действителен.\nДата рождения: {birth_date}",
        "en": "PINFL is valid.\nDate of birth: {birth_date}",
    },
    "pinfl_invalid_header": {
        "uz": "Noto'g'ri PINFL. Quyidagi xatolarni tekshiring:\n",
        "ru": "Неверный PINFL. Проверьте следующие ошибки:\n",
        "en": "Invalid PINFL. Check the following errors:\n",
    },
    "invalid_date": {
        "uz": "- Noto'g'ri tug'ilgan sana.\n",
        "ru": "- Неправильная дата рождения.\n",
        "en": "- Invalid date of birth.\n",
    },
    "invalid_check_digit": {
        "uz": "- Noto'g'ri nazorat raqami. Kutilgan nazorat raqami: {correct_digit}\n",
        "ru": "- Неправильная контрольная цифра. Ожидаемая контрольная цифра: {correct_digit}\n",
        "en": "- Invalid check digit. Expected check digit: {correct_digit}\n",
    },
    "invalid_area_code": {
        "uz": "- Noto'g'ri hudud kodi.\n",
        "ru": "- Неправильный код региона.\n",
        "en": "- Invalid area code.\n",
    },
    "invalid_serial_number": {
        "uz": "- Noto'g'ri fuqaro seriya raqami.\n",
        "ru": "- Неправильный серийный номер гражданина.\n",
        "en": "- Invalid citizen serial number.\n",
    },
    "pinfl_format_error": {
        "uz": (
            "Noto'g'ri PINFL. U faqat raqamlardan iborat bo'lishi "
            "va kamida 14 ta belgidan iborat bo'lishi kerakligini tekshiring."
        ),
        "ru": (
            "Неверный PINFL. Проверьте, что он содержит только "
            "цифры и имеет длину не менее 14 символов."
        ),
        "en": (
            "Invalid PINFL. Check that it contains only "
            "digits and is at least 14 characters long."
        ),
    },
    "generated_pinfl": {
        "uz": "Tug'ilgan sana: {birth_date}\nJins: #{gender}",
        "ru": "Дата рождения: {birth_date}\nПол: #{gender}",
        "en": "Date of birth: {birth_date}\nGender: #{gender}",
    },
    "gender_male": {"uz": "erkak", "ru": "мужской", "en": "male"},
    "gender_female": {"uz": "ayol", "ru": "женский", "en": "female"},
    "issues_message": {
        "uz": (
            "Agar sizda muammolar bo'lsa yoki takliflaringiz bo'lsa, "
            'iltimos, loyiha <a href="{issue_link}">issue</a> qoldiring.'
        ),
        "ru": (
            "Если у вас возникли проблемы или у вас есть предложения, "
            'пожалуйста, оставьте <a href="{issue_link}">issue</a> проекта.'
        ),
        "en": (
            "If you have problems or suggestions, please leave an "
            '<a href="{issue_link}">issue</a> on the project.'
        ),
    },
    "stats_title": {
        "uz": "📊 {month}/{year} statistikasi:",
        "ru": "📊 Статистика за {month}/{year}:",
        "en": "📊 Statistics for {month}/{year}:",
    },
    "stats_generate_requests": {
        "uz": "🔢 Yaratish so'rovlari: {count}",
        "ru": "🔢 Запросы генерации: {count}",
        "en": "🔢 Generate requests: {count}",
    },
    "stats_analyze_requests": {
        "uz": "🔍 Tahlil so'rovlari: {count}",
        "ru": "🔍 Запросы анализа: {count}",
        "en": "🔍 Analyze requests: {count}",
    },
    "stats_new_users": {
        "uz": "👥 Yangi foydalanuvchilar: {count}",
        "ru": "👥 Новые пользователи: {count}",
        "en": "👥 New users: {count}",
    },
    "stats_total_users": {
        "uz": "📈 Jami foydalanuvchilar: {count}",
        "ru": "📈 Всего пользователей: {count}",
        "en": "📈 Total users: {count}",
    },
    "month_names": {
        "uz": [
            "Yanvar",
            "Fevral",
            "Mart",
            "Aprel",
            "May",
            "Iyun",
            "Iyul",
            "Avgust",
            "Sentyabr",
            "Oktyabr",
            "Noyabr",
            "Dekabr",
        ],
        "ru": [
            "Январь",
            "Февраль",
            "Март",
            "Апрель",
            "Май",
            "Июнь",
            "Июль",
            "Август",
            "Сентябрь",
            "Октябрь",
            "Ноябрь",
            "Декабрь",
        ],
        "en": [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ],
    },
}


def get_text(key: str, lang: str = "ru", **kwargs: Any) -> str:
    """Get translated text by key and language."""
    if key not in TRANSLATIONS:
        return key

    if lang not in TRANSLATIONS[key]:
        lang = "ru"  # fallback to Russian

    text = TRANSLATIONS[key][lang]

    # Handle list case (like month_names)
    if isinstance(text, list):
        return str(text)

    # Format text with provided arguments
    if kwargs:
        try:
            return text.format(**kwargs)
        except KeyError:
            return text

    return text


def get_month_name(month: int, lang: str = "ru") -> str:
    """Get month name by number and language."""
    if month < 1 or month > 12:
        return str(month)

    if lang not in TRANSLATIONS["month_names"]:
        lang = "ru"

    return TRANSLATIONS["month_names"][lang][month - 1]
