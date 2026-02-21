"""
Keep-Alive механизм для Telegram бота
Предотвращает "засыпание" на GitHub Actions
"""

import threading
import time
import requests
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def keep_alive():
    """Функция для поддержания активности бота"""
    counter = 0
    while True:
        try:
            counter += 1
            logging.info(f"💓 Keep-alive сигнал #{counter} в {time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Здесь можно добавить легкий запрос к любому сервису
            # или просто логировать активность
            
            time.sleep(240)  # Ждём 4 минуты перед следующим сигналом
        except Exception as e:
            logging.error(f"❌ Ошибка keep-alive: {e}")
            time.sleep(60)

def start_keep_alive():
    """Запускает keep-alive в отдельном потоке"""
    thread = threading.Thread(target=keep_alive, daemon=True)
    thread.start()
    logging.info("✅ Keep-alive механизм запущен в отдельном потоке")
