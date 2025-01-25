import pytest
from datetime import datetime

from src.models.movement import OperationType
from src.models.purchase import purchase_factory, subscription_factory


@pytest.fixture
def setup_data():
    return {
        'Entrada/Saída': 'Credito',
        'Data': '18/01/2024',
        'Quantidade': 2,
        'Preço unitário': 5.60,
    }


def test_purchase_factory_success(setup_data):
    """
    Teste para fabricar objetos com sucesso.
    """
    purchase = purchase_factory(setup_data)
    assert purchase.operation_date == datetime(2024, 1, 18)
    assert purchase.operation == OperationType.BUY
    assert purchase.price == 5.60
    assert purchase.quantity == 2


def test_purchase_factory_fail(setup_data):
    """
    Teste para fabricar objeto tratando campo de preço.
    """
    setup_data['Preço unitário'] = '-'
    purchase = purchase_factory(setup_data)
    assert purchase.price == 0.0
    assert purchase.operation == OperationType.TRANSFER

    setup_data['Data'] = '/'
    with pytest.raises(ValueError):
        purchase_factory(setup_data)


def test_create_purchase_unfold(setup_data):
    row_dict = setup_data
    row_dict['Entrada/Saída'] = 'Debito'
    row_dict['Desdobro'] = 10
    purchase = purchase_factory(row_dict)

    assert purchase.operation == OperationType.SELL
    assert purchase.price == 5.60
    assert purchase.quantity == 2


def test_create_subscription(setup_data):
    purchase = subscription_factory(setup_data)
    assert purchase.operation == OperationType.SUBSCRIPTION
