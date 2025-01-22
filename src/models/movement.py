from enum import Enum
from typing import Optional
from datetime import date, datetime
from dataclasses import dataclass

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


@dataclass
class Movement:
    operation: OperationType = OperationType.INCOME
    operation_date: Optional[date] = None
    quantity: Optional[int] = 0

    def __post_init__(self):
        """
        Validações e tratamentos pós-inicialização
        """
        if self.operation_date and not isinstance(self.operation_date, date):
            raise TypeError('Operation date must be a date')

        if self.operation and not isinstance(self.operation, OperationType):
            raise TypeError('Operation must be a OperationType')

        if self.quantity and not isinstance(self.quantity, int):
            raise TypeError('Quantity must be a int')

        self.quantity = int(self.quantity or 0)

    @classmethod
    def create(cls, **kwargs):
        """
        Método de fábrica para criação segura de movimentos

        Args:
            **kwargs: Argumentos de inicialização

        Returns:
            Movement: Nova instância do movimento
        """
        valid_args = {
            'operation_date', 'operation', 'quantity'
        }
        filtered_args = {
            k:v for k, v in kwargs.items() if k in valid_args
        }
        return cls(**filtered_args)


def movement_factory(data_row: dict) -> Movement:
    operation = OperationType.UNFOLD
    qty = data_row[SheetColuns.QUANTITY.value]
    dt = None

    try:
        dt = datetime.strptime(data_row[SheetColuns.DATE.value], "%d/%m/%Y")
    except ValueError:
        raise ValueError('Error on convert operation date')

    return Movement.create(operation=operation, operation_date=dt, quantity=qty)