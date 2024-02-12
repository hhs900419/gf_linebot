import pathlib
import textwrap
import os

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, 
    TemplateSendMessage, ButtonsTemplate, ConfirmTemplate,
    CarouselTemplate, CarouselColumn,
    ImageCarouselTemplate, ImageCarouselColumn,
    MessageTemplateAction, PostbackAction, URIAction, MessageAction
)
from reply import *
from gemini import Gemini


# channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
line_bot_api = LineBotApi(channel_access_token)

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))



def trigger_LLM(event, input_text, gemini):
    if input_text.lower() == "ai":
        gemini.clear_history()
        reply_text = "Google Gemini AI模型已啟動，妳可以問AI任何問題，輸入\"結束\"來退出AI助手模式~~"
        reply_TextMsg(event.reply_token, reply_text)
        return True
    return False

def trigger_weather(event, text, state_dict, weatherAPI):
    if ("天氣" == text or "weather" == text.lower()) and get_current_state(state_dict) != "WEATHER_STATE":
        reply_text = "i am weather assistant. please share your location or tell me your location."
        # reply_TextMsg(event.reply_token, reply_text)
        # Send button template
        token = event.reply_token
        img_url = None
        title = "天氣小助手"
        if weatherAPI.location_key:
            description = f"妳的位置: {weatherAPI.location_key}"
        else:    
            description = "要跟我說妳的地點我才能找到天氣資訊喔!\n"
        # description = "1. 分享妳的位置資訊\n"
        # description = "2. 直接輸入縣市\n"
        label_list = ["設定地點", 
                      "目前天氣", 
                      "天氣預報 (12小時)",
                      "天氣預報 (5日)",
                      ]
        
        text_list = ["設定地點", 
                      "目前天氣", 
                      "天氣預報 (12小時)",
                      "天氣預報 (5日)",
                      ]
        reply_ButtonsTemplate(token, title, description, label_list, text_list)
        return True
    return False

def trigger_reset(event, text):
    if "結束" in text or "reset" in text.lower():
        reply_text = "System reset."
        reply_TextMsg(event.reply_token, reply_text)
        return True
    return False
    
def state_controller(state_dict, new_state):
    for k in state_dict.keys():
        if k == new_state:
            state_dict[k] = True
        else:
            state_dict[k] = False
    print(state_dict)
    return state_dict

def get_current_state(state_dict):
    for k in state_dict.keys():
        if state_dict[k] == True:
            return k
        
def state_reset(state_dict):
    for k in state_dict.keys():
        if k == "NORMAL_STATE":
            state_dict[k] = True
        else:
            state_dict[k] = False
    print(state_dict)
    return state_dict

def fahrenheit_to_celsius(fahrenheit):
  celsius = (fahrenheit - 32) * 5 / 9
  return format(celsius, ".1f")
    