from src.sheet import SheetColuns
from src.movement import Movement, OperationType
from src.utils import get_operation


class Purchase(Movement):
    def __init__(self, date: str, operation: OperationType, quantity: int, price = 0.0, unfold_factor = 1):
        super().__init__(date, operation, quantity)

        self.price = price
        self.unfold = unfold_factor

    @property
    def qty(self) -> int:
        """
        Unfolded if unfold value exist
        """
        return int(self.quantity * self.unfold)

    def __str__(self) -> str:
        return super().__str__()


def create_purchase(data_row: dict) -> Purchase:
    dt = data_row[SheetColuns.DATE.value]
    operation = get_operation(data_row[SheetColuns.FLOW.value])
    qty = data_row[SheetColuns.QUANTITY.value]

    try:
        unfold = int(data_row[SheetColuns.ULFOLD.value])
    except (ValueError, KeyError):
        unfold = 1

    try:
        price = float(data_row[SheetColuns.PRICE.value])
    except (ValueError, KeyError):
        operation = OperationType.TRANSFER
        price = 0.0

    return Purchase(date=dt, operation=operation, quantity=qty, price=price, unfold_factor=unfold)


def create_subscription(data_row: dict) -> Purchase:
    dt = data_row[SheetColuns.DATE.value]
    operation = OperationType.SUBSCRIPTION
    qty = data_row[SheetColuns.QUANTITY.value]

    try:
        unfold = int(data_row[SheetColuns.ULFOLD.value])
    except (ValueError, KeyError):
        unfold = 1

    return Purchase(date=dt, operation=operation, quantity=qty, unfold_factor=unfold)