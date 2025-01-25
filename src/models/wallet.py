from typing import List, Optional, Dict, Any

from src.utils.utils import get_logger
from src.service.config_service import ConfigService
from src.models.asset import Asset, AssetType


class Wallet():
    def __init__(self, config = None):
        """
        Inicialização segura da carteira com validação de configuração
        """
        self.config_service = config or ConfigService()
        self.stocks: List[Asset] = []
        self.reits: List[Asset] = []
        self.others: List[Asset] = []

    def add_asset(self, **kwargs) -> Asset:
        """
        Método defensivo para adicionar ativos à carteira
        """

        try:
            self._validate_asset_kwargs(kwargs)
            new_asset = Asset(
                asset_type=kwargs['asset_type'],
                ticker=kwargs['ticker'],
                name=kwargs['name']
            )
            return self._add_asset_by_type(new_asset)
        except (KeyError, ValueError) as e:
            raise ValueError(f"Invalid asset input: {str(e)}")

    def _validate_asset_kwargs(self, kwargs: Dict[str, Any]):
        """
        Validação rigorosa dos argumentos de entrada
        """

        required_keys = ['asset_type', 'ticker', 'name']
        for key in required_keys:
            if key not in kwargs:
                raise KeyError(f"Missing required argument: {key}")

        if not isinstance(kwargs['asset_type'], AssetType):
            raise ValueError("Invalid asset type")

    def _add_asset_by_type(self, new_asset: Asset) -> Asset:
        """
        Adiciona ativo a lista correta e verifica possível duplicidade
        """

        asset_lists = {
            AssetType.STOCK: (self._stocks, self.find_stock),
            AssetType.REIT: (self._reits, self.find_reit),
            AssetType.OTHER: (self._others, self.find_other)
        }

        target_list, finder_method = asset_lists.get(new_asset.type, (self._others, self.find_other))

        if existing_asset := finder_method(new_asset.ticker if new_asset.type != AssetType.OTHER else new_asset.name):
            return existing_asset

        if new_asset.unfold_factor is None:
            try:
                new_asset.set_unfold_factor(
                    self.config_service.get_unfold_factor(new_asset.ticker)
                )
            except Exception as e:
                get_logger().error(f"Error on set unfolde factor to {new_asset.ticker} \n{str(e)}")
                pass

        target_list.append(new_asset)
        return new_asset

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

    def get_total_value_wallet(self) -> float:
        return 0.0

    def get_total_value_stock(self) -> float:
        return sum([item.price * item.quantity for item in self.reits if item.type == AssetType.STOCK])

    def get_total_value_reit(self) -> float:
        return sum([item.price * item.quantity for item in self.reits if item.type == AssetType.REIT])

    def get_total_value_others(self) -> float:
        return sum([item.price * item.quantity for item in self.reits if item.type == AssetType.OTHER])

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