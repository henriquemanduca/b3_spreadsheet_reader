import pytest

from datetime import datetime, date

from src.models.movement import OperationType
from src.utils.utils import float_format_pt_br, str_to_date, get_operation, round_trunc, manual_trunc, format_date_pt_br


def test_float_format_positive():
    """
    Testa formatação de número float positivo para string com duas casas decimais
    """
    assert float_format_pt_br(10.456) == "10,46"
    assert float_format_pt_br(5.0) == "5,00"


def test_float_format_negative():
    """
    Testa formatação de número float negativo para string com duas casas decimais
    """
    assert float_format_pt_br(-10.456) == "-10,46"
    assert float_format_pt_br(-5.0) == "-5,00"


def test_str_to_date_valid():
    """
    Testa conversão de string para data com formato padrão
    """
    result = str_to_date("25/12/2023")
    assert isinstance(result, datetime)
    assert result.day == 25
    assert result.month == 12
    assert result.year == 2023


def test_str_to_date_custom_format():
    """
    Testa conversão de string para data com formato customizado
    """
    result = str_to_date("2023-12-25", "%Y-%m-%d")
    assert isinstance(result, datetime)
    assert result.day == 25
    assert result.month == 12
    assert result.year == 2023


def test_str_to_date_invalid():
    """
    Testa conversão de string inválida para data
    """
    result = str_to_date("invalidDate")
    assert result is None


def test_float_format_types():
    """
    Testa tratamento de diferentes tipos de entrada
    """
    with pytest.raises(TypeError):
        float_format_pt_br("não é um float")

    with pytest.raises(TypeError):
        float_format_pt_br(None)


def test_get_operation_credit():
    """
    Testa conversão de 'Credito' para OperationType.BUY
    """
    result = get_operation('Credito')
    assert result == OperationType.BUY


def test_get_operation_debit():
    """
    Testa conversão de 'Debito' para OperationType.SELL
    """
    result = get_operation('Debito')
    assert result == OperationType.SELL


def test_get_operation_invalid():
    """
    Testa entrada inválida retornando None
    """
    result = get_operation('Outro')
    assert result is None


def test_get_operation_empty_string():
    """
    Testa entrada de string vazia
    """
    result = get_operation('')
    assert result is None


def test_get_operation_none_input():
    """
    Testa entrada None
    """
    with pytest.raises(TypeError):
        get_operation(None)


def test_round_trunc_positive():
    """
    Testa arredondamento de números positivos para 2 casas decimais
    """
    assert round_trunc(10.456) == 10.46
    assert round_trunc(5.005) == 5.01


def test_round_trunc_negative():
    """
    Testa arredondamento de números negativos para 2 casas decimais
    """
    assert round_trunc(-10.456) == -10.46
    assert round_trunc(-5.005) == -5.01


def test_manual_trunc_positive():
    """
    Testa truncamento manual de números positivos para 2 casas decimais
    """
    assert manual_trunc(10.456) == 10.45
    assert manual_trunc(5.005) == 5.00


def test_manual_trunc_negative():
    """
    Testa truncamento manual de números negativos para 2 casas decimais
    """
    assert manual_trunc(-10.456) == -10.45
    assert manual_trunc(-5.005) == -5.00


def test_format_date_pt_br():
    """
    Testa formatação de data no padrão brasileiro
    """
    test_date = date(2023, 12, 25)
    assert format_date_pt_br(test_date) == "25/12/2023"


def test_format_date_pt_br_different_dates():
    """
    Testa formatação de diferentes datas
    """
    test_dates = [
        (date(2023, 1, 1), "01/01/2023"),
        (date(2023, 12, 31), "31/12/2023"),
        (date(2000, 2, 29), "29/02/2000")
    ]

    for test_date, expected in test_dates:
        assert format_date_pt_br(test_date) == expected


def test_format_date_pt_br_input_validation():
    """
    Testa tratamento de entradas inválidas
    """
    with pytest.raises(TypeError):
        format_date_pt_br("não é uma data")

    with pytest.raises(TypeError):
        format_date_pt_br(None)

