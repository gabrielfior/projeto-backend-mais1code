import sqlmodel
from sqlmodel import SQLModel, Field, Session


class Item(SQLModel, table=True):
  id: int | None = Field(default=None, primary_key=True)
  preco: float # ToDo - Mudar este tipo para Decimal (apenas 2 casas decimais)
  cor: str
  qtde_estoque: int
  descricao: str
  imagem: str
  ativo: bool = True
