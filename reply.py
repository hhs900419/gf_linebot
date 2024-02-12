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


# channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
line_bot_api = LineBotApi(channel_access_token)


def reply_TextMsg(reply_token, text):
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))
    return 

def reply_ImageURL(reply_token, img_url):
    img_message = ImageSendMessage(
        original_content_url=img_url,
        preview_image_url=img_url
    )
    line_bot_api.reply_message(reply_token, img_message)
    return 

def reply_ButtonsTemplate(reply_token, title, description, label_list, text_list, img_url=None):
    button_actions = []
    for lb, txt in zip(label_list, text_list):
        button_actions.append(
            MessageTemplateAction(
                label = lb,
                text = txt
            )
        )

    message = TemplateSendMessage(
        alt_text = 'Buttons template',
        template = ButtonsTemplate(
            thumbnail_image_url = img_url,
            title = title,
            text = description,
            actions = button_actions
        )
    )
    line_bot_api.reply_message(reply_token, message)
    return

def reply_ImgCarouselTemplate(reply_token):
    image_carousel_template_message = TemplateSendMessage(
        alt_text='ImageCarousel template',
        template=ImageCarouselTemplate(
            columns=[
                ImageCarouselColumn(
                    image_url='https://example.com/item1.jpg',
                    action=PostbackAction(
                        label='postback1',
                        display_text='postback text1',
                        data='action=buy&itemid=1'
                    )
                ),
                ImageCarouselColumn(
                    image_url='https://example.com/item2.jpg',
                    action=PostbackAction(
                        label='postback2',
                        display_text='postback text2',
                        data='action=buy&itemid=2'
                    )
                )
            ]
        )
    )
    line_bot_api.reply_message(reply_token, image_carousel_template_message)
    return