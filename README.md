# Polymarket Event Bot

This bot monitors the APR (Annual Percentage Rate) of a specific launchpool on Bybit and sends updates to a specified Telegram user.

## Configuration
To use this bot, fill in the configuration variables in the code:

- `BOT_TOKEN`: Telegram bot token.
- `API_ID`: Telegram API ID.
- `API_HASH`: Telegram API hash.
- `DELAY`: Delay in seconds between APR checks (default value is 10).
- `TELEGRAM_ID`: Your Telegram ID to which notifications will be sent.
- `PERIOD_FOR_APR`: Period for APR calculation in days (default value is 1 day).
- `LAUNCHPOOL_TICKER`: Ticker of the token for which APR is calculated.
- `STAKEPOOL_TICKER`: Ticker of the staking pool.

## How to Run

### Install Dependencies
Run the following command to install dependencies:
```sh
pip install -r requirements.txt
```

### Running the Program
After configuring the necessary values, run the program using the following command:
```sh
python main.py
```

## Features
- Monitors APR for a specific launchpool on Bybit.
- Sends APR updates to a specified Telegram user.

## Requirements
- **Python Version**: Python 3.7+
- **Dependencies**:
  - `aiohttp`: For making asynchronous HTTP requests.
  - `pyrogram`: For interacting with Telegram.
  - `loguru`: For advanced logging.

## Notes
- Make sure to create and add a Telegram bot token using BotFather in Telegram.
- Update the necessary tokens and identifiers directly in the script.

## License
This project is open source and available under the [MIT License](LICENSE).

---
Feel free to update or ask questions if you encounter any issues!
