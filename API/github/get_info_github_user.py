import os

import requests
from dotenv.main import load_dotenv


def response_github(url):
    headers = {'Authorization': f'token {os.getenv("GITHUB_TOKEN")}'}
    response = requests.get(url, headers=headers)
    json_response = (response.json())
    return json_response


load_dotenv()
url_user = 'https://api.github.com/user'
json_response_1 = response_github(url_user)
user_id = json_response_1['id']
url_repos = json_response_1['repos_url']
json_response_2 = response_github(url_repos)
for item in json_response_2:
    id = item['owner']['id']
    if id == user_id:
        print('УРА проект делал сам автор')
    else:
        print('Ложь это не его проект')
