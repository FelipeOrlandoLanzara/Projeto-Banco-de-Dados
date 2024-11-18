from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import random
from faker import Faker
import json


# cassandra-driver
# ----- CONECTANDO COM O BANCO DATASTAX -----

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
lista_hist_professor = [num for num in random.sample(range(500001, 999999), 20)]

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


# ----- CRIAÇÃO DOS DICIONÁRIOS -----

# Cria um dicionario de ids de materias, onde cada id que vai referenciar uma materia - assim podemos ter varios alunos fazendo aquela mesma materia (com mesmo id, logo mesma sala de aula)
materias_ids = {}
for i in lista_materias:
    materias_ids[i] = primary_keys['nome_materia'][random.randint(0,4)]

# Sequência de dicionários criados pois muitos dados se repetem nas Tabelas, e logo, devem ser iguais

# Cria um dicionário com chave de RA e valor sendo o seu nome
professor_ids = {}
for i in ra_professor_formatado:
    professor_ids[i] = fake.first_name() #o valor de dentro do dicionário será o nome específico ao professor

# Cria um dicionário com chave sendo o RA e o valor sendo seu nome
aluno_ids = {}
lista_alunos = [] # Lista para armazenar todos os nomes do Alunos
for i in ra_aluno_formatado:
    student = fake.first_name()
    aluno_ids[i] = student # O valor de dentro do dicionário será o nome específico ao aluno
    lista_alunos.append(student)

# Cria um dicionário onde cada aluno vai ter a sua própria nota e semestre
students = {}
for aluno in lista_alunos:
    students[aluno] = { # A chave é o nome do aluno
        'nota': round(random.uniform(0.0,10.0),2),
        'semestre': random.choice(semestre)
    }

# Cria um dicionário onde o nome do departamento é chave o o nome do chefe é o valor
departamentos = {}
for departamento in primary_keys["nome_departamento"]:
    departamentos[departamento] = fake.first_name()


# ----- DROP DAS TABELAS -----

# Drop da Tabela Aluno
def deletaAluno(session):
    session.execute(
        """
        DROP TABLE IF EXISTS Aluno;
        """
    )

# Drop da Tabela Historico Escolar
def deletaHistoricoEscolar(session):
    session.execute(
        """
        DROP TABLE IF EXISTS HistoricoEscolar;
        """
    )

# Drop da Tabela Materia
def deletaMateria(session):
    session.execute(
        """
        DROP TABLE IF EXISTS Materia;
        """
    )

# Drop da Tabela Professor
def deletaProfessor(session):
    session.execute(
        """
        DROP TABLE IF EXISTS Professor;
        """
    )

# Drop da Tabela Historico Professor
def deletaHistoricoProfessor(session):
    session.execute(
        """
        DROP TABLE IF EXISTS HistoricoProfessor;
        """
    )

# Drop da Tabela Curso
def deletaCurso(session):
    session.execute(
        """
        DROP TABLE IF EXISTS Curso;
        """
    )

# Drop da Tabela Departamento
def deletaDepartamento(session):
    session.execute(
        """
        DROP TABLE IF EXISTS Departamento;
        """
    )

# Drop da Tabela TCC
def deletaTCC(session):
    session.execute(
        """
        DROP TABLE IF EXISTS TCC;
        """
    )


# ----- CRIAÇÃO DAS TABELAS -----

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
            PRIMARY KEY (ID_Aluno, Nome_Aluno, Idade_Aluno)
        )
        """
        )
    for ra in ra_aluno_formatado:
        curso_aleatorio = primary_keys["id_curso"][random.randint(0, 4)] # Pega um nome de curso aleatório
        dados_aluno = {
            'ID_Aluno': ra,
            'Nome_Aluno': aluno_ids[ra],
            'Idade_Aluno': random.randint(18, 65),
            'Nome_Curso': curso_aleatorio,
            'ID_Curso': cursos_ids[curso_aleatorio],
            'Semestre': students[aluno_ids[ra]]['semestre'],
            'Ano': 2020,
            'Nota': students[aluno_ids[ra]]['nota']
        }
        session.execute(
            """
            INSERT INTO Aluno (ID_Aluno, Nome_Aluno, Idade_Aluno, Nome_Curso, ID_Curso, Semestre, Ano, Nota) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            tuple(dados_aluno.values())
        )

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
            PRIMARY KEY (ID_HistoricoEscolar, Semestre, Ano, Nota)
        )
        """
    )
    for id_he, ra in zip(lista_hist_escolar, ra_aluno_formatado):
        chave = random.choice(list(materias_ids.keys())) # Pega uma chave aleatoria
        dados_historico_escolar = {
            'ID_HistoricoEscolar': id_he,
            'Semestre': students[aluno_ids[ra]]['semestre'],
            'Ano': 2020,
            'Nota': students[aluno_ids[ra]]['nota'],
            'Nome_Aluno': aluno_ids[ra],
            'ID_Materia': chave,
            'Nome_Materia' : materias_ids[chave]
        }
        session.execute(
            """
            INSERT INTO HistoricoEscolar (ID_HistoricoEscolar, Semestre, Ano, Nota, Nome_Aluno, ID_Materia, Nome_Materia)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            tuple(dados_historico_escolar.values())
        )
    
