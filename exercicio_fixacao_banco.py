from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from pymongo import MongoClient
import datetime
import pprint

Base = declarative_base()


class Cliente(Base):
    __tablename__ = "cliente"
    id = Column(Integer, primary_key=True, autoincrement=True)
    Nome = Column(String(50))
    cpf = Column(String(13))
    endereço = Column(String(50))

    address = relationship(
        "Conta", back_populates="id_cliente", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Cliente(id={self.id}, Nome={self.Nome}, fullname={self.cpf}, endereço={self.endereço})"


class Conta(Base):
    __tablename__ = "conta"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo = Column(String(30))
    agencia = Column(String(10))
    num = Column(Integer)
    id_cliente = Column(Integer, ForeignKey("cliente.id"), nullable=False)
    saldo = Column(Integer)

    user = relationship(
        "Cliente", back_populates="conta"
    )

    def __repr__(self):
        return f"Conta(id={self.id}, tipo={self.tipo}, agencia={self.agencia}, num={self.num}, id_cliente={self.id_cliente}, saldo={self.saldo})"


variavel = MongoClient(
    "mongodb+srv://pymongoUser:oIG4Zj0l4tWpsqBb@cluster0.jluu6k1.mongodb.net/?retryWrites=true&w=majority")

db = variavel.ttst
collection = db.ttst_collection
print(db.list_collection_names)

# definicao de informacao para compor o documento
post = {
    "id": "1",
    "Nome": "Felipe Gusmao",
    "cpf": "00055533344",
    "endereço": "alameda feliz 345",
    "tipo": "conta corrente",
    "agencia": "0001",
    "num": "10000003",
    "saldo": "3200"
}

# preparando para submeter as infos
posts = db.posts
post_id = posts.insert_one(post).inserted_id
print(post_id)

# print(db.posts.find_one())
pprint.pprint(db.posts.find_one())

# bulk inserts
new_posts = [{
    "id": "2",
    "Nome": "Marcos Almeida",
    "cpf": "11122233344",
    "endereço": "rua dos girassois 300",
    "tipo": "conta corrente",
    "agencia": "0001",
    "num": "10000001",
    "saldo": "1000"

},
    {
    "id": "3",
    "Nome": "Ana Serra",
    "cpf": "44422200055",
    "endereço": "avenida principal 1300",
    "tipo": "conta corrente",
    "agencia": "0001",
    "num": "10000002",
    "saldo": "5000"
}]

result = posts.insert_many(new_posts)
print(result.inserted_ids)

print("\nRecuperação Final")
pprint.pprint(db.posts.find_one({"Nome": "Marcos Almeida"}))
pprint.pprint(db.posts.find_one({"cpf": "44422200055"}))
pprint.pprint(db.posts.find_one({"endereço": "alameda feliz 345"}))
