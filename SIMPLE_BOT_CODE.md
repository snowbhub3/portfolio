# Простий код для бота з inline кнопкою

## Проблема

Telegram версія 6.0 не передає дані користувача через Menu Button.

## Рішення

Використайте inline кнопку - працює у всіх версіях Telegram.

## Код для Python (Telebot):

```python
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# Вставте ваш токен бота
BOT_TOKEN = "ВАШ_ТОКЕН_БОТА"
bot = telebot.TeleBot(BOT_TOKEN)

# URL вашого додатку
WEBAPP_URL = "https://a1c16b064f7149d9a9291176d41387b1-pulse-field.projects.builder.my/"

@bot.message_handler(commands=['start', 'wallet'])
def send_wallet(message):
    # Створення inline кнопки з Web App
    markup = InlineKeyboardMarkup()
    webapp_button = InlineKeyboardButton(
        text="💰 Відкрити Кошелёк",
        web_app=WebAppInfo(url=WEBAPP_URL)
    )
    markup.add(webapp_button)

    # Відправка повідомлення з кнопкою
    bot.reply_to(
        message,
        "🚀 Ласкаво просимо до Crypto Wallet!\n\n"
        "Натисніть кнопку нижче для відкриття вашого кошелька:",
        reply_markup=markup
    )

# Запуск бота
if __name__ == "__main__":
    print("🤖 Бот запущено!")
    bot.polling(none_stop=True)
```

## Код для Node.js:

```javascript
const TelegramBot = require("node-telegram-bot-api");

// Вставте ваш токен бота
const token = "ВАШ_ТОКЕН_БОТА";
const bot = new TelegramBot(token, { polling: true });

// URL вашого додатку
const webappUrl =
  "https://a1c16b064f7149d9a9291176d41387b1-pulse-field.projects.builder.my/";

// Обробник команд /start та /wallet
bot.onText(/\/(start|wallet)/, (msg) => {
  const chatId = msg.chat.id;

  const opts = {
    reply_markup: {
      inline_keyboard: [
        [
          {
            text: "💰 Відкрити Кошелёк",
            web_app: {
              url: webappUrl,
            },
          },
        ],
      ],
    },
  };

  bot.sendMessage(
    chatId,
    "🚀 Ласкаво просимо до Crypto Wallet!\n\nНатисніть кнопку нижче для відкриття вашого кошелька:",
    opts,
  );
});

console.log("🤖 Бот запущено!");
```

## Встановлення та запуск:

### Python:

```bash
pip install pyTelegramBotAPI
python bot.py
```

### Node.js:

```bash
npm install node-telegram-bot-api
node bot.js
```

## Що має статися після налаштування:

✅ При натисканні `/start` або `/wallet` з'явиться inline кнопка  
✅ При натисканні кнопки відкриється міні-застосунок  
✅ Дані користувача будуть передаватися автоматично  
✅ Працює у всіх версіях Telegram

## Отримання токену бота:

1. Напишіть @BotFather у Telegram
2. Відправте `/newbot`
3. Вкажіть назву бота
4. Вкажіть username бота
5. ��копіюйте токен і вставте у код

## Альтернативно - готові рішення:

- **Manybot.io** - створення ботів без програмування
- **Chatfuel** - конструктор ботів з Web App підтримкою
- **BotFramework** - розширені можливості

## Тестування:

Після запуску бота:

1. Знайдіть бота у Telegram
2. Напишіть `/start`
3. Натисніть inline кнопку "💰 Відкрити Кошелёк"
4. Перевірте консоль - має з'явитися реальні дані користувача

```
👤 User data: {id: 123456, first_name: "Ваше ім'я", ...}
```
