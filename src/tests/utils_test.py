from datetime import datetime

from src.utils import get_code_and_name_asset, get_operation, get_code_and_name_asset, str_to_date
from src.movement import OperationType


def test_get_code_and_name_asset():
    code, name = get_code_and_name_asset('VGIR11 - VALORA CRI CDI FUNDO DE INVESTIMENTO IMOBILIÁRIO ')
    assert code == 'VGIR11'
    assert name == 'VALORA CRI CDI FUNDO DE INVESTIMENTO IMOBILIÁRIO'


def test_get_operation():
    assert get_operation('Credito') == OperationType.BUY
    assert get_operation('Debito') == OperationType.SELL
    assert get_operation('Outro') == None


def test_str_to_date():
    assert str_to_date('18/01/2024') == datetime(2024, 1, 18, 0, 0)