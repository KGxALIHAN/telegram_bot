import asyncio
from bot_config import bot, dp
from handlers.start import start_kb
from handlers.other import start_router
async def main():
    dp.include_router(start_kb)
    dp.include_router(start_router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
