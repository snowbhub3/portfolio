# Інструкції для виправлення проблеми з Telegram ботом

## Проблема

Telegram Web App API працює, але дані користувача не передаються (`User data: undefined`).

## Причина

Бот не налаштований для передачі даних користувача до міні-застосунку.

## Крок за кроком розв'язання:

### 1. Відкрийте @BotFather у Telegram

### 2. Налаштуйте Menu Button правильно

```
/setmenubutton
```

- Виберіть вашого бота
- **Назва кнопки:** `Кошелёк`
- **URL:** `https://a1c16b064f7149d9a9291176d41387b1-pulse-field.projects.builder.my/`

### 3. ВАЖЛИВО: Налаштуйте Web App Domain

```
/newapp
```

- Виберіть вашого бота
- **Назва:** `Crypto Wallet`
- **Опис:** `Персональний криптовалютний кошелёк`
- **Фото:** (завантажте іконку 512x512)
- **Web App URL:** `https://a1c16b064f7149d9a9291176d41387b1-pulse-field.projects.builder.my/`

### 4. Альтернативний метод - Inline кнопка

Додайте цей код до вашого бота (якщо ви маєте доступ до коду):

```python
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

# У вашому обробнику команд
def start(update, context):
    keyboard = [
        [InlineKeyboardButton(
            "💰 Відкрити Кошелёк",
            web_app=WebAppInfo(url="https://a1c16b064f7149d9a9291176d41387b1-pulse-field.projects.builder.my/")
        )]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Ласкаво просимо до Crypto Wallet!", reply_markup=reply_markup)
```

### 5. Перевірка налашту��ань бота

```
/mybots
```

- Виберіть вашого бота
- Перевірте що Web App налаштовано
- Перевірте що Menu Button встановлено

### 6. Тестування

1. **Закрийте і перезапустіть Telegram**
2. **Знайдіть вашого бота**
3. **Натисніть кнопку меню (☰) поруч з полем вводу**
4. **Виберіть "Кошелёк"**

### 7. Перевірка через команду

Додайте команду до бота:

```
/setcommands

start - Запустити кошелёк
wallet - Відкрити кошелёк
```

І у коді бота додайте:

```python
def wallet_command(update, context):
    keyboard = [
        [InlineKeyboardButton(
            "💰 Відкрити Кошелёк",
            web_app=WebAppInfo(url="https://a1c16b064f7149d9a9291176d41387b1-pulse-field.projects.builder.my/")
        )]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Натисніть кнопку нижче:", reply_markup=reply_markup)
```

## Що має працювати після налаштування:

✅ Дані користувача передаються автоматично  
✅ Фото користувача відображається  
✅ Кнопка "Назад" працює  
✅ Haptic feedback (якщо версія Telegram > 6.1)

## Альтернативні варіанти:

### Якщо використовуєте готового бота:

1. **Manybot** - підтримує Web Apps
2. **Chatfuel** - має інтеграцію з Web Apps
3. **BotFramework** - повна підтримка Telegram Web Apps

### Якщо створюєте власного бота:

Використайте бібліотеки:

- **Python:** python-telegram-bot
- **Node.js:** node-telegram-bot-api
- **PHP:** TelegramBotAPI

## Перевірка результату:

Після правильного налаштування у консолі має бути:

```
👤 User data: {id: 123456, first_name: "Ваше ім'я", ...}
```

Замість:

```
👤 User data: undefined
```
