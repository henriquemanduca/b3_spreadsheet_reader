import json
import logging

from typing import Tuple
from datetime import date, datetime
from typing import Union

from src.movement import OperationType


logging.basicConfig()
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


def get_logger():
    return LOGGER

def str_to_date(str_date: str, from_format: str = "%d/%m/%Y") -> Union[date, None]:
    """
    Converte uma string para um objeto date

    :param data_str: A data em formato de string
    :param formato: O formato da string de data. Padrão é "%d-%m-%Y"
    :return: Um objeto datetime ou None se a conversão falhar.
    """
    try:
        return datetime.strptime(str_date, from_format)
    except ValueError as e:
        print(f"Error reading str date: {e}")
        return None


def get_operation(operation: str) -> Union[OperationType, None]:
    if operation == 'Credito':
        return OperationType.BUY

    elif operation == 'Debito':
        return OperationType.SELL

    return None


def get_code_and_name_asset(description: str) -> Tuple[str, str]:
    index = description.find('-')
    code = description[0:index-1].strip()
    name = description[index+2:].strip()
    return code, name


def read_json(file_path):
    try:
        with open(file_path if file_path else './src/helpers/unfold_helper.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError as e:
        get_logger().error(f"Erro: O arquivo não foi encontrado - {e}")
        # raise
    except json.JSONDecodeError as e:
        get_logger().error(f"Erro: O conteúdo do arquivo não é um JSON válido - {e}")
        # raise