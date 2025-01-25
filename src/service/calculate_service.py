from typing import Tuple
import yfinance as yf

from datetime import datetime

from src.exceptions.exceptions import DataFrameError, AssetError
from src.sheet import SheetColuns
from src.service.cache_service import CacheService
from src.service.config_service import ConfigService
from src.models.asset import AssetType
from src.models.wallet import Wallet
from src.models.movement import MovementValues, movement_factory
from src.models.income import IncomeValues, income_factory
from src.models.purchase import purchase_factory, subscription_factory
from src.utils.utils import get_logger


class CalculateService():
    def __init__(self, config = None, cache = None):
        self.cache_service = cache or CacheService()
        self.config_service = config or ConfigService()
        self.wallet = Wallet(self.config_service)

    def __get_ticker_and_name_asset(self, description: str) -> Tuple[AssetType, str, str]:
        index = description.find('-')

        if index > 0:
            ticker = description[0:index-1].strip()
            name = description[index+2:].strip()

            if int(ticker[4:]) in [3, 4]:
                asset_type = AssetType.STOCK

            elif int(ticker[4:]) in [11, 12, 13]:
                asset_type = AssetType.REIT

            if new_ticker := self.config_service.get_altered_ticker(ticker):
                ticker = new_ticker

            return asset_type, ticker, name

        raise AssetError()

    def __get_asset_price(self, ticker: str) -> float:
        get_logger().debug(f"Geting last price for {ticker}")

        try:
            if value := self.cache_service.get_value(ticker):
                return value['price']

            asset = yf.Ticker(f"{ticker}.SA")
            data_history = asset.history(period='1d')

            if not data_history.empty:
                price = float(data_history['Close'].iloc[-1])
                value = {
                    'price': price,
                    'timestamp': datetime.now().isoformat()
                }
                self.cache_service.set_value(ticker, value)
                return price

            return 0.0
        except Exception as e:
            self.cache_service.save()
            get_logger().error(f"{ticker}: {e}")
            return 0.0

    def read_operations(self, data_frame, filter) -> Wallet:
        if data_frame is None:
            raise DataFrameError()

        for idx, row in data_frame.iterrows():
            data_row = row.to_dict()

            try:
                name_value = data_row[SheetColuns.NAME.value]
                asset_type, ticker, name = self.__get_ticker_and_name_asset(name_value)
            except AssetError as e:
                self.wallet.add_asset(asset_type=AssetType.OTHER, name=name_value)
                get_logger().warning(f"{e.message}: {name_value}")
                continue

            if ticker in self.config_service.get_tickers_to_skip():
                continue

            if (filter and not asset_type.name == filter):
                continue

            asset = self.wallet.add_asset(asset_type=asset_type, ticker=ticker, name=name)

            if int(asset.price) == 0:
                asset.price = self.__get_asset_price(asset.ticker)

            type_row = data_row[SheetColuns.TYPE.value]

            if type_row == IncomeValues.INCOME.value:
                asset.add_income(income_factory(data_row))

            elif type_row == MovementValues.BY_OR_SELL.value:
                asset.add_movement(purchase_factory(data_row))

            elif type_row == MovementValues.SUBSCRIPTION.value:
                asset.add_movement(subscription_factory(data_row))

            elif type_row == MovementValues.UNFOLD.value:
                asset.add_movement(movement_factory(data_row))

        return self.wallet





