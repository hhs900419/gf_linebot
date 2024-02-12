import os
import sys
import pathlib
import textwrap
import google.generativeai as genai
from reply import *

# client.api_key = os.getenv("OPENAI_API_KEY")
google_api_key = os.getenv("GOOGLE_API_KEY", None)
if google_api_key is None:
    print("Specify GOOGLE_API_KEY as environment variable.")
    sys.exit(1)
genai.configure(api_key=google_api_key)

class Gemini:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-pro')
        self.messages = []

    def get_response(self, event, usr_prompt):
        # print(self.prompt.generate_prompt())
        usr_dict = {'role':'user',
                    'parts': [usr_prompt]}
        self.messages.append(usr_dict)
        response = self.model.generate_content(self.messages, stream=True)
        response.resolve()
        reply_msg = self.format_response(response.text)
        model_dict = {'role':'model',
                        'parts': [response.text]}
        self.messages.append(model_dict)
        reply_TextMsg(event.reply_token, reply_msg)
        return
    
    def format_response(self, response):
        new_response = response.replace("*", "")
        # new_response = new_response.replace(":", ":\n")
        # new_response = new_response.replace("：", "：")
        return new_response
    
    def clear_history(self):
        self.messages = []
        return
        
        

