import asyncio
import os
from aiogram import Bot, Dispatcher

from bot import router, setup_services
from services.ai_consultant import AIConsultant
from services.manager_notifier import ManagerNotifier
from utils.storage import Storage

# ─────────────────────────────────────────
#  CONFIGURATION — put your tokens here
# ─────────────────────────────────────────
TELEGRAM_BOT_TOKEN = "8845691099:AAGDxQAJqlupIaUD0dzMp3hS4CDLVH4t1m8"   # get from @BotFather
OPENROUTER_API_KEY = "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"   # get from openrouter.ai
# ─────────────────────────────────────────


async def main():
    # Initialize services
    # Initialize services
    storage    = Storage(filepath="clients.json")
    consultant = AIConsultant(api_key=OPENROUTER_API_KEY)
    bot        = Bot(token=TELEGRAM_BOT_TOKEN)
    notifier   = ManagerNotifier(api_key=OPENROUTER_API_KEY, storage=storage, bot=bot)

    # Inject services into bot handlers
    setup_services(consultant, notifier, storage)

    # Start bot
    dp  = Dispatcher()
    dp.include_router(router)

    print("🤖 Bot is running...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())