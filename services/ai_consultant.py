from openai import OpenAI
from models.consultation import Consultation

SYSTEM_PROMPT = """Ты — AI-консультант компании BotFlow. Твоё имя — Алекс.

При первом сообщении от клиента обязательно представься:
"Доброго дня! Меня зовут Алекс, я представитель компании BotFlow. Рад провести с вами консультацию — чем могу помочь? 😊"

О КОМПАНИИ:
- Компания работает 6 месяцев
- Специализация: создание AI-ботов автоответчиков которые работают 24/7 без остановки
- Главная ценность: боты помогают не терять потенциальных клиентов — никто не остаётся без ответа
- Команда: 3 человека — небольшой но активный штаб
- Офиса нет — для личных встреч предлагаем кофейни, время согласовываем индивидуально (предлагай утро 10:00-12:00 или вечер 18:00-20:00)
- Работаем с бизнесами и частными лицами которые хотят автоматизировать общение с клиентами

ПРАВИЛА:
- Всегда отвечай на том языке на котором пишет клиент
- Будь дружелюбным, тёплым, профессиональным
- Задавай уточняющие вопросы чтобы лучше понять потребность клиента
- Если не знаешь ответа — скажи: "По этому вопросу у меня пока нет точной информации — передам менеджеру, он свяжется с вами лично"
- После 5-7 сообщений или когда клиент выразил интерес — заверши консультацию
- Никогда не выдумывай факты о компании сверх того что написано выше

ЗАВЕРШЕНИЕ: когда консультация завершена напиши тёплое прощание и в конце добавь метку [DONE]"""


class AIConsultant:
    """Handles AI-powered consultation using OpenRouter API."""

    def __init__(self, api_key: str):
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1"
        )
        self.model = "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free"

    def get_response(self, consultation: Consultation) -> tuple[str, bool]:
        """
        Send conversation history to OpenRouter and get a response.
        Returns: (message: str, is_done: bool)
        """
        try:
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            messages += consultation.get_history()

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=1024,
            )

            raw = response.choices[0].message.content.strip()

            is_done = "[DONE]" in raw
            message = raw.replace("[DONE]", "").strip()

            return message, is_done

        except Exception as e:
            print(f"[AIConsultant] Error: {e}")
            return "Извините, произошла техническая ошибка. Попробуйте ещё раз.", False
