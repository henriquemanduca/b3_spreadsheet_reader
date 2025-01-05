import pandas as pd
import logging
import sys
import csv

from typing import List

from src.utils.utils import get_logger, float_format

from src.sheet import SheetColuns
from src.movement import MovementValues, create_unfold
from src.income import IncomeValues
from src.purchase import create_purchase, create_subscription
from src.asset import Asset, get_or_create_asset, get_code_and_name_asset
from src.income import create_income


def load_from_file(input_file: str, sheet: str):
    try:
        return pd.read_excel(input_file, sheet_name=sheet)
    except Exception as e:
        get_logger().error(f"{e}")
        sys.exit()


def read_operations(data_frame, filter):
    assets = []

    if data_frame is not None:
        for index, row in data_frame.iterrows():
            data_row = row.to_dict()
            asset_type, code, name = get_code_and_name_asset(data_row[SheetColuns.NAME.value])

            if (filter and not asset_type.name == filter):
                continue

            asset = get_or_create_asset(assets, asset_type=asset_type, code=code, name=name)

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
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            writer.writerow(['ASSET', 'QUANTITY', 'AVERAGE'])

            for asset in assets:
                if asset.quantity == 0:
                    get_logger().debug(f"Asset {asset.code} has 0 quantity")
                    writer.writerow([asset.code, 0, 0])
                    continue

                get_logger().debug(f"Printing {asset.code}")

                writer.writerow([
                    asset.code,
                    int(asset.quantity),
                    float_format(asset.average_price)
                ])

        get_logger().info(f"Report saved on {output_file}")
    except IOError as e:
        get_logger().error(f"{e}")
        sys.exit()


def calculate_spreadsheet(args):
    if args.verbose:
        get_logger().setLevel(logging.DEBUG)

    input_file = args.input if args.input else 'sample.xlsx'
    sheet = args.sheet if args.sheet else 'Movimentação'
    output_file = args.output if args.output else 'report.csv'
    filter_type = args.filter if args.filter else None

    data_frame = load_from_file(input_file, sheet)
    assets = read_operations(data_frame, filter_type)

    print_assets(output_file, assets)
