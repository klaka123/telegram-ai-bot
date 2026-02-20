import requests
import base64

class SuperGodAI:
    def __init__(self):
        # ВСТАВЬ СЮДА КЛЮЧ ОТ OPENROUTER
        self.api_key = "sk-or-v1-..."  # получишь ниже
        self.client = None
        print("🚀 Бот запущен")
    
    def analyze_photo_math(self, photo_bytes):
        import base64
        base64_image = base64.b64encode(photo_bytes).decode('utf-8')
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "openai/gpt-4o",
            "messages": [
                {"role": "system", "content": "Ты математик. Реши примеры с фото."},
                {"role": "user", "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]}
            ]
        }
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload
        )
        
        return response.json()['choices'][0]['message']['content']
