import json
import logging
import locale

from datetime import date, datetime
from typing import Union

from src.models.movement import OperationType


LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
formatter = logging.Formatter('%(levelname)s: %(message)s')
console_handler.setFormatter(formatter)
LOGGER.addHandler(console_handler)


def get_logger():
    return LOGGER


def float_format(value: float) -> str:
    return "{:.{}f}".format(value, 2).replace('.', ',')


def str_to_date(str_date: str, from_format: str = "%d/%m/%Y") -> Union[date, None]:
    try:
        return datetime.strptime(str_date, from_format)
    except ValueError as e:
        print(f"Error reading str date: {e}")
        return None


def format_date_pt_br(date_obj: date) -> str:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    return date_obj.strftime("%d/%m/%Y")


def get_operation(operation: str) -> Union[OperationType, None]:
    if operation == 'Credito':
        return OperationType.BUY
    elif operation == 'Debito':
        return OperationType.SELL
    return None


