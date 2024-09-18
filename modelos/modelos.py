from datetime import datetime
from decimal import Decimal

from sqlmodel import Relationship
from sqlmodel import SQLModel, Field


class Item(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    preco: Decimal = Field(max_digits=6, decimal_places=2)
    cor: str
    qtde_estoque: int
    descricao: str
    imagem: str
    ativo: bool = True

    avaliacoes: list["AvaliacaoItem"] = Relationship(back_populates="item")


class Pessoa(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    email: str
    telefone: int
    pais: str
    cidade: str
    estado: str
    ativo: bool = True


class Vendedor(Pessoa, table=True):
    id: int | None = Field(default=None, primary_key=True)
    avaliacoes: list["AvaliacaoVendedor"] = Relationship(back_populates="vendedor")


class AvaliacaoVendedor(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    imagem: str
    comentario: str
    nota: int
    criado_em: datetime

    vendedor_id: int | None = Field(default=None, foreign_key="vendedor.id")
    vendedor: Vendedor | None = Relationship(back_populates="avaliacoes")


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


class Usuario(Pessoa, table=True):
    id: int | None = Field(default=None, primary_key=True)
