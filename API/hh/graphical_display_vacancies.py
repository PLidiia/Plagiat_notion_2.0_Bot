import matplotlib.pyplot as plt
import pandas as pd

from API.hh.get_vacancy import middle_salary_vacancies
from API.hh.record_vacancies_csv import record_csv


def draw_diagram(text):
    data_vacancies = record_csv(text)
    middle_value_salary = middle_salary_vacancies(data_vacancies)
    data = pd.read_csv('cur_vacancies.csv', delimiter=':', header=None,
                       names=['Ссылка', 'Вакансия', 'Зарплата', 'от', 'до'],
                       skiprows=1, nrows=5)
    plt.figure(figsize=(8, 5))
    plt.bar(data['Вакансия'], data['Зарплата'], color='skyblue', width=0.8)
    plt.axhline(y=middle_value_salary, color='r', linestyle='--', label=f'средняя зп {text}')
    plt.xlabel('Вакансии')
    plt.ylabel('Зарплата')
    plt.title('Зарплата по вакансиям')
    plt.xticks(rotation=35)
    plt.legend()
    plt.tight_layout()
    plt.savefig('salary_chart.png')
