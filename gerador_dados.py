from faker import Faker
from random import choice,randint
from json import dumps

# Cria uma instância do Faker para o português do Brasil
fake = Faker('pt_BR')

# Lista para armazenar as pessoas fictícias
pessoas = []

# Loop para criar 100 pessoas fictícias
for c in range(100):
    primeiro_nome = fake.unique.first_name()
    ultimo_nome = fake.last_name()
    pessoas.append({
        "primeiro_nome": primeiro_nome,
        "ultimo_nome": ultimo_nome,
        "email": f"{primeiro_nome}.{ultimo_nome}@hotmail.com"
    })

#Lista de dicionários com os nome das categorias 
categorias = [{"nome": "Bebidas"},
              {"nome": "Comidas"},
              {"nome": "Eletrônicos"},
              {"nome": "Roupas"},
              {"nome": "Joia"}]

#Lista de produtos e preços associados a uma categoria por meio do "id_categoria"
produtos = [{"id_categoria":1,"nome":"Água","preco":8.00},
            {"id_categoria":1,"nome":"Refrigerante","preco":15.00},
            {"id_categoria":1,"nome":"Limonada","preco":20.00},
            {"id_categoria":1,"nome":"Suco","preco":5.00},
            {"id_categoria":1,"nome":"Agua c/ gas","preco":8.00},
            {"id_categoria":2,"nome":"Pao","preco":7.00},
            {"id_categoria":2,"nome":"Feijao","preco":9.00},
            {"id_categoria":2,"nome":"Leite","preco":5.00},
            {"id_categoria":2,"nome":"Sal","preco":3.00},
            {"id_categoria":2,"nome":"Macarrao","preco":8.00},
            {"id_categoria":3,"nome":"Celular","preco":2000.00},
            {"id_categoria":3,"nome":"Caixa de som","preco":250.00},
            {"id_categoria":3,"nome":"Tv","preco":3500.00},
            {"id_categoria":3,"nome":"Tablet","preco":8.00},
            {"id_categoria":3,"nome":"Computador","preco":12000.00},
            {"id_categoria":4,"nome":"Camiseta","preco":40.00},
            {"id_categoria":4,"nome":"Saia","preco":28.00},
            {"id_categoria":4,"nome":"Vestido","preco":58.00},
            {"id_categoria":4,"nome":"Casaco","preco":169.00},
            {"id_categoria":4,"nome":"Meias","preco":35.00},
            {"id_categoria":5,"nome":"Colar","preco":120.00},
            {"id_categoria":5,"nome":"Brincos","preco":110.00},
            {"id_categoria":5,"nome":"Pulseira","preco":115.00},
            {"id_categoria":5,"nome":"Anel de Ouro","preco":190.00},
            {"id_categoria":5,"nome":"Anel de Prata","preco":145.00}]

#Lista para armazenar as vendas
vendas = []

#Loop que que gera 1000 vendas fictícias contendo em um dicionário informações da pessoa que fez a compra,o produto e a quantidade.
for i in range(1000):
    vendas.append({"id_pessoa":pessoas.index(choice(pessoas))+1,
                   "id_produto":produtos.index(choice(produtos))+1,
                   "quantidade":randint(1,100)})

#Converte a estrutura de dados (para o formato de string json) e salva em um aquivo json 
with open("dados_db.json","w") as file:
    file.write(dumps({"pessoas": pessoas,
                      "categorias": categorias,
                      "produtos": produtos,
                      "vendas": vendas}))