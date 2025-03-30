import json
import logging
import re

import pandas as pd

from config import ROOT_DIR

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(
    ROOT_DIR + "/logs/services.log", mode="w", encoding="utf-8"
)
file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def read_excel_file(file_path: str) -> pd.DataFrame:
    """Функция для чтения excel файла"""
    try:
        df = pd.read_excel(file_path)
        logger.info(f"Файл в директории {file_path} найден и обработан")
        return df
    except FileNotFoundError as e:
        logger.error("Файл не найден")
        raise e
    except Exception as e:
        logger.error(f"Произошла непредвиденная ошибка: {e}")
        raise e


def rec_search_request(data_transactions: pd.DataFrame, search_word: str | None) -> str:
    """Функция получает запрос поиска от пользователя по строке"""
    if search_word:
        excel_data = data_transactions.to_dict("records")
        get_string = [
            data
            for data in excel_data
            if search_word in str(data["Категория"])
            or search_word in str(data["Описание"])
        ]
        logger.info("Данные получены")
        return json.dumps(get_string, ensure_ascii=False)
    logger.error("Значение для поиска ничего не содержит")
    raise ValueError("Значение для поиска ничего не содержит")


def search_mobile_number_excel(data_transactions: pd.DataFrame) -> str:
    """Функция для поиска мобильных номеров в поле 'Категория'"""
    data_mobile_number = []
    excel_data = data_transactions.to_dict("records")
    for data in excel_data:
        re_search = re.search(r"\+7 \d{3} \d{2,3}-\d{2}-\d{2}", str(data["Описание"]))
        if re_search:
            data_mobile_number.append(data)
    logger.info("Данные считаны")
    return json.dumps(data_mobile_number, ensure_ascii=False)


def search_transactions_to_people(data_transactions: pd.DataFrame) -> str:
    """Функция для поиска переводов физ лицам"""
    sent_transaction = []
    excel_data = data_transactions.to_dict("records")
    for data in excel_data:
        re_search = re.search(
            r"^[А-ЯЁ][а-яё]+\s+[А-ЯЁ]\.$", str(data["Описание"]), re.I
        )
        if "Переводы" in str(data["Категория"]) and re_search:
            sent_transaction.append(data)
    logger.info("Данные по переводам считаны")
    return json.dumps(sent_transaction, ensure_ascii=False)
