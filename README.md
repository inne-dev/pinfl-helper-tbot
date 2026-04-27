# Telegram Bot for PINFL Analysis

[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint)

This project is a Telegram bot that analyzes PINFL (Personal Identification Number for Individual Taxpayer) entered by users and provides detailed analysis including validity, structure breakdown, birth date, region code, and specific error descriptions.

## Why is this project needed?

PINFL is a unique identification number used in several countries to identify citizens. This project processes and analyzes PINFL to ensure correctness and provide information about birth date and other data contained in this number.

## Features

- **Detailed PINFL Analysis**: Comprehensive validation with structure breakdown and specific error identification
- **Educational Information**: Built-in help system explaining PINFL structure and validation process
- **PINFL Generation**: Generate random valid PINFL numbers for testing purposes
- **Custom PINFL via Mini App Forms**: Build PINFL with user-selected date, gender, area code, and serial number from SSE form responses
- **Multi-language Support**: Full internationalization in Uzbek (O'zbekcha), Russian (Русский), and English
- **Database Integration**: SQLite database for user management and request statistics
- **Public Statistics**: Monthly statistics available to all users for transparency and trust
- **User Management**: Automatic user registration and activity tracking
- **Official Disclaimer**: Clear warnings about unofficial status and limitations

## Available Commands

- `/start` - Start working with the bot and view command overview
- `/help` - Detailed information about PINFL structure and bot functionality
- `/generate` - Generate random valid PINFL for testing
- `/generate_custom` - Generate PINFL with specific values
- `/language` - Choose interface language (Uzbek/Russian/English)
- `/stats` - View monthly usage statistics (public for transparency)
- `/issues` - Report bugs or suggest improvements

You can also send any 14-digit number directly to the bot for detailed PINFL analysis.

## PINFL Analysis Features

### Detailed Structure Breakdown
When you send a PINFL to the bot, it provides:

- **Visual Structure**: PINFL formatted with clear separators (e.g., `3 25 05 90 012 345 9`)
- **Component Analysis**: Each part explained (century/gender, birth date, region code, serial number, check digit)
- **Validation Results**: Clear indication of validity with specific error descriptions
- **Birth Date Extraction**: Automatic date parsing and validation
- **Error Identification**: Precise description of what's wrong with invalid PINFLs

### Educational Content
The `/help` command provides comprehensive information about:
- What is PINFL and its purpose
- Detailed structure explanation (14-digit format breakdown)
- How the bot validates each component
- Limitations and unofficial status disclaimer

### Example Output

**Valid PINFL:**
```
📋 PINFL structure:
3 25 05 90 012 345 9

🔢 Century/Gender: 3 (male, 19 century)
📅 Day: 25
📅 Month: 05
📅 Year: 90 (1990 year)
🗺️ Area code: 012
🔢 Serial number: 345
✅ Check digit: 9

✅ PINFL is valid
📅 1990-05-25
```

**Invalid PINFL:**
```
❌ PINFL is invalid

🔍 Found errors:
❌ Check digit error: 6 (expected: 9)
```

## Supported Languages

- **Uzbek (O'zbekcha)** - uz
- **Russian (Русский)** - ru
- **English** - en

## How to use?

### Local Development

1. Navigate to the project directory.

2. Create a `.env` file with the required environment variables:
```shell
TELEGRAM_BOT_TOKEN=your_bot_token_here
ISSUE_LINK=https://github.com/your-repo/issues
```

3. Run with Docker Compose:
```shell
docker-compose up -d
```

### Environment Variables

- `TELEGRAM_BOT_TOKEN` - Your Telegram Bot API token (required)
- `ISSUE_LINK` - Link to your project's issue tracker (optional)
- `MINI_APP_FORMS_ENABLED` - Enable mini app form stream listener (`true/false`, optional)
- `MINI_APP_FORMS_LAUNCH_URL` - Mini app URL for `/generate_custom` inline button
- `MINI_APP_FORMS_STREAM_URL` - SSE endpoint URL for form responses (required if feature enabled)
- `MINI_APP_FORMS_WEBHOOK_SECRET` - Secret for `X-Wappy-Webhook-Secret` header (required if feature enabled)
- `MINI_APP_FORMS_START_FROM_NOW` - Start listener from current moment (`true` by default, avoids replay spam)
- `MINI_APP_FORMS_TRANSPORT` - `sse` (default) or `poll`
- `MINI_APP_FORMS_POLL_INTERVAL_SECONDS` - Poll interval in seconds (default `3`)
- `MINI_APP_FORMS_BIRTH_DATE_FIELD_ID` - Form field id for birth date (optional, has default)
- `MINI_APP_FORMS_GENDER_FIELD_ID` - Form field id for gender (optional, has default)
- `MINI_APP_FORMS_AREA_CODE_FIELD_ID` - Form field id for area code (optional, has default)
- `MINI_APP_FORMS_SERIAL_NUMBER_FIELD_ID` - Form field id for serial number (optional, has default)



## Database

The bot uses SQLite database to store:
- User information (ID, username, language preference, registration date)
- Request statistics (generate/analyze requests with timestamps)
- Activity tracking

Database file is stored in `data/pinfl_bot.db` and is persisted through Docker volumes.

## Mini App Forms Integration

When `MINI_APP_FORMS_ENABLED=true`, bot starts background SSE listener and handles
`form.response.created` events from mini app forms.

For weak servers/ngrok, prefer poll transport:
- `MINI_APP_FORMS_TRANSPORT=poll`
- `MINI_APP_FORMS_STREAM_URL=.../responses_poll`

Expected payload fields:
- Birth date in `YYYY-MM-DD` format
- Gender (`male/female`, `Мужской/Женский`, `erkak/ayol`)
- Area code (`001-999`)
- Serial number (`001-999`)

After event processing bot generates valid PINFL and sends result to `tg_user_id`
from event context.

## Statistics

All users can access monthly statistics using the `/stats` command, which shows:
- Number of generate requests in current month
- Number of analyze requests in current month
- Number of new users registered in current month
- Total number of users

Statistics are public to provide transparency about bot usage and popularity.

## Additional Features

1. The bot pre-validates entered text for digits only and minimum 14 character length.

2. **Multi-language Interface**: Users can switch between Uzbek, Russian, and English using the `/language` command.

3. **Database Persistence**: All user data and statistics are stored in SQLite database with proper volume mounting.

4. **Public Analytics**: Statistics and usage data available for all users to understand bot popularity.

## Development

### Project Structure

```
pinfl-helper-tbot/
├── main.py                      # Main bot logic
├── database.py                  # Database operations
├── translations.py              # Multi-language support
├── pinfl_utilities_generator.py # PINFL generation utilities
├── pinfl_utilities_parser.py    # PINFL parsing utilities
├── docker-compose.yml           # Docker configuration
├── Dockerfile                   # Docker build file
├── data/                        # Database storage directory
├── documentation/               # Project documentation
│   ├── SETUP.md                # Local setup guide
│   └── USAGE_GUIDE.md          # User manual
├── CLAUDE.md                    # AI project overview
└── README.md                    # This file
```

### Adding New Languages

See [documentation/SETUP.md](documentation/SETUP.md) for detailed setup instructions.

### Adding New Languages

To add a new language:

1. Add language code and name to `LANGUAGES` dict in `translations.py`
2. Add translations for all keys in `TRANSLATIONS` dict
3. Test with `/language` command

### Adding New Statistics

To add new statistics:

1. Add new fields to database schema in `database.py`
2. Update `get_monthly_stats()` method
3. Add translations for new statistics in `translations.py`
4. Update `stats()` function in `main.py`

## Personal Project Context

This is a personal pet project created in 2025 for:
- **Company workflow optimization** - Simplifying PINFL validation processes
- **Portfolio demonstration** - Showcasing technical skills to potential employers
- **Best practices showcase** - Modern development, testing, and deployment practices

This project demonstrates:
- Clean architecture with decorator patterns
- Comprehensive testing and CI/CD
- Multi-language support and internationalization
- Docker containerization and local development
- Database design and statistics tracking

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Personal Project Notice**: This software is actively used in production and maintained as part of a professional portfolio.
