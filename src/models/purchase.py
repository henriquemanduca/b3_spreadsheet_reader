from src.sheet import SheetColuns
from src.models.movement import Movement, OperationType
from src.utils.utils import get_operation


class Purchase(Movement):
    def __init__(self, date: str, operation: OperationType, quantity: int, price = 0.0):
        super().__init__(date, operation, quantity)
        self.price = price

    def __str__(self) -> str:
        return super().__str__()


def create_purchase(data_row: dict) -> Purchase:
    dt = data_row[SheetColuns.DATE.value]
    operation = get_operation(data_row[SheetColuns.FLOW.value])
    qty = data_row[SheetColuns.QUANTITY.value]

    try:
        price = float(data_row[SheetColuns.PRICE.value])
    except (ValueError, KeyError):
        operation = OperationType.TRANSFER
        price = 0.0

    return Purchase(date=dt, operation=operation, quantity=qty, price=price)


def create_subscription(data_row: dict) -> Purchase:
    dt = data_row[SheetColuns.DATE.value]
    operation = OperationType.SUBSCRIPTION
    qty = data_row[SheetColuns.QUANTITY.value]

    return Purchase(date=dt, operation=operation, quantity=qty)