import requests
import os
import sys
import datetime
from datetime import datetime
from reply import *
from utils import *

API_KEY = "68IVLcGtC0DdWKbaaUQiT69lkI4YJHiF"


class WeatherAPI:
    def __init__(self):
        # self.api_key = os.getenv("ACCUWEATHER_API_KEY_2", None)
        self.api_key = os.getenv("ACCUWEATHER_API_KEY", None)
        self.location_key = None
        # self.location_key = 2516935
        self.location = None
        self.country_code = "TW"
        self.language = "zh-tw"
        self.GET_LOCATION_INFO = False
        self.weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        
        if self.api_key is None:
            print("Specify ACCUWEATHER_API_KEY as environment variable.")
            sys.exit(1)
            
    def get_location_key_by_map(self, latitude, longitude):
        api_base_url = "http://dataservice.accuweather.com/locations/v1/cities/geoposition/search"
        api_endpoint = f"?apikey={self.api_key}"
        api_endpoint += f"&q={latitude},{longitude}"
        api_endpoint += f"&language={self.language}"
        api_request = api_base_url + api_endpoint
        print(api_request)
        response = requests.get(api_request)
        status_code = response.status_code
        if status_code != 200:
            error_message = response.json().get("message")
            print(f"[API ERROR {response.status_code}]: {error_message}")
            return status_code
        response = response.json()
        print(response)
        print(response["Key"])
        self.location_key = response["Key"]
        city = response["AdministrativeArea"]["LocalizedName"]
        postal = response["SupplementalAdminAreas"][0]["LocalizedName"]
        area = response["LocalizedName"]
        self.location = f"{city} {postal} {area}"
        return 200
    
    def get_location_key_by_text(self, text):
        api_base_url = f"http://dataservice.accuweather.com/locations/v1/{self.country_code}/search"
        api_endpoint = f"?apikey={self.api_key}"
        api_endpoint += f"&q={text}"
        api_endpoint += f"&language={self.language}"
        api_request = api_base_url + api_endpoint
        print(api_request)
        
        response = requests.get(api_request)
        status_code = response.status_code
        if status_code != 200:
            error_message = response.json().get("message")
            print(f"[API ERROR {response.status_code}]: {error_message}")
            return status_code, -1
        response = response.json()
        print(len(response))
        print(response)
        if len(response) > 0:
            print(response[0])
            self.location_key = response[0]["Key"]
            self.location = response[0]["LocalizedName"]
            return status_code, 1
        else:
            return status_code, -1
            
    
    def current_weather(self, details=False):
        api_base_url = f"http://dataservice.accuweather.com/currentconditions/v1/{self.location_key}"
        api_endpoint = f"?apikey={self.api_key}"
        api_endpoint += f"&language={self.language}"
        api_endpoint += f"&details={details}"
        api_request = api_base_url + api_endpoint
        print(api_request)
        
        response = requests.get(api_request).json()
        # print(response)
        
        data = response[0]
        weather_text = data["WeatherText"]
        temperature = data["Temperature"]["Metric"]["Value"]
        real_feel_temperature = data["RealFeelTemperature"]["Metric"]["Value"]
        real_feel_phrase = data["RealFeelTemperature"]["Metric"]["Phrase"]
        uv_index = data["UVIndex"]
        uv_text = data["UVIndexText"]
        mobile_link = data["MobileLink"]
        
        current_weather = f"{real_feel_phrase}~~\n\n"
        current_weather += f"目前天氣：{weather_text}\n"
        current_weather += f"氣溫：{temperature} °C\n"
        current_weather += f"體感溫度：{real_feel_temperature} °C\n"
        current_weather += f"紫外線指數：{uv_index} ({uv_text})\n\n"
        current_weather += f"更多資訊：\n{mobile_link}"
        # print(current_weather)
        
        return current_weather
        
    def forecast_5days(self, details=False):
        api_base_url = f"http://dataservice.accuweather.com/forecasts/v1/daily/5day/{self.location_key}"
        api_endpoint = f"?apikey={self.api_key}"
        api_endpoint += f"&language={self.language}"
        api_endpoint += f"&details={details}"
        api_request = api_base_url + api_endpoint
        print(api_request)
        
        response = requests.get(api_request).json()
        daily_data = response["DailyForecasts"]
        daily_forecast_msg = ""
        for data in daily_data:
            date = data["Date"].split("T")[0]
            # date = date.replace("-", "/")
            date_object = datetime.strptime(str, '%Y-%m-%d')
            idx = date_object.weekday()
            weekday = self.weekdays[idx]
            min_temp = fahrenheit_to_celsius(data["Temperature"]["Minimum"]["Value"])
            max_temp = fahrenheit_to_celsius(data["Temperature"]["Maximum"]["Value"])
            perception_prob = data["Day"]["PrecipitationProbability"]
            day_phrase = data["Day"]["IconPhrase"]
            night_phrase = data["Night"]["IconPhrase"]
            
            msg = ""
            msg += f"{date}\t{weekday}\n"
            msg += f"最高溫：{max_temp} °C\n"
            msg += f"最低溫：{min_temp} °C\n"
            msg += f"降雨機率：{perception_prob} %\n"
            msg += f"白天：{day_phrase}\n"
            msg += f"晚上：{night_phrase}\n\n"
            
            daily_forecast_msg += msg
        ref_link = response["Headline"]["MobileLink"]
        daily_forecast_msg += f"詳細資訊: {ref_link}"
        return daily_forecast_msg
    
    def forecast_12hours(self, details=False):
        api_base_url = f"http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/{self.location_key}"
        api_endpoint = f"?apikey={self.api_key}"
        api_endpoint += f"&language={self.language}"
        api_endpoint += f"&details={details}"
        api_request = api_base_url + api_endpoint
        print(api_request)
        
        response = requests.get(api_request).json()
        hourly_forecast_msg = ""
        for i in range(len(response)):
            hour_data = response[i]
            datetime = hour_data["DateTime"].split("T")[1].split("+")[0][:-3]
            hour_phrase = hour_data["IconPhrase"]
            temperature = fahrenheit_to_celsius(hour_data["Temperature"]["Value"])
            perception_prob = hour_data["PrecipitationProbability"]
            
            msg = ""
            msg += f"{datetime}    {hour_phrase}\n"
            msg += f"氣溫：{temperature} °C\n"
            msg += f"降雨機率：{perception_prob} %\n\n"
            hourly_forecast_msg += msg
        ref_link = response[0]["MobileLink"]
        hourly_forecast_msg += f"詳細資訊: {ref_link}"
        return hourly_forecast_msg
    
    def controller(self, event, text):
        if self.GET_LOCATION_INFO:
            status, return_val = self.get_location_key_by_text(text)
            if status != 200:
                print(self.api_key)
                reply_text = f"[API ERROR]: {status}"
                reply_TextMsg(event.reply_token, reply_text)
            elif return_val > 0:
                token = event.reply_token
                img_url = rand_select_img()
                title = "天氣小助手"
                description = f"妳的位置: {self.location}"
                # description += f"location key: {self.location_key}"
                label_list = ["設定地點", "目前天氣", "天氣預報 (12小時)", "天氣預報 (5日)"]
                text_list = ["設定地點", "目前天氣", "天氣預報 (12小時)", "天氣預報 (5日)"]
                reply_ButtonsTemplate(token, title, description, label_list, text_list, img_url)
                self.GET_LOCATION_INFO = False
            else:
                reply_text = f"錯誤! 請重新設定\n"
                reply_text += "1. 分享妳的位置資訊\n"
                reply_text += "2. 直接輸入縣市"
                reply_TextMsg(event.reply_token, reply_text)
        elif text == "設定地點":
            self.location_key = None
            self.location = None
            reply_text = "1. 分享妳的位置資訊\n"
            reply_text += "2. 直接輸入縣市"
            reply_TextMsg(event.reply_token, reply_text)
            self.GET_LOCATION_INFO = True
        elif self.location_key == None and not self.GET_LOCATION_INFO:
            reply_text = "我還不知道妳在哪裡餒~~\n妳可以點選[設定地點]讓我知道!"
            reply_TextMsg(event.reply_token, reply_text)
        elif text == "目前天氣":
            current_weather = self.current_weather(details=True)
            reply_TextMsg(event.reply_token, current_weather)
        elif text == "天氣預報 (12小時)":
            twelve_hours_forcast = self.forecast_12hours(details=True)
            reply_TextMsg(event.reply_token, twelve_hours_forcast)
        elif text == "天氣預報 (5日)":
            five_days_forcast = self.forecast_5days(details=True)
            reply_TextMsg(event.reply_token, five_days_forcast)
        else:
            pass
        return
    
if __name__ == "__main__":
    weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    str = "2024/2/28"
    date_object = datetime.strptime(str, '%Y/%m/%d')
    idx = date_object.weekday()
    print(weekdays[idx])
