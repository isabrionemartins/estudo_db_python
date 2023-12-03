from sqlalchemy import create_engine,text
from sqlalchemy_utils import database_exists, create_database
from json import loads
from pandas import read_sql

# Função para conexão com o banco postgresql e para executar os comandos
def executar_query_sql_sem_retorno(query):
   with engine.connect() as conn:
       conn.execute(text(query))
       conn.commit()

# Função para organizar e preprocessar os dados para inserir no banco
def preprocessar_dados_para_insert_sql(dados):
    return {
        "colunas": list(dados[0].keys()),
        "valores": criar_values_insert_sql(list(map(lambda dado: list(dado.values()),dados)))
    }

# Função para reestruturar os valores para o sql de insert 
def criar_values_insert_sql(valores):
    sql = []
    for linha in valores:
        lista_str = ""
        for coluna in linha:
            if not lista_str:
                lista_str += "("
            if isinstance(coluna,str):
                lista_str += f"'{coluna}',"
            else:
                lista_str += f"{coluna},"
        lista_str = lista_str[:-1] + ")"
        sql.append(lista_str)
    return sql

# Função para inserir os dados na tabela do banco 
def inserir_dados(tabela,dados):
    dados = preprocessar_dados_para_insert_sql(dados)
    executar_query_sql_sem_retorno(f"""INSERT INTO {tabela} ({", ".join(dados["colunas"])}) VALUES {", ".join(dados["valores"])}; """)

# Função para executar uma consulta no banco de dados com retorno 
def executar_query_sql_com_retorno(query):
    with engine.connect() as conn:
        return read_sql(query,conn)
    
# Detalhes da conexão
host = HOST_LOCAL
user = USER_LOCAL
password = PASSWORD_LOCAL
port = PORT_LOCAL
database = "estudo_db_postgre"
engine = create_engine(f"postgresql://{user}:{password}@{host}/{database}")

# Verifica se o banco de dados existe,caso não exista ele é criado
if not database_exists(engine.url):
    create_database(engine.url)

# Executa o comando de criação das tabelas se elas não existirem no banco de dados
#   Tabela "pessoas"
#       id : Chave primaria
#       primeiro_nome : string obrigatória
#       ultimo_nome : string obrigatória
#       email : string obrigatória
executar_query_sql_sem_retorno("""CREATE TABLE IF NOT EXISTS pessoas (
    id SERIAL PRIMARY KEY,
    primeiro_nome VARCHAR(255) NOT NULL,
    ultimo_nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL
);""")

#   Tabela "categorias"
#       id : Chave primaria
#       nome: string obrigatória
executar_query_sql_sem_retorno("""CREATE TABLE IF NOT EXISTS categorias(
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL
);""")

#   Tabela "produtos"
#       id : Chave primaria
#       id_categoria : chave estrangeira para tabela categorias
#       nome : string obrigatória
#       preco : float obrigatório
executar_query_sql_sem_retorno("""CREATE TABLE IF NOT EXISTS produtos(
    id SERIAL PRIMARY KEY,
    id_categoria INT NOT NULL,
    nome VARCHAR(255) NOT NULL,
    preco FLOAT NOT NULL,
    FOREIGN KEY(id_categoria) REFERENCES categorias(id)
);""")

#   Tabela "vendas"
#       id : Chave primaria
#       id_pessoa : chave estrangeira para tabela pessoas
#       id_produto : chave estrangeira para tabela produtos
#       quantidade : int obrigatória
executar_query_sql_sem_retorno("""CREATE TABLE IF NOT EXISTS vendas(
    id SERIAL PRIMARY KEY,
    id_pessoa INT NOT NULL,
    id_produto INT NOT NULL,
    quantidade INT NOT NULL,
    FOREIGN KEY(id_pessoa) REFERENCES pessoas(id),
    FOREIGN KEY(id_produto) REFERENCES produtos(id)
);""")

# Lê os dados do arquivo json e converte para os tipos nativos do Python 
with open("dados_db.json","r") as file:
    dados = loads(file.read())

# Insere os dados nas respectivas tabelas
inserir_dados("pessoas",dados["pessoas"])
inserir_dados("categorias",dados["categorias"])
inserir_dados("produtos",dados["produtos"])
inserir_dados("vendas",dados["vendas"])

# Cria backup das tabelas do banco no formato csv com separador "|"
executar_query_sql_com_retorno("SELECT * FROM pessoas").to_csv("bkp_postgres_pessoas.csv", sep = "|", index = False)
executar_query_sql_com_retorno("SELECT * FROM categorias").to_csv("bkp_postgres_categorias.csv", sep = "|", index = False)
executar_query_sql_com_retorno("SELECT * FROM produtos").to_csv("bkp_postgres_produtos.csv", sep = "|", index = False)
executar_query_sql_com_retorno("SELECT * FROM vendas").to_csv("bkp_postgres_vendas.csv", sep = "|", index = False)

# Gera um relatório de vendas com as informações dos produtos, pessoas e total. Salva o resultado num aquivo de formato csv com separador "|"
executar_query_sql_com_retorno("""SELECT 
    vendas.id,
    vendas.quantidade,
    pessoas.primeiro_nome,
    pessoas.ultimo_nome,
    pessoas.email,
    produtos.nome,
    produtos.preco,
    vendas.quantidade * produtos.preco as total
FROM
    vendas
        LEFT JOIN
    pessoas ON vendas.id_pessoa = pessoas.id
        LEFT JOIN
	produtos ON vendas.id_produto = produtos.id
""").to_csv("relatorio_postgres_vendas.csv", sep = "|", index = False)