import json
from typing import List
from typing import Union

import requests

from API.weather_API.get_location_user_computer import get_location


def get_areas_info() -> List[List[str]]:
    req = requests.get('https://api.hh.ru/areas')
    data = req.content.decode()
    req.close()
    jsObj = json.loads(data)
    areas = []
    for k in jsObj:
        for i in range(len(k['areas'])):
            if len(k['areas'][i]['areas']) != 0:
                for j in range(len(k['areas'][i]['areas'])):
                    areas.append([k['id'],
                                  k['name'],
                                  k['areas'][i]['areas'][j]['id'],
                                  k['areas'][i]['areas'][j]['name']])
            else:
                areas.append([k['id'],
                              k['name'],
                              k['areas'][i]['id'],
                              k['areas'][i]['name']])
    return areas


def get_area_user() -> Union[list, None]:
    data_user = get_location()
    city, country = data_user['city'], data_user['country']
    areas = get_areas_info()
    # item[1] - страна
    # item[3] - город
    id = None
    for item in areas:
        if item[3] == city and item[1] == country:
            id = item[2]
    return [id, city]


def get_vacancies(text):
    data = get_area_user()
    response = requests.get(
        f'http://api.hh.ru/vacancies?clusters=true&enable_snippets=true'
        f'&st=searchVacancy&only_with_salary=true&text={text}&per_page=100&area={data[0]}')
    if response.status_code == 200:
        json_response = response.json()
        salaries_vacancies = []
        info_vacancy_response = dict()
        for vacancy in json_response['items']:
            if vacancy['alternate_url'] not in info_vacancy_response:
                info_vacancy_response[vacancy['alternate_url']] = vacancy['name']
            salaries_vacancies.append(vacancy['salary'])
        middle_salary = middle_salary_vacancy(salaries_vacancies)
        return f'{middle_salary} - средняя зарплата в регионе {data[1]}' + f'{info_vacancy_response}'


def middle_salary_vacancy(info_salaries):
    summa_salaries = 0
    for salary_vacancy in info_salaries:
        if salary_vacancy['from'] and salary_vacancy['to']:
            middle_cur_vacancy = (salary_vacancy['from'] + salary_vacancy['to']) // 2
        elif salary_vacancy['to']:
            middle_cur_vacancy = salary_vacancy['to']
        else:
            middle_cur_vacancy = salary_vacancy['from']
        summa_salaries += middle_cur_vacancy
    return summa_salaries // len(info_salaries)



