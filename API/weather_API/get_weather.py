import datetime
import math
import os
from typing import Union

import requests
from dotenv.main import load_dotenv

from get_location_user_computer import get_location


def json_data_weather_processing(json_response) -> dict:
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


def get_weather_today(city_entered=None) -> Union[dict, str]:
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
        json_data_weather_processing(json_response)
    else:
        return f'{response.status_code}-----{response.reason}'


def get_weather_15_day(city_entered=None):
    load_dotenv()
    info_location = get_location()
    if not city_entered:
        response_for_key = requests.get(f'http://dataservice.accuweather.com/locations/v1/cities/search?'
                                        f'apikey={os.getenv("ACCUWEATHER_KEY")}'
                                        f'&q={info_location["city"]}&language=en')
        if response_for_key.status_code == 200:
            json_response = response_for_key.json()
            key_location = json_response[0]['Key']
            response = requests.get(f'http://dataservice.accuweather.com/forecasts/v1/daily/5day/{key_location}'
                                    f'?apikey={os.getenv("ACCUWEATHER_KEY")}')
            json_response_2 = response.json()
            for daily_weather in json_response_2['DailyForecasts']:
                data = daily_weather['Date']
                bad_index = data.index('T')
                data_need = data[:bad_index]
                temp_min_need = int(daily_weather['Temperature']['Minimum']['Value'])
                temp_max_need = int(daily_weather['Temperature']['Maximum']['Value'])
                print(data_need, temp_min_need - 32, temp_max_need - 32)

        else:
            return f'{response_for_key.status_code}-----{response_for_key.reason}'

