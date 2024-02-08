from api.prompt import Prompt
import os
from openai import OpenAI
client = OpenAI()

client.api_key = os.getenv("OPENAI_API_KEY")

class ChatGPT:
    def __init__(self):
        self.prompt = Prompt()
        self.model = os.getenv("OPENAI_MODEL", default = "gpt-3.5-turbo-0125")
        self.temperature = float(os.getenv("OPENAI_TEMPERATURE", default = 0.5))
        self.max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", default = 500))

    def get_response(self):
        print(self.prompt.generate_prompt())
        response = client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            messages=self.prompt.generate_prompt(),
        )
        return response.choices[0].message.content

    def add_msg(self, text):
        self.prompt.add_msg(text)
        
    def trigger_GPT(self, input_text):
        if input_text[:5].lower() == "hi ai":
            return True
        return False
    
