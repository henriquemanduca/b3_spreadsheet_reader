import pytest
import pandas as pd

from src.calculate import read_operations
from src.asset import Asset


rows = [
    {
        'Entrada/Saída': 'Credito',
        'Data': '06/12/2024',
        'Produto': 'KNSC11 - KINEA SECURITIES FDO. DE INV. IMOB. - FII',
        'Movimentação': 'Transferência - Liquidação',
        'Quantidade': 100,
        'Preço unitário': 8.32,
    },
    {
        'Entrada/Saída': 'Debito',
        'Data': '21/12/2023',
        'Produto': 'KNSC11 - KINEA SECURITIES FUNDO DE INVESTIMENTO IMOBILIARIO - FII',
        'Movimentação': 'Transferência - Liquidação',
        'Quantidade': 220,
        'Preço unitário': 8.80,
    },
    {
        'Entrada/Saída': 'Credito',
        'Data': '07/11/2023',
        'Produto': 'KNSC11 - KINEA SECURITIES FUNDO DE INVESTIMENTO IMOBILIARIO - FII',
        'Movimentação': 'Desdobro',
        'Quantidade': 621,
        'Preço unitário': '-',
    },
    {
        'Entrada/Saída': 'Credito',
        'Data': '24/07/2023',
        'Produto': 'KNSC11 - KINEA SECURITIES FUNDO DE INVESTIMENTO IMOBILIARIO - FII',
        'Movimentação': 'Transferência - Liquidação',
        'Quantidade': 12,
        'Preço unitário': 86.42,
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
        'Data': '20/09/2021',
        'Produto': 'KNSC11 - KINEA SECURITIES FUNDO DE INVESTIMENTO IMOBILIARIO - FII',
        'Movimentação': 'Transferência - Liquidação',
        'Quantidade': 37,
        'Preço unitário': 100.08,
    }
]


@pytest.fixture
def setup_data():
    return read_operations(pd.DataFrame(rows), None)


def test_asset_has_unfold(setup_data):
    asset = setup_data[0]
    assert asset.has_unfold() == True


def test_asset_quantity(setup_data):
    asset: Asset = setup_data[0]
    assert asset.get_unfolds() == 621


def test_asset_properties(setup_data):
    asset: Asset = setup_data[0]
    assert asset.quantity == 570


def test_asset_set_unfold_factor(setup_data):
    asset: Asset = setup_data[0]
    data = { "date": "2023-09-26", "factor": 10 }
    assert asset.unfold_factor['factor'] == 10

    data = { "date": "2023-09-26", "factor": 20 }
    asset.set_unfold_factor(data)
    assert asset.unfold_factor['factor'] == 20