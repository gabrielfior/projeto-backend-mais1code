import sys
from decimal import Decimal
import datetime
sys.path.append("./modelos")

from modelos import Item, AvaliacaoItem, Vendedor, AvaliacaoVendedor
from sqlmodel import Field, Session, SQLModel, create_engine, select

def test_modelo():
    novo_item = Item(descricao = "sorvete", preco= Decimal(2.134))
    print(novo_item)
    assert novo_item

def test_modelo():
    novo_vendedor = Vendedor(nome = "Dilson", telefone = "55")
    print(novo_vendedor)
    assert novo_vendedor
            

def test_avaliacao_item():
    #criar um item
    #criar 2 avaliacoes do item
    #salvar no banco de dados
    #procurar item no banco de dados
    #ter certeza que tem 2 avaliacoes ligadas ao item
    novo_item = Item(descricao = "sorvete", cor = "azul", preco= Decimal(2.134), qtde_estoque = 50, imagem = "abc")
    #qtde_estoque: int
    #descricao: str 
    #imagem: str
    avaliacaoum = AvaliacaoItem(note = "12", imagem_url = "abc", 
    video_url = "url", comentario = "like", localizacao = "cep", criado_em = datetime.datetime.now())

    avaliacaodois = AvaliacaoItem(note = "12", imagem_url = "abc", video_url = "url", comentario = "like", localizacao = "cep", criado_em = datetime.datetime.now())
    engine = create_engine('sqlite://', echo=True)
    SQLModel.metadata.create_all(engine)

    
    with Session(engine) as session:
        session.add(novo_item)
        session.commit()
        avaliacaoum.item_id = novo_item.id
        avaliacaodois.item_id = novo_item.id
        session.add_all ([avaliacaoum, avaliacaodois])
        session.commit()
        
    with Session(engine) as session:
        item = session.exec(select(Item)).one()
        print ("avaliacoes", item.avaliacoes)

def test_avaliacao_vendedor():
    novo_vendedor = Vendedor(nome = "Dilson", email = "123", telefone = "55", pais = "BR", cidade = "ssa", estado = "ba")

    avaliacaovendum = AvaliacaoVendedor(nome = "ilson", imagem = "URL", comentario = "ABC", note = "12", criado_em = datetime.datetime.now())
    engine = create_engine('sqlite://', echo=True)
    SQLModel.metadata.create_all(engine)

  #id: int | None = Field(default=None, primary_key=True)
  #nome: str
  #email: str
  #telefone: int
  #pais: str
  #cidade: str
  #estado: str  
    with Session(engine) as session:
        session.add(novo_vendedor)
        session.commit()
        avaliacaovendum.vendedor_id = novo_vendedor.id
        session.add(avaliacaovendum)
        session.commit()
    
    with Session(engine) as session:
        vendedor = session.exec(select(Vendedor)).one()
        print ("avaliacoes", vendedor.avaliacoes)
    

  #imagem: str
  #comentario: str
  #nota: int
  #criado_em: datetime




