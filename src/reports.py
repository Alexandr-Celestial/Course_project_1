import json
import logging
from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Callable, Optional

import pandas as pd

from src.utils import ROOT_DIR

reports_logger = logging.getLogger(__name__)
reports_logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(
    ROOT_DIR + "/logs/logs_reports.log", mode="w", encoding="utf-8"
)
file_formatter = logging.Formatter(
    "%(asctime)s %(module)s %(funcName)s %(levelname)s: %(message)s"
)
file_handler.setFormatter(file_formatter)
reports_logger.addHandler(file_handler)


def log(filename: str | None = None) -> Callable:
    """Декоратор для логирования функции, а также её результата или ошибок"""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                result = func(*args, **kwargs)
                data_excel = result.to_dict("records")
                result_ = json.dumps(data_excel, default=str, ensure_ascii=False)
                reports_logger.info("Функция декоратора выполнена успешно")
            except Exception as e:
                result_ = f"Произошла непредвиденная ошибка {e}"
                reports_logger.error(result_)
            finally:
                if filename:
                    with open(
                        ROOT_DIR + f"/logs/{filename}.log", "w", encoding="utf-8"
                    ) as f:
                        f.write(result_ + "\n")
                    reports_logger.info(
                        f"Декоратор отработал успешно, результат записан в  {filename}.log"
                    )
                else:
                    print(result_)
                    reports_logger.info(
                        "Декоратор отработал успешно, результат выведен в консоль"
                    )
            return result_

        return wrapper

    return decorator


@log(filename="logs_reports")
def spending_by_category(
    transactions: pd.DataFrame, category: str, date: Optional[str] = None
) -> pd.DataFrame:
    """Функция возвращает траты по заданной категории за последние три месяца"""
    try:
        if not date:
            date_conv = datetime.now()
        else:
            date_conv = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        three_month_date = date_conv - timedelta(days=92)
        df = transactions
        df["Дата операции"] = pd.to_datetime(df["Дата операции"])
        filtered_df = df[
            (df["Дата операции"] >= three_month_date)
            & (df["Дата операции"] <= date_conv)
            & (df["Категория"] == category)
        ]
        reports_logger.info("Функция выполнена успешно")
        return filtered_df
    except Exception as e:
        reports_logger.error(f"Произошла ошибка: {e}")
    return pd.DataFrame([{}])
