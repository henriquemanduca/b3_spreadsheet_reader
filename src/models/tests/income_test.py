import pytest

from datetime import datetime

from src.models.movement import OperationType
from src.models.income import income_factory


@pytest.fixture
def setup_data():
    return {
        'Data': '18/01/2024',
        'Quantidade': 2,
        'Preço unitário': 5.60,
    }


def test_income_factory_success(setup_data):
    """
    Testa função fabrica de Rendimentos
    """
    income = income_factory(setup_data)
    assert income.operation_date == datetime(2024, 1, 18)
    assert income.operation == OperationType.INCOME
    assert income.quantity == 2
    assert income.value == 5.60


def test_income_factory_price_fail(setup_data):
    """
    Testa função fabrica de Rendimentos com preço inválido
    """
    setup_data['Preço unitário'] = '-'
    income = income_factory(setup_data)
    assert income.value == 0.0

    setup_data['Preço unitário'] = ''
    income = income_factory(setup_data)
    assert income.value == 0.0


def test_income_factory_operation_date_fail(setup_data):
    """
    Testa função fabrica de Rendimentos com data inválida
    """
    setup_data['Data'] = '2024-01'
    with pytest.raises(ValueError):
        income_factory(setup_data)
