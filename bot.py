import os
import telebot
from model import brain  # ЭТО ПРАВИЛЬНО! Только здесь импорт

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я бот! Напиши мне что-нибудь!")

@bot.message_handler(func=lambda m: True)
def handle(message):
    response = brain.get_response(message.from_user.id, message.text)
    bot.reply_to(message, response)

bot.infinity_polling()
