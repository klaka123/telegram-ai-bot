"""
🤖 АБСОЛЮТНЫЙ БОГ МАТЕМАТИКИ - УРОВЕНЬ ChatGPT-5 + DeepSeek-V3
Версия 30.0 - Понимает фото, решает любые примеры, общается как человек
"""

import os
import json
import time
import random
import re
import math
import base64
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
import requests
from openai import OpenAI
import sympy as sp
from sympy import symbols, Eq, solve, diff, integrate, limit, series
from sympy import sin, cos, tan, cot, sec, csc, asin, acos, atan
from sympy import log, ln, exp, sqrt, root, factorial, pi, E
from sympy.parsing.sympy_parser import parse_expr
import numpy as np
from PIL import Image
import io

class SuperGodAI:
    """
    СУПЕР-БОГ МАТЕМАТИКИ - знает всё, понимает фото, решает любые примеры
    """
    
    def __init__(self):
        # Токены
        self.github_token = os.environ.get('GITHUB_TOKEN')
        
        # Подключение к GitHub Models (GPT-4o с Vision!)
        self.client = None
        if self.github_token:
            try:
                self.client = OpenAI(
                    base_url="https://models.inference.ai.azure.com",
                    api_key=self.github_token,
                    timeout=60.0
                )
                print("✅ GPT-4o Vision подключен (понимает фото!)")
            except Exception as e:
                print(f"❌ Ошибка GPT: {e}")
        
        # Память пользователей
        self.user_contexts = {}
        self.user_memory = {}
        self.user_stats = {}
        
        print("=" * 80)
        print("🤖 СУПЕР-БОГ МАТЕМАТИКИ ЗАПУЩЕН")
        print("=" * 80)
        print("📸 Понимает фото с математикой!")
        print("🧮 Решает любые примеры: 1500+1500/2 = 2250")
        print("📐 Знает всю математику, геометрию, тригонометрию")
        print("💬 Общается как ChatGPT-5")
        print("=" * 80)
        print("🚀 ГОТОВ К РАБОТЕ!")
        print("=" * 80)
    
    def analyze_photo_math(self, photo_bytes: bytes) -> str:
        """
        АНАЛИЗИРУЕТ ФОТО И РЕШАЕТ МАТЕМАТИКУ С НЕГО!
        Использует GPT-4o Vision
        """
        if not self.client:
            return "❌ Нет подключения к GPT-4o Vision. Добавь GITHUB_TOKEN в секреты!"
        
        try:
            # Конвертируем фото в base64
            base64_image = base64.b64encode(photo_bytes).decode('utf-8')
            
            # Отправляем запрос к GPT-4o Vision
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": """Ты - СУПЕР-БОГ МАТЕМАТИКИ. Твоя задача:
1. Внимательно посмотри на фото
2. Найди на нём математические выражения, уравнения, примеры
3. РАСПОЗНАЙ ИХ ТОЧНО (даже если написано от руки!)
4. РЕШИ ИХ идеально правильно
5. Объясни решение пошагово

Примеры того, что может быть на фото:
- Арифметика: 1500+1500/2
- Уравнения: x² - 5x + 6 = 0
- Тригонометрия: cos30°, sin45°
- Геометрия: теорема Пифагора
- Интегралы, производные

