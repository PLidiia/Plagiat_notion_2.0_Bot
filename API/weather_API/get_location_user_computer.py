import http.client
import re

import requests



def get_ip() -> str:
    conn = http.client.HTTPConnection("ifconfig.me")
    conn.request("GET", "/ip")
    ip_user_str = str(conn.getresponse().read())
    ip_address_str_cleaned = re.sub(r"b'|'", "", ip_user_str)
    return ip_address_str_cleaned


def get_location() -> dict:
    ip_user = get_ip()
    response = requests.get(f'http://ip-api.com/json/{ip_user}?lang=ru')
    if response.status_code == 200:
        json_response = response.json()
        info_user = {'lat': json_response['lat'],
                     'lon': json_response['lon'],
                     'country': json_response['country'],
                     'region': json_response['regionName'],
                     'city': json_response['city'],
                     'country_code': json_response['countryCode']}
        return info_user
