import pytest

from datetime import date, datetime

from src.models.movement import Movement, OperationType, movement_factory


@pytest.fixture
def setup_data():
    return {
        'Entrada/Saída': 'Credito',
        'Data': '20/09/2021',
        'Produto': 'KNSC11 - KINEA SECURITIES - FII',
        'Movimentação': 'Transferência - Liquidação',
        'Quantidade': 10
    }


def test_movement_default_creation():
    """
    Testa a criação de Movimento com valores padrão
    """
    movement = Movement()
    assert movement.operation_date is None
    assert movement.operation == OperationType.INCOME
    assert movement.quantity == 0


def test_movement_custom_creation():
    """
    Testa a criação de Movimento com valores personalizados
    """
    today = date.today()
    movement = Movement(
        operation_date=today,
        operation=OperationType.BUY,
        quantity=100
    )
    assert movement.operation_date == today
    assert movement.operation == OperationType.BUY
    assert movement.quantity == 100


def test_movement_creation_with_none_quantity():
    """
    Testa criação de Movimento com quantidade None
    """
    movement = Movement(quantity=None)
    assert movement.quantity == 0


def test_movement_invalid_operation_creation():
    """
    Testa criação de Movimento com operação inválida
    """
    with pytest.raises(TypeError, match='Operation must be a OperationType'):
        Movement(operation='INVALID')


def test_movement_invalid_quantity_creation():
    """
    Testa criação de Movimento com quantidade inválida
    """
    with pytest.raises(TypeError, match='Quantity must be a int'):
         Movement(quantity='50')


def test_movement_create_method():
    """
    Testa o método de fábrica  de Movimentos
    """
    movement = Movement.create(
        date=date.today(),
        operation=OperationType.SELL,
        quantity=75
    )
    assert isinstance(movement, Movement)
    assert movement.operation == OperationType.SELL


def test_movement_factory_success(setup_data):
    """
    Testa função fabrica de Movimentos
    """
    movement = movement_factory(data_row=setup_data)

    assert isinstance(movement.operation_date, date)
    assert movement.operation_date == datetime(2021, 9, 20)
    assert movement.operation == OperationType.UNFOLD
    assert movement.quantity == 10


def test_movement_factory_fail_date(setup_data):
    """
    Testa função fabrica de Movimentos
    """
    setup_data['Data'] = '2024'
    with pytest.raises(ValueError, match='Error on convert operation date'):
        movement_factory(data_row=setup_data)
