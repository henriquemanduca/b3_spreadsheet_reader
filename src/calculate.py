import pandas as pd
import logging
import sys

from typing import List

from src.utils.utils import get_logger, get_code_and_name_asset, read_json

from src.sheet import SheetColuns
from src.movement import OperationType, MovementValues, create_unfold
from src.income import IncomeValues
from src.purchase import Purchase, create_purchase, create_subscription
from src.asset import Asset, get_or_create_asset
from src.income import create_income


def load_from_file(input_file: str, sheet: str):
    try:
        return pd.read_excel(input_file, sheet_name=sheet)
    except Exception as e:
        get_logger().error(f"{e}")
        sys.exit()


def read_operations(data_frame, filter):
    unfold_factor_helper = read_json(None)

    assets = []

    if data_frame is not None:
        for index, row in data_frame.iterrows():
            data_row = row.to_dict()
            code, name = get_code_and_name_asset(data_row[SheetColuns.NAME.value])

            if filter and not code[:-2] == filter[:-2]:
                continue

            asset = get_or_create_asset(assets, code, name)

            if asset.unfold_factor == None:
                asset.set_unfold_factor(unfold_factor_helper.get(asset.code))

            type_row = data_row[SheetColuns.TYPE.value]

            if type_row == IncomeValues.INCOME.value:
                asset.add_income(create_income(data_row))

            elif type_row == MovementValues.BY_OR_SELL.value:
                asset.add_movement(create_purchase(data_row))

            elif type_row == MovementValues.SUBSCRIPTION.value:
                asset.add_movement(create_subscription(data_row))

            elif type_row == MovementValues.UNFOLD.value:
                asset.add_movement(create_unfold(data_row))

    return assets


def print_assets(output_file: str, assets: List[Asset]):
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            for asset in assets:
                if asset.quantity == 0:
                    continue

                file.write(f'{asset.code} - QTY: {str(asset.quantity).zfill(3)} - Avarege: ${asset.average_price}\n')

                purchases: List[Purchase] = [
                    pur for pur in asset.movements
                    if pur.operation in [OperationType.BUY, OperationType.SELL, OperationType.SUBSCRIPTION]
                ]

                for item in purchases:
                    if item.operation == OperationType.BUY:
                        file.write(f'BUY : {str(int(item.quantity)).zfill(3)} at ${item.price}\n')
                    elif item.operation == OperationType.SUBSCRIPTION:
                        file.write(f'SUB : {str(int(item.quantity)).zfill(3)} at ${item.price}\n')
                    else:
                        file.write(f'SELL: {str(int(item.quantity)).zfill(3)} at ${item.price}\n')

                file.write('-----------------------------\n')

        get_logger().info(f"Report saved on {output_file}")
    except IOError as e:
        get_logger().error(f"{e}")
        sys.exit()


def calculate_spreadsheet(args):
    if args.verbose:
        get_logger().setLevel(logging.DEBUG)

    input_file = args.input if args.input else 'sample.xlsx'
    sheet = args.sheet if args.sheet else 'Movimentação'

    data_frame = load_from_file(input_file, sheet)

    filter_code = args.filter if args.filter else None
    assets = read_operations(data_frame, filter_code)

    output_file = args.output if args.output else 'report.txt'

    print_assets(output_file, assets)
