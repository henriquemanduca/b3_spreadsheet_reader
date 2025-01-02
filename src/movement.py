from enum import Enum

from src.sheet import SheetColuns


class MovementValues(Enum):
    BY_OR_SELL = 'Transferência - Liquidação'
    SUBSCRIPTION = 'Direitos de Subscrição - Exercido'
    UNFOLD = 'Desdobro'


class OperationType(Enum):
    BUY = 1
    SELL = 2
    TRANSFER = 3
    SUBSCRIPTION = 4
    INCOME = 5
    UNFOLD = 6


operation_labels = {
    OperationType.BUY: "Compra",
    OperationType.SELL: "Venda",
    OperationType.TRANSFER: "Transferência",
    OperationType.SUBSCRIPTION: "Subscrição",
    OperationType.UNFOLD: "Desdobro"
}


class Movement:
    def __init__(self, date: str, operation: OperationType, quantity: int):
        from src.utils.utils import str_to_date
        self.date = str_to_date(date) if date else None
        self.operation = operation
        self.quantity = quantity

    def __str__(self) -> str:
        return f'Operation: {operation_labels.get(self.operation, 'Not found')}, QTY: {self.quantity}'


def create_unfold(data_row: dict) -> Movement:
    dt = data_row[SheetColuns.DATE.value]
    operation = OperationType.UNFOLD
    qty = data_row[SheetColuns.QUANTITY.value]
    return Movement(dt, operation, qty)