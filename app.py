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
from linebot.models import MessageEvent, TextMessage, TextSendMessage, LocationMessage
from gemini import *
from utils import *
from reply import *
from weatherAPI import *
from love import *


channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)

if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)
    
    
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

app = Flask(__name__)
gemini = Gemini()
weatherAPI = WeatherAPI()
love = Love()

state_dict = {
    "NORMAL_STATE" : True,
    "AI_STATE" : False,
    "WEATHER_STATE" : False, 
    "LOVE_STATE": False,
}


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
    if trigger_LLM(event, text, gemini):
        state_controller(state_dict, "AI_STATE")
        return
    elif trigger_weather(event, text, state_dict, weatherAPI):
        state_controller(state_dict, "WEATHER_STATE")
        return
    elif trigger_love(event, text):
        state_controller(state_dict, "LOVE_STATE")
        return
    elif trigger_reset(event, text):
        state_reset(state_dict)
    elif text.lower() == "state":
        reply_text = get_current_state(state_dict)
    else:
        reply_text = "寶貝說: " + text
        
    # State specific task
    if get_current_state(state_dict) == "AI_STATE":
        response = gemini.get_response(event, text)
        return
    
    elif get_current_state(state_dict) == "WEATHER_STATE":
        weatherAPI.controller(event, text)
        return
    
    elif get_current_state(state_dict) == "LOVE_STATE":
        love.controller(event, text)
        return
        
    elif get_current_state(state_dict) == "NORMAL_STATE":
        pass
    else:
        print("[ERROR] Not in any state")
        
    try:
        reply_TextMsg(event.reply_token, reply_text)
    except Exception as e:
        print(e)
        
@handler.add(MessageEvent, message=LocationMessage)
def handle_location(event):
    print("LOCATION")
    print(weatherAPI.location)
    print(weatherAPI.GET_LOCATION_INFO)
    if weatherAPI.GET_LOCATION_INFO and weatherAPI.location == None:
        print(weatherAPI.location)
        latitude = event.message.latitude
        longitude = event.message.longitude
        status = weatherAPI.get_location_key_by_map(latitude, longitude)
        # send button template
        if status != 200:
            reply_text = f"[API ERROR]: {status}"
            reply_TextMsg(event.reply_token, reply_text)
        else:
            token = event.reply_token
            img_url = rand_select_img()
            title = "天氣小助手"
            description = f"妳的位置: {weatherAPI.location}"
            label_list = ["設定地點", "目前天氣", "天氣預報 (12小時)", "天氣預報 (5日)"]
            text_list = ["設定地點", "目前天氣", "天氣預報 (12小時)", "天氣預報 (5日)"]
            reply_ButtonsTemplate(token, title, description, label_list, text_list, img_url)
            weatherAPI.GET_LOCATION_INFO = False
        

if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)