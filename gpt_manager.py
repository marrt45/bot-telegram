from openai import OpenAI
from config import OPENAI_API_KEY
from collections import deque
import logging

class ConversationManager:  # Cambiamos el nombre de SalesAssistant a ConversationManager
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.history = deque(maxlen=5)
        self.current_order = []
        logging.basicConfig(level=logging.INFO)

    def add_message(self, role, content):
        self.history.append({"role": role, "content": content})
    
    def get_response(self, user_message, products_data):
        try:
            self.add_message("user", user_message)
            
            # Crear prompt contextualizado
            products_text = "\n".join([f"{p[1]} (${p[2]} | Stock: {p[3]})" for p in products_data])
            
            system_prompt = f"""
            Eres un asistente de ventas profesional. Reglas:
            1. Estilo: Formal pero amable (use 'usted')
            2. Productos disponibles:
            {products_text}
            3. Responda:
               - Confirmando disponibilidad primero
               - Pidiendo cantidades específicas
               - Ofreciendo alternativas si no hay stock
               - Mostrando el total antes de confirmar
            """
            
            messages = [
                {"role": "system", "content": system_prompt},
                *list(self.history)
            ]
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.5
            )
            
            bot_reply = response.choices[0].message.content
            self.add_message("assistant", bot_reply)
            return bot_reply
            
        except Exception as e:
            logging.error(f"Error en GPT: {e}")
            return "Disculpe, estoy teniendo dificultades. ¿Podría repetir?"