from abc import ABC, abstractmethod

import requests


class HHVacancy(ABC):
    """Абстрактный класс получения вакансий"""

    @abstractmethod
    def get_employer_vacancy(self) -> None:
        pass


class EmployerVacancy(HHVacancy):
    """Класс получения вакансий по id работодателя"""

    all_vacancy: list = []

    def __init__(self, employee_id: int) -> None:
        """Инициализатор класса EmployerVacancy"""
        self.url = "https://api.hh.ru/vacancies"
        self.headers = {"User-Agent": "HH-User-Agent"}
        self.params = {"employer_id": employee_id, "page": 0, "per_page": 100}

    def get_employer_vacancy(self) -> None:
        """Функция получения вакансий"""
        try:
            response = requests.get(url=self.url, headers=self.headers, params=self.params)
            vacancy = response.json()["items"]
            for item in vacancy:
                vacancy_info = (
                    item["id"],
                    item["name"],
                    item["area"]["url"],
                    item["salary"]["from"] if item["salary"] is not None else 0,
                    item["salary"]["to"] if item["salary"] is not None else 0,
                    item["employer"]["id"],
                    item["employer"]["name"],
                )
                self.all_vacancy.append(vacancy_info)
        except ConnectionError:
            print("Ошибка соединения")
