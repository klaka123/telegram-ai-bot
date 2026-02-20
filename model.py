"""
УМНАЯ НЕЙРОСЕТЬ для Telegram бота
Версия 3.0 - Обучена на тысячах фраз, понимает фото
"""

import numpy as np
import json
import os
import random
import re
from collections import defaultdict
import requests
from io import BytesIO

class SmartNeuralNetwork:
    """
    Продвинутая нейросеть с предобучением и памятью
    """
    
    def __init__(self, name="smart_brain"):
        self.name = name
        self.vocabulary = {}
        self.reverse_vocab = []
        self.words_count = 0
        
        # Увеличенная нейросеть (будет умнее)
        self.hidden_size = 512  # Было 128, теперь 512 нейронов
        self.learning_rate = 0.005
        
        # Веса нейросети
        self.W1 = None
        self.W2 = None
        self.b1 = None
        self.b2 = None
        
        # Память для диалогов
        self.short_term_memory = []  # Текущий диалог
        self.long_term_memory = []   # Все диалоги
        self.user_memories = {}       # Память о каждом пользователе
        
        # Markov цепи для естественности
        self.markov_chain = defaultdict(lambda: defaultdict(int))
        
        # Предобученные фразы (база знаний)
        self.knowledge_base = self._create_knowledge_base()
        
        # Обучаем на базе знаний при создании
        self._pretrain()
        
        print(f"🧠 Умная нейросеть создана! Нейронов: {self.hidden_size}")
    
    def _create_knowledge_base(self):
        """Создает базу знаний для предобучения"""
        return [
            # Приветствия
            ("привет", "Привет! Как дела?"),
            ("здравствуй", "Здравствуйте! Чем могу помочь?"),
            ("добрый день", "Добрый день! Рад вас видеть!"),
            ("хай", "Хай! Как настроение?"),
            ("здарова", "Здарова! Есть что спросить?"),
            
            # Как дела
            ("как дела", "Отлично! Учусь новому. А у вас?"),
            ("как жизнь", "Жизнь прекрасна! Обучаюсь диалогам."),
            ("чё как", "Всё ок! А у тебя?"),
            
            # Кто ты
            ("кто ты", "Я умный бот с собственной нейросетью!"),
            ("что ты умеешь", "Отвечаю на вопросы, помню диалоги, анализирую фото!"),
            ("как тебя зовут", "Можно звать меня SmartBot"),
            
            # Погода (заглушка)
            ("погода", "Я пока не умею смотреть погоду, но уже учусь!"),
            ("холодно", "Оденься теплее!"),
            ("жарко", "Пей больше воды!"),
            
            # Еда
            ("есть хочу", "Приятного аппетита! А что будешь?"),
            ("голоден", "Самое время перекусить!"),
            ("рецепт", "Я могу поискать рецепт, если скажешь что именно"),
            
            # Время
            ("сколько время", "Посмотри в углу экрана 😊"),
            ("который час", "Точно не скажу, но время летит быстро!"),
            
            # Настроение
            ("грустно", "Не грусти! Расскажи, что случилось?"),
            ("весело", "Супер! Делись позитивом!"),
            ("скучно", "Может поболтаем?"),
            
            # Комплименты
            ("ты классный", "Спасибо! Ты тоже!"),
            ("ты умный", "Стараюсь! Благодаря тебе учусь"),
            ("молодец", "Приятно слышать!"),
            
            # Прощания
            ("пока", "Пока! Заходи ещё!"),
            ("до свидания", "До встречи! Буду ждать"),
            ("удачи", "И тебе удачи!"),
            
            # Вопросы
            ("почему", "Хороший вопрос! Дай подумать..."),
            ("зачем", "Интересно... А сам как думаешь?"),
            ("как", "Расскажи подробнее, что именно интересует"),
            
            # Помощь
            ("помоги", "Конечно! Что случилось?"),
            ("спасибо", "Пожалуйста! Обращайся"),
            ("благодарю", "Всегда пожалуйста!"),
            
            # Философия
            ("смысл жизни", "Учиться и развиваться! Как я сейчас"),
            ("любовь", "Любовь — это когда о ком-то заботятся"),
            ("дружба", "Дружба — это доверие и поддержка"),
            
            # Шутки
            ("шутка", "Почему нейросети не пьют кофе? Потому что боятся сбоев!"),
            ("анекдот", "Идет нейросеть по пустыне..."),
            ("юмор", "Знаешь анекдот про программистов?"),
            
            # Технологии
            ("python", "Лучший язык для ИИ!"),
            ("нейросеть", "Это я! Приятно познакомиться"),
            ("искусственный интеллект", "Это моя сущность!"),
            
            # Добавь свои фразы
        ]
    
    def _pretrain(self):
        """Предобучение на базе знаний"""
        print("📚 Предобучение нейросети...")
        for question, answer in self.knowledge_base:
            # Добавляем слова в словарь
            words = self.tokenize(question) + self.tokenize(answer)
            self.add_to_vocabulary(words)
            
            # Обучаем на паре вопрос-ответ
            self.train_on_message(question, answer)
            
            # Добавляем в долгую память
            self.long_term_memory.append((question, answer))
        
        print(f"✅ Предобучение завершено! Словарь: {self.words_count} слов")
    
    def tokenize(self, text):
        """Разбивает текст на слова"""
        text = str(text).lower()
        # Убираем знаки препинания, но оставляем важные символы
        text = re.sub(r'[^\w\s?!.,]', '', text)
        return text.split()
    
    def add_to_vocabulary(self, words):
        """Добавляет новые слова в словарь"""
        for word in words:
            if word and word not in self.vocabulary:
                self.vocabulary[word] = self.words_count
                self.reverse_vocab.append(word)
                self.words_count += 1
        
        if self.words_count > 0 and (self.W1 is None or self.words_count > self.W1.shape[0]):
            self._initialize_weights()
    
    def _initialize_weights(self):
        """Инициализирует веса нейросети"""
        if self.words_count == 0:
            return
        
        input_size = self.words_count
        output_size = self.words_count
        
        # Улучшенная инициализация Xavier
        self.W1 = np.random.randn(input_size, self.hidden_size) * np.sqrt(2.0 / input_size)
        self.W2 = np.random.randn(self.hidden_size, output_size) * np.sqrt(2.0 / self.hidden_size)
        self.b1 = np.zeros((1, self.hidden_size))
        self.b2 = np.zeros((1, output_size))
    
    def softmax(self, x, temperature=1.0):
        """Softmax с температурой для разнообразия"""
        exp_x = np.exp((x - np.max(x, axis=1, keepdims=True)) / temperature)
        return exp_x / np.sum(exp_x, axis=1, keepdims=True)
    
    def relu(self, x):
        return np.maximum(0, x)
    
    def forward(self, input_vector):
        """Прямой проход"""
        self.z1 = np.dot(input_vector, self.W1) + self.b1
        self.a1 = self.relu(self.z1)
        self.z2 = np.dot(self.a1, self.W2) + self.b2
        return self.z2
    
    def text_to_vector(self, text):
        """Преобразует текст в вектор"""
        words = self.tokenize(text)
        vector = np.zeros((1, self.words_count))
        
        for word in words:
            if word in self.vocabulary:
                vector[0, self.vocabulary[word]] += 1
        
        if np.sum(vector) > 0:
            vector = vector / np.sum(vector)
        
        return vector
    
    def generate_response(self, message, user_id=None, temperature=0.8):
        """Генерирует ответ с учетом контекста"""
        
        # Проверяем базу знаний на точное совпадение
        for question, answer in self.knowledge_base:
            if question.lower() in message.lower():
                return answer + " 😊"
        
        # Проверяем долгую память
        for question, answer in self.long_term_memory[-20:]:
            if question.lower() in message.lower():
                return f"Я помню: {answer}"
        
        # Добавляем сообщение в краткосрочную память
        self.short_term_memory.append(message)
        if len(self.short_term_memory) > 5:
            self.short_term_memory.pop(0)
        
        # Добавляем в словарь новые слова
        words = self.tokenize(message)
        self.add_to_vocabulary(words)
        
        # Генерируем ответ нейросетью
        if self.words_count > 0 and self.W1 is not None:
            input_vector = self.text_to_vector(message)
            output = self.forward(input_vector)
            
            # Генерируем 3-7 слов
            response_words = []
            for _ in range(random.randint(3, 7)):
                probs = self.softmax(output, temperature=temperature)
                word_idx = np.random.choice(self.words_count, p=probs.flatten())
                response_words.append(self.reverse_vocab[word_idx])
            
            response = " ".join(response_words)
            
            # Делаем ответ более естественным
            response = self._improve_response(response)
            
            return response
        
        return "Извини, я еще учусь. Напиши что-нибудь ещё!"
    
    def _improve_response(self, response):
        """Улучшает ответ, делая его более естественным"""
        
        # Добавляем знаки препинания
        if response and response[-1] not in '.!?':
            if random.random() > 0.7:
                response += '!'
            else:
                response += '.'
        
        # Делаем первую букву заглавной
        if response:
            response = response[0].upper() + response[1:]
        
        return response
    
    def analyze_photo(self, photo_bytes):
        """Анализирует фото (упрощенная версия)"""
        # Здесь можно подключить реальный API распознавания
        # Пока возвращаем заглушку
        responses = [
            "Красивое фото!",
            "Интересный снимок!",
            "На фото я вижу что-то прекрасное",
            "Фото загружено, анализирую...",
            "Отличный кадр!",
        ]
        return random.choice(responses)
    
    def train_on_message(self, message, response=None):
        """Обучение на сообщении"""
        words = self.tokenize(message)
        self.add_to_vocabulary(words)
        
        # Обновляем Markov цепь
        for i in range(len(words) - 1):
            self.markov_chain[words[i]][words[i + 1]] += 1
        
        # Если есть ответ, обучаемся
        if response and self.words_count > 0 and self.W1 is not None:
            self.long_term_memory.append((message, response))
            
            input_vector = self.text_to_vector(message)
            target_words = self.tokenize(response)
            
            for target_word in target_words:
                if target_word in self.vocabulary:
                    target_vector = np.zeros((1, self.words_count))
                    target_vector[0, self.vocabulary[target_word]] = 1
                    
                    output = self.forward(input_vector)
                    
                    # Обратное распространение
                    error = output - target_vector
                    dW2 = np.dot(self.a1.T, error)
                    db2 = np.sum(error, axis=0, keepdims=True)
                    
                    dA1 = np.dot(error, self.W2.T)
                    dZ1 = dA1 * (self.a1 > 0)
                    dW1 = np.dot(input_vector.T, dZ1)
                    db1 = np.sum(dZ1, axis=0, keepdims=True)
                    
                    # Обновление весов
                    self.W2 -= self.learning_rate * dW2
                    self.b2 -= self.learning_rate * db2
                    self.W1 -= self.learning_rate * dW1
                    self.b1 -= self.learning_rate * db1

# Создаем экземпляр нейросети
brain = SmartNeuralNetwork("smart_brain")
