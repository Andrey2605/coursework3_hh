from abc import ABC, abstractmethod
from typing import Any

import psycopg2


class CreateDB(ABC):
    """Абстрактный класс создания базы данных"""

    @abstractmethod
    def create_database(self):
        """Абстрактный метод создания базы данных"""
        pass


class CreateDatabase(CreateDB):
    """Класс создания базы данных"""

    def __init__(self, params: dict[str, Any]) -> None:
        """Инициализация"""
        self.params = params

    def create_database(self) -> None:
        """Метод создания базы данных"""
        conn = psycopg2.connect(dbname="postgres", **self.params)
        conn.autocommit = True
        cursor = conn.cursor()
        sql = "CREATE DATABASE EMPLOYERS_VACANCY"
        cursor.execute(sql)
        print("База данных успешно создана")

        cursor.close()
        conn.close()
