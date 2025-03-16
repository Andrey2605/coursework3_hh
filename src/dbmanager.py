from abc import ABC, abstractmethod
from typing import Any

import psycopg2


class Manager(ABC):
    """Абстрактный класс подключения к базе данных"""

    @abstractmethod
    def get_companies_and_vacancies_count(self) -> None:
        """Абстрактный метод получения списка всех компаний и количество вакансий у каждой компании."""
        pass

    @abstractmethod
    def get_all_vacancies(self) -> None:
        """Абстрактный метод получения списка всех вакансий с указанием названия компании, названия вакансии, зарплаты
        и ссылки на вакансию."""
        pass

    @abstractmethod
    def get_avg_salary(self) -> None:
        """Абстрактный метод получения средней зарплаты по вакансиям."""
        pass

    @abstractmethod
    def get_vacancies_with_higher_salary(self) -> None:
        """Абстрактный метод получения списка всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        pass

    @abstractmethod
    def get_vacancies_with_keyword(self) -> None:
        """Абстрактный метод получает список всех вакансий, в названии которых содержатся переданные в метод слова."""
        pass


class DBManager(Manager):
    """Класс подключения к базе данных"""

    def __init__(self, params: dict[str, Any]) -> None:
        """Инициализация"""
        self.params = params

    def get_companies_and_vacancies_count(self) -> None:
        """Метод получения списка всех компаний и количество вакансий у каждой компании."""
        conn = psycopg2.connect(dbname="employers_vacancy", **self.params)
        cursor = conn.cursor()
        cursor.execute("SELECT company_name, open_vacancies FROM employers")
        rows = cursor.fetchall()
        for row in rows:
            print(" ".join([str(x) for x in list(row)]))
        cursor.close()
        conn.close()

    def get_all_vacancies(self) -> None:
        """Метод получения списка всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на
        вакансию."""
        conn = psycopg2.connect(dbname="employers_vacancy", **self.params)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vacancy INNER JOIN employers ON vacancy.employee_id = employers.employee_id")
        rows = cursor.fetchall()
        for row in rows:
            print(" ".join([str(x) for x in list(row)]))
        cursor.close()
        conn.close()

    def get_avg_salary(self) -> None:
        """Метод получения средней зарплаты по вакансиям."""
        conn = psycopg2.connect(dbname="employers_vacancy", **self.params)
        cursor = conn.cursor()
        cursor.execute("SELECT (AVG(salary_from)) FROM vacancy")
        rows = cursor.fetchall()
        print(round(list(rows[0])[0], 2))
        cursor.close()
        conn.close()

    def get_vacancies_with_higher_salary(self) -> None:
        """Метод получения списка всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        conn = psycopg2.connect(dbname="employers_vacancy", **self.params)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vacancy WHERE salary_from > (SELECT AVG(salary_from) FROM vacancy)")
        rows = cursor.fetchall()
        for row in rows:
            print(" ".join([str(x) for x in list(row)]))
        cursor.close()
        conn.close()

    def get_vacancies_with_keyword(self, user_word="") -> None:
        """Метод получает список всех вакансий, в названии которых содержатся переданные в метод слова."""
        conn = psycopg2.connect(dbname="employers_vacancy", **self.params)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM vacancy WHERE vacancy_name LIKE '%{user_word[1:]}%'")
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append(row)

        if len(result) == 0:
            print("Ваш запрос не дал результата, попробуйте ввести: 'врач' или 'оператор'.")
        else:
            for item in result:
                print(" ".join([str(x) for x in list(row)]))
        cursor.close()
        conn.close()
