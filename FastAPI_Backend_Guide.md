# FastAPI Backend для Crypto Wallet Telegram Mini App

Этот документ описывает структуру и API endpoints для FastAPI бэкенда, которые нужно реализовать для поддержки фронтенда крипто-кошелька.

## Структура проекта

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # Основной файл FastAPI приложения
│   ├── models/              # SQLAlchemy модели
│   │   ├── __init__.py
│   │   ├── user.py          # Модель пользователя
│   │   ├── wallet.py        # Модель кошелька
│   │   ├── transaction.py   # Модель транзакций
│   │   └── asset.py         # Модель активов
│   ├── schemas/             # Pydantic схемы
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── wallet.py
│   │   ├── transaction.py
│   │   └── asset.py
│   ├── api/                 # API маршруты
│   │   ├── __init__.py
│   │   ├── auth.py          # Аутентификация через Telegram
│   │   ├── wallet.py        # Операции с кошельком
│   │   ├── transactions.py  # История транзакций
│   │   ├── assets.py        # Криптоактивы
│   │   └── cfd.py           # CFD торговля
│   ├── core/                # Основные настройки
│   │   ├── __init__.py
│   │   ├── config.py        # Конфигурация
│   │   ├── database.py      # Настройки БД
│   │   └── security.py      # Безопасность
│   └── services/            # Бизнес-логика
│       ├── __init__.py
│       ├── telegram_auth.py
│       ├── wallet_service.py
│       └── market_service.py
├── requirements.txt
└── docker-compose.yml
```

## Основные dependencies

```txt
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9  # для PostgreSQL
sqlite3  # для SQLite (встроенный)
pydantic==2.5.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
httpx==0.25.2
python-dotenv==1.0.0
```

## API Endpoints

### Аутентификация

#### `POST /api/auth/telegram`

Аутентификация через Telegram WebApp данные

```python
class TelegramAuthRequest(BaseModel):
    init_data: str
    hash: str

class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse
```

### Пользователь

#### `GET /api/user/profile`

Получить профиль пользователя

```python
class UserResponse(BaseModel):
    id: int
    telegram_id: int
    first_name: str
    last_name: str | None
    username: str | None
    language_code: str | None
    created_at: datetime
```

### Кошелек

#### `GET /api/wallet/balance`

Получить баланс кошелька

```python
class WalletBalance(BaseModel):
    total_usd: float
    assets: List[AssetBalance]

class AssetBalance(BaseModel):
    symbol: str
    name: str
    balance: float
    price_usd: float
    value_usd: float
    change_24h: float
```

#### `GET /api/wallet/address`

Получить адрес кошелька

```python
class WalletAddress(BaseModel):
    address: str
    network: str
```

### Транзакции

#### `GET /api/transactions/history`

История транзакций с пагинацией

```python
class TransactionResponse(BaseModel):
    id: int
    type: str  # "send", "receive", "exchange", "bonus"
    asset: str
    amount: float
    usd_value: float
    status: str  # "completed", "pending", "failed"
    timestamp: datetime
    description: str
    hash: str | None

class TransactionHistory(BaseModel):
    transactions: List[TransactionResponse]
    total: int
    page: int
    per_page: int
```

#### `POST /api/transactions/send`

Отправить криптовалюту

```python
class SendTransactionRequest(BaseModel):
    to_address: str
    asset: str
    amount: float

class TransactionResult(BaseModel):
    transaction_id: int
    hash: str
    status: str
```

### Активы и рынок

#### `GET /api/assets/trending`

Топовые/трендовые активы

```python
class MarketAsset(BaseModel):
    symbol: str
    name: str
    price_usd: float
    change_24h: float
    market_cap: float
    volume_24h: float
    sparkline: List[float]
```

#### `GET /api/assets/{symbol}/price`

Цена конкретного актива

```python
class AssetPrice(BaseModel):
    symbol: str
    price_usd: float
    change_24h: float
    timestamp: datetime
```

### CFD Торговля

#### `GET /api/cfd/positions`

Получить открытые CFD позиции

```python
class CFDPosition(BaseModel):
    id: int
    symbol: str
    side: str  # "buy" or "sell"
    size: float
    entry_price: float
    current_price: float
    pnl: float
    pnl_percent: float
    created_at: datetime
```

#### `POST /api/cfd/open`

Открыть CFD позицию

```python
class OpenCFDRequest(BaseModel):
    symbol: str
    side: str  # "buy" or "sell"
    size: float
    leverage: int = 1

class CFDOrderResult(BaseModel):
    position_id: int
    status: str
    entry_price: float
```

### Бонусы

#### `GET /api/bonuses/active`

Активные бонусные программы

```python
class BonusProgram(BaseModel):
    id: int
    name: str
    asset: str
    apy_percent: float
    min_amount: float
    status: str
    icon: str
```

#### `POST /api/bonuses/stake`

Заблокировать средства в бонусной программе

```python
class StakeRequest(BaseModel):
    bonus_id: int
    amount: float

class StakeResult(BaseModel):
    stake_id: int
    estimated_reward: float
    unlock_date: datetime
```

## Модели базы данных

### User

```python
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String)
    username = Column(String)
    language_code = Column(String, default="en")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

### Wallet

```python
class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    address = Column(String, unique=True, nullable=False)
    network = Column(String, default="TON")
    encrypted_private_key = Column(Text)  # Зашифрованный приватный ключ
    created_at = Column(DateTime, default=datetime.utcnow)
```

### Transaction

```python
class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    wallet_id = Column(Integer, ForeignKey("wallets.id"))
    type = Column(String, nullable=False)  # send, receive, exchange, bonus
    asset = Column(String, nullable=False)
    amount = Column(Numeric(18, 8), nullable=False)
    usd_value = Column(Numeric(18, 2))
    status = Column(String, default="pending")
    description = Column(String)
    hash = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
```

## Настройка CORS

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",  # Локальная разработка
        "https://your-telegram-app.com",  # Продакшн домен
        "https://web.telegram.org",  # Telegram Web
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Безопасность

1. **Проверка Telegram WebApp данных**: Всегда проверяйте hash в init_data
2. **JWT токены**: Используйте для авторизации API запросов
3. **Rate limiting**: Ограничивайте количество запросов от одного пользователя
4. **Шифрование**: Никогда не храните приватные ключи в открытом виде
5. **Валидация**: Валидируйте все входящие данные через Pydantic

## Запуск

### Локально

```bash
# Установка зависимостей
pip install -r requirements.txt

# Создание таблиц БД
python -c "from app.core.database import create_tables; create_tables()"

# Запуск сервера
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Docker

```bash
docker-compose up -d
```

## Переменные окружения

```env
DATABASE_URL=postgresql://user:password@localhost/crypto_wallet
SECRET_KEY=your-secret-key-here
TELEGRAM_BOT_TOKEN=your-bot-token
JWT_SECRET=your-jwt-secret
ENVIRONMENT=development
```

Этот бэкенд обеспечит полную функциональность для Telegram Mini App крипто-кошелька с поддержкой торговли CFD, бонусных программ и безопасного управления криптоактивами.
