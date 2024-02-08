import os
import sys
from openai import OpenAI
import openai
import pathlib
import textwrap
import google.generativeai as genai

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from api.chatgpt import *
from utils import *




# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
google_api_key = os.getenv("GOOGLE_API_KEY", None)
# openai_api_key = os.getenv("OPENAI_API_KEY", None)

if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)
if google_api_key is None:
    print("Specify GOOGLE_API_KEY as environment variable.")
    sys.exit(1)



genai.configure(api_key=google_api_key)
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)
# openai.api_key = chatgpt_api_key

for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)
print("######################################")

app = Flask(__name__)
chatgpt = ChatGPT()
model = genai.GenerativeModel('gemini-pro')


# Webhook URL for receiving messages
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# Handler to process incoming messages
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    if chatgpt.trigger_GPT(text):
        response = model.generate_content(f"{text[6:]}", stream=True)
        response.resolve()
        # print(response.text)
        # print(format_response("" + response.text))
        reply_text = format_response(response.text)
    else:
        reply_text = "You said: " + text
        
    try:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text)
        )
    except Exception as e:
        print(e)

if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)