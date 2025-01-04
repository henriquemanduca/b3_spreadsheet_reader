from typing import List

from src.utils.utils import str_to_date, get_logger
from src.movement import Movement, OperationType
from src.income import Income


class Asset:
    def __init__(self, code: str, name: str):
        self.code = code
        self.name = name
        self.movements = []
        self.incomes = []
        self.unfold_factor = None

    @property
    def quantity(self) -> int:
        return int(self.get_buys() + self.get_unfolds() - self.get_sells())

    @property
    def average_price(self) -> float:
        """
        Exemplo Prático:

        Vamos supor que você fez as seguintes transações:
            Compra 1: 100 ações a R$10,00 (custo total: R$1000,00 + R$5,00 de corretagem = R$1005,00)
            Compra 2: 50 ações a R$12,00 (custo total: R$600,00 + R$3,00 de corretagem = R$603,00)
            Venda 1: 75 ações a R$15,00 (valor total: R$1125,00 - R$4,00 de corretagem = R$1121,00)
            Compra 3: 100 ações a R$13,00 (custo total: R$1300,00 + R$5,00 de corretagem = R$1305,00)

        Cálculos:
            Número Total de Ações: 100 + 50 - 75 + 100 = 175 ações
            Custo Total das Ações: R$1005,00 + R$603,00 - R$1121,00 + R$1305,00 = R$1792,00
            Preço Médio Ponderado: R$1792,00 / 175 = R$10,24 por ação (aproximadamente)
        """

        buys_qty = 0
        buys_cost = 0.0

        for item in [item for item in self.movements if item.operation in [OperationType.BUY, OperationType.SUBSCRIPTION]]:
            if getattr(item, 'price', 0.0) == 0.0:
                continue

            unfold_factor = 1
            if self.has_unfold():
                try:
                   unfold_factor = self.unfold_factor['factor'] if item.mov_date <= str_to_date(self.unfold_factor['date'], "%Y-%m-%d") else 1
                except TypeError:
                    unfold_factor = 1

            buys_qty += item.quantity * unfold_factor
            buys_cost += (item.quantity * unfold_factor) * (item.price / unfold_factor)

            get_logger().debug("%s, Qty: %s, Cost: $%s", item.operation, int(item.quantity), "{:.{}f}".format(buys_cost, 2))

        sells_qty = 0
        sells_cost = 0.0

        for item in [item for item in self.movements if item.operation == OperationType.SELL]:
            if getattr(item, 'price', 0.0) <= 0.0:
                continue

            if self.has_unfold():
                try:
                   unfold_factor = self.unfold_factor['factor'] if item.mov_date <= str_to_date(self.unfold_factor['date'], "%Y-%m-%d") else 1
                except TypeError:
                    unfold_factor = 1

            sells_qty += item.quantity * unfold_factor
            sells_cost += (item.quantity * unfold_factor) * (item.price / unfold_factor)

            get_logger().debug("%s, Qty: %s, Cost: $%s", item.operation, int(item.quantity), "{:.{}f}".format(sells_cost, 2))

        qty = buys_qty - sells_qty
        values = (buys_cost - sells_cost) / qty

        get_logger().debug("Total itens: %d, Avarege: $%s", qty, "{:.{}f}".format(values, 2))

        return "{:.{}f}".format(values, 2)

    def add_movement(self, movement: Movement):
        if movement.operation != OperationType.TRANSFER:
            self.movements.append(movement)

        self.movements = sorted(self.movements, key=lambda item: item.mov_date, reverse=False)

    def add_income(self, income: Income):
        if income.operation == OperationType.INCOME:
            self.incomes.append(income)

        self.incomes = sorted(self.incomes, key=lambda item: item.mov_date, reverse=False)

    def get_sells(self) -> int:
        return sum(
            value.quantity
            for value in self.movements
            if value.operation == OperationType.SELL
        )

    def get_buys(self) -> int:
        return sum(
            value.quantity
            for value in self.movements
            if value.operation in [OperationType.BUY, OperationType.SUBSCRIPTION]
        )

    def get_unfolds(self) -> int:
        return sum(
            value.quantity
            for value in self.movements
            if value.operation in [OperationType.UNFOLD]
        )

    def has_unfold(self) -> bool:
        return len([value for value in self.movements if value.operation in [OperationType.UNFOLD]])

    def set_unfold_factor(self, value: dict):
        self.unfold_factor = value

    def __str__(self) -> str:
        return f'Asset: {self.code} - {self.name}, Quantity: {self.quantity}'


def get_or_create_asset(assets: List, code: str, name: str) -> Asset:
    for item in assets:
        if item.code[:-2] == code[:-2]:
            return item

    assets.append(Asset(code, name))
    return assets[len(assets)-1]