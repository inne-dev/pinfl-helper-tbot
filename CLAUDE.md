# CLAUDE.md - AI Project Overview

## Project Summary
PINFL Helper Telegram Bot is a multi-language bot for analyzing and generating PINFL (Personal Identification Number for Individual Taxpayer) numbers used in Uzbekistan. The bot validates PINFL structure, extracts birth dates, and provides public statistics for transparency.

**Personal Project Context (2025):**
- Pet project for company workflow optimization
- Portfolio demonstration for potential employers
- Showcase of modern development practices
- Local development and containerization focus

## Architecture Overview

### Core Components
- **main.py** - Bot handlers with decorator-based user context management
- **database.py** - SQLite database operations for users and statistics  
- **translations.py** - Multi-language support (Uzbek, Russian, English)
- **pinfl_utilities_parser.py** - PINFL validation and parsing logic
- **pinfl_utilities_generator.py** - Random PINFL generation

### Key Features
1. **PINFL Analysis** - Validates 14-digit PINFL numbers, checks date validity, region codes, and control digits
2. **PINFL Generation** - Creates random valid PINFL numbers for testing
3. **Multi-language** - Full i18n support with language selection UI
4. **Public Statistics** - Monthly stats (requests, users) available to all users for transparency and trust
5. **User Management** - Automatic user registration and activity tracking

## Technical Stack
- **Python 3.9** with python-telegram-bot library
- **SQLite** database with automatic schema creation
- **Docker** containerized deployment
- **GitHub Actions** for CI/CD testing

## Database Schema
```sql
-- Users table
users (user_id, username, first_name, last_name, language_code, created_at, last_activity)

-- Requests table for statistics
requests (id, user_id, request_type, created_at)
```

## Bot Commands
- `/start` - Welcome + language selection for new users
- `/generate` - Generate random valid PINFL
- `/language` - Change interface language
- `/stats` - View monthly statistics (public for transparency and trust)
- `/issues` - Report problems
- **Direct PINFL** - Send 14-digit number for analysis

## Code Patterns

### Decorator Pattern
Uses `@with_user_context()` decorator (Rails-style before_action) to:
- Auto-register/update users
- Extract user language preference
- Log requests for statistics
- Provide consistent context to handlers

### Internationalization
```python
get_text("key", user_lang, **kwargs)  # Dynamic translation lookup
```

### Error Handling
All database operations have try-catch blocks with logging.

## PINFL Format
14-digit structure: AABBCCDDEE FFGG H
- AA: Region code
- BBCCDD: Birth date (DDMMYY) 
- EE: Century/gender indicator
- FFGG: Serial number
- H: Control digit (weighted checksum)

## Environment Variables
- `TELEGRAM_BOT_TOKEN` - Bot API token (required)
- `ISSUE_LINK` - GitHub issues URL (optional)

## Development Notes
- All code/comments in English (except user-facing translations)
- Clean code without obvious comments
- Statistics public for transparency and user trust
- Extensive input validation and error handling
- Containerized with volume persistence
- Rails-style before_action decorators for DRY code
- Comprehensive test coverage

## File Structure
```
├── main.py                 # Bot handlers and logic
├── database.py             # Data layer
├── translations.py         # I18n strings
├── pinfl_utilities_*.py    # PINFL logic
├── requirements.txt        # Dependencies
├── Dockerfile             # Container config
├── docker-compose.yml     # Deployment
├── test_bot.py            # Comprehensive tests
└── data/                  # SQLite storage
```

## Testing Strategy
Comprehensive test suite covers:
- Database operations and statistics
- PINFL generation/validation algorithms
- Translation system and fallbacks
- User context management decorators
- Integration workflows

## Personal & Professional Value
This project demonstrates:
- **Modern Architecture**: Clean code, decorators, separation of concerns
- **Development Skills**: Containerization, testing, CI/CD
- **Full-Stack Thinking**: Database design, API integration, user experience
- **Quality Standards**: Comprehensive testing, documentation

This is a well-architected Telegram bot with clean code patterns, proper error handling, comprehensive multi-language support, and professional development practices suitable for portfolio demonstration.