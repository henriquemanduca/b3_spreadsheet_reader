from enum import Enum

from src.sheet import SheetColuns
from src.movement import Movement, OperationType


class IncomeValues(Enum):
    INCOME = 'Rendimento'


class Income(Movement):
    def __init__(self, date, quantity: int, value: float):
        super().__init__(date, OperationType.INCOME, quantity)

        self.value = value

    def __str__(self) -> str:
        return super().__str__()


def create_income(data_row: dict) -> Income:
    dt = data_row[SheetColuns.DATE.value]
    qty = data_row[SheetColuns.QUANTITY.value]

    try:
        price = float(data_row[SheetColuns.PRICE.value])
    except (ValueError, KeyError):
        price = 0.0

    return Income(date=dt, quantity=qty, value=price)