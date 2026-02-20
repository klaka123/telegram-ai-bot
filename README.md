# telegram-ai-bot
# 🤖 Telegram Bot с СОБСТВЕННОЙ нейросетью

## 🚀 Как запустить на GitHub

### 1. Создай репозиторий
- Зайди на [GitHub.com](https://github.com)
- Нажми "New repository"
- Назови его `telegram-ai-bot`
- Загрузи туда все 4 файла

### 2. Получи токен бота
- Найди в Telegram @BotFather
- Отправь `/newbot`
- Назови бота
- Получи токен (типа `123456:ABC-DEF1234gh...`)

### 3. Вставь токен в код
- Открой файл `bot.py`
- Найди строку `TOKEN = "8039595780..."`
- Вставь СВОЙ токен вместо моего

### 4. Запусти на GitHub
- Зайди в свой репозиторий
- Нажми "Actions"
- Создай новый workflow
- Вставь этот код:

```yaml
name: Run Telegram Bot

on:
  push:
    branches: [ main ]
  schedule:
    - cron: '*/5 * * * *'  # Каждые 5 минут

jobs:
  bot:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Run bot
        env:
          TOKEN: ${{ secrets.TOKEN }}
        run: python bot.py
        timeout-minutes: 4
