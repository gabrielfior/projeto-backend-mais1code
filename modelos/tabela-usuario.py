  import sqlmodel
  from sqlmodel import SQLModel, Field, Session
  from decimal import Decimal
  from datetime import datetime
  from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select


  class Usuario(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    email: str
    telefone: int
    pais: str
    cidade: str
    estado: str
    ativo: bool = True
    senha: str
    