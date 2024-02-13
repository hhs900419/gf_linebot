import os
import sys
from linebot.models import (
    ImageCarouselColumn, MessageAction
)
from reply import *
from img_dict import *
from utils import random_gen_nums

class Love:
    def __init__(self):
        self.capsule_str = "Lovely Memories"
        self.trap_str = "妳按下了\"帥哥區\"按鈕，這些帥哥照片妳應該喜歡!"
        self.service_str = "客服專區"
        self.dcard_str = "Dcard 熱門文章"
        self.service_msg = "寶貝如果想要增加什麼功能，可以跟男友許願喔，兩個月可以許一個功能哈哈"
        self.imgCols = []
        
    def gen_imgCarousel_cols(self, col_num, img_list, both=True):
        self.imgCols = []
        idx_list = random_gen_nums(0, len(img_list)-1, col_num)
        for idx in idx_list:
            if both:
                url = img_list[idx]["url"] + ".jpg"
            else:
                url = img_list[idx] + ".jpg"
            print(url)
            imgcol_obj = ImageCarouselColumn(
                            image_url = url,
                            action = MessageAction(
                            text = "換一組" if both else "看更多帥哥"
                            )
                        )
            self.imgCols.append(imgcol_obj)
        return
        
    
    def controller(self, event, text):
        if text == self.capsule_str:
            self.gen_imgCarousel_cols(7, both_list)
            reply_ImgCarouselTemplate(event.reply_token, self.imgCols)
        elif text == self.trap_str:
            print(self.trap_str)
            self.gen_imgCarousel_cols(5, handsome_list, both=False)
            reply_ImgCarouselTemplate(event.reply_token, self.imgCols)
        elif text == self.service_str:
            reply_text = self.service_msg
            reply_TextMsg(event.reply_token, reply_text)
        elif text == self.dcard_str:
            reply_text = "這個功能我來不及做出來QQ"
            reply_TextMsg(event.reply_token, reply_text)
        elif text == "換一組":
            self.gen_imgCarousel_cols(7, both_list)
            reply_ImgCarouselTemplate(event.reply_token, self.imgCols)
        elif text == "看更多帥哥":
            self.gen_imgCarousel_cols(5, handsome_list, both=False)
            reply_ImgCarouselTemplate(event.reply_token, self.imgCols)