from abc import ABC, abstractmethod
from typing import Any

import psycopg2


class FillTable(ABC):
    """Абстрактный класс создания и заполнения таблиц"""

    @abstractmethod
    def fill_table_employers(self) -> None:
        """Абстрактный метод создания и заполнения таблицы информации о работодателях"""
        pass

    @abstractmethod
    def fill_table_vacancy(self) -> None:
        """Абстрактный метод создания и заполнения таблицы вакансий работодателя"""
        pass

    @abstractmethod
    def foreign_key(self) -> None:
        """Абстрактный метод связи таблицы вакансий с таблицей организаций через FK"""
        pass


class FillTableEV(FillTable):
    """Класс создания и заполнения таблиц"""

    def __init__(self, information_employer: list, vacation_employer: list, params: dict[str, Any]) -> None:
        """Инициализация"""
        self.information_employer = information_employer
        self.vacation_employer = vacation_employer
        self.params = params

    def fill_table_vacancy(self) -> None:
        """Метод создания и заполнения таблицы вакансий работодателя"""
        conn = psycopg2.connect(dbname="employers_vacancy", **self.params)

        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS vacancy")
        conn.commit()
        cursor.execute(
            "CREATE TABLE vacancy(vacancy_id CHAR(9) PRIMARY KEY NOT NULL, vacancy_name VARCHAR(100)"
            "NOT NULL,url VARCHAR(100), salary_from INT, salary_to INT, employee_id "
            "SERIAL NOT NULL, company_name VARCHAR(100));"
        )
        conn.commit()
        for row in self.vacation_employer:
            query = (
                "INSERT INTO vacancy (vacancy_id, vacancy_name, url, salary_from, salary_to, employee_id, "
                "company_name) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            )
            cursor.execute(query, row)

        conn.commit()
        cursor.close()
        conn.close()

    def fill_table_employers(self) -> None:
        """Метод создания и заполнения таблицы информации о работодателях"""
        conn = psycopg2.connect(dbname="employers_vacancy", **self.params)

        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS employers")
        conn.commit()
        cursor.execute(
            "CREATE TABLE employers(employee_id SERIAL PRIMARY KEY NOT NULL, company_name VARCHAR(100)"
            "NOT NULL, type VARCHAR(100) NOT NULL,area VARCHAR(100), open_vacancies INT NOT NULL);"
        )
        conn.commit()
        for row in self.information_employer:
            query = (
                "INSERT INTO employers (employee_id, company_name, type, area, open_vacancies) VALUES (%s, %s, %s, "
                "%s, %s)"
            )
            cursor.execute(query, row)

        conn.commit()
        cursor.close()
        conn.close()

    def foreign_key(self):
        """Метод связи таблицы вакансий с таблицей организаций через FK"""
        conn = psycopg2.connect(dbname="employers_vacancy", **self.params)

        cursor = conn.cursor()
        cursor.execute(
            "ALTER TABLE vacancy ADD CONSTRAINT fk_vacancy_employers FOREIGN KEY(employee_id)"
            " REFERENCES employers(employee_id);"
        )
        conn.commit()
        cursor.close()
        conn.close()
