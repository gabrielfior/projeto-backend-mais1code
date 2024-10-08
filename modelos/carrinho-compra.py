from sqlmodel import SQLModel, Field, Session, create_engine
from typing import Optional, List

# Definindo as tabelas do banco de dados
class Produto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    cor: str
    tamanho: str
    quantidade_disponivel: int
    preco: float

class CarrinhoItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    produto_id: int = Field(foreign_key="produto.id")
    quantidade: int
    preco_total: float

class Favorito(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    produto_id: int = Field(foreign_key="produto.id")

# Configurando o banco de dados SQLite
engine = create_engine("sqlite:///database.db")
SQLModel.metadata.create_all(engine)

class CarrinhoDeCompras:
    def __init__(self):
        # Inicializando a sessão com o banco e variáveis do carrinho
        self.session = Session(engine)
        self.itens: List[CarrinhoItem] = []
        self.total = 0.0
        self.desconto = 0.0
        self.frete = 0.0

    def adicionar_item(self, produto_id: int, quantidade: int):
        # Adicionando produto ao carrinho se houver estoque
        produto = self.session.get(Produto, produto_id)
        if produto and produto.quantidade_disponivel >= quantidade:
            preco_total = produto.preco * quantidade
            item = CarrinhoItem(produto_id=produto_id, quantidade=quantidade, preco_total=preco_total)
            self.itens.append(item)
            self.total += preco_total
            produto.quantidade_disponivel -= quantidade
            self.session.add(item)
            self.session.commit()
            print(f"{quantidade}x {produto.nome} adicionado.")
        else:
            print(f"Estoque insuficiente para {produto.nome}.")

    def remover_item(self, produto_id: int):
        # Removendo item do carrinho
        item_remover = next((item for item in self.itens if item.produto_id == produto_id), None)
        if item_remover:
            self.itens.remove(item_remover)
            self.total -= item_remover.preco_total
            produto = self.session.get(Produto, produto_id)
            produto.quantidade_disponivel += item_remover.quantidade
            self.session.delete(item_remover)
            self.session.commit()
            print("Item removido.")
        else:
            print("Item não encontrado.")

    def aplicar_cupom_desconto(self, desconto: float):
        # Aplicando desconto no total
        self.desconto = desconto
        print(f"Desconto de {desconto}% aplicado.")
        self.calcular_total()

    def calcular_total(self):
        # Calculando total com desconto
        total_com_desconto = self.total * ((100 - self.desconto) / 100)
        print(f"Total com desconto: R${total_com_desconto:.2f}")
        return total_com_desconto

    def calcular_frete(self, valor_frete: float):
        # Adicionando valor do frete
        self.frete = valor_frete
        print(f"Frete: R${valor_frete:.2f}")
        self.calcular_total_com_frete()

    def calcular_total_com_frete(self):
        # Calculando total com frete
        total_com_frete = self.calcular_total() + self.frete
        print(f"Total com frete: R${total_com_frete:.2f}")
        return total_com_frete

    def salvar_favorito(self, produto_id: int):
        # Salvando produto como favorito
        favorito = Favorito(produto_id=produto_id)
        self.session.add(favorito)
        self.session.commit()
        print("Produto favoritado.")

    def visualizar_carrinho(self):
        # Exibindo o carrinho
        print("\nCarrinho:")
        for item in self.itens:
            produto = self.session.get(Produto, item.produto_id)
            print(f"{item.quantidade}x {produto.nome} - Total: R${item.preco_total:.2f}")
        print(f"Total: R${self.total:.2f}\n")


# Função para adicionar produtos de exemplo
def adicionar_produto_exemplo():
    with Session(engine) as session:
        produto = Produto(nome="Camiseta", cor="Azul", tamanho="M", quantidade_disponivel=10, preco=50.0)
        session.add(produto)
        session.commit()

adicionar_produto_exemplo()

# Testando o carrinho
carrinho = CarrinhoDeCompras()
carrinho.adicionar_item(produto_id=1, quantidade=2)
carrinho.visualizar_carrinho()
carrinho.aplicar_cupom_desconto(desconto=10)
carrinho.calcular_frete(valor_frete=15.0)
carrinho.salvar_favorito(produto_id=1)
carrinho.remover_item(produto_id=1)
