import csv
from get_vacancy import get_vacancies


def record_csv(text):
    with open('cur_vacancies.csv', 'w', encoding='utf-8', newline='') as csvfile:
        cur_vacancies = get_vacancies(text)
        fieldnames = ['ссылка для поиска в браузере', 'имя вакансии', 'зарплата', 'from', 'to']
        writer = csv.DictWriter(csvfile, delimiter=':', fieldnames=fieldnames)
        writer.writeheader()
        for vacancy in cur_vacancies:
            writer.writerow(vacancy)
        return cur_vacancies
