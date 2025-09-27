# Telegram Bot for PINFL Analysis

[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint)

This project is a Telegram bot that analyzes PINFL (Personal Identification Number for Individual Taxpayer) entered by users and reports its validity, birth date, region code, and other parameters.

## Why is this project needed?

PINFL is a unique identification number used in several countries to identify citizens. This project processes and analyzes PINFL to ensure correctness and provide information about birth date and other data contained in this number.

## Features

- **PINFL Validation**: Analyze PINFL numbers for validity and extract information
- **PINFL Generation**: Generate random valid PINFL numbers for testing
- **Multi-language Support**: Support for Uzbek (O'zbekcha), Russian (Русский), and English
- **Database Integration**: SQLite database for user management and statistics
- **Public Statistics**: Monthly statistics available to all users for transparency
- **User Management**: Track user activity and preferences

## Available Commands

- `/start` - Start working with the bot
- `/generate` - Generate random PINFL
- `/language` - Choose interface language
- `/stats` - Monthly statistics (public for transparency)
- `/issues` - Report an issue

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



## Database

The bot uses SQLite database to store:
- User information (ID, username, language preference, registration date)
- Request statistics (generate/analyze requests with timestamps)
- Activity tracking

Database file is stored in `data/pinfl_bot.db` and is persisted through Docker volumes.

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
