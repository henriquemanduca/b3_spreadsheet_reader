from enum import Enum
from dataclasses import dataclass

from src.utils.utils import str_to_date
from src.sheet import SheetColuns
from src.models.movement import Movement, OperationType


class IncomeValues(Enum):
    INCOME = 'Rendimento'


@dataclass
class Income(Movement):
    value: float = 0.0

    def __post_init__(self):
        """
        Validações e tratamentos pós-inicialização
        """
        if self.operation and not self.operation == OperationType.INCOME:
            raise TypeError('Operation type must be a INCOME')

        self.value = float(self.value or 0.0)

    @classmethod
    def create(cls, **kwargs):
        """
        Método de fábrica para criação de Rendimentos

        Args:
            **kwargs: Argumentos de inicialização

        Returns:
            Movement: Nova instância de Redimento
        """
        valid_args = {
            'operation_date', 'quantity', 'value'
        }
        filtered_args = {
            k:v for k, v in kwargs.items() if k in valid_args
        }
        filtered_args['operation'] = OperationType.INCOME
        return cls(**filtered_args)


def income_factory(data_row: dict) -> Income:
    dt = str_to_date(data_row[SheetColuns.DATE.value])
    qty = data_row[SheetColuns.QUANTITY.value]

    try:
        income = float(data_row[SheetColuns.PRICE.value])
    except (ValueError, KeyError):
        income = 0.0

    return Income.create(operation_date=dt, quantity=qty, value=income)