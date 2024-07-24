import sys
from decimal import Decimal
sys.path.append("./modelos")

from modelos import Item
def test_modelo():
    novo_item = Item(descricao = "sorvete", preco= Decimal(2.134))
    print(novo_item)
    assert novo_item