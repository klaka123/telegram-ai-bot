# ========== ОБРАБОТКА ТЕКСТА ==========
@bot.message_handler(func=lambda m: True)
def handle_text(message):
    """Обработка всех текстовых сообщений"""
    
    user_id = message.from_user.id
    user_text = message.text
    
    # Обновляем статистику
    if user_id not in users_stats:
        users_stats[user_id] = {'messages': 0, 'first_seen': datetime.now()}
    users_stats[user_id]['messages'] += 1
    
    # Обработка кнопок
    # Обработка кнопок
if user_text == '💬 Поговорить':
    bot.send_message(message.chat.id, "👋 Отлично! Я слушаю... Напиши мне что-нибудь!")
    return  # ЭТОТ return НЕ ДАЕТ БОТУ ОТВЕТИТЬ НА СЛЕДУЮЩЕЕ СООБЩЕНИЕ!
    elif user_text == '📊 Статистика':
        stats_command(message)
        return
    elif user_text == '📸 Прислать фото':
        bot.send_message(message.chat.id, "📸 Отправляй фото, я проанализирую!")
        return
    elif user_text == '❓ Помощь':
        help_command(message)
        return
    
    # Показываем что бот печатает
    bot.send_chat_action(message.chat.id, 'typing')
    
    # Генерируем ответ
    response = brain.generate_response(user_text, user_id)
    
    # Добавляем эмодзи
    emojis = ['😊', '🤔', '🌟', '💫', '✨', '🎯', '🚀', '💡']
    if random.random() > 0.5 and not any(e in response for e in emojis):
        response += ' ' + random.choice(emojis)
    
    # Отправляем ответ
    bot.reply_to(message, response)
    
    # Обучаемся на диалоге
    brain.train_on_message(user_text, response)
    
    # Автосохранение каждые 10 сообщений
    if users_stats[user_id]['messages'] % 10 == 0:
        print(f"💾 Автосохранение для пользователя {user_id}")
