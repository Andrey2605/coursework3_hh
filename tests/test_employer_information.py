from unittest.mock import MagicMock, patch

import pytest

from src.employer_information import EmployerInformation


@pytest.fixture
def get_employer():
    """Создание тестового класса"""
    return EmployerInformation(123456)


def test_employer_information_init(get_employer):
    """Тест инициализации"""
    assert get_employer.url == "https://api.hh.ru/employers/123456"


@patch("requests.get")
def test_get_employee_information(mock_get, get_employer):
    """Тест получения данных по api"""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "id": "123456",
        "name": "Autodata",
        "type": "company",
        "area": {
            "name": "Алматы",
        },
        "open_vacancies": 1,
    }
    mock_get.return_value = mock_response
    get_employer.get_employee_information()
    assert get_employer.all_information == [("123456", "Autodata", "company", "Алматы", 1)]
