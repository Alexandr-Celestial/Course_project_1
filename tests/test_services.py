from unittest.mock import patch

import pandas as pd
import pytest

from src.services import (
    read_excel_file,
    rec_search_request,
    search_mobile_number_excel,
    search_transactions_to_people,
)


def test_read_excel_file() -> None:
    """Тест функции чтения файла excel"""
    with pytest.raises(FileNotFoundError):
        read_excel_file("")
    with pytest.raises(Exception):
        with patch("pd.read_excel") as pd_mock:
            pd_mock.return_value = ""
            read_excel_file("")


def test_rec_search_request() -> None:
    """Тест функции получает запрос поиска от пользователя по строке"""
    with pytest.raises(ValueError):
        rec_search_request(pd.DataFrame([{}]), None)

    with patch("json.dumps", return_value=[{}]):
        assert rec_search_request(pd.DataFrame([{}]), "aabbcc") == [{}]


def test_search_mobile_number_excel() -> None:
    """Тест функции для поиска мобильных номеров в поле 'Категория'"""
    with patch("json.dumps", return_value="[{}]"):
        assert search_mobile_number_excel(pd.DataFrame([{}])) == "[{}]"


def test_search_transactions_to_people() -> None:
    """Тест функции для поиска мобильных номеров в поле 'Категория'"""
    with patch("json.dumps", return_value="[{}]"):
        assert search_transactions_to_people(pd.DataFrame([{}])) == "[{}]"
