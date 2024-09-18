from sqlmodel import SQLModel, Field, Relationship, Session, create_engine, select
from decimal import Decimal
from datetime import datetime

class Usuario(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    email: str
    telefone: str
    pais: str
    cidade: str
    estado: str
    ativo: bool = True
    senha: str
