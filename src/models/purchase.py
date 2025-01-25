from dataclasses import dataclass

from src.sheet import SheetColuns
from src.models.movement import Movement, OperationType
from src.utils.utils import get_operation, str_to_date, get_logger


@dataclass
class Purchase(Movement):
    price: float = 0.0

    def __post_init__(self):
        """
        Validações e tratamentos pós-inicialização
        """
        super().__post_init__()
        self.price = float(self.price or 0.0)

    @classmethod
    def create(cls, **kwargs):
        """
        Método de fábrica para criação segura de Compras

        Args:
            **kwargs: Argumentos de inicialização

        Returns:
            Purchase: Nova instância da compra
        """
        valid_args = {
            'operation_date', 'operation', 'quantity', 'price'
        }
        filtered_args = {
            k:v for k, v in kwargs.items() if k in valid_args
        }
        return cls(**filtered_args)


def purchase_factory(data_row: dict) -> Purchase:
    dt = str_to_date(data_row[SheetColuns.DATE.value])
    operation = get_operation(data_row[SheetColuns.FLOW.value])
    qty = data_row[SheetColuns.QUANTITY.value]

    try:
        price = float(data_row[SheetColuns.PRICE.value])
    except (ValueError, KeyError):
        operation = OperationType.TRANSFER
        price = 0.0

    return Purchase.create(operation_date=dt, operation=operation, quantity=qty, price=price)


def subscription_factory(data_row: dict) -> Purchase:
    dt = str_to_date(data_row[SheetColuns.DATE.value])
    operation = OperationType.SUBSCRIPTION
    qty = data_row[SheetColuns.QUANTITY.value]
    return Purchase.create(operation_date=dt, operation=operation, quantity=qty)