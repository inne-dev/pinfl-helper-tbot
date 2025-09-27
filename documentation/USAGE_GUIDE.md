# PINFL Helper Telegram Bot - Usage Guide

## Overview

PINFL Helper Bot is a Telegram bot for analyzing and generating PINFL (Personal Identification Number for Individual Taxpayer) numbers. The bot supports three interface languages and provides public usage statistics.

## Core Features

### 🔍 PINFL Analysis
- Validate PINFL numbers
- Extract birth date information
- Identify errors in the number
- Verify control digit checksum

### 🎲 PINFL Generation
- Create random valid PINFL numbers
- Specify gender and birth date
- Display additional information

### 🌐 Multi-language Support
- **Uzbek** (O'zbekcha) - uz
- **Russian** (Русский) - ru  
- **English** - en

### 📊 Public Statistics
- Number of generation requests
- Number of analysis requests
- New user statistics
- Monthly reports (available to all users for transparency and trust)

## Available Commands

| Command | Description |
|---------|-------------|
| `/start` | Start working with the bot |
| `/generate` | Generate random PINFL |
| `/language` | Choose interface language |
| `/stats` | View monthly statistics (for transparency and trust) |
| `/issues` | Report an issue |

## Using the Bot

### First Launch

1. **Find the bot**: Search for your bot in Telegram by username
2. **Start dialogue**: Send `/start`
3. **Choose language**: New users will see language selection first
4. **Get instructions**: Start message appears after language selection

### Analyzing PINFL

Simply send a PINFL to the bot as a regular message:

```
32005901234567
```

**Valid PINFL result:**
```
✅ PINFL is valid.
Date of birth: 15.05.1990
```

**Invalid PINFL result:**
```
❌ Invalid PINFL. Check the following errors:
- Invalid date of birth.
- Invalid check digit. Expected: 7
```

### Generating PINFL

Use the `/generate` command:

```
/generate
```

**Result:**
```
32005901234567
Date of birth: 15.05.1990
Gender: #male
```

### Changing Language

1. Send `/language`
2. Select desired language from the buttons
3. Receive confirmation of the change

### Viewing Statistics (Public)

Use the `/stats` command:

```
/stats
```

**Result:**
```
📊 Statistics for December/2024 (for transparency and trust):

🔢 Generate requests: 156
🔍 Analyze requests: 324  
👥 New users: 45
📈 Total users: 1,234
```

Statistics are available to all users to provide transparency about bot usage and build trust.

## Usage Examples

### Example 1: Valid PINFL Check
```
User: 32005901234567
Bot: ✅ PINFL is valid.
     Date of birth: 15.05.1990
```

### Example 2: Invalid PINFL Check
```
User: 32005901234568
Bot: ❌ Invalid PINFL. Check the following errors:
     - Invalid check digit. Expected: 7
```

### Example 3: Generate New PINFL
```
User: /generate
Bot: 41203851987654
     Date of birth: 28.03.1985
     Gender: #female
```

### Example 4: Language Change
```
User: /language
Bot: [Shows language selection buttons]
User: [Clicks "English"]
Bot: Language changed successfully!
```

## Common Issues and Solutions

### PINFL Not Recognized
**Problem**: Bot doesn't analyze sent text
**Solution**: 
- Ensure PINFL contains only digits
- Check length is at least 14 characters
- Remove spaces and special characters

### Bot Not Responding
**Problem**: Bot doesn't react to messages
**Solution**: 
- Check internet connection
- Try sending `/start`
- Contact bot administrator

## Technical Details

### PINFL Format
PINFL consists of 14 digits:
- Positions 1-2: Region code
- Positions 3-8: Birth date (DDMMYY)
- Position 9: Gender and century indicator
- Positions 10-13: Serial number
- Position 14: Control digit

### Validation Algorithm
1. **Format check**: Digits only, length 14
2. **Date validation**: Valid birth date
3. **Region check**: Existing region code
4. **Control sum verification**: Weighted sum algorithm

### Supported Regions
The bot supports all official region codes of Uzbekistan.

## Privacy

- Bot **DOES NOT SAVE** the content of your messages
- Only usage statistics are stored (request counts)
- Personal data from PINFL is not analyzed or stored
- All analysis is performed locally

## Support

For issues or suggestions:

1. Use `/issues` command for quick reporting
2. Describe the problem in detail
3. Specify steps to reproduce the error
4. Include screenshot if possible

## Updates

The bot is regularly updated with new features:
- Algorithm improvements
- New language additions
- Extended statistical capabilities
- Bug fixes

Stay tuned for update announcements!

---

*Documentation version: 2.0*  
*Last updated: December 2024*