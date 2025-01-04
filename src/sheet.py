from enum import Enum


class SheetColuns(Enum):
    FLOW = 'Entrada/Saída'
    DATE = 'Data'
    TYPE = 'Movimentação'
    NAME = 'Produto'
    QUANTITY = 'Quantidade'
    PRICE = 'Preço unitário'