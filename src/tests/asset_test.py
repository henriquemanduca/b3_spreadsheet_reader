import pytest
import pandas as pd


from src.calculate import read_operations


rows = [
    {
        'Entrada/Saída': 'Credito',
        'Data': '01/01/2024',
        'Produto': 'VGIR11 - VALORA CRI CDI FUNDO DE INVESTIMENTO IMOBILIÁRIO ',
        'Movimentação': 'Transferência - Liquidação',
        'Quantidade': 10,
        'Preço unitário': 5.60,
    },
    {
        'Entrada/Saída': 'Credito',
        'Data': '03/01/2024',
        'Produto': 'VGIR11 - VALORA CRI CDI FUNDO DE INVESTIMENTO IMOBILIÁRIO ',
        'Movimentação': 'Desdobro',
        'Quantidade': 90,
        'Preço unitário': '-',
    }
]


@pytest.fixture
def setup_data():
    return read_operations(pd.DataFrame(rows), None)


def test_asset_has_unfold(setup_data):
    asset = setup_data[0]
    assert asset.has_unfold() == True