from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import random
from faker import Faker
import json


# ----- CONECTANDO COM O BANCO -----

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


# ----- CRIANDO TODOS OS DADOS ALEATÓRIOS -----

# Criacao da instância do Faker para pt-br
fake = Faker('pt-br')

# Criação das variáveis que serão usadas nas tabelas - serão gerados números aleatórios e sem repetição
ra_aluno = random.sample(range(100000000, 500000000), 60)
ra_professor = random.sample(range(500000001, 999999999), 20)
lista_materias = [num for num in random.sample(range(100000, 999999), 60)]

# Gera aleatoriamente e sem repetir a lista de historico escolar dos alunos (60)
lista_hist_escolar = [num for num in random.sample(range(1, 500000), 60)]
# Gera aleatoriamente e sem repetir a lista do historico dos professores (60)
lista_hist_professor = [num for num in random.sample(range(500001, 999999), 60)]

# Arrumando a formatação dos RAs de aluno e professor
ra_aluno_formatado = []
ra_professor_formatado = []
for i in ra_aluno:
    ra_aluno_formatado.append(f"{str(i)[:2]}.{str(i)[2:5]}.{str(i)[5:8]}-{str(i)[8]}")
for i in ra_professor:
    ra_professor_formatado.append(f"{str(i)[:2]}.{str(i)[2:5]}.{str(i)[5:8]}-{str(i)[8]}")

# Valores chaves de variáveis para quando for criar valores ficticios
primary_keys = {
    "nome_departamento" : ["Matemática", "Física", "Ciência da Computação", "Engenharia Elétrica", "Engenharia Mecânica"],
    "id_curso" : ['MA', 'FI', 'CC', 'EE', 'EM'],
    "nome_materia": ["Calculo 1", "Calculo 2", "Calculo 3", "Calculo 4", "Probabilidade e Estatística", "Desenvolvimento de Projetos", "Introdução a Computação"]
}
semestre = ["Primeiro", "Segundo", "Terceiro", "Quarto", "Quinto", "Sexto", "Setimo", "Oitavo"]

# Cria um dicionário de ids de curso, onde cada id que vai representar um nome de dapartamento
cursos_ids = {
    'MA': 'Matemática',
    'FI': 'Física',
    'CC': 'Ciência da Computação',
    'EE': 'Engenharia Elétrica',
    'EM': 'Engenharia Mecânica'
}

# Cria um dicionario de ids de materias, onde cada id que vai referenciar uma materia - assim podemos ter varios alunos fazendo aquela mesma materia (com mesmo id, logo mesma sala de aula)
materias_ids = {}
for i in lista_materias:
    materias_ids[i] = primary_keys['nome_materia'][random.randint(0,4)]


# ----- DROP DAS TABELAS -----

# Drop da Tabela Aluno
def deletaAluno(session):
    session.execute(
        """
        DROP TABLE Aluno;
        """
    )

# Drop da Tabela Historico Escolar
def deletaHistoricoEscolar(session):
    session.execute(
        """
        DROP TABLE HistoricoEscolar;
        """
    )

# Drop da Tabela Materia
def deletaMateria(session):
    session.execute(
        """
        DROP TABLE Materia;
        """
    )

# Drop da Tabela Professor
def deletaProfessor(session):
    session.execute(
        """
        DROP TABLE Professor;
        """
    )

# Drop da Tabela Historico Professor
def deletaHistoricoProfessor(session):
    session.execute(
        """
        DROP TABLE HistoricoProfessor;
        """
    )

# Drop da Tabela Curso
def deletaCurso(session):
    session.execute(
        """
        DROP TABLE Curso;
        """
    )

# Drop da Tabela Departamento
def deletaDepartamento(session):
    session.execute(
        """
        DROP TABLE Departamento;
        """
    )

# Drop da Tabela TCC
def deletaTCC(session):
    session.execute(
        """
        DROP TABLE TCC;
        """
    )


# ----- CRIANDO AS TABELAS -----

