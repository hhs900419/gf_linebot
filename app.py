import os
import sys
from openai import OpenAI
import openai
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from api.chatgpt import *




# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
openai_api_key = os.getenv("OPENAI_API_KEY", None)

if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)
# openai.api_key = chatgpt_api_key


app = Flask(__name__)
chatgpt = ChatGPT()
# client = OpenAI()
# client.api_key = os.getenv("OPENAI_API_KEY")
# openai.api_key = os.getenv("OPENAI_API_KEY")
# if client.api_key is None:
#     print("Specify OPENAI_API_KEY as environment variable.")
#     sys.exit(1)

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
    print(event)
    text = event.message.text
    print(text)
    if chatgpt.trigger_GPT(text):
        print("GPT")
        reply_msg = chatgpt.get_response().replace("AI:", "", 1)
        print("GPT")
        chatgpt.add_msg(f"AI:{reply_msg}\n")
        print("GPT")
        print(reply_msg)
        # print(response.choices[0].message)
        # reply_msg = response.choices[0].message.content.replace('\n','')
    else:
        reply_text = "You said: " + text
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)