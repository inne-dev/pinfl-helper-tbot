"""Translations and localization for the PINFL Helper Telegram Bot."""

from typing import Any

# Available languages
LANGUAGES = {"uz": "O'zbekcha", "ru": "Русский", "en": "English"}

# Translation dictionary
TRANSLATIONS = {
    "start_message": {
        "uz": (
            "Salom! PINFL tahlil qilish uchun menga yuboring va men uning to'g'ri yoki noto'g'ri ekanligini aytaman.\n"
            "Mavjud buyruqlar:\n\n"
            "/generate - Tasodifiy PINFL yaratish\n"
            "/generate_custom - Muayyan qiymatlar bilan PINFL yarating\n"
            "Yoki tahlil qilish uchun oddiy xabar sifatida PINFL yuborishingiz mumkin.\n\n"
            "/start - Bot bilan ishlashni boshlash\n"
            "/help - Bot haqida ma'lumot\n"
            "/language - Tilni tanlash\n"
            "/stats - Oylik statistika\n"
            "/issues - Muammo haqida xabar berish\n"
        ),
        "ru": (
            "Привет! Отправь мне PINFL для анализа и я скажу валидный он или нет.\n"
            "Доступные команды:\n\n"
            "/generate - Сгенерировать случайный PINFL\n"
            "/generate_custom - Создать PINFL с определенными значениями\n"
            "Или вы можете отправить мне PINFL для анализа обычным сообщением.\n\n"
            "/start - Начать работу с ботом\n"
            "/help - Информация о боте\n"
            "/language - Выбрать язык\n"
            "/stats - Месячная статистика\n"
            "/issues - Сообщить о проблеме"

        ),
        "en": (
            "Hello! Send me a PINFL for analysis and I'll tell you if it's valid or not.\n"
            "Available commands:\n\n"
            "/generate - Generate random PINFL\n"
            "/generate_custom - Generate PINFL with specific values\n"
            "Or you can send me PINFL as a regular message for analysis.\n\n"
            "/start - Start working with the bot\n"
            "/help - Information about the bot\n"
            "/language - Choose language\n"
            "/stats - Monthly statistics\n"
            "/issues - Report an issue"
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
            "цифры и имеет длину 14 символов."
        ),
        "en": (
            "Invalid PINFL. Check that it contains only "
            "digits and is exactly 14 characters long."
        ),
    },
    "generated_pinfl": {
        "uz": "Tug'ilgan sana: {birth_date}\nJins: #{gender}",
        "ru": "Дата рождения: {birth_date}\nПол: #{gender}",
        "en": "Date of birth: {birth_date}\nGender: #{gender}",
    },
    "custom_pinfl_generated": {
        "uz": (
            "<b>Kastomnyy PINFL:</b>\n"
            "<pre>{pinfl}</pre>\n"
            "Tug'ilgan sana: {birth_date}\n"
            "Jins: #{gender}\n"
            "Hudud kodi: {area_code}\n"
            "Seriya raqami: {serial_number}"
        ),
        "ru": (
            "<b>Кастомный PINFL по заявке:</b>\n"
            "<pre>{pinfl}</pre>\n"
            "Дата рождения: {birth_date}\n"
            "Пол: #{gender}\n"
            "Код региона: {area_code}\n"
            "Серийный номер: {serial_number}"
        ),
        "en": (
            "<b>Custom PINFL:</b>\n"
            "<pre>{pinfl}</pre>\n"
            "Date of birth: {birth_date}\n"
            "Gender: #{gender}\n"
            "Area code: {area_code}\n"
            "Serial number: {serial_number}"
        ),
    },
    "generate_custom_open_mini_app": {
        "uz": (
            "Zapolnite formula\n"
            "PINFL tayyor bo'lgach bot sizga javob yuboradi."
        ),
        "ru": (
            "Заполните форму\n"
            "После обработки бот пришлет вам PINFL."
        ),
        "en": (
            "Fill out the form.\n"
            "Bot will send generated PINFL after processing."
        ),
    },
    "generate_custom_open_button": {
        "uz": "Shaklni ochish",
        "ru": "Открыть Форму",
        "en": "Open Form",
    },
    "generate_custom_not_configured": {
        "uz": (
            "Mini app URL sozlanmagan. Administrator `MINI_APP_FORMS_LAUNCH_URL` ni "
            "o'rnatishi kerak."
        ),
        "ru": (
            "URL mini app не настроен. Администратор должен задать "
            "`MINI_APP_FORMS_LAUNCH_URL`."
        ),
        "en": (
            "Mini app URL is not configured. Admin must set "
            "`MINI_APP_FORMS_LAUNCH_URL`."
        ),
    },
    "generate_custom_https_required": {
        "uz": (
            "Mini app ochilishi uchun `MINI_APP_FORMS_LAUNCH_URL` HTTPS bo'lishi kerak "
            "(https://...)."
        ),
        "ru": (
            "Для открытия mini app `MINI_APP_FORMS_LAUNCH_URL` должен быть HTTPS "
            "(https://...)."
        ),
        "en": (
            "To open mini app, `MINI_APP_FORMS_LAUNCH_URL` must be HTTPS "
            "(https://...)."
        ),
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
    "disclaimer": {
        "uz": (
            "⚠️ <b>Ogohlantirish:</b> Bu bot norasmiy bo'lib, davlat xizmatlariga "
            "murojaat qilmasdan tahlil qiladi. Shuning uchun u haqiqiy hududlarni "
            "yoki PINFL mavjudligini tekshira olmaydi, faqat matematik hisob-kitoblar "
            "asosida to'g'rilik tekshiruvini amalga oshiradi.\n"
        ),
        "ru": (
            "⚠️ <b>Предупреждение:</b> Этот бот неофициальный и проводит анализ "
            "не обращаясь к государственным сервисам. Поэтому он не может проверить "
            "реальные регионы или существование PINFL, а проводит только проверку "
            "корректности на основе математических вычислений.\n"
        ),
        "en": (
            "⚠️ <b>Warning:</b> This bot is unofficial and performs analysis "
            "without accessing government services. Therefore, it cannot verify "
            "real regions or PINFL existence, only performs correctness checks "
            "based on mathematical calculations.\n"
        ),
    },
    "pinfl_structure_header": {
        "uz": "📋 <b>PINFL tuzilishi:</b>",
        "ru": "📋 <b>Структура PINFL:</b>",
        "en": "📋 <b>PINFL structure:</b>",
    },
    "pinfl_part_century_gender": {
        "uz": "🔢 Millennium/Jins: <code>{value}</code> ({gender}, {century} Millennium)",
        "ru": "🔢 Миллениум/Пол: <code>{value}</code> ({gender}, {century} миллениум)",
        "en": "🔢 Mingyillik/Gender: <code>{value}</code> ({gender}, {century} mingyillik)",
    },
    "pinfl_part_day": {
        "uz": "📅 Kun: <code>{value}</code>",
        "ru": "📅 День: <code>{value}</code>",
        "en": "📅 Day: <code>{value}</code>",
    },
    "pinfl_part_month": {
        "uz": "📅 Oy: <code>{value}</code>",
        "ru": "📅 Месяц: <code>{value}</code>",
        "en": "📅 Month: <code>{value}</code>",
    },
    "pinfl_part_year": {
        "uz": "📅 Yil: <code>{value}</code> ({full_year} yil)",
        "ru": "📅 Год: <code>{value}</code> ({full_year} год)",
        "en": "📅 Year: <code>{value}</code> ({full_year} year)",
    },
    "pinfl_part_area_code": {
        "uz": "🗺️ Hudud kodi: <code>{value}</code>",
        "ru": "🗺️ Код региона: <code>{value}</code>",
        "en": "🗺️ Area code: <code>{value}</code>",
    },
    "pinfl_part_serial": {
        "uz": "🔢 Seriya raqami: <code>{value}</code>",
        "ru": "🔢 Серийный номер: <code>{value}</code>",
        "en": "🔢 Serial number: <code>{value}</code>",
    },
    "pinfl_part_check_digit": {
        "uz": "✅ Nazorat raqami: <code>{value}</code>",
        "ru": "✅ Контрольная цифра: <code>{value}</code>",
        "en": "✅ Check digit: <code>{value}</code>",
    },
    "validation_result_valid": {
        "uz": "✅ <b>PINFL to'g'ri</b>",
        "ru": "✅ <b>PINFL действителен</b>",
        "en": "✅ <b>PINFL is valid</b>",
    },
    "validation_result_invalid": {
        "uz": "❌ <b>PINFL noto'g'ri</b>",
        "ru": "❌ <b>PINFL недействителен</b>",
        "en": "❌ <b>PINFL is invalid</b>",
    },
    "error_details_header": {
        "uz": "🔍 <b>Topilgan xatolar:</b>",
        "ru": "🔍 <b>Найденные ошибки:</b>",
        "en": "🔍 <b>Found errors:</b>",
    },
    "error_date_invalid": {
        "uz": "❌ Noto'g'ri sana: {day}.{month:02d}.{year} - bunday sana mavjud emas",
        "ru": "❌ Неверная дата: {day}.{month:02d}.{year} - такой даты не существует",
        "en": "❌ Invalid date: {day}.{month:02d}.{year} - such date does not exist",
    },
    "error_check_digit": {
        "uz": "❌ Nazorat raqami xato: {given} (kutilgan: {expected})",
        "ru": "❌ Ошибка контрольной цифры: {given} (ожидаемая: {expected})",
        "en": "❌ Check digit error: {given} (expected: {expected})",
    },
    "error_area_code_zero": {
        "uz": "❌ Hudud kodi 000 bo'lishi mumkin emas",
        "ru": "❌ Код региона не может быть 000",
        "en": "❌ Area code cannot be 000",
    },
    "error_serial_zero": {
        "uz": "❌ Seriya raqami 000 bo'lishi mumkin emas",
        "ru": "❌ Серийный номер не может быть 000",
        "en": "❌ Serial number cannot be 000",
    },
    "help_command_title": {
        "uz": "ℹ️ <b>PINFL Helper Bot haqida</b>",
        "ru": "ℹ️ <b>О боте PINFL Helper</b>",
        "en": "ℹ️ <b>About PINFL Helper Bot</b>",
    },
    "help_what_is_pinfl": {
        "uz": (
            "📖 <b>PINFL nima?</b>\n"
            "PINFL (Jismoniy shaxsning soliq to'lovchi identifikatsiya raqami) - "
            "O'zbekistonda fuqarolarni identifikatsiya qilish uchun ishlatiladigan 14 xonali raqam.\n\n"
        ),
        "ru": (
            "📖 <b>Что такое PINFL?</b>\n"
            "PINFL (Персональный идентификационный номер налогоплательщика-физического лица) - "
            "14-значный номер, используемый для идентификации граждан в Узбекистане.\n\n"
        ),
        "en": (
            "📖 <b>What is PINFL?</b>\n"
            "PINFL (Personal Identification Number for Individual Taxpayer) - "
            "a 14-digit number used to identify citizens in Uzbekistan.\n\n"
        ),
    },
    "help_structure": {
        "uz": (
            "🏗️ <b>PINFL tuzilishi (AABBCCDDEE FFGG H):</b>\n"
            "• <b>AA</b> - Asr va jins kodi (1-8)\n"
            "• <b>BB</b> - Tug'ilgan kun (01-31)\n"
            "• <b>CC</b> - Tug'ilgan oy (01-12)\n"
            "• <b>DD</b> - Tug'ilgan yilning so'nggi ikki raqami\n"
            "• <b>EEE</b> - Hudud kodi (001-999)\n"
            "• <b>FF</b> - Seriya raqami (001-999)\n"
            "• <b>H</b> - Nazorat raqami (0-9)\n\n"
        ),
        "ru": (
            "🏗️ <b>Структура PINFL (AABBCCDDEE FFGG H):</b>\n"
            "• <b>A</b> - Код века и пола (1-8)\n"
            "• <b>BB</b> - День рождения (01-31)\n"
            "• <b>CC</b> - Месяц рождения (01-12)\n"
            "• <b>DD</b> - Последние две цифры года рождения\n"
            "• <b>EEE</b> - Код региона (001-999)\n"
            "• <b>FFF</b> - Серийный номер (001-999)\n"
            "• <b>H</b> - Контрольная цифра (0-9)\n\n"
        ),
        "en": (
            "🏗️ <b>PINFL structure (AABBCCDDEE FFGG H):</b>\n"
            "• <b>A</b> - Century and gender code (1-8)\n"
            "• <b>BB</b> - Birth day (01-31)\n"
            "• <b>CC</b> - Birth month (01-12)\n"
            "• <b>DD</b> - Last two digits of birth year\n"
            "• <b>EEE</b> - Area code (001-999)\n"
            "• <b>FFF</b> - Serial number (001-999)\n"
            "• <b>H</b> - Check digit (0-9)\n\n"
        ),
    },
    "help_validation": {
        "uz": (
            "🔍 <b>Bot qanday tekshiradi:</b>\n"
            "1. ✏️ Formatni tekshiradi (14 raqam)\n"
            "2. 📅 Sananing to'g'riligini tekshiradi\n"
            "3. 🔢 Nazorat raqamini hisoblaydi va taqqoslaydi\n"
            "4. 🗺️ Hudud kodining 000 emasligini tekshiradi\n"
            "5. 📄 Seriya raqamining 000 emasligini tekshiradi\n\n"
        ),
        "ru": (
            "🔍 <b>Как бот проверяет:</b>\n"
            "1. ✏️ Проверяет формат (14 цифр)\n"
            "2. 📅 Проверяет корректность даты\n"
            "3. 🔢 Вычисляет и сравнивает контрольную цифру\n"
            "4. 🗺️ Проверяет, что код региона не 000\n"
            "5. 📄 Проверяет, что серийный номер не 000\n\n"
        ),
        "en": (
            "🔍 <b>How the bot validates:</b>\n"
            "1. ✏️ Checks format (14 digits)\n"
            "2. 📅 Validates date correctness\n"
            "3. 🔢 Calculates and compares check digit\n"
            "4. 🗺️ Ensures area code is not 000\n"
            "5. 📄 Ensures serial number is not 000\n\n"
        ),
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
