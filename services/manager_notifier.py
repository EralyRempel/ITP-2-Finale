from aiogram import Bot
from services.ai_consultant import AIConsultant
from models.consultation import Consultation
from utils.storage import Storage

# Your Telegram ID — manager notifications will be sent here
MANAGER_TELEGRAM_ID = 5195555247

FAREWELL_MESSAGE = (
    "Отлично, я зафиксировал ваш запрос! 🙌\n\n"
    "Наш менеджер свяжется с вами в ближайшее время — обычно это занимает до нескольких часов.\n"
    "Спасибо что обратились в BotFlow!"
)

FAREWELL_MESSAGE_EN = (
    "Great, I've noted your request! 🙌\n\n"
    "Our manager will get in touch with you shortly — usually within a few hours.\n"
    "Thank you for reaching out to BotFlow!"
)


class ManagerNotifier(AIConsultant):
    """
    Extends AIConsultant with the ability to finalize consultations,
    notify the manager via Telegram, and save data to storage.
    Demonstrates inheritance (OOP requirement).
    """

    def __init__(self, api_key: str, storage: Storage, bot: Bot = None):
        super().__init__(api_key)  # call parent constructor
        self.storage = storage
        self.bot = bot  # Telegram bot instance for sending notifications

    def finalize(self, consultation: Consultation, language: str = "ru") -> str:
        """
        Finish the consultation:
        1. Save client data to JSON file
        2. Return farewell message to user
        """
        try:
            consultation.finish()
            self.storage.save_consultation(consultation)
            print(f"[ManagerNotifier] Saved consultation for user {consultation.user.telegram_id}")
        except Exception as e:
            print(f"[ManagerNotifier] Failed to save consultation: {e}")

        if language == "en":
            return FAREWELL_MESSAGE_EN
        return FAREWELL_MESSAGE

    async def notify_manager(self, consultation: Consultation):
        """Send a notification to the manager with client details."""
        if not self.bot:
            return

        user = consultation.user
        summary = consultation.summarize()

        # Build username link or fallback to full name
        if user.username and user.username != "Unknown":
            client_ref = f"@{user.username}"
        else:
            client_ref = f"{user.full_name} (ID: {user.telegram_id})"

        text = (
            "🔔 *Новая заявка от клиента!*\n\n"
            f"👤 Клиент: {client_ref}\n"
            f"🆔 Telegram ID: `{user.telegram_id}`\n"
            f"📝 Краткое содержание:\n_{summary}_"
        )

        try:
            await self.bot.send_message(
                chat_id=MANAGER_TELEGRAM_ID,
                text=text,
                parse_mode="Markdown"
            )
            print(f"[ManagerNotifier] Manager notified about user {user.telegram_id}")
        except Exception as e:
            print(f"[ManagerNotifier] Failed to notify manager: {e}")

    def detect_language(self, consultation: Consultation) -> str:
        """Simple language detection based on first user message."""
        history = consultation.get_history()
        for msg in history:
            if msg["role"] == "user":
                text = msg["content"]
                # Check for Cyrillic characters
                if any("\u0400" <= c <= "\u04FF" for c in text):
                    return "ru"
                return "en"
        return "ru"