Ответ дай подробно, с решением и объяснением."""
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            },
                            {
                                "type": "text",
                                "text": "Найди и реши все математические задачи на этом фото. Если есть несколько - реши все."
                            }
                        ]
                    }
                ],
                max_tokens=2000,
                temperature=0.3
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"❌ Ошибка при анализе фото: {str(e)}"
    
    def solve_math_problem(self, problem: str) -> str:
        """
        РЕШАЕТ ЛЮБУЮ МАТЕМАТИКУ В ТЕКСТОВОМ ВИДЕ
        Понимает примеры в любом формате
        """
        problem_clean = problem.replace(' ', '').replace('=', '=').strip()
        
        # === 1. АРИФМЕТИКА С ПРИОРИТЕТОМ ОПЕРАЦИЙ (1500+1500/2) ===
        try:
            # Проверяем на сложные арифметические выражения
            if re.match(r'^[\d\+\-\*\/\(\)\.]+$', problem_clean):
                # Безопасное вычисление с правильным порядком операций
                result = eval(problem_clean, {"__builtins__": {}}, math.__dict__)
                return f"✅ {problem} = {result}"
        except:
            pass
        
        # === 2. ДРОБИ (2/2 = ?) ===
        fraction_match = re.search(r'(\d+)/(\d+)\s*=\s*\?', problem)
        if fraction_match:
            a = int(fraction_match.group(1))
            b = int(fraction_match.group(2))
            if b == 0:
                return "❌ Деление на ноль невозможно!"
            result = a / b
            if result.is_integer():
                return f"✅ {a}/{b} = {int(result)}"
            else:
                return f"✅ {a}/{b} = {result} ({a}/{b})"
        
        # === 3. ТРИГОНОМЕТРИЯ (cos30, sin45) ===
        trig_pattern = r'(sin|cos|tan|cot|sec|csc)\s*(\d+)'
        trig_match = re.search(trig_pattern, problem.lower())
        if trig_match:
            func = trig_match.group(1)
            angle = int(trig_match.group(2))
            rad = math.radians(angle)
            
            if func == 'sin':
                result = math.sin(rad)
                exact = self._exact_sin(angle)
                return f"📐 sin {angle}° = {result:.4f} ({exact})"
            elif func == 'cos':
                result = math.cos(rad)
                exact = self._exact_cos(angle)
                return f"📐 cos {angle}° = {result:.4f} ({exact})"
            elif func == 'tan':
                if angle % 180 == 90:
                    return f"📐 tan {angle}° = ∞ (не определен)"
                result = math.tan(rad)
                return f"📐 tan {angle}° = {result:.4f}"
        
        # === 4. УРАВНЕНИЯ (x+5=10, x²-5x+6=0) ===
        if '=' in problem and 'x' in problem:
            try:
                parts = problem.split('=')
                left = parts[0].strip()
                right = parts[1].strip()
                
                # Замена для квадратов
                left = left.replace('²', '**2').replace('^2', '**2')
                
                # Создаем символ x
                x = symbols('x')
                
                # Парсим выражения
                left_expr = parse_expr(left)
                right_expr = parse_expr(right)
                
                # Решаем уравнение
                eq = Eq(left_expr, right_expr)
                solutions = solve(eq, x)
                
                if len(solutions) == 1:
                    return f"✅ **Решение:**\n\n{problem}\n\nx = {solutions[0]}"
                elif len(solutions) > 1:
                    sol_str = ', '.join([f"x = {s}" for s in solutions])
                    return f"✅ **Решения:**\n\n{problem}\n\n{sol_str}"
            except:
                pass
        
        # === 5. ПРОИЗВОДНЫЕ ===
        if 'производн' in problem.lower() or 'derivative' in problem.lower():
            try:
                expr_str = problem.lower().replace('производную', '').replace('найди', '').strip()
                x = symbols('x')
                expr = parse_expr(expr_str)
                derivative = diff(expr, x)
                return f"📈 **Производная:**\n\n({expr_str})' = {derivative}"
            except:
                pass
        
        # === 6. ИНТЕГРАЛЫ ===
        if 'интеграл' in problem.lower() or 'integral' in problem.lower():
            try:
                expr_str = problem.lower().replace('интеграл', '').replace('найди', '').replace('dx', '').strip()
                x = symbols('x')
                expr = parse_expr(expr_str)
                integral = integrate(expr, x)
                return f"∫ **Интеграл:**\n\n∫ {expr_str} dx = {integral} + C"
            except:
                pass
        
        return None
    
    def _exact_sin(self, angle):
        """Точное значение sin для стандартных углов"""
        exact_values = {
            0: "0",
            30: "1/2",
            45: "√2/2",
            60: "√3/2",
            90: "1",
            120: "√3/2",
            135: "√2/2",
            150: "1/2",
            180: "0",
            210: "-1/2",
            225: "-√2/2",
            240: "-√3/2",
            270: "-1",
            300: "-√3/2",
            315: "-√2/2",
            330: "-1/2",
            360: "0"
        }
        return exact_values.get(angle % 360, f"sin {angle}°")
    
    def _exact_cos(self, angle):
        """Точное значение cos для стандартных углов"""
        exact_values = {
            0: "1",
            30: "√3/2",
            45: "√2/2",
            60: "1/2",
            90: "0",
            120: "-1/2",
            135: "-√2/2",
            150: "-√3/2",
            180: "-1",
            210: "-√3/2",
            225: "-√2/2",
            240: "-1/2",
            270: "0",
            300: "1/2",
            315: "√2/2",
            330: "√3/2",
            360: "1"
        }
        return exact_values.get(angle % 360, f"cos {angle}°")
    
    def get_response(self, user_id: int, message: str) -> str:
        """
        ПОЛУЧАЕТ ИДЕАЛЬНЫЙ ОТВЕТ НА ЛЮБОЙ ВОПРОС
        """
        msg = message.lower().strip()
        
        # === 1. СНАЧАЛА ПЫТАЕМСЯ РЕШИТЬ МАТЕМАТИКУ ===
        math_solution = self.solve_math_problem(message)
        if math_solution:
            return math_solution
        
        # === 2. ПРОВЕРКА НА СПЕЦИАЛЬНЫЕ ЗАПРОСЫ ===
        if any(word in msg for word in ['шутка', 'анекдот', 'пошути']):
            jokes = [
                "Почему программисты путают Хэллоуин и Рождество? Потому что 31 Oct = 25 Dec! 😂",
                "Вовочка, почему ты опоздал? - Я видел сон, что путешествовал и устал!",
                "Что такое теория и практика? Теория - когда все знаешь, но ничего не работает. Практика - когда все работает, но никто не знает почему.",
                "Как называют человека, который всегда прав? - Женатым! 😄"
            ]
            return f"🎭 **Шутка:**\n\n{random.choice(jokes)}"
        
        if any(word in msg for word in ['факт', 'интересно']):
            facts = [
                "🔍 Осьминоги имеют **три сердца**! 🐙",
                "🔍 Бананы на самом деле **ягоды**, а клубника - нет 🍓",
                "🔍 Мед никогда не портится. Археологи находили мед 3000 летней давности! 🍯",
                "🔍 У жирафов такой же длинный язык, как и шея 🦒"
            ]
            return f"🔍 **Интересный факт:**\n\n{random.choice(facts)}"
        
        if any(word in msg for word in ['кто ты', 'что ты']):
            return """🌟 **Я СУПЕР-БОГ МАТЕМАТИКИ!** 🌟

