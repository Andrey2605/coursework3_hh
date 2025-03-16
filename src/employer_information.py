from abc import ABC, abstractmethod

import requests


class HHEmployee(ABC):
    """Абстрактный метод для вывода информации об работодателе"""

    @abstractmethod
    def get_employee_information(self) -> None:
        pass


class EmployerInformation(HHEmployee):
    """Класс получения информации работодателя"""

    all_information: list = []

    def __init__(self, employer_id: int) -> None:
        """Инициализатор класса EmployerInformation"""
        self.url = f"https://api.hh.ru/employers/{employer_id}"

    def get_employee_information(self) -> None:
        """Функция получения информации работодателя"""
        try:
            response = requests.get(url=self.url)
            information = response.json()
            information_set = (
                information["id"],
                information["name"],
                information["type"],
                information["area"]["name"],
                information["open_vacancies"],
            )
            self.all_information.append(information_set)
        except ConnectionError:
            print("Ошибка соединения")
