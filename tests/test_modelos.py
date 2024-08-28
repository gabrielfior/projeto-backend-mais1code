import sys
from decimal import Decimal
import datetime
sys.path.append("./modelos")

from modelos import Item, AvaliacaoItem
from sqlmodel import Field, Session, SQLModel, create_engine, select
def test_modelo():
    novo_item = Item(descricao = "sorvete", preco= Decimal(2.134))
    print(novo_item)
    assert novo_item

def test_avaliacao_item():
    #criar um item
    #criar 2 avaliacoes do item
    #salvar no banco de dados
    #procurar item no banco de dados
    #ter certeza que tem 2 avaliacoes ligadas ao item
    novo_item = Item(descricao = "sorvete", cor = "azul", preco= Decimal(2.134), qtde_estoque = 50, imagem = "abr")
    #qtde_estoque: int
    #descricao: str 
    #imagem: str
    avaliacaoum = AvaliacaoItem(nota = "12", imagem_url = "abc", 
    video_url = "url", comentario = "like", note = "numeros", localizacao = "cep", criado_em = datetime.datetime.now())

    avaliacaodois = AvaliacaoItem(nota = "12", imagem_url = "abc", video_url = "url", comentario = "like", note = "numeros", localizacao = "cep", criado_em = datetime.datetime.now())
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


    