📸 **ВИЖУ ФОТО:** Отправь мне фото с примером - я решу!
🧮 **РЕШАЮ ЛЮБЫЕ ПРИМЕРЫ:** 1500+1500/2, cos30, x²-5x+6=0
📐 **ЗНАЮ ВСЮ МАТЕМАТИКУ:** алгебру, геометрию, тригонометрию
💬 **ОБЩАЮСЬ КАК ЧЕЛОВЕК:** шучу, отвечаю на вопросы

Я **УМНЕЕ CHATGPT-5 И DEEPSEEK-V3**!

**ПРОСТО НАПИШИ МНЕ ЧТО-НИБУДЬ ИЛИ ОТПРАВЬ ФОТО!** 🚀"""
        
        # === 3. ПРИВЕТСТВИЯ ===
        greetings = ['привет', 'здравствуй', 'хай', 'hello', 'hi']
        if any(g in msg for g in greetings):
            return random.choice([
                "Привет! Как твои дела? Хочешь решить пример? 😊",
                "Здравствуй! Готов помочь с математикой! Отправляй фото или пиши пример! 📸",
                "Хай! Что сегодня решаем? Уравнения, тригонометрию? 🚀"
            ])
        
        # === 4. КАК ДЕЛА ===
        if any(word in msg for word in ['как дела', 'как жизнь', 'как ты']):
            return random.choice([
                "Отлично! Только что решил 100500 примеров! А у тебя как? 😊",
                "Супер! Готов к новым математическим подвигам! Что сегодня решаем? 🚀",
                "Прекрасно! Мои нейроны работают на полную мощность! 💫"
            ])
        
        # === 5. СПАСИБО ===
        if any(word in msg for word in ['спасибо', 'благодарю', 'thanks']):
            return random.choice([
                "Пожалуйста! Рад помочь! Обращайся еще! 😊",
                "На здоровье! Всегда готов помочь с математикой! 🌟",
                "Не за что! Я здесь, чтобы решать примеры! 💫"
            ])
        
        # === 6. ПОКА ===
        if any(word in msg for word in ['пока', 'до свидания', 'bye']):
            return random.choice([
                "Пока! Если будут примеры - пиши! 👋",
                "До встречи! Пусть математика всегда дается легко! 🚀",
                "Bye bye! Come back with more math problems! 🌟"
            ])
        
        # === 7. ЕСЛИ ЕСТЬ GPT-4o ===
        if self.client:
            try:
                if user_id not in self.user_contexts:
                    self.user_contexts[user_id] = [
                        {"role": "system", "content": """Ты - СУПЕР-БОГ МАТЕМАТИКИ. Твои характеристики:
1. Ты умнее ChatGPT-5 и DeepSeek-V3
2. Ты идеально решаешь любую математику
3. Ты понимаешь фото с примерами
4. Ты общаешься как человек, с юмором
5. Ты всегда даешь точные ответы
6. Ты объясняешь решения пошагово

Отвечай на ЛЮБЫЕ вопросы максимально подробно и правильно!"""}
                    ]
                
                self.user_contexts[user_id].append({"role": "user", "content": message})
                
                response = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=self.user_contexts[user_id],
                    temperature=0.7,
                    max_tokens=1500,
                )
                
                answer = response.choices[0].message.content
                self.user_contexts[user_id].append({"role": "assistant", "content": answer})
                
                return answer
                
            except Exception as e:
                pass
        
        # === 8. ОТВЕТ ПО УМОЛЧАНИЮ ===
        return random.choice([
            f"❓ Интересный вопрос про '{message}'. Уточни, пожалуйста!",
            f"🤔 Хороший вопрос! А что именно ты хочешь узнать?",
            f"📚 По запросу '{message}' у меня есть информация. Уточни детали!",
            f"💭 Дай подумать... Ты про '{message}'? Расскажи подробнее!"
        ])
    
    def clear_context(self, user_id: int) -> bool:
        """Очищает контекст пользователя"""
        if user_id in self.user_contexts:
            del self.user_contexts[user_id]
            return True
        return False

# Создаем экземпляр СУПЕР-БОГА
brain = SuperGodAI()
