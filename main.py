import asyncio 
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
import random
import os 
from dotenv import load_dotenv
from handlers.start import start_kb
from handlers.other import start_router
load_dotenv()
bot_token = os.getenv('BOT_TOKEN')

bot = Bot(token=bot_token)

dp = Dispatcher()

async def main():
    dp.include_router(start_kb)
    dp.include_router(start_router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