# Criação da Tabela Matéria
def criaMateria(session):
    session.execute(
        """
        CREATE TABLE IF NOT EXISTS Materia (
            ID_Materia int,
            Nome_Materia text,
            Prova boolean,
            PRIMARY KEY (ID_Materia, Nome_Materia, Prova)
        )
        """
    )
    for id in lista_materias:
        dados_materia = {
            'ID_Materia': id,
            'Nome_Materia': materias_ids[id],
            'Prova': fake.pybool()
        }
        session.execute(
            """
            INSERT INTO Materia (ID_Materia, Nome_Materia, Prova)
            VALUES (%s, %s, %s)
            """,
            tuple(dados_materia.values())
        )

# Criação da Tabela Professor
def criaProfessor(session):
    session.execute(
        """
        CREATE TABLE IF NOT EXISTS Professor (
            ID_Professor text,
            Nome_Professor text,
            Salario int,
            Nome_Departamento text,
            Chefe_Departamento text,
            PRIMARY KEY (ID_Professor, Nome_Professor, Salario)
        )
        """
    )
    for id in ra_professor_formatado:
        random_departamento = random.choice(primary_keys['nome_departamento'])
        dados_professor = {
            'ID_Professor': id,
            'Nome_Professor': professor_ids[id],
            'Salario': random.randint(2000, 20000),
            'Nome_Departamento': random_departamento,
            'Chefe_Departamento': departamentos[random_departamento] # Nome do Chefe de Departamento
        }
        session.execute(
            """
            INSERT INTO Professor (ID_Professor, Nome_Professor, Salario , Nome_Departamento, Chefe_Departamento)
            VALUES (%s, %s, %s, %s, %s)
            """,
            tuple(dados_professor.values())
        )
    session.execute(
        """
        INSERT INTO Professor (ID_Professor, Nome_Professor, Salario , Nome_Departamento, Chefe_Departamento)
        VALUES (%s, %s, %s, %s, %s)
        """,
        ('24.122.049-0', 'Julia', 22000, 'Engenharia de Produção', 'Julia')
    )

# Criação da Tabela Histórico Professor
def criaHistoricoProfessor(session):
    session.execute(
        """
        CREATE TABLE IF NOT EXISTS HistoricoProfessor (
            ID_HistoricoProfessor int,
            Semestre text,
            Ano int,
            Quantidade_Aulas int,
            Nome_Professor text,
            ID_Materia int,
            Nome_Materia text,
            PRIMARY KEY (ID_HistoricoProfessor, Semestre, Ano, Quantidade_Aulas)
        )
        """
    )
    for id_hist, id_prof in zip(lista_hist_professor, ra_professor_formatado):
        chave = random.choice(list(materias_ids.keys())) # Pega uma chave aleatoria
        dados_historico_professor = {
            'ID_HistoricoProfessor': id_hist,
            'Semestre': random.choice(semestre),
            'Ano': 2020,
            'Quantidade_Aulas': random.randint(1, 100),
            'Nome_Professor': professor_ids[id_prof],
            'ID_Materia': chave,
            'Nome_Materia': materias_ids[chave]
        }
        session.execute(
            """
            INSERT INTO HistoricoProfessor (ID_HistoricoProfessor, Semestre, Ano, Quantidade_Aulas, Nome_Professor, ID_Materia, Nome_Materia)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            tuple(dados_historico_professor.values())
        )

# Criação da Tabela Curso
def criaCurso(session):
    session.execute(
        """
        CREATE TABLE IF NOT EXISTS Curso (
            ID_Curso text,
            Nome_Curso text,
            Horas_Extras int,
            PRIMARY KEY (ID_Curso, Nome_Curso, Horas_Extras)
        )
        """
    )
    for id in primary_keys["id_curso"]:
        dados_curso = {
            'ID_Curso': id,
            'Nome_Curso': cursos_ids[id],
            'Horas_Extras': random.randint(120, 360) 
        }
        session.execute(
            """
            INSERT INTO Curso (ID_Curso, Nome_Curso, Horas_Extras)
            VALUES (%s , %s , %s)
            """,
            tuple(dados_curso.values())
        )

# Criação da Tabela Departamento
def criaDepartamento(session):
    session.execute(
        """
        CREATE TABLE IF NOT EXISTS Departamento (
            Nome_Departamento text,
            Chefe_Departamento text,
            PRIMARY KEY (Nome_Departamento, Chefe_Departamento)
        )
        """
    )
    for name in primary_keys["nome_departamento"]:
        dados_departamento = {
            'Nome_Departamento': name,
            'Chefe_Departamento': departamentos[name]
        }
        session.execute(
            """
            INSERT INTO Departamento (Nome_Departamento, Chefe_Departamento)
            VALUES (%s, %s)
            """,
            tuple(dados_departamento.values())
        )
    session.execute(
        """
        INSERT INTO Departamento (Nome_Departamento, Chefe_Departamento)
        VALUES (%s, %s)
        """,
        ('Engenharia de Produção', 'Julia')
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
            PRIMARY KEY (ID_TCC, Titulo)
        )
        """
    )
    for i, ra_aluno in enumerate(ra_aluno_formatado):
        random_professor = random.choice(ra_professor_formatado) # Pega um ra aleatório de Professor -> mesmo professor pode dar tcc para mais de um aluno
        dados_tcc = {
            'ID_TCC': i, 
            'Titulo': "Título " + str(i),
            'Nome_Aluno': aluno_ids[ra_aluno],
            'Nome_Professor': professor_ids[random_professor]
        }
        session.execute(
            """
            INSERT INTO TCC (ID_TCC, Titulo, Nome_Aluno, Nome_Professor)
            VALUES (%s, %s, %s, %s)
            """,
            tuple(dados_tcc.values())
        )


