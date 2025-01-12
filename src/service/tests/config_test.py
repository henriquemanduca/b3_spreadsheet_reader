import pytest
import json

from unittest.mock import mock_open, patch

from src.service.config_service import ConfigService, empty_config


@pytest.fixture
def mock_config_file():
    """
    Fixture para criar um arquivo de configuração mock.
    """
    config_data = {
        "skip": ["CIEL3"],
        "unfolds": {
            "VGIR11": { "date": "2023-09-26", "factor": 10 },
            "KNSC11": { "date": "2023-11-06", "factor": 10 }
        }
    }
    with patch("builtins.open", mock_open(read_data=json.dumps(config_data))) as mock_file:
        yield mock_file


def test_load_configuration_from_file_success(mock_config_file):
    """
    Testa o carregamento bem-sucedido da configuração do arquivo.
    """
    config_service = ConfigService()
    assert config_service._ConfigService__config == {
        "skip": ["CIEL3"],
        "unfolds": {
            "VGIR11": { "date": "2023-09-26", "factor": 10 },
            "KNSC11": { "date": "2023-11-06", "factor": 10 }
        }
    }


def test_load_configuration_from_file_file_not_found():
    """
    Testa o retorno da configuração quando o arquivo não existe.
    """
    with patch("os.path.exists", return_value=False):
        config_service = ConfigService()
        assert config_service._ConfigService__config == empty_config()


def test_load_configuration_from_file_json_decode_error():
    """
    Testa o retorno da configuração quando há um erro de JSON.
    """
    with patch("builtins.open", mock_open(read_data="invalid json")):
        config_service = ConfigService()
        assert config_service._ConfigService__config == empty_config()


def test_get_unfold_factor_success(mock_config_file):
    """
    Testa o retorno do fator de desdobramento.
    """
    config_service = ConfigService()
    assert config_service.get_unfold_factor("VGIR11") == {'date': '2023-09-26', 'factor': 10}


def test_get_unfold_factor_not_found(mock_config_file):
    """
    Testa a retorno do fator de desdobramento para ticker inválido.
    """
    config_service = ConfigService()
    assert config_service.get_unfold_factor("BBAS3") is None


def test_get_tickers_to_skip(mock_config_file):
    """
    Testa a retorno da lista de tickers ignorados.
    """
    config_service = ConfigService()
    assert config_service.get_tickers_to_skip() == ["CIEL3"]
