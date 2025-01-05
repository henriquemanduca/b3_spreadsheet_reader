from typing import List, Optional

from src.utils.utils import read_json
from src.models.asset import Asset, AssetType


class Wallet():
    def __init__(self,):
        self.stocks: List[Asset] = []
        self.reits: List[Asset] = []
        self.others: List[Asset] = []

    def add_asset(self, **kwargs) -> Asset:
        new_asset = Asset(asset_type=kwargs.get('asset_type'), code=kwargs.get('code'), name=kwargs.get('name'))

        if new_asset.type == AssetType.STOCK:
            if asset := self.find_stock(new_asset.code):
                return asset
            self.stocks.append(new_asset)

        elif new_asset.type == AssetType.REIT:
            if asset := self.find_reit(new_asset.code):
                return asset
            self.reits.append(new_asset)

        else:
            if asset := self.find_other(kwargs.get('name')):
                return asset
            self.others.append(new_asset)

        if new_asset.unfold_factor == None:
            new_asset.set_unfold_factor(read_json().get(new_asset.code))

        return new_asset

    def find_stock(self, code: str) -> Optional[Asset]:
        try:
            return [item for item in self.stocks if item.code[0:4] == code[0:4]][0]
        except IndexError:
            return None

    def find_reit(self, code: str) -> Optional[Asset]:
        try:
            return [item for item in self.reits if item.code[0:4] == code[0:4]][0]
        except IndexError:
            return None

    def find_other(self, name: str) -> Optional[Asset]:
        try:
            return [item for item in self.others if item.name == name][0]
        except IndexError:
            return None