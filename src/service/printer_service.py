import csv

from typing import List

from src.utils.utils import get_logger, float_format, format_date_pt_br
from src.models.asset import Asset
from src.models.wallet import Wallet
from src.service.config_service import ConfigService


class PrinterService():
    def __init__(self, config=ConfigService()):
        self.config = config

    def __default_printing(self, file_parts, sufix, assets: List[Asset]):

        assets = sorted(assets, key=lambda item: item.ticker, reverse=False)

        with open(f"{file_parts[0]}_{sufix}.{file_parts[1]}", mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                'ATIVO',
                'PRIMEIRA COMPRA',
                'ULTIMA COMPRA',
                'QUANTIDADE',
                'MÉDIA',
                'PREÇO',
                'INVESTIDO',
                'POSIÇÃO',
                'RENDIMENTOS'])

            for asset in assets:
                if asset.quantity == 0:
                    # name = asset.name if asset.code == '' else asset.code
                    # get_logger().debug(f"Asset {name} has 0 quantity")
                    # writer.writerow([name, 0,  0,  0, '', '', 0, 0, 0])
                    continue

                get_logger().debug(f"Printing {asset.ticker}")
                first_date, last_date = asset.get_buy_dates()

                writer.writerow([
                    asset.ticker,
                    format_date_pt_br(first_date),
                    format_date_pt_br(last_date),
                    int(asset.quantity),
                    float_format(asset.average_price),
                    float_format(asset.price),
                    float_format(asset.get_invested_amount()),
                    float_format(asset.price * asset.quantity),
                    float_format(asset.get_income_amount()),
                ])

    def print_assets_csv(self, output_file: str, wallet: Wallet):
        file_parts = output_file.rsplit(".", 1)

        if len(wallet.stocks) > 0:
            self.__default_printing(file_parts, 'stocks', wallet.stocks)

        if len(wallet.reits) > 0:
            self.__default_printing(file_parts, 'reits', wallet.reits)

        if len(wallet.others) > 0:
            self.__default_printing(file_parts, 'others', wallet.others)