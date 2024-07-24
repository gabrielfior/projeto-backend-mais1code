import sqlmodel
from sqlmodel import SQLModel, Field, Session
from decimal import Decimal


class Item(SQLModel, table=True):
  id: int | None = Field(default=None, primary_key=True)
  preco: Decimal = Field(max_digits=6, decimal_places=2)
  cor: str
  qtde_estoque: int
  descricao: str
  imagem: str
  ativo: bool = True
