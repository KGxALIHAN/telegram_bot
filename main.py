import asyncio
from bot_config import bot, dp
from handlers.start import start_kb
from handlers.other import start_router
from handlers.review_dialog import opros_router
async def main():
    dp.include_router(start_kb)
    dp.include_router(start_router)
    dp.include_router(opros_router)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
