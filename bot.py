"""
TELEGRAM БОТ — Умный выбор нейросетей
"""

import os
import telebot
from telebot import types
from model import brain
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

TOKEN = os.environ.get('BOT_TOKEN')
if not TOKEN:
    logging.error("❌ Нет токена!")
    exit(1)

bot = telebot.TeleBot(TOKEN)
brain.set_bot(bot)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('📷 Фото', '📝 Пример', '🧠 Сложный вопрос')
    markup.row('🎭 Шутка', '📊 Факт', '❓ Помощь')
    
    welcome = """
🔬 **ИНТЕЛЛЕКТУАЛЬНАЯ СИСТЕМА — 31 НЕЙРОСЕТЬ**

⚡ **БЫСТРЫЕ МОДЕЛИ** (для простых вопросов):
• Step 3.5 Flash (2-3 сек)
• Trinity Mini (3-4 сек)
• Mistral 7B (4-5 сек)

🧠 **МОЩНЫЕ МОДЕЛИ** (для сложных задач):
• Gemini 2.0 Flash (1M контекста)
• Llama 3.3 70B (GPT-4 уровень)
• DeepSeek R1 (математика)
• Qwen3 235B (наука)

📸 **VISION МОДЕЛИ** (для фото):
• Gemini 2.0 Flash (быстрейшая)
• NVIDIA Nemotron VL (OCR)
• Qwen3 VL (видео/фото)

📝 **Примеры:**
• Простой: `150 + 150 / 2`
• Сложный: `Объясни теорию относительности`

Система сама выберет лучшие модели для вашего вопроса!
    """
    
    bot.send_message(message.chat.id, welcome, reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        bot.send_chat_action(message.chat.id, 'typing')
        status = bot.reply_to(message, "📸 **Анализ фото...**\n\nЗапускаю vision-нейросети...")
        
        analysis = brain.analyze_photo(
            downloaded_file, 
            message.from_user.id,
            chat_id=message.chat.id,
            status_message_id=status.message_id
        )
        
        bot.delete_message(message.chat.id, status.message_id)
        bot.reply_to(message, analysis)
        
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {str(e)}")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    user_text = message.text
    
    # Обработка кнопок
    if user_text == '📷 Фото':
        bot.reply_to(message, "📸 Отправьте фото с примером для анализа")
        return
    if user_text == '📝 Пример':
        bot.reply_to(message, "📝 **Примеры:**\n• Простой: `150 + 150 / 2`\n• Сложный: `Объясни теорию относительности`", parse_mode='Markdown')
        return
    if user_text == '🧠 Сложный вопрос':
        bot.reply_to(message, "🧠 Задайте сложный вопрос (наука, философия, математика). Будут использованы мощные модели.")
        return
    if user_text == '🎭 Шутка':
        user_text = "расскажи шутку"
    if user_text == '📊 Факт':
        user_text = "интересный факт"
    if user_text == '❓ Помощь':
        bot.reply_to(message, "❓ /start - начало\n📷 Фото - анализ изображения\n🧠 Сложный вопрос - для сложных тем")
        return
    
    bot.send_chat_action(message.chat.id, 'typing')
    status = bot.reply_to(message, "🔬 **Анализ запроса...**\n\nОпределяю сложность и выбираю модели...")
    
    try:
        response = brain.get_response(
            message.from_user.id, 
            user_text,
            chat_id=message.chat.id,
            status_message_id=status.message_id
        )
        
        bot.delete_message(message.chat.id, status.message_id)
        bot.reply_to(message, response)
    except Exception as e:
        bot.delete_message(message.chat.id, status.message_id)
        bot.reply_to(message, f"❌ Ошибка: {str(e)}")

if __name__ == "__main__":
    logging.info("=" * 80)
    logging.info("🚀 ЗАПУСК БОТА — 31 НЕЙРОСЕТЬ, УМНЫЙ ВЫБОР")
    logging.info("=" * 80)
    
    try:
        bot.polling(non_stop=True, interval=0, timeout=20)
    except Exception as e:
        logging.error(f"❌ Ошибка: {e}")
