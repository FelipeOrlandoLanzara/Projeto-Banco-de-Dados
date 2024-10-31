from neo4j import GraphDatabase
import json
from faker import Faker
import random

# Pegando os dados de conexão do json
with open ('./GraphDatabase/acessNeo4j.json','r') as file:
    config = json.load(file)

# Conexão com o banco
driver = GraphDatabase.driver(config['uri'], auth=(config['user'], config['password']))

# Criacao da instância do Faker para pt-br
fake = Faker('pt-br')

# Criação das variáveis que serão usadas nas coleçõe - serão gerados números aleatórios
ra_aluno = random.sample(range(100000000, 500000000), 60)
ra_professor = random.sample(range(500000001, 999999999), 20)
lista_materias = [num for num in random.sample(range(100000, 999999), 60)]

# gera aleatoriamente e sem repetir a lista de historico escolar dos alunos (60)
lista_hist_escolar = [num for num in random.sample(range(1, 500000), 60)]
# gera aleatoriamente e sem repetir a lista do historico dos professores (60)
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
semestre = ["Primeiro","Segundo","Terceiro","Quarto","Quinto","Sexto","Setimo","Oitavo"]

# Cria um dicionário de ids de curso, onde cada id que vai representar um nome de dapartamento
cursos_ids = {
    'MA': 'Matemática',
    'FI': 'Física',
    'CC': 'Ciência da Computação',
    'EE': 'Engenharia Elétrica',
    'EM' : 'Engenharia Mecânica'
}

# Cria um dicionario de ids de materias, onde cada id que vai referenciar uma materia - assim podemos ter varios alunos fazendo aquela mesma materia (com mesmo id, logo mesma sala de aula)
materias_ids = {}
for i in lista_materias:
    materias_ids[i] = primary_keys['nome_materia'][random.randint(0,4)]

# Função para remover todos os nós e tabelas criadas
def removeNos():
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")

# Criação da Tabela Alunos
def criaAluno():
    with driver.session() as session:
        for ra in ra_aluno_formatado:
            session.run("CREATE (a:Aluno {ID_Aluno: $ID_Aluno, Nome_Aluno: $Nome_Aluno, Idade_Aluno: $Idade_Aluno})",
            ID_Aluno = ra,
            Nome_Aluno = fake.first_name(),
            Idade_Aluno = random.randint(18,65))
            session.run("MATCH (a:aluno), (he:HistoricoEscolar)")
            session.run("CREATE (a)-[teste:relacionamento]-> (he)")
            

def criaHistoricoEscolar():
    with driver.session() as session:
        for id in lista_hist_escolar:
            session.run("CREATE (he:HistóricoEscolar {ID_HistoricoEscolar: $ID_HistoricoEscolar, Nota: $Nota , Semestre: $Semestre, Ano: $Ano})",
            ID_HistoricoEscolar = id,
            Nota = round(random.uniform(0.0,10.0),2),
            Semestre = random.choice(semestre),
            Ano = 2020)



try:
    removeNos()
    criaAluno()
    criaHistoricoEscolar()
finally:
    driver.close()