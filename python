"""
НАША СОБСТВЕННАЯ НЕЙРОСЕТЬ
Создана полностью с нуля, без использования готовых моделей
Обучается на ваших сообщениях и отвечает как вы!
"""

import numpy as np
import json
import os
import random
from collections import defaultdict
import re

class TelegramNeuralNetwork:
    """
    Простая, но эффективная нейросеть для Telegram бота
    Основана на комбинации Markov цепей и нейронной сети прямого распространения
    """
    
    def __init__(self, name="my_brain"):
        self.name = name
        self.vocabulary = {}  # Словарь: слово -> индекс
        self.reverse_vocab = []  # Обратный словарь: индекс -> слово
        self.words_count = 0  # Количество уникальных слов
        
        # Параметры нейросети
        self.hidden_size = 128  # Количество нейронов в скрытом слое
        self.learning_rate = 0.01  # Скорость обучения
        
        # Веса нейросети (инициализируем позже)
        self.W1 = None  # Веса вход -> скрытый слой
        self.W2 = None  # Веса скрытый -> выход
        self.b1 = None  # Смещение скрытого слоя
        self.b2 = None  # Смещение выходного слоя
        
        # Markov цепь для улучшения качества ответов
        self.markov_chain = defaultdict(lambda: defaultdict(int))
        
        # История диалогов
        self.conversations = []
        
        # Файл для сохранения
        self.save_file = f"{name}_weights.json"
        
        print("🤖 Нейросеть инициализирована!")
    
    def tokenize(self, text):
        """Разбивает текст на слова"""
        # Приводим к нижнему регистру и убираем знаки препинания
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        return text.split()
    
    def add_to_vocabulary(self, words):
        """Добавляет новые слова в словарь"""
        for word in words:
            if word not in self.vocabulary:
                self.vocabulary[word] = self.words_count
                self.reverse_vocab.append(word)
                self.words_count += 1
        
        # Если словарь увеличился, обновляем размеры нейросети
        if self.words_count > 0 and (self.W1 is None or self.words_count > self.W1.shape[0]):
            self._initialize_weights()
    
    def _initialize_weights(self):
        """Инициализирует веса нейросети"""
        input_size = self.words_count
        output_size = self.words_count
        
        if input_size == 0:
            return
        
        # Инициализация весов методом Xavier/Glorot
        self.W1 = np.random.randn(input_size, self.hidden_size) * np.sqrt(2.0 / input_size)
        self.W2 = np.random.randn(self.hidden_size, output_size) * np.sqrt(2.0 / self.hidden_size)
        self.b1 = np.zeros((1, self.hidden_size))
        self.b2 = np.zeros((1, output_size))
        
        print(f"🧠 Размер нейросети: вход={input_size}, скрытый={self.hidden_size}, выход={output_size}")
    
    def softmax(self, x):
        """Функция активации softmax"""
        exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=1, keepdims=True)
    
    def relu(self, x):
        """Функция активации ReLU"""
        return np.maximum(0, x)
    
    def relu_derivative(self, x):
        """Производная ReLU"""
        return (x > 0).astype(float)
    
    def forward(self, input_vector):
        """Прямой проход по нейросети"""
        # Входной слой -> скрытый слой
        self.z1 = np.dot(input_vector, self.W1) + self.b1
        self.a1 = self.relu(self.z1)
        
        # Скрытый слой -> выходной слой
        self.z2 = np.dot(self.a1, self.W2) + self.b2
        self.a2 = self.softmax(self.z2)
        
        return self.a2
    
    def backward(self, input_vector, target_vector, output):
        """Обратное распространение ошибки"""
        m = input_vector.shape[0]
        
        # Ошибка на выходном слое
        dZ2 = output - target_vector
        dW2 = (1/m) * np.dot(self.a1.T, dZ2)
        db2 = (1/m) * np.sum(dZ2, axis=0, keepdims=True)
        
        # Ошибка на скрытом слое
        dA1 = np.dot(dZ2, self.W2.T)
        dZ1 = dA1 * self.relu_derivative(self.a1)
        dW1 = (1/m) * np.dot(input_vector.T, dZ1)
        db1 = (1/m) * np.sum(dZ1, axis=0, keepdims=True)
        
        # Обновление весов
        self.W2 -= self.learning_rate * dW2
        self.b2 -= self.learning_rate * db2
        self.W1 -= self.learning_rate * dW1
        self.b1 -= self.learning_rate * db1
    
    def text_to_vector(self, text):
        """Преобразует текст в вектор для нейросети"""
        words = self.tokenize(text)
        vector = np.zeros((1, self.words_count))
        
        for word in words:
            if word in self.vocabulary:
                vector[0, self.vocabulary[word]] += 1
        
        # Нормализация
        if np.sum(vector) > 0:
            vector = vector / np.sum(vector)
        
        return vector
    
    def vector_to_text(self, vector, temperature=0.8):
        """Преобразует вектор нейросети обратно в текст"""
        if self.words_count == 0:
            return "..."
        
        # Применяем температуру для разнообразия ответов
        logits = np.log(vector + 1e-10) / temperature
        exp_logits = np.exp(logits - np.max(logits))
        probs = exp_logits / np.sum(exp_logits)
        
        # Выбираем слово
        try:
            word_index = np.random.choice(self.words_count, p=probs.flatten())
            return self.reverse_vocab[word_index]
        except:
            return random.choice(self.reverse_vocab)
    
    def update_markov_chain(self, text):
        """Обновляет Markov цепь на основе текста"""
        words = self.tokenize(text)
        for i in range(len(words) - 1):
            self.markov_chain[words[i]][words[i + 1]] += 1
    
    def generate_with_markov(self, start_word=None, max_length=10):
        """Генерирует текст с помощью Markov цепи"""
        if not self.markov_chain:
            return ""
        
        if start_word is None or start_word not in self.markov_chain:
            start_word = random.choice(list(self.markov_chain.keys()))
        
        result = [start_word]
        current_word = start_word
        
        for _ in range(max_length - 1):
            if current_word not in self.markov_chain:
                break
            
            next_words = self.markov_chain[current_word]
            if not next_words:
                break
            
            # Выбираем следующее слово с учетом вероятностей
            words = list(next_words.keys())
            counts = list(next_words.values())
            total = sum(counts)
            probs = [c/total for c in counts]
            
            current_word = np.random.choice(words, p=probs)
            result.append(current_word)
        
        return " ".join(result)
    
    def train_on_message(self, message, response=None):
        """Обучает нейросеть на одном сообщении"""
        words = self.tokenize(message)
        self.add_to_vocabulary(words)
        self.update_markov_chain(message)
        
        # Если это диалог (есть и вопрос и ответ)
        if response:
            self.conversations.append((message, response))
            
            # Обучаем нейросеть предсказывать ответы
            if self.words_count > 0 and self.W1 is not None:
                input_vector = self.text_to_vector(message)
                target_words = self.tokenize(response)
                
                for target_word in target_words:
                    if target_word in self.vocabulary:
                        target_vector = np.zeros((1, self.words_count))
                        target_vector[0, self.vocabulary[target_word]] = 1
                        
                        # Прямой проход
                        output = self.forward(input_vector)
                        
                        # Обратный проход
                        self.backward(input_vector, target_vector, output)
        
        print(f"📚 Обучен на сообщении: {message[:50]}...")
    
    def generate_response(self, message, use_neural=True, use_markov=True):
        """Генерирует ответ на сообщение"""
        if self.words_count == 0:
            return "Я еще не научился говорить. Напиши мне что-нибудь, чтобы я мог учиться!"
        
        # Добавляем сообщение в обучение
        self.train_on_message(message)
        
        # Пробуем разные методы генерации
        response = ""
        
        # Метод 1: Чистая нейросеть
        if use_neural and self.W1 is not None:
            input_vector = self.text_to_vector(message)
            output = self.forward(input_vector)
            
            # Генерируем несколько слов
            words = []
            for _ in range(random.randint(3, 8)):
                word = self.vector_to_text(output)
                words.append(word)
            
            neural_response = " ".join(words)
            response = neural_response
        
        # Метод 2: Markov цепь
        if use_markov and self.markov_chain:
            words = self.tokenize(message)
            if words:
                start_word = words[-1] if words[-1] in self.markov_chain else None
                markov_response = self.generate_with_markov(start_word, random.randint(5, 12))
                
                if markov_response and random.random() > 0.5:
                    response = markov_response
        
        # Метод 3: Комбинация
        if not response:
            # Если ничего не сгенерировалось, берем случайную фразу из обучения
            if self.conversations:
                random_pair = random.choice(self.conversations)
                response = f"Я помню, ты говорил: {random_pair[0]}. А я отвечал: {random_pair[1]}"
            else:
                response = "Интересно... Расскажи еще!"
        
        return response
    
    def save_weights(self):
        """Сохраняет веса нейросети"""
        if self.W1 is None:
            return
        
        data = {
            'vocabulary': self.vocabulary,
            'reverse_vocab': self.reverse_vocab,
            'W1': self.W1.tolist(),
            'W2': self.W2.tolist(),
            'b1': self.b1.tolist(),
            'b2': self.b2.tolist(),
            'markov_chain': dict(self.markov_chain),
            'conversations': self.conversations
        }
        
        with open(self.save_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Нейросеть сохранена в {self.save_file}")
    
    def load_weights(self):
        """Загружает веса нейросети"""
        if not os.path.exists(self.save_file):
            print("📭 Файл с весами не найден, начинаем обучение с нуля")
            return
        
        try:
            with open(self.save_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.vocabulary = data['vocabulary']
            self.reverse_vocab = data['reverse_vocab']
            self.words_count = len(self.vocabulary)
            
            self.W1 = np.array(data['W1'])
            self.W2 = np.array(data['W2'])
            self.b1 = np.array(data['b1'])
            self.b2 = np.array(data['b2'])
            
            self.markov_chain = defaultdict(lambda: defaultdict(int), data['markov_chain'])
            self.conversations = data['conversations']
            
            print(f"✅ Нейросеть загружена! Словарь: {self.words_count} слов, Диалогов: {len(self.conversations)}")
        except Exception as e:
            print(f"❌ Ошибка загрузки: {e}")

# Создаем экземпляр нейросети для использования в боте
brain = TelegramNeuralNetwork("telegram_brain")

# Пробуем загрузить сохраненные веса
brain.load_weights()
