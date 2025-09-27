# Setup and Deployment Guide - PINFL Helper Telegram Bot

## Environment Variables

Create a `.env` file in the project root directory with the following variables:

```bash
# Required variables
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

# Optional variables
ISSUE_LINK=https://github.com/your-username/pinfl-helper-tbot/issues
```

### Variable descriptions:

- **TELEGRAM_BOT_TOKEN** (required) - Your Telegram bot token from @BotFather
- **ISSUE_LINK** (optional) - Link to your project's issues page

## Getting Bot Token

1. Find @BotFather in Telegram
2. Send command `/newbot`
3. Follow instructions to create your bot
4. Copy the token and add it to `TELEGRAM_BOT_TOKEN`

## Running the Bot

### With Docker Compose (recommended)

```bash
# Clone repository
git clone <your-repo-url>
cd pinfl-helper-tbot

# Create configuration file
echo "TELEGRAM_BOT_TOKEN=your_token_here" > .env
# Edit .env file with your actual token

# Start the bot
docker-compose up -d

# View logs
docker-compose logs -f
```

### Without Docker

```bash
# Install dependencies
pip install -r requirements.txt

# Export environment variables
export $(xargs < .env)

# Run the bot
python main.py
```

## File Structure

```
pinfl-helper-tbot/
├── data/                        # Database (created automatically)
│   └── pinfl_bot.db            # SQLite database
├── documentation/              # Project documentation
├── main.py                     # Main bot logic
├── database.py                 # Database operations
├── translations.py             # Multi-language support
├── pinfl_utilities_generator.py # PINFL generation
├── pinfl_utilities_parser.py   # PINFL analysis
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker configuration
├── docker-compose.yml          # Docker Compose configuration
├── .env                        # Environment variables (create this)
└── README.md                   # Documentation
```

## Database

SQLite database is created automatically on first run in the `data/` folder.

Contains tables:
- `users` - user information
- `requests` - request statistics

## Bot Commands

- `/start` - Start working with the bot
- `/generate` - Generate random PINFL
- `/language` - Choose interface language
- `/stats` - Statistics (available to all users)
- `/issues` - Report an issue

## Supported Languages

- Uzbek (uz)
- Russian (ru)
- English (en)

## Docker Configuration

The project uses `docker-compose.yml` for local development:
- Builds image locally from source code
- Creates persistent data directory for SQLite database
- Includes health checks and logging configuration
- Run with: `docker-compose up -d`

## Updates

```bash
# Stop container
docker-compose down

# Update code
git pull

# Rebuild and start
docker-compose up -d --build
```

## Backup

The database is located at `data/pinfl_bot.db`. Regularly backup this file.

## Troubleshooting

1. **Bot not responding**: Check token correctness in `.env`
2. **Database errors**: Check write permissions to `data/` folder

## Logs

```bash
# View logs
docker-compose logs -f

# View specific container logs
docker-compose logs -f pinfl-helper-tbot
```
