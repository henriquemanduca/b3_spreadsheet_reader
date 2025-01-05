from typing import List
from enum import Enum
from typing import Tuple

from src.utils.utils import str_to_date, get_logger, read_json
from src.movement import Movement, OperationType
from src.income import Income


class AssetType(Enum):
    STOCK = 1
    # Real Estate Investment Trusts / FIIs
    REIT = 2
    # Others
    OTHER = 3


class Asset:
    def __init__(self, **kwargs):
        self.type = kwargs.get('asset_type')
        self.code = kwargs.get('code')
        self.name = kwargs.get('name')
        self.movements = []
        self.incomes = []
        self.unfold_factor = None

    @property
    def quantity(self) -> int:
        return int(self.get_buys() + self.get_unfolds() - self.get_sells())

    @property
    def average_price(self) -> float:
        """
        Let's assume you made the following transactions:
        Purchase 1: 100 shares at $10.00 (total cost: $1000.00 + $5.00 brokerage = $1005.00)
        Purchase 2: 50 shares at $12.00 (total cost: $600.00 + $3.00 brokerage = $603.00)
        Sale 1: 75 shares at $15.00 (total value: $1125.00 - $4.00 brokerage = $1121.00)
        Purchase 3: 100 shares at $13.00 (total cost: $1300.00 + $5.00 brokerage = $1305.00)

        Calculations:
            Total Number of Shares: 100 + 50 - 75 + 100 = 175 shares
            Total Cost of Shares: $1005.00 + $603.00 - $1121.00 + $1305.00 = $1792.00
            Weighted Average Price: $1792.00 / 175 = $10.24 per share (approximately)
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
            if getattr(item, 'price', 0.0) <= 1.0:
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

        get_logger().debug("Total: %d, Avarege: $%s", qty, values)
        return values

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


def get_code_and_name_asset(description: str) -> Tuple[AssetType, str, str]:
    index = description.find('-')

    if index > 0:
        code = description[0:index-1].strip()
        name = description[index+2:].strip()

        if int(code[4:]) in [3, 4]:
            asset_type = AssetType.STOCK

        elif int(code[4:]) in [11, 12, 13]:
            asset_type = AssetType.REIT

        return asset_type, code, name

    return AssetType.OTHER, "", description


def get_or_create_asset(assets: List[Asset], **kwargs) -> Asset:
    for item in assets:
        if item.type in [AssetType.STOCK, AssetType.REIT] and item.code[0:4] == kwargs.get('code')[0:4]:
            return item
        elif item.name == kwargs.get('name'):
            return item

    asset = Asset(asset_type=kwargs.get('asset_type'), code=kwargs.get('code'), name=kwargs.get('name'))

    if asset.unfold_factor == None:
        asset.set_unfold_factor(read_json(None).get(asset.code))

    assets.append(asset)

    return asset
