import requests


def get_location(address) -> str:
    geocoder_request_address = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={address}&format=json"
    response = requests.get(geocoder_request_address)
    if response:
        json_response = response.json()
        location = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]['Point']['pos']
        return location


def get_image_location(location):
    clear_location = f"{location.split(' ')[0]},{location.split(' ')[1]}"
    map_request = f"https://static-maps.yandex.ru/1.x/?ll={clear_location}&pt={clear_location}&spn=0.005,0.005&l=map"
    response_map = requests.get(map_request)
    map_file_1 = "map.png"
    with open(map_file_1, "wb") as file:
        file.write(response_map.content)