# ----- RESOLUÇÃO DAS QUERIES -----

# 1- Histórico escolar de qualquer aluno, retornando o código e nome da disciplina, semestre e ano que a disciplina foi cursada e nota final
def query1(session):
    query1 = session.execute(
        """
        SELECT Nome_Aluno, ID_Materia, Nome_Materia, Semestre, Ano, Nota
        FROM HistoricoEscolar
        """
    ).one() # Para pegar apenas um
    if query1:
        print(f'Nome do Aluno: {query1.nome_aluno}, ID da Matéria: {query1.id_materia}, Nome da Matéria: {query1.nome_materia}, Semestre: {query1.semestre}, Ano: {query1.ano}, Nota: {query1.nota:.2f}')

# 2- Histórico de disciplinas ministradas por qualquer professor, com semestre e ano
def query2(session):
    query2 = session.execute(
        """
        SELECT Nome_Professor, Nome_Materia, ID_Materia, Semestre, Ano
        FROM HistoricoProfessor
        """
    ).one()
    if query2:
        print(f'Nome do Professor: {query2.nome_professor}, Nome da Matéria: {query2.nome_materia}, ID da Matéria: {query2.id_materia}, Semestre: {query2.semestre}, Ano: {query2.ano}')

# 3- Listar alunos que já se formaram (foram aprovados em todos os cursos de uma matriz curricular) em um determinado semestre de um ano
def query3(session):
    numero_aleatorio = random.randint(0, 7) # Pega um número aleatório para buscar na lista Semestre
    semestre_aleatorio = semestre[numero_aleatorio]
    query3 = session.execute(
        """
        SELECT Nome_Aluno, Nome_Curso, ID_Curso, Semestre, Ano, Nota
        FROM Aluno
        WHERE Nota > %s AND Semestre = %s AND Ano = %s ALLOW FILTERING
        """,
        (5, semestre_aleatorio, 2020)
    )
    if query3:
        for elemento in query3:
            print(f'Nome do Aluno: {elemento.nome_aluno}, Nome do Curso: {elemento.nome_curso}, ID do Curso: {elemento.id_curso}, Semestre: {elemento.semestre}, Ano: {elemento.ano}, Nota: {elemento.nota:.2f}')    

# 4- Listar todos os professores que são chefes de departamento, junto com o nome do departamento
def query4(session):
    query4 = session.execute(
        """
        SELECT Nome_Departamento, Nome_Professor, Chefe_Departamento
        FROM Professor
        """
    )
    if query4:
        for elemento in query4:
            if elemento.chefe_departamento == elemento.nome_professor:
                print(f'Nome do Departamento: {elemento.nome_departamento}, Nome do Professor: {elemento.nome_professor}')

# 5- Saber quais alunos formaram um grupo de TCC e qual professor foi o orientador
def query5(session):
    query5 = session.execute(
        """
        SELECT Nome_Aluno, Nome_Professor, ID_TCC
        FROM TCC
        """
    )
    if query5:
        for resultado in query5:
            print(f'Nome do Aluno: {resultado.nome_aluno}, Nome do Professor: {resultado.nome_professor}, ID do TCC: {resultado.id_tcc}')


# ----- CHAMANDO AS FUNÇÕES -----

# Funções para dropar todas as Colunas
deletaAluno(session)
deletaHistoricoEscolar(session)
deletaMateria(session)
deletaProfessor(session)
deletaHistoricoProfessor(session)
deletaCurso(session)
deletaDepartamento(session)
deletaTCC(session)
print('----- Todas as Tabelas foram dropadas -----')

# Funções para a criação da Tabelas
criaAluno(session)
criaHistoricoEscolar(session)
criaMateria(session)
criaProfessor(session)
criaHistoricoProfessor(session)
criaCurso(session)
criaDepartamento(session)
criaTCC(session)
print('\n----- Todas as Tabelas foram criadas -----')

# Funções para a criação das Queries
print('\n----- RESOLUÇÃO DAS QUERIES -----\n')
print("----- QUERY 1 -----")
query1(session)
print("\n----- QUERY 2 -----")
query2(session)
print("\n----- QUERY 3 -----")
query3(session)
print("\n----- QUERY 4 -----")
query4(session)
print("\n----- QUERY 5 -----")
query5(session)
print('\n----- Todas as Queries foram criadas -----')

# Função para desligar a sessão
session.shutdown()
