import os
import asyncio

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from src.handlers.user import user

async def main() -> None:
    load_dotenv()
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()
    dp.include_router(router=user)
    await dp.start_polling(bot)
    await bot.delete_webhook()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped")
