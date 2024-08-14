import sqlmodel
from sqlmodel import SQLModel, Field, Session
from decimal import Decimal
from datetime import datetime
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select


class Item(SQLModel, table=True):
  id: int | None = Field(default=None, primary_key=True)
  preco: Decimal = Field(max_digits=6, decimal_places=2)
  cor: str
  qtde_estoque: int
  descricao: str
  imagem: str
  ativo: bool = True
  
  avaliacoes: list["AvaliacaoItem"] = Relationship(back_populates="item")
  

class Vendedor(SQLModel, table=True):
  id: int | None = Field(default=None, primary_key=True)
  nome: str
  email: str
  telefone: int
  pais: str
  cidade: str
  estado: str
  ativo: bool = True

class AvaliacaoVendedor(SQLModel, table=True):
  id: int | None = Field(default=None, primary_key=True)
  imagem: str
  comentario: str
  nota: int
  criado_em: datetime

class AvaliacaoItem(SQLModel, table=True):
  id: int | None = Field(default=None, primary_key=True)
  imagem_url: str
  video_url: str
  comentario: str
  nota: int
  localizacao: str
  criado_em: datetime

  item_id: int | None = Field(default=None, foreign_key="item.id")
  item: Item | None = Relationship(back_populates="avaliacoes")

