"""
Keep-Alive механизм для Telegram бота
Предотвращает "засыпание" на GitHub Actions
"""

import requests
import threading
import time

def keep_alive():
    """Функция для поддержания активности бота"""
    while True:
        try:
            # Делаем простой запрос к самому себе (если бот имеет веб-сервер)
            # или просто логируем активность
            print(f"💓 Keep-alive сигнал в {time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Здесь можно добавить любой легкий запрос к вашему боту
            # Например, проверка статуса или получение информации
            
            time.sleep(240)  # Ждём 4 минуты перед следующим сигналом
        except Exception as e:
            print(f"❌ Ошибка keep-alive: {e}")
            time.sleep(60)

def start_keep_alive():
    """Запускает keep-alive в отдельном потоке"""
    thread = threading.Thread(target=keep_alive, daemon=True)
    thread.start()
    print("✅ Keep-alive механизм запущен")