# Criação da Tabela Alunos
def criaAluno(session):
    session.execute(
        """
        CREATE TABLE IF NOT EXISTS Aluno (
            ID_Aluno text,
            Nome_Aluno text,
            Idade_Aluno int,
            Nome_Curso text,
            ID_Curso text,
            Semestre text,
            Ano int,
            Nota float,
            PRIMARY KEY (ID_Aluno)
        )
        """
        )
    for ra in ra_aluno_formatado:
        curso_aleatorio = primary_keys["id_curso"][random.randint(0, 4)] # Pega um nome de curso aleatório
        dados_aluno = {
            'ID_Aluno': ra,
            'Nome_Aluno': fake.first_name(),
            'Idade_Aluno': random.randint(18, 65),
            'Nome_Curso': curso_aleatorio,
            'ID_Curso': cursos_ids[curso_aleatorio],
            'Semestre': random.choice(semestre),
            'Ano': 2020,
            'Nota': round(random.uniform(0.0,10.0),2)
        }
        session.execute(
            """
            INSERT INTO Aluno (ID_Aluno, Nome_Aluno, Idade_Aluno, Nome_Curso, ID_Curso, Semestre, Ano, Nota) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            tuple(dados_aluno.values())
        )

def consultar_aluno(session):
    rows = session.execute("SELECT ID_Aluno, Nome_Aluno, Idade_Aluno, Nome_Curso, ID_Curso, Semestre, Ano, Nota FROM Aluno")
    for row in rows:
        #print(f"ID_Aluno: {row.id_aluno}, Nome_Aluno: {row.nome_aluno}, Idade_Aluno: {row.idade_aluno}")
        print(row)

        


# Criação da Tabela Histórico Escolar
def criaHistoricoEscolar(session):
    session.execute(
        """
        CREATE TABLE IF NOT EXISTS HistoricoEscolar (
            ID_HistoricoEscolar int,
            Semestre text,
            Ano int,
            Nota float,
            Nome_Aluno text,
            ID_Materia int,
            Nome_Materia text,
            PRIMARY KEY (ID_HistoricoEscolar)
        )
        """
    )
    # for id_he in lista_hist_escolar:
    #     chave = random.choice(list(materias_ids.keys())) # Pega uma chave aleatoria
    #     dados_historico_escolar = {
    #         'ID_HistoricoEscolar': id_he,
    #         'Semestre': random.choice(semestre),
    #         'Ano': 2020,
    #         'Nota': round(random.uniform(0.0,10.0),2),
    #         'Nome_Aluno': fake.first_name(),
    #         'ID_Materia': chave,
    #         'Nome_Materia' : materias_ids[chave]
    #     }
    #     session.execute(
    #         """
    #         INSERT INTO HistoricoEscolar (ID_HistoricoEscolar, Semestre, Ano, Nota, Nome_Aluno, ID_Materia, Nome_Materia)
    #         VALUES (%s, %s, %s, %s, %s, %s, %s)
    #         """,
    #         tuple(dados_historico_escolar.values())
    #     )

# def consultar_historico_escolar(session):
#     rows = session.execute("SELECT ID_HistoricoEscolar, Semestre, Ano, Nota, Nome_Aluno, ID_Materia, Nome_Materia FROM HistoricoEscolar")
#     for row in rows:
#         #print(f"ID_Aluno: {row.id_aluno}, Nome_Aluno: {row.nome_aluno}, Idade_Aluno: {row.idade_aluno}")
#         print(row)

    
# Criação da Tabela Matéria
def criaMateria(session):
    session.execute(
        """
        CREATE TABLE IF NOT EXISTS Materia (
            ID_Materia text,
            Nome_Materia text,
            Prova boolean,
            PRIMARY KEY (ID_MATERIA)
        )
        """
    )

# Criação da Tabela Professor
def criaProfessor(session):
    session.execute(
        """
        CREATE TABLE IF NOT EXISTS Professor (
            ID_Professor text,
            Nome_Professor text,
            Salario int,
            PRIMARY KEY (ID_Professor)
        )
        """
    )

# Criação da Tabela Histórico Professor
def criaHistoricoProfessor(session):
    session.execute(
        """
        CREATE TABLE IF NOT EXISTS HistoricoProfessor (
            ID_HistoricoProfessor text,
            Semestre text,
            Ano text,
            Quantidade_Aulas int,
            Nome_Professor text,
            ID_Materia text,
            Nome_Materia text,
            PRIMARY KEY (ID_HistoricoProfessor)
        )
        """
    )

# Criação da Tabela Curso
def criaCurso(session):
    session.execute(
        """
        CREATE TABLE IF NOT EXISTS Curso (
            ID_Curso text,
            Nome_Curso text,
            Horas_Extras int,
            PRIMARY KEY (ID_Curso)
        )
        """
    )

# Criação da Tabela Departamento
def criaDepartamento(session):
    session.execute(
        """
        CREATE TABLE IF NOT EXISTS Departamento (
            Nome_Departamento text,
            Chefe_Departamento text,
            PRIMARY KEY (Nome_Departamento)
        )
        """
    )

# Criação da Tabela TCC
def criaTCC(session):
    session.execute(
        """
        CREATE TABLE IF NOT EXISTS TCC (
            ID_TCC int,
            Titulo text,
            Nome_Aluno text,
            Nome_Professor text,
            PRIMARY KEY (ID_TCC)
        )
        """
    )



# Exemplo de consulta

# Fechando a conexão
        
# ----- CHAMANDO AS FUNÇÕES -----
deletaAluno(session)
deletaHistoricoEscolar(session)
deletaMateria(session)
deletaProfessor(session)
deletaHistoricoProfessor(session)
deletaCurso(session)
deletaDepartamento(session)
deletaTCC(session)
# Funções para a criação da Tabelas
criaAluno(session)
criaHistoricoEscolar(session)
criaMateria(session)
criaProfessor(session)
criaHistoricoProfessor(session)
criaCurso(session)
criaDepartamento(session)
criaTCC(session)
#Funções para consultar tabelas
consultar_aluno(session)
consultar_historico_escolar(session)
session.shutdown()
