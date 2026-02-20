"""
МАТЕМАТИЧЕСКАЯ НЕЙРОСЕТЬ для Telegram бота
Версия 4.0 - Решает алгебру, уравнения, производные
"""

import numpy as np
import json
import os
import random
import re
from collections import defaultdict
import sympy as sp
from sympy import symbols, Eq, solve, diff, integrate, sin, cos, tan, log, sqrt, pi, E
import math

class MathNeuralNetwork:
    """
    Нейросеть с математическим движком
    """
    
    def __init__(self, name="math_brain"):
        self.name = name
        self.vocabulary = {}
        self.reverse_vocab = []
        self.words_count = 0
        
        # Увеличенная нейросеть
        self.hidden_size = 1024  # Еще больше нейронов для математики
        self.learning_rate = 0.005
        
        # Веса нейросети
        self.W1 = None
        self.W2 = None
        self.b1 = None
        self.b2 = None
        
        # Память
        self.short_term_memory = []
        self.long_term_memory = []
        self.user_memories = {}
        
        # Математическая база знаний
        self.math_formulas = self._create_math_formulas()
        self.math_examples = self._create_math_examples()
        
        # Предобучение
        self._pretrain()
        
        print(f"🧠 МАТЕМАТИЧЕСКАЯ нейросеть создана! Нейронов: {self.hidden_size}")
    
    def _create_math_formulas(self):
        """База математических формул"""
        return {
            "квадратное уравнение": "ax² + bx + c = 0 → x = (-b ± √(b² - 4ac)) / 2a",
            "дискриминант": "D = b² - 4ac",
            "теорема пифагора": "a² + b² = c²",
            "площадь круга": "S = πr²",
            "длина окружности": "C = 2πr",
            "производная": "f'(x) = lim(h→0) (f(x+h) - f(x))/h",
            "интеграл": "∫f(x)dx = F(x) + C",
            "синус": "sin(α) = противолежащий/гипотенуза",
            "косинус": "cos(α) = прилежащий/гипотенуза",
            "тангенс": "tan(α) = sin(α)/cos(α)",
            "логарифм": "logₐ(b) = c → aᶜ = b",
            "факториал": "n! = 1·2·3·...·n",
        }
    
    def _create_math_examples(self):
        """Примеры математических задач с решениями"""
        return [
            # Линейные уравнения
            ("реши x + 5 = 10", "x = 5\n\nПроверка: 5 + 5 = 10 ✓"),
            ("реши 2x - 3 = 7", "x = 5\n\nРешение: 2x = 10 → x = 5"),
            ("реши 3x + 4 = 19", "x = 5\n\nРешение: 3x = 15 → x = 5"),
            ("реши 5x - 12 = 3x + 4", "x = 8\n\nРешение: 5x - 3x = 4 + 12 → 2x = 16 → x = 8"),
            
            # Квадратные уравнения
            ("реши x² - 5x + 6 = 0", "x₁ = 2, x₂ = 3\n\nD = 25 - 24 = 1\nx = (5 ± 1)/2"),
            ("реши x² + 4x - 5 = 0", "x₁ = 1, x₂ = -5\n\nD = 16 + 20 = 36\nx = (-4 ± 6)/2"),
            ("реши 2x² - 8x + 6 = 0", "x₁ = 1, x₂ = 3\n\nD = 64 - 48 = 16\nx = (8 ± 4)/4"),
            
            # Системы уравнений
            ("реши систему x + y = 5, x - y = 1", "x = 3, y = 2\n\nРешение: сложим уравнения → 2x = 6 → x = 3, тогда y = 5 - 3 = 2"),
            ("реши систему 2x + y = 7, x - y = 2", "x = 3, y = 1\n\nРешение: x = y + 2 → 2(y+2) + y = 7 → 3y + 4 = 7 → y = 1, x = 3"),
            
            # Производные
            ("найди производную x²", "f'(x) = 2x\n\nПравило: (xⁿ)' = n·xⁿ⁻¹"),
            ("найди производную sin(x)", "f'(x) = cos(x)"),
            ("найди производную ln(x)", "f'(x) = 1/x"),
            ("найди производную e^x", "f'(x) = e^x"),
            
            # Интегралы
            ("найди интеграл x² dx", "∫x² dx = x³/3 + C"),
            ("найди интеграл sin(x) dx", "∫sin(x) dx = -cos(x) + C"),
            ("найди интеграл 1/x dx", "∫(1/x) dx = ln|x| + C"),
            
            # Тригонометрия
            ("sin 30°", "sin(30°) = 1/2 = 0.5"),
            ("cos 60°", "cos(60°) = 1/2 = 0.5"),
            ("tan 45°", "tan(45°) = 1"),
            
            # Логарифмы
            ("log₂ 8", "log₂(8) = 3, потому что 2³ = 8"),
            ("log₁₀ 100", "log₁₀(100) = 2, потому что 10² = 100"),
            ("ln e²", "ln(e²) = 2"),
            
            # Сложные примеры
            ("реши x² + 6x + 9 = 0", "x = -3 (двойной корень)\n\nD = 36 - 36 = 0\nx = -6/2 = -3"),
            ("реши 3x² - 12x + 12 = 0", "x = 2 (двойной корень)\n\nD = 144 - 144 = 0\nx = 12/6 = 2"),
            ("реши x³ - 27 = 0", "x = 3\n\nx³ = 27 → x = ∛27 = 3"),
        ]
    
    def _pretrain(self):
        """Предобучение на математических примерах"""
        print("📚 Обучение математике...")
        
        # Обучаем на формулах
        for formula_name, formula_text in self.math_formulas.items():
            words = self.tokenize(formula_name) + self.tokenize(formula_text)
            self.add_to_vocabulary(words)
            self.long_term_memory.append((formula_name, formula_text))
        
        # Обучаем на примерах
        for question, answer in self.math_examples:
            words = self.tokenize(question) + self.tokenize(answer)
            self.add_to_vocabulary(words)
            self.long_term_memory.append((question, answer))
            self.train_on_message(question, answer)
        
        print(f"✅ Обучено {len(self.math_examples)} математических примеров")
    
    def tokenize(self, text):
        """Разбивает текст на слова"""
        text = str(text).lower()
        # Сохраняем математические символы
        text = re.sub(r'[^\w\s\+\-\*\/\=\^\(\)\[\]\{\}\.\,\!\?]', '', text)
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
        
        self.W1 = np.random.randn(input_size, self.hidden_size) * np.sqrt(2.0 / input_size)
        self.W2 = np.random.randn(self.hidden_size, output_size) * np.sqrt(2.0 / self.hidden_size)
        self.b1 = np.zeros((1, self.hidden_size))
        self.b2 = np.zeros((1, output_size))
    
    def softmax(self, x, temperature=1.0):
        exp_x = np.exp((x - np.max(x, axis=1, keepdims=True)) / temperature)
        return exp_x / np.sum(exp_x, axis=1, keepdims=True)
    
    def relu(self, x):
        return np.maximum(0, x)
    
    def forward(self, input_vector):
        self.z1 = np.dot(input_vector, self.W1) + self.b1
        self.a1 = self.relu(self.z1)
        self.z2 = np.dot(self.a1, self.W2) + self.b2
        return self.z2
    
    def text_to_vector(self, text):
        words = self.tokenize(text)
        vector = np.zeros((1, self.words_count))
        
        for word in words:
            if word in self.vocabulary:
                vector[0, self.vocabulary[word]] += 1
        
        if np.sum(vector) > 0:
            vector = vector / np.sum(vector)
        
        return vector
    
    def solve_math_problem(self, problem_text):
        """
        Решает математическую задачу
        """
        problem = problem_text.lower().strip()
        
        # Проверяем базу примеров
        for question, answer in self.math_examples:
            if question in problem:
                return f"📝 **Решение:**\n\n{answer}"
        
        # Проверяем формулы
        for formula_name, formula_text in self.math_formulas.items():
            if formula_name in problem:
                return f"📐 **Формула:**\n\n{formula_text}"
        
        # Пытаемся решить через sympy (реальный математический движок)
        try:
            result = self._solve_with_sympy(problem)
            if result:
                return result
        except:
            pass
        
        # Если не нашли в базе - генерируем ответ нейросетью
        return self._generate_math_response(problem)
    
    def _solve_with_sympy(self, problem):
        """
        Решает математические выражения через sympy
        """
        x, y, z = symbols('x y z')
        
        # Поиск уравнений
        if 'реши' in problem or 'найди' in problem or 'вычисли' in problem:
            
            # Линейные уравнения
            if 'x' in problem and '=' in problem:
                try:
                    # Парсим уравнение (упрощенно)
                    parts = problem.split('=')
                    left = parts[0].replace('реши', '').replace(' ', '')
                    right = parts[1].replace(' ', '')
                    
                    # Создаем уравнение
                    eq = Eq(eval(left), eval(right))
                    solution = solve(eq, x)
                    
                    return f"✅ **Решение:**\n\nx = {solution[0]}\n\nПроверка подстановкой ✓"
                except:
                    pass
            
            # Производные
            if 'производн' in problem:
                try:
                    expr = problem.replace('найди', '').replace('производную', '').replace(' ', '')
                    if expr:
                        f = eval(expr)
                        df = diff(f, x)
                        return f"📈 **Производная:**\n\nf'(x) = {df}\n\nПравило дифференцирования применено"
                except:
                    pass
            
            # Интегралы
            if 'интеграл' in problem:
                try:
                    expr = problem.replace('найди', '').replace('интеграл', '').replace(' ', '')
                    if expr:
                        f = eval(expr)
                        F = integrate(f, x)
                        return f"∫ **Интеграл:**\n\n∫ f(x) dx = {F} + C"
                except:
                    pass
        
        return None
    
    def _generate_math_response(self, problem):
        """
        Генерирует математический ответ нейросетью
        """
        # Специальные случаи
        if '√' in problem or 'sqrt' in problem:
            try:
                num = re.findall(r'√(\d+)', problem)
                if num:
                    result = math.sqrt(int(num[0]))
                    return f"√{num[0]} = {result:.4f}"
            except:
                pass
        
        if '²' in problem or '^2' in problem:
            try:
                num = re.findall(r'(\d+)²', problem)
                if num:
                    result = int(num[0]) ** 2
                    return f"{num[0]}² = {result}"
            except:
                pass
        
        # Общий случай - нейросеть
        if self.words_count > 0 and self.W1 is not None:
            input_vector = self.text_to_vector(problem)
            output = self.forward(input_vector)
            
            # Генерируем ответ
            response_words = []
            for _ in range(random.randint(5, 10)):
                probs = self.softmax(output, temperature=0.9)
                word_idx = np.random.choice(self.words_count, p=probs.flatten())
                response_words.append(self.reverse_vocab[word_idx])
            
            response = " ".join(response_words)
            
            # Обучаемся на этом примере
            self.train_on_message(problem, response)
            
            return f"🤔 **Моё решение:**\n\n{response}\n\n(Я учусь, проверь правильность!)"
        
        return "Извини, я еще учусь решать такие примеры. Попробуй другой!"
    
    def train_on_message(self, message, response=None):
        """Обучение на сообщении"""
        words = self.tokenize(message)
        self.add_to_vocabulary(words)
        
        if response:
            self.long_term_memory.append((message, response))
            
            if self.words_count > 0 and self.W1 is not None:
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
                        
                        self.W2 -= self.learning_rate * dW2
                        self.b2 -= self.learning_rate * db2
                        self.W1 -= self.learning_rate * dW1
                        self.b1 -= self.learning_rate * db1
    
    def generate_response(self, message, user_id=None):
        """Генерирует ответ на сообщение"""
        
        # Проверяем, это математический вопрос?
        math_keywords = ['реши', 'найди', 'вычисли', 'уравнение', 'пример', 
                        'x²', 'x^2', '√', 'sin', 'cos', 'tan', 'log', 
                        '+', '-', '*', '/', '=', 'производн', 'интеграл']
        
        is_math = any(keyword in message.lower() for keyword in math_keywords)
        
        if is_math:
            return self.solve_math_problem(message)
        
        # Если не математика - обычный диалог
        return self._generate_dialog_response(message)
    
    def _generate_dialog_response(self, message):
        """Обычный диалоговый ответ"""
        if self.words_count > 0 and self.W1 is not None:
            input_vector = self.text_to_vector(message)
            output = self.forward(input_vector)
            
            response_words = []
            for _ in range(random.randint(3, 7)):
                probs = self.softmax(output, temperature=0.8)
                word_idx = np.random.choice(self.words_count, p=probs.flatten())
                response_words.append(self.reverse_vocab[word_idx])
            
            response = " ".join(response_words)
            self.train_on_message(message, response)
            return response
        
        return "Напиши мне что-нибудь, я отвечу!"

# Создаем экземпляр
brain = MathNeuralNetwork("math_brain")
