import pandas as pd
import pytest
from _pytest.capture import CaptureFixture

from config import ROOT_DIR
from src.reports import log, spending_by_category


def test_log() -> None:
    """Тест функции log"""

    @log("test_log")
    def decorator_test() -> pd.DataFrame:
        return pd.DataFrame([{"key": 1}])

    decorator_test()
    with open(ROOT_DIR + "/logs/test_log.log", "r", encoding="utf-8") as file:
        log_load = file.read()
    assert '[{"key": 1}]' in log_load


def test_log_print(capsys: CaptureFixture) -> None:
    """Тест функции log с выводом результата в консоль при помощи capsys"""

    @log()
    def decorator_test_print() -> pd.DataFrame:
        return pd.DataFrame([{"key": 1}])

    decorator_test_print()
    captured = capsys.readouterr()
    assert '[{"key": 1}]' in captured.out


@pytest.mark.parametrize(
    "category, date, expected",
    [
        (
            "Пополнения",
            "2018-02-25 20:14:08",
            '[{"Дата операции": "2018-01-25 20:14:08", "Дата платежа": "25.01.2018", "Номер карты": null,'
            ' "Статус": "OK", "Сумма операции": 9700.0, "Валюта операции": "RUB", "Сумма платежа": 9700.0, '
            '"Валюта платежа": "RUB", "Кэшбэк": null, "Категория": "Пополнения", "MCC": 6012.0, "Описание": '
            '"Перевод с карты", "Бонусы (включая кэшбэк)": 0, "Округление на инвесткопилку": 0, '
            '"Сумма операции с округлением": 9700.0}]',
        ),
        ("Супермаркеты", "", "[]"),
    ],
)
def test_spending_by_category(
    excel_data: list, category: str, date: str, expected
) -> None:
    """Тест функции spending_by_category"""
    transactions_date_frame = pd.DataFrame(excel_data)
    transactions = spending_by_category(transactions_date_frame, category, date)
    assert transactions == expected
