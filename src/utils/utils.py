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


def float_format_pt_br(value: float) -> str:
    """
    Formata um float para duas casas decimais com virgula

    Args:
        value (float): Valor a ser formatado

    Returns:
        str: Valor formatado para duas casas decimais
    """
    return '{:.{}f}'.format(value, 2).replace('.', ',')


def str_to_date(str_date: str, from_format: str = '%d/%m/%Y') -> Union[date, None]:
    try:
        return datetime.strptime(str_date, from_format)
    except ValueError as e:
        raise ValueError(f'Error on convert string to date: \n{e}')


def round_trunc(value: float) -> float:
    """
    Arredonda um valor float para 2 casas decimais usando round()

    Args:
        value (float): Valor a ser arredondado

    Returns:
        float: Valor arredondado com 2 casas decimais
    """
    return round(value, 2)


def manual_trunc(value: float) -> float:
    """
    Trunca um valor float para 2 casas decimais

    Args:
        value (float): Valor a ser truncado

    Returns:
        float: Valor truncado com 2 casas decimais
    """
    return int(value * 100) / 100


def format_date_pt_br(date_obj: date) -> str:
    """
    Formata uma data no padrão brasileiro

    Args:
        date_obj (date): Objeto tipo date para formatar

    Returns:
        str: Data formatada no padrão dd/mm/aaaa

    Raises:
        TypeError: Se o input não for um date
    """
    if not isinstance(date_obj, date):
        raise TypeError('Input must be a date object')

    try:
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    except locale.Error:
        return date_obj.strftime('%d/%m/%Y')

    return date_obj.strftime('%d/%m/%Y')


def get_operation(operation: str) -> Union[OperationType, None]:
    """
    Converte string de operação para OperationType.

    Args:
        operation (str): Tipo de operação ('Credito' ou 'Debito')

    Returns:
        OperationType ou None: Tipo de operação correspondente

    Raises:
        TypeError: Se o input for um None
    """
    if operation is None:
        raise TypeError('Operation cannot be None')

    operation_upper = operation.strip().upper()

    if operation_upper == 'CREDITO':
        return OperationType.BUY
    elif operation_upper == 'DEBITO':
        return OperationType.SELL

    return None

