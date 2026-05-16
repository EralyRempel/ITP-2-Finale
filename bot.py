from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from models.user import User
from models.consultation import Consultation
from services.ai_consultant import AIConsultant
from services.manager_notifier import ManagerNotifier
from utils.storage import Storage

router = Router()

# In-memory session storage: {telegram_id: Consultation}
active_sessions: dict[int, Consultation] = {}

# Services (initialized in main.py and injected here)
_consultant: AIConsultant = None
_notifier: ManagerNotifier = None
_storage: Storage = None


def setup_services(consultant: AIConsultant, notifier: ManagerNotifier, storage: Storage):
    """Inject service dependencies into bot handlers."""
    global _consultant, _notifier, _storage
    _consultant = consultant
    _notifier = notifier
    _storage = storage


@router.message(CommandStart())
async def handle_start(message: Message):
    """Handle /start command — begin a new consultation."""
    user = User(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        full_name=message.from_user.full_name,
    )

    consultation = Consultation(user=user)
    active_sessions[user.telegram_id] = consultation

    await message.answer(
        "Доброго дня! Меня зовут Алекс, я представитель компании BotFlow. "
        "Рад провести с вами консультацию — чем могу помочь? 😊"
    )


@router.message(Command("stop"))
async def handle_stop(message: Message):
    """Handle /stop command — manually end the consultation."""
    user_id = message.from_user.id
    if user_id in active_sessions:
        consultation = active_sessions.pop(user_id)
        lang = _notifier.detect_language(consultation)
        farewell = _notifier.finalize(consultation, language=lang)
        await _notifier.notify_manager(consultation)
        await message.answer(farewell)
    else:
        await message.answer("У вас нет активной консультации. Напишите /start чтобы начать.")


@router.message(F.text)
async def handle_message(message: Message):
    """Handle regular text messages — continue the consultation."""
    user_id = message.from_user.id

    # Auto-create session if user writes without /start
    if user_id not in active_sessions:
        user = User(
            telegram_id=user_id,
            username=message.from_user.username,
            full_name=message.from_user.full_name,
        )
        active_sessions[user_id] = Consultation(user=user)

    consultation = active_sessions[user_id]

    # Don't continue if already finished
    if consultation.is_finished:
        await message.answer(
            "Ваша консультация уже завершена. Напишите /start чтобы начать новую."
        )
        return

    # Add user message to history
    consultation.add_message("user", message.text)

    # Show typing indicator
    await message.bot.send_chat_action(message.chat.id, "typing")

    # Get AI response
    reply, is_done = _consultant.get_response(consultation)

    # Add assistant reply to history
    consultation.add_message("assistant", reply)

    # Send the AI reply
    await message.answer(reply)

    # If AI signals the consultation is done — finalize
    if is_done:
        lang = _notifier.detect_language(consultation)
        farewell = _notifier.finalize(consultation, language=lang)
        await _notifier.notify_manager(consultation)
        active_sessions.pop(user_id, None)
        await message.answer(farewell)
