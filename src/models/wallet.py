from typing import List, Optional

from src.service.config_service import ConfigService
from src.models.asset import Asset, AssetType


class Wallet():
    def __init__(self, config=ConfigService()):
        self.config_service = config
        self.stocks: List[Asset] = []
        self.reits: List[Asset] = []
        self.others: List[Asset] = []

    def add_asset(self, **kwargs) -> Asset:
        new_asset = Asset(asset_type=kwargs.get('asset_type'), ticker=kwargs.get('ticker'), name=kwargs.get('name'))

        if new_asset.type == AssetType.STOCK:
            if asset := self.find_stock(new_asset.ticker):
                return asset
            self.stocks.append(new_asset)

        elif new_asset.type == AssetType.REIT:
            if asset := self.find_reit(new_asset.ticker):
                return asset
            self.reits.append(new_asset)

        else:
            if asset := self.find_other(kwargs.get('name')):
                return asset
            self.others.append(new_asset)

        if new_asset.unfold_factor == None:
            new_asset.set_unfold_factor(self.config_service.get_unfold_factor(new_asset.ticker))

        return new_asset

    def find_stock(self, ticker: str) -> Optional[Asset]:
        try:
            return [item for item in self.stocks if item.ticker[0:4] == ticker[0:4]][0]
        except IndexError:
            return None

    def find_reit(self, ticker: str) -> Optional[Asset]:
        try:
            return [item for item in self.reits if item.ticker[0:4] == ticker[0:4]][0]
        except IndexError:
            return None

    def find_other(self, name: str) -> Optional[Asset]:
        try:
            return [item for item in self.others if item.name == name][0]
        except IndexError:
            return None