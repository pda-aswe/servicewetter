import requests
from datetime import datetime
import time
import os
import json

class OpenWeatherMapAPI:
    BASE_URL = "https://api.openweathermap.org/data/2.5/"

    def __init__(self):
        self.api_key = self.__loadAPIKey()
    
    def __loadAPIKey(self):
        if os.path.exists('key.txt'):
            with open('key.txt') as f:
                return f.readline().strip('\n')
        else:
            print("api key file missing")
            #quit()

    # def get_current_weather_by_city(self, city_name):
    #     url = f"{self.BASE_URL}weather?q={city_name}&appid={self.api_key}&units=metric"
    #     response = requests.get(url)
    #     if response.status_code == 200:
    #         data = response.json()
    #         weather = {
    #             "location": data["name"],
    #             "country": data["sys"]["country"],
    #             "temperature": data["main"]["temp"],
    #             "humidity": data["main"]["humidity"],
    #             "description": data["weather"][0]["description"]
    #         }
    #         return weather
    #     else:
    #         return None

    # def get_weather_by_city_and_date(self, city_name, date_time):
    #     unix_timestamp = int(time.mktime(datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S").timetuple()))
    #     url = f"{self.BASE_URL}forecast?q={city_name}&appid={self.api_key}&units=metric"
    #     response = requests.get(url)
    #     if response.status_code == 200:
    #         data = response.json()
    #         weather_list = data["list"]
    #         closest_weather = None
    #         closest_diff = float('inf')
    #         for weather in weather_list:
    #             diff = abs(weather["dt"] - unix_timestamp)
    #             if diff < closest_diff:
    #                 closest_weather = weather
    #                 closest_diff = diff
    #         if closest_weather is not None:
    #             weather_data = {
    #                 "location": data["city"]["name"],
    #                 "country": data["city"]["country"],
    #                 "temperature": closest_weather["main"]["temp"],
    #                 "humidity": closest_weather["main"]["humidity"],
    #                 "description": closest_weather["weather"][0]["description"]
    #             }
    #             return weather_data
    #         else:
    #             return None
    #     else:
    #         return None
    
    def get_current_weather_with_gps(self, latitude, longitude):
        url = f"{self.BASE_URL}weather?lat={latitude}&lon={longitude}&appid={self.api_key}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather = {
                "location": data["name"],
                "country": data["sys"]["country"],
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "description": data["weather"][0]["description"]
            }
            print(weather)
            return json.dumps(weather)
        else:
            return None
    
    def get_weather_by_date_with_gps(self, latitude, longitude, date_time):
        unix_timestamp = int(time.mktime(datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S").timetuple()))
        url = f"{self.BASE_URL}forecast?lat={latitude}&lon={longitude}&appid={self.api_key}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather_list = data["list"]
            closest_weather = None
            closest_diff = float('inf')
            for weather in weather_list:
                diff = abs(weather["dt"] - unix_timestamp)
                if diff < closest_diff:
                    closest_weather = weather
                    closest_diff = diff
            if closest_weather is not None:
                weather_data = {
                    "location": data["city"]["name"],
                    "country": data["city"]["country"],
                    "temperature": closest_weather["main"]["temp"],
                    "humidity": closest_weather["main"]["humidity"],
                    "description": closest_weather["weather"][0]["description"]
                }
                print(weather_data)
                return str(weather_data)
            else:
                return None
        else:
            return None