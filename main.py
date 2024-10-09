import asyncio
import datetime
import re
import sys

from pyrogram import Client
import aiohttp
from aiohttp import ClientSession
from loguru import logger

# Config
# -------------------------------------------------
BOT_TOKEN = ''
API_ID = 
API_HASH = ''
DELAY = 10
TELEGRAM_ID = 
PERIOD_FOR_APR = 1  # in days
LAUNCHPOOL_TICKER = ''
STAKEPOOL_TICKER = ''
# -------------------------------------------------


VIEWED_EVENTS = []


def formatter(record, format_string):
    return format_string + record["extra"].get("end", "\n") + "{exception}"


def clean_brackets(raw_str):
    return re.sub(r'<.*?>', '', raw_str)


format_info = "<green>{time:YYYY-MM-DD HH:mm:ss.SS}</green> | <blue>{level}</blue> | <level>{message}</level>"
format_error = ("<green>{time:HH:mm:ss.SS}</green> | <blue>{level}</blue> | <cyan>{name}</cyan>:<cyan>{function}"
                "</cyan>:<cyan>{line}</cyan> | <level>{message}</level>")

logger_path = "logs/logs/out.log"

logger.remove()
logger.add(logger_path, colorize=True, format=lambda record: formatter(record, clean_brackets(format_error)),
           encoding="utf-8")

logger.add(sys.stdout, colorize=True, format=lambda record: formatter(record, format_info), level="INFO")


def make_date_readable(date_str):
    dt = datetime.datetime.fromisoformat(date_str.removesuffix('Z'))
    return dt.strftime("%Y-%m-%d at %H:%M:%S")


async def get_launchpool(session):
    resp = await session.get('https://api2.bybit.com/spot/api/launchpool/v1/home')
    r = await resp.json()
    launchpools = r['result']['list']
    for launchpool in launchpools:
        if launchpool['returnCoin'] == LAUNCHPOOL_TICKER:
            for stakepool in launchpool['stakePoolList']:
                if stakepool['stakeCoin'] == STAKEPOOL_TICKER:
                    return stakepool
    return None


async def parse_info(stakepool):
    pool_amount = stakepool['poolAmount']
    total_amount = stakepool['totalAmount']
    return pool_amount, total_amount

async def calculate_apr(pool_amount, total_amount):
    return (float(pool_amount) / float(total_amount)) / int(PERIOD_FOR_APR) * 100


async def init_bot():
    bot = Client(
        'polymarket_bot',
        bot_token=str(BOT_TOKEN),
        api_id=int(API_ID),
        api_hash=str(API_HASH)
    )

    return bot


async def worker(session):
    bot = await init_bot()
    await bot.start()
    while True:
        try:
            stakepool = await get_launchpool(session)
            pool_amount, total_amount = await parse_info(stakepool)
            apr = await calculate_apr(pool_amount, total_amount)
            message = f'APR for {LAUNCHPOOL_TICKER}/{STAKEPOOL_TICKER} for PERIOD_FOR_APR days: {apr}%'
            logger.info(message)
            await bot.send_message(TELEGRAM_ID, message)
            await asyncio.sleep(DELAY)
        except Exception as e:
            logger.error(e)


async def main():
    session = None
    try:
        session = aiohttp.ClientSession(trust_env=True)
        await worker(session)
    except Exception as e:
        logger.error(e)
    finally:
        try:
            await session.close()
        except:
            pass


if __name__ == '__main__':
    asyncio.run(main())
