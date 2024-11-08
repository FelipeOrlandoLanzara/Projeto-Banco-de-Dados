from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

import json

with open ('./Wide-ColumnStore/acessCassandra.json','r') as file:
    config = json.load(file)


id_cliente = config['clientId']
secret = config['secret']
token = config['token']

auth_provider = PlainTextAuthProvider(id_cliente, secret)


session = Cluster(
    cloud={"secure_connect_bundle": "secure-connect-faculdade.zip"},
    auth_provider=PlainTextAuthProvider("token", token),
).connect()

session.set_keyspace('faculdade')  # Seleciona o keyspace

def criar_tabela(session):
    session.execute(
        """
        CREATE TABLE IF NOT EXISTS Aluno (
            ID_Aluno text,
            Nome_Aluno text,
            Idade_Aluno int,
            PRIMARY KEY (ID_Aluno)
        )
        """
        )
    session.execute(
        """
        INSERT INTO Aluno (ID_Aluno, Nome_Aluno, Idade_Aluno) VALUES ('24.122.049-0', 'Pedro', 20)
        """
        )
    print("Tabela criada com sucesso!")

def consultar_usuarios(session):
    rows = session.execute("SELECT ID_Aluno, Nome_Aluno, Idade_Aluno FROM Aluno")
    for row in rows:
        print(f"ID_Aluno: {row.id_aluno}, Nome_Aluno: {row.nome_aluno}, Idade_Aluno: {row.idade_aluno}")
        #print(row)

# Exemplo de consulta

# Fechando a conexão
criar_tabela(session)
consultar_usuarios(session)
session.shutdown()