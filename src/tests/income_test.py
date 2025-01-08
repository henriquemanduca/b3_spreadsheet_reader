from src.models.income import create_income
from src.models.movement import OperationType


def test_create_income():
    row = {
        'Data': '18/01/2024',
        'Quantidade': 2,
        'Preço unitário': 5.60,
    }
    income = create_income(row)

    assert income.operation == OperationType.INCOME