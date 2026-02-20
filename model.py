"""
🤖 СУПЕР-БОГ МАТЕМАТИКИ - Понимает фото!
"""

import os
import json
import time
import random
import re
import math
import base64
from datetime import datetime
from typing import Dict, List, Optional, Any
import requests
from openai import OpenAI
import sympy as sp
from sympy import symbols, Eq, solve, diff, integrate
from sympy import sin, cos, tan, log, ln, exp, sqrt, pi
from sympy.parsing.sympy_parser import parse_expr
import numpy as np
from PIL import Image
import io

class SuperGodAI:
    def __init__(self):
        # ПРОВЕРКА ТОКЕНА
        print("=" * 50)
        print("🔍 ПРОВЕРКА ТОКЕНОВ:")
        self.github_token = os.environ.get('GH_TOKEN')
        
        if self.github_token:
            print(f"✅ GH_TOKEN найден! Длина: {len(self.github_token)}")
            print(f"   Первые символы: {self.github_token[:10]}...")
        else:
            print("❌ GH_TOKEN НЕ НАЙДЕН!")
            print("   Проверь Secrets в GitHub: Settings → Secrets and variables → Actions")
            print("   Там должен быть GH_TOKEN с твоим токеном")
        
        self.client = None
        if self.github_token:
            try:
                self.client = OpenAI(
                    base_url="https://models.inference.ai.azure.com",
                    api_key=self.github_token,
                    timeout=60.0
                )
                print("✅ GPT-4o Vision подключен")
            except Exception as e:
                print(f"❌ Ошибка GPT: {e}")
        else:
            print("❌ GPT-4o Vision НЕ подключен - токена нет")
        
        self.user_contexts = {}
        print("=" * 50)
        print("🤖 СУПЕР-БОГ МАТЕМАТИКИ ЗАПУЩЕН")
        print("=" * 50)
    
    def analyze_photo_math(self, photo_bytes: bytes) -> str:
        """
        АНАЛИЗИРУЕТ ФОТО И РЕШАЕТ МАТЕМАТИКУ
        """
        if not self.client:
            return """❌ **Нет подключения к GPT-4o Vision**

Возможные причины:
1. Токен GH_TOKEN не добавлен в Secrets GitHub
2. Токен неправильный или истек
3. Нет интернета у сервера

**Как исправить:**
1. Settings → Secrets and variables → Actions
2. Добавь GH_TOKEN с твоим токеном
3. Перезапусти Actions

Пока можешь писать примеры текстом, например:
• `1500+1500/2`
• `cos30`
• `x²-5x+6=0`"""
        
        try:
            base64_image = base64.b64encode(photo_bytes).decode('utf-8')
            
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": """Ты - СУПЕР-БОГ МАТЕМАТИКИ. Найди на фото все математические примеры и реши их!
Если видишь дробь 2/2 - ответь: 2/2 = 1
Если видишь 1500+1500/2 - ответь: 1500+1500/2 = 2250
Если видишь cos30 - ответь: cos30° = 0.866 (√3/2)
Решай всё пошагово и подробно!"""
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=2000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"❌ Ошибка при анализе: {str(e)}"
    
    def solve_math(self, problem: str) -> str:
        """Решает математику из текста"""
        problem_clean = problem.replace(' ', '')
        
        # Арифметика
        try:
            if re.match(r'^[\d\+\-\*\/\(\)]+$', problem_clean):
                result = eval(problem_clean)
                return f"✅ {problem} = {result}"
        except:
            pass
        
        # Дроби
        if '/' in problem and '=' in problem:
            parts = problem.split('=')
            if '?' in parts[1]:
                frac = parts[0].strip()
                try:
                    a, b = map(int, frac.split('/'))
                    if b == 0:
                        return "❌ Деление на ноль!"
                    result = a / b
                    if result.is_integer():
                        return f"✅ {frac} = {int(result)}"
                    else:
                        return f"✅ {frac} = {result}"
                except:
                    pass
        
        # Тригонометрия
        trig = re.search(r'(sin|cos|tan)(\d+)', problem.lower())
        if trig:
            func, angle = trig.group(1), int(trig.group(2))
            rad = math.radians(angle)
            if func == 'sin':
                return f"📐 sin{angle}° = {math.sin(rad):.4f}"
            if func == 'cos':
                return f"📐 cos{angle}° = {math.cos(rad):.4f}"
        
        return None
    
    def get_response(self, user_id: int, message: str) -> str:
        """Отвечает на сообщения"""
        msg = message.lower().strip()
        
        # Сначала пробуем решить математику
        math_solution = self.solve_math(message)
        if math_solution:
            return math_solution
        
        # Приветствия
        if msg in ['привет', 'здравствуй', 'хай']:
            return "Привет! Отправь фото с примером или напиши математику! 📸"
        
        # Шутки
        if 'шутка' in msg:
            return "🎭 Почему программисты путают Хэллоуин и Рождество? 31 Oct = 25 Dec!"
        
        # Факты
        if 'факт' in msg:
            return "🔍 Осьминоги имеют три сердца! 🐙"
        
        # Кто ты
        if 'кто ты' in msg:
            return """Я Супер-бог математики! 📸

📸 Отправь фото - решу примеры!
🧮 Напиши текст - тоже решу!

Примеры:
• `1500+1500/2`
• `cos30`
• `x²-5x+6=0`"""
        
        return f"❓ Я не понял. Отправь фото или напиши пример (например: 1500+1500/2)"

brain = SuperGodAI()
