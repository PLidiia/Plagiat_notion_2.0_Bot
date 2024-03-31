import datetime
import math
import os
from typing import Union

import requests
from dotenv.main import load_dotenv

from get_location_user_computer import get_location


def get_weather_due_to_ip(city_entered=None) -> Union[dict, str]:
    load_dotenv()
    if not city_entered:
        info_location = get_location()
        response = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={info_location['city']}"
            f"&lang={info_location['country_code'].lower()}"
            f"&units=metric&appid={os.getenv('OPEN_WEATHER_TOKEN')}"
        )
    else:
        response = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city_entered}"
            f"&lang=ru"
            f"&units=metric&appid={os.getenv('OPEN_WEATHER_TOKEN')}"
        )
    if response.status_code == 200:
        json_response = response.json()
        description = json_response['weather'][0]['description']
        pressure_international_sys = json_response['main']['pressure']
        pressure_mercury_sys = math.ceil(int(pressure_international_sys) / 1.333)
        speed_wind = json_response['wind']['speed']
        temp = json_response['main']['temp']
        sunrise_time = datetime.datetime.fromtimestamp(json_response['sys']['sunrise'])
        sunset_time = datetime.datetime.fromtimestamp(json_response['sys']['sunset'])
        length_of_the_day = sunset_time - sunrise_time
        data_weather = {
            'Погода': description,
            'Давление': f'{pressure_mercury_sys} мм.рт.ст',
            'Скорость ветра': f'{speed_wind} м/c',
            'Температура': f'{temp}C',
            'Время восхода': sunrise_time,
            'Время заката': sunset_time,
            'Продолжительность дня': length_of_the_day
        }
        return data_weather
    else:
        return f'{response.status_code}-----{response.reason}'
