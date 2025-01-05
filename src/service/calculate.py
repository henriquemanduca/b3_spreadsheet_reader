from typing import Tuple

from src.exceptions.exceptions import DataFrameError

from src.sheet import SheetColuns
from src.models.asset import AssetType
from src.models.wallet import Wallet
from src.models.movement import MovementValues, create_unfold
from src.models.income import IncomeValues

from src.models.purchase import create_purchase, create_subscription
from src.models.income import create_income


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


def read_operations(data_frame, filter) -> Wallet:

    if data_frame is None:
        raise DataFrameError()

    wallet = Wallet()

    for idx, row in data_frame.iterrows():
        data_row = row.to_dict()

        asset_type, code, name = get_code_and_name_asset(data_row[SheetColuns.NAME.value])

        if (filter and not asset_type.name == filter):
            continue

        asset = wallet.add_asset(asset_type=asset_type, code=code, name=name)
        type_row = data_row[SheetColuns.TYPE.value]

        if type_row == IncomeValues.INCOME.value:
            asset.add_income(create_income(data_row))

        elif type_row == MovementValues.BY_OR_SELL.value:
            asset.add_movement(create_purchase(data_row))

        elif type_row == MovementValues.SUBSCRIPTION.value:
            asset.add_movement(create_subscription(data_row))

        elif type_row == MovementValues.UNFOLD.value:
            asset.add_movement(create_unfold(data_row))

    return wallet
