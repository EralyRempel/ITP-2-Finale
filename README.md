# ITP-2-Finale
# BotFlow Consultant Bot 

An AI-powered Telegram consultant bot for **BotFlow** company, built with Python.

---

## About

The bot automatically consults potential clients of BotFlow on Telegram. It answers questions about the company, maintains a friendly conversation, and when the consultation is complete — notifies the manager with the client's details.

---

## Features

- Greets the client and introduces itself as a BotFlow consultant
- Answers questions about the company's services, team, and terms
- If it doesn't know the answer — informs the client that a manager will follow up
- Sends the manager a Telegram notification when a consultation ends
- Saves all client data to `clients.json`
- Supports Russian and English languages

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.11+ | Core language |
| aiogram 3.x | Telegram Bot framework |
| OpenAI SDK | AI connection via OpenRouter |
| OpenRouter API | Free access to AI models |
| JSON | Client data storage |
| unittest | Unit testing |

---

## Project Structure
TgBot/
├── main.py                  # Entry point, token configuration
├── bot.py                   # Telegram message handlers
├── clients.json             # Client database (auto-created)
├── requirements.txt         # Project dependencies
├── models/
│   ├── init.py
│   ├── user.py              # User class — stores client data
│   └── consultation.py      # Consultation class — manages dialog session
├── services/
│   ├── init.py
│   ├── ai_consultant.py     # AIConsultant class — handles AI requests
│   └── manager_notifier.py  # ManagerNotifier(AIConsultant) — sends notifications
├── utils/
│   ├── init.py
│   └── storage.py           # Storage class — reads/writes JSON file
└── tests/
└── test_consultation.py # Unit tests

---

## Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/TgBot.git
cd TgBot
```

### 2. Create a virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate       # Windows
source .venv/bin/activate    # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your tokens to `main.py`
```python
TELEGRAM_BOT_TOKEN = "your token from @BotFather"
OPENROUTER_API_KEY = "your key from openrouter.ai"
```

### 5. Run the bot
```bash
python main.py
```

---

## Getting Tokens

**Telegram Bot Token:**
1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot` and follow the instructions
3. Copy the token you receive

**OpenRouter API Key:**
1. Register at [openrouter.ai](https://openrouter.ai)
2. Go to the **Keys** section
3. Click **Create Key** and copy it

---

## Running Tests

```bash
python -m unittest discover tests/
```

---

## OOP Architecture
AIConsultant
│
└── ManagerNotifier  (inheritance)
User  ◄──── Consultation  (composition)
│
└── Storage  (persistence)

- **User** — stores client data (telegram ID, username, full name)
- **Consultation** — manages the dialog session and message history
- **AIConsultant** — sends requests to the AI and processes responses
- **ManagerNotifier** — inherits AIConsultant, adds manager notification logic
- **Storage** — reads and writes client data to a JSON file

---

## How It Works
Client sends /start
↓
bot.py creates User + Consultation
↓
Client asks questions
↓
AIConsultant sends history to AI → receives response
↓
After 5-7 messages AI adds [DONE] tag
↓
ManagerNotifier saves data to clients.json
↓
Manager receives Telegram notification with client details

---

## Example Conversation
Client: /start
Bot: Good day! My name is Alex, I represent BotFlow company...
Client: What does your company do?
Bot: We specialize in creating AI chatbots that work 24/7...
Client: How many people are on your team?
Bot: Our team consists of 3 people...
[After several messages]
Bot: Great, I've noted your request! Our manager will contact you shortly...
[Manager receives in Telegram:]
🔔 New client inquiry!
👤 Client: @username
🆔 Telegram ID: 123456789
📝 Summary: ...

---
