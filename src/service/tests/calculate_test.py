import pytest
import yfinance as yf
import pandas as pd

from datetime import datetime
from unittest.mock import patch, MagicMock

from src.exceptions.exceptions import DataFrameError, AssetError
from src.models.asset import AssetType
from src.service.calculate_service import CalculateService


@pytest.fixture
def calculate_service_instance():
    """
    Fixture para criar uma instância da classe com mocks de serviços.
    """
    config_service_mock = MagicMock()
    config_service_mock.get_unfold_factor.return_value = None
    config_service_mock.get_altered_ticker.return_value = None
    cache_service_mock = MagicMock()
    cache_service_mock.get_value.return_value = None
    return CalculateService(config_service_mock, cache_service_mock)


@pytest.fixture
def setup_wallet(calculate_service_instance):
    rows = [
        {
            'Entrada/Saída': 'Credito',
            'Data': '20/09/2021',
            'Produto': 'KNSC11 - KINEA SECURITIES FUNDO DE INVESTIMENTO IMOBILIARIO - FII',
            'Movimentação': 'Transferência - Liquidação',
            'Quantidade': 37,
            'Preço unitário': 100.08,
        },
        {
            'Entrada/Saída': 'Debito',
            'Data': '04/03/2022',
            'Produto': 'KNSC12 - KINEA SECURITIES FUNDO DE INVESTIMENTO IMOBILIARIO - FII',
            'Movimentação': 'Direitos de Subscrição - Exercido',
            'Quantidade': 20,
            'Preço unitário': '-',
        },
        {
            'Entrada/Saída': 'Credito',
            'Data': '07/01/2022',
            'Produto': 'PETR4 - PETROBRAS',
            'Movimentação': 'Transferência - Liquidação',
            'Quantidade': 50,
            'Preço unitário': 15.08,
        },
        {
            'Entrada/Saída': 'Debito',
            'Data': '10/01/2022',
            'Produto': 'PETR4 - PETROBRAS',
            'Movimentação': 'Transferência - Liquidação',
            'Quantidade': 20,
            'Preço unitário': 17.90,
        },
        {
            'Entrada/Saída': 'Credito',
            'Data': '11/01/2022',
            'Produto': 'Outro Investimento',
            'Movimentação': '',
            'Quantidade': 20,
            'Preço unitário': 17.90,
        }
    ]
    return calculate_service_instance.read_operations(pd.DataFrame(rows), None)


def test_setup_data_frame_not_provide(calculate_service_instance):
    """
    Testa verificação de data frame não informado
    """
    with pytest.raises(DataFrameError):
        calculate_service_instance.read_operations(None, None)


def test_get_ticker_and_name_asset_sucess_stock(calculate_service_instance):
    """
    Testa desmembramento das informaçãos do ativo tipo stock
    """
    asset_type, ticker, name = calculate_service_instance._CalculateService__get_ticker_and_name_asset('PETR4 - PETROBRAS')
    assert asset_type == AssetType.STOCK
    assert ticker == 'PETR4'
    assert name == 'PETROBRAS'


def test_get_ticker_and_name_asset_sucess_reit(calculate_service_instance):
    """
    Testa desmembramento das informaçãos do ativo tipo reit
    """
    asset_type, ticker, name = calculate_service_instance._CalculateService__get_ticker_and_name_asset('KNSC11 - KINEA SECURITIES')
    assert asset_type == AssetType.REIT
    assert ticker == 'KNSC11'
    assert name == 'KINEA SECURITIES'


def test_get_ticker_and_name_asset_other_types(calculate_service_instance):
    """
    Testa verificação de ativos não tratados
    """
    with pytest.raises(AssetError):
        calculate_service_instance._CalculateService__get_ticker_and_name_asset('Outro Investimento')


def test_get_asset_price_with_cache(calculate_service_instance):
    """
    Teste para busca de preço com cache.
    """
    ticker = 'KNSC11'
    cached_value = {
        'price': 99.90,
        'timestamp': datetime.now().isoformat()
    }

    calculate_service_instance.cache_service.get_value.return_value = cached_value
    price = calculate_service_instance._CalculateService__get_asset_price(ticker)

    assert price == 99.90
    calculate_service_instance.cache_service.get_value.assert_called_once_with(ticker)


@patch('yfinance.Ticker')
def test_get_asset_price_without_cache(mock_ticker, calculate_service_instance):
    """
    Teste para busca de preço sem cache.
    """
    ticker = 'PETR4'
    mock_data = pd.DataFrame({
        'Close': [25.75]
    })
    mock_instance = mock_ticker.return_value
    mock_instance.history.return_value = mock_data

    price = calculate_service_instance._CalculateService__get_asset_price(ticker)

    assert price == 25.75


def test_get_asset_price_with_exception(calculate_service_instance):
    """
    Teste para tratamento de exceções na busca de preço.
    """
    ticker = 'ERRO4'
    calculate_service_instance.cache_service.get_value.side_effect = Exception('Test error')
    price = calculate_service_instance._CalculateService__get_asset_price(ticker)

    assert price == 0.0
    calculate_service_instance.cache_service.save.assert_called_once()


def test_setup_wallet_sucess(setup_wallet):
    """
    Testa a leitura dos dados e carregamento da carteira
    """
    assert len(setup_wallet.reits) == 1
    assert len(setup_wallet.stocks) == 1
    assert len(setup_wallet.others) == 1

