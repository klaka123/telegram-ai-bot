"""
TELEGRAM БОТ — С отображением прогресса обработки
"""

import os
import telebot
from telebot import types
from model import brain
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

TOKEN = os.environ.get('BOT_TOKEN')
if not TOKEN:
    logging.error("❌ Нет токена!")
    exit(1)

bot = telebot.TeleBot(TOKEN)

# Передаем экземпляр бота в нейросеть для обновления статуса
brain.set_bot(bot)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('📷 Фото', '📝 Пример')
    markup.row('🎭 Шутка', '📊 Факт', '❓ Помощь')
    
    welcome = """
🔬 **АНАЛИТИЧЕСКАЯ СИСТЕМА — 30+ НЕЙРОСЕТЕЙ**

Принцип работы:
• 30+ нейросетей одновременно анализируют ваш вопрос
• Система собирает ответы от всех доступных моделей
• Выдаётся самый быстрый и точный ответ
• Прогресс отображается в реальном времени

📊 **Сейчас в работе:**
• Gemini 2.0 Flash (быстрейшая)
• NVIDIA Nemotron VL (фото/видео)
• Step 3.5 Flash (350 токенов/сек)
• Trinity Mini (молниеносная)
• И ещё 25+ нейросетей

📝 **Примеры:**
• 150 + 150 / 2 = 225
• cos 30° = 0.866
• x² - 5x + 6 = 0 → x = 2, x = 3

Отправьте сообщение или фото для анализа.
    """
    
    bot.send_message(message.chat.id, welcome, reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = """
📚 **Доступные команды:**
/start - начало работы
/help - справка
/clear - сброс диалога

📝 **Примеры запросов:**
• 150 + 150 / 2
• cos 30°
• x² - 5x + 6 = 0
• расскажи шутку
• интересный факт

📸 **Фото:** отправьте изображение с примером
    """
    bot.reply_to(message, help_text, parse_mode='Markdown')

@bot.message_handler(commands=['clear'])
def clear_command(message):
    if brain.clear_context(message.from_user.id):
        bot.reply_to(message, "🧹 История диалога очищена")
    else:
        bot.reply_to(message, "✅ История уже пуста")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        bot.send_chat_action(message.chat.id, 'typing')
        status = bot.reply_to(message, "📸 **Анализ фото...**\n\n⏳ Запускаю vision-нейросети...")
        
        analysis = brain.analyze_photo(
            downloaded_file, 
            message.from_user.id,
            chat_id=message.chat.id,
            status_message_id=status.message_id
        )
        
        bot.delete_message(message.chat.id, status.message_id)
        bot.reply_to(message, f"📸 **Результат анализа:**\n\n{analysis}")
        
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
        bot.reply_to(message, "📝 **Примеры:**\n• `150 + 150 / 2`\n• `cos 30°`\n• `x² - 5x + 6 = 0`", parse_mode='Markdown')
        return
    if user_text == '🎭 Шутка':
        user_text = "расскажи шутку"
    if user_text == '📊 Факт':
        user_text = "интересный факт"
    if user_text == '❓ Помощь':
        help_command(message)
        return
    
    bot.send_chat_action(message.chat.id, 'typing')
    status = bot.reply_to(message, "🔄 **Анализ запроса...**\n\n⏳ Запускаю 30+ нейросетей...")
    
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
    logging.info("🚀 ЗАПУСК TELEGRAM БОТА — 30+ НЕЙРОСЕТЕЙ")
    logging.info("=" * 80)
    
    try:
        bot.polling(non_stop=True, interval=0, timeout=20)
    except Exception as e:
        logging.error(f"❌ Ошибка: {e}")
