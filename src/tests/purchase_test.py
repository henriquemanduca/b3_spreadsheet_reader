import pytest

from src.movement import OperationType
from src.purchase import Purchase, create_purchase, create_subscription


@pytest.fixture
def setup_purchase() -> Purchase:
    return Purchase(date=None, operation=OperationType.BUY, quantity=5, price=10.5)


@pytest.fixture
def setup_row():
    return {
        'Entrada/Saída': 'Credito',
        'Data': '18/01/2024',
        'Quantidade': 2,
        'Preço unitário': 5.60,
    }


def test_purchase_qty_no_unfold(setup_purchase):
    purchase = setup_purchase

    assert purchase.quantity == 5


def test_create_purchase_no_unfold(setup_row):
    purchase = create_purchase(setup_row)

    assert purchase.operation == OperationType.BUY
    assert purchase.price == 5.60
    assert purchase.unfold == 1


def test_create_purchase_unfold(setup_row):
    row_dict = setup_row
    row_dict['Entrada/Saída'] = 'Debito'
    row_dict['Desdobro'] = 10
    purchase = create_purchase(row_dict)

    assert purchase.operation == OperationType.SELL
    assert purchase.price == 5.60
    assert purchase.unfold == 10
    assert purchase.quantity == 2


def test_create_create_subscription(setup_row):
    purchase = create_subscription(setup_row)

    assert purchase.operation == OperationType.SUBSCRIPTION
    assert purchase.unfold == 1