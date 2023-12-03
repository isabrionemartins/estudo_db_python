import pymongo 
from json import loads,dumps

# Detalhes da conexão
host = HOST_LOCAL
port = PORT_LOCAL

# Criação da conexão com o banco mongodb
conector = pymongo.MongoClient(host,port)

# Criação da referência ao banco "estudo_mongodb"
database = conector["estudo_mongodb"]

# Criação da referência para as collections
pessoas = database["pessoas"]
categorias = database["categorias"]
produtos = database["produtos"]
vendas = database["vendas"]

# Lê os dados do arquivo json e converte para os tipos nativos do Python 
with open("dados_db.json","r") as file:
    dados = loads(file.read())

# Insere os dados nas respectivas collections
pessoas.insert_many(dados["pessoas"])
categorias.insert_many(dados["categorias"])
produtos.insert_many(dados["produtos"])
vendas.insert_many(dados["vendas"])

# Cria backup das collections do banco no formato json com a conversão dos tipos de dados para string 
with open("bkp_mongodb_pessoas.json","w") as file:
    file.write(dumps(list(pessoas.find({})), default = str))
with open("bkp_mongodb_categorias.json","w") as file:
    file.write(dumps(list(categorias.find({})), default = str))
with open("bkp_mongodb_produtos.json","w") as file:
    file.write(dumps(list(produtos.find({})), default = str))
with open("bkp_mongodb_vendas.json","w") as file:
    file.write(dumps(list(vendas.find({})), default = str))