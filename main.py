import json
import os.path

from config import DATA_DIR, config
from src.create_database import CreateDatabase
from src.dbmanager import DBManager
from src.employer_information import EmployerInformation
from src.employer_vacancy import EmployerVacancy
from src.fill_table import FillTableEV


def main():
    """Главная функция"""

    # Получение id работодателей
    path = os.path.join(DATA_DIR, "employers_id.json")
    with open(path, encoding="UTF8") as file:
        content = file.read()
        employers_id = json.loads(content)

    # получение информации о работодателях
    for id_ in employers_id:
        employers_information = EmployerInformation(id_)
        employers_information.get_employee_information()

    # Получение вакансий работодателя
    for id_ in employers_id:
        all_vacancy = EmployerVacancy(id_)
        all_vacancy.get_employer_vacancy()

    # Создание базы данных
    params = config()
    try:
        CreateDatabase(params).create_database()
    except Exception:
        pass
    finally:

        # Создание таблиц с данными
        create_table = FillTableEV(EmployerInformation.all_information, EmployerVacancy.all_vacancy, params)
        create_table.fill_table_vacancy()
        create_table.fill_table_employers()
        create_table.foreign_key()

        db_manager = DBManager(params)

        # Взаимодействие с пользователем
        user_input = input(
            "Для получения списка всех компаний и количество вакансий у каждой компании нажмите 1.\nДля "
            "получения списка всех вакансий с указанием названия компании, названия вакансии и зарплаты "
            "и ссылки на вакансию нажмите 2.\nДля получения средней зарплаты по "
            "вакансиям нажмите 3.\nДля получения списка всех вакансий, у которых зарплата выше средней "
            "по всем вакансиям нажмите 4.\nДля получения списка всех вакансий, в названии которых "
            "содержатся переданные в метод слова нажмите 5.\nДля выхода нажмите 0\n"
        )
        if user_input == "1":
            db_manager.get_companies_and_vacancies_count()
        elif user_input == "2":
            db_manager.get_all_vacancies()
        elif user_input == "3":
            db_manager.get_avg_salary()
        elif user_input == "4":
            db_manager.get_vacancies_with_higher_salary()
        elif user_input == "5":
            user_word = input("Введите слово по которому искать вакансию\n")
            db_manager.get_vacancies_with_keyword(user_word.title())
        elif user_input == "0":
            print("Завершение работы")


if __name__ == "__main__":
    main()
