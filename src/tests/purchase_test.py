
from src.movement import OperationType
from src.purchase import Purchase, create_purchase, create_subscription


def get_purchase_mock() -> Purchase:
    return Purchase(date=None, operation=OperationType.BUY, quantity=5, price=10.5)


def get_row_dict():
    return {
        'Entrada/Saída': 'Credito',
        'Data': '18/01/2024',
        'Quantidade': 2,
        'Preço unitário': 5.60,
    }


def test_purchase_qty_no_unfold():
    purchase = get_purchase_mock()

    assert purchase.qty == 5


def test_purchase_qty_unfold():
    purchase = get_purchase_mock()
    purchase.unfold = 10

    assert purchase.qty == 50


def test_create_purchase_no_unfold():
    purchase = create_purchase(get_row_dict())

    assert purchase.operation == OperationType.BUY
    assert purchase.price == 5.60
    assert purchase.unfold == 1


def test_create_purchase_unfold():
    row_dict = get_row_dict()
    row_dict['Entrada/Saída'] = 'Debito'
    row_dict['Desdobro'] = 10
    purchase = create_purchase(row_dict)

    assert purchase.operation == OperationType.SELL
    assert purchase.price == 5.60
    assert purchase.unfold == 10
    assert purchase.qty == 20


def test_create_create_subscription():
    purchase = create_subscription(get_row_dict())

    assert purchase.operation == OperationType.SUBSCRIPTION
    assert purchase.unfold == 1