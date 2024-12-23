from neo4j import GraphDatabase
import json
from faker import Faker
import random
import warnings

# Remove qualquer tipo de warning que dá no terminal
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Pegando os dados de conexão do json
with open ('./GraphDatabase/acessNeo4j.json','r') as file:
    config = json.load(file)

# Conexão com o banco
driver = GraphDatabase.driver(config['uri'], auth=(config['user'], config['password']))

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

# Função para remover todos os nós e tabelas criadas
def removeNos():
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")

# ----- CRIAÇÃO DE TODAS OS GRAFOS -----

# Criação da Tabela Alunos
def criaAluno():
    with driver.session() as session:
        for ra in ra_aluno_formatado:
            session.run("CREATE (a:Aluno {ID_Aluno: $ID_Aluno, Nome_Aluno: $Nome_Aluno, Idade_Aluno: $Idade_Aluno})",
                        ID_Aluno = ra,
                        Nome_Aluno = fake.first_name(),
                        Idade_Aluno = random.randint(18,65)
                        )
            
# Criação da Tabela Histórico Escolar
def criaHistoricoEscolar():
    with driver.session() as session:
        for id in lista_hist_escolar:
            session.run("CREATE (he:HistóricoEscolar {ID_HistoricoEscolar: $ID_HistoricoEscolar, Nota: $Nota , Semestre: $Semestre, Ano: $Ano})",
                        ID_HistoricoEscolar = id,
                        Nota = round(random.uniform(0.0,10.0),2),
                        Semestre = random.choice(semestre),
                        Ano = 2020
                        )

# Criação da Tabela Matéria
def criaMateria():
    with driver.session() as session:
        for id in lista_materias:
            session.run("CREATE (m:Matéria {ID_Materia: $ID_Materia, Nome_Materia: $Nome_Materia, Prova: $Prova})",
                        ID_Materia = id,
                        Nome_Materia = materias_ids[id],
                        Prova = fake.pybool()
                        )
            
# Criação da Tabela Professor
def criaProfessor():
    with driver.session() as session:
        for ra in ra_professor_formatado:
            session.run("CREATE (p:Professor {ID_Professor: $ID_Professor, Nome_Professor: $Nome_Professor, Salario: $Salario})",
                        ID_Professor = ra,
                        Nome_Professor = fake.first_name(),
                        Salario = random.randint(2000, 20000)
                        )
            
# Adiciona uma nova Professora Julia
def adicionaProfessor():
    with driver.session() as session:
        session.run("CREATE (p:Professor {ID_Professor: $ID_Professor, Nome_Professor: $Nome_Professor, Salario: $Salario})",
                    ID_Professor = "24.122.055-7",
                    Nome_Professor = "Julia",
                    Salario = 20000
                    )

# Criação da Tabela Histórico Professor
def criaHistoricoProfessor():
    with driver.session() as session:
        for id in lista_hist_professor:
            session.run("CREATE (hp:HistóricoProfessor {ID_HistoricoProfessor: $ID_HistoricoProfessor, Semestre: $Semestre, Ano: $Ano, Quantidade_Aulas: $Quantidade_Aulas})",
                        ID_HistoricoProfessor = id,
                        Semestre = random.choice(semestre),
                        Ano = 2020,
                        Quantidade_Aulas = random.randint(1, 100)
                        )

# Criação da Tabela Curso
def criaCurso():
    with driver.session() as session:
        for id in primary_keys["id_curso"]:
            session.run("CREATE (c:Curso {ID_Curso: $ID_Curso, Nome_Curso: $Nome_Curso, Horas_Extras: $Horas_Extras})",
                        ID_Curso = id,
                        Nome_Curso = cursos_ids[id],
                        Horas_Extras = random.randint(120, 360)
                        )
    
# Criação da Tabela Departamento
def criaDepartamento():
    with driver.session() as session:
        for name in primary_keys["nome_departamento"]:
            session.run("CREATE (d:Departamento {Nome_Departamento: $Nome_Departamento, Chefe_Departamento: $Chefe_Departamento})",
                        Nome_Departamento = name,
                        Chefe_Departamento = fake.first_name()
                        )
            
# Adiciona uma Chefe de Departamento Julia em um novo Departamento Engenharia de Produção
def adicionaDepartamento():
    with driver.session() as session:
        session.run("CREATE (d:Departamento {Nome_Departamento: $Nome_Departamento, Chefe_Departamento: $Chefe_Departamento})",
                    Nome_Departamento = "Engenharia de Produção",
                    Chefe_Departamento = "Julia"
                    )

# Criação da Tabela TCC
def criaTCC():
    with driver.session() as session:
        for id in range(len(ra_aluno_formatado)):
            session.run("CREATE (t:TCC {ID_TCC: $ID_TCC, Titulo: $Titulo})",
                        ID_TCC = id,
                        Titulo = "Título: " + str(id)
                        )


# ----- CRIAÇÃO DE TODAS AS RELAÇÕES -----

# Criação da Relação Aluno com Histórico Escolar
def relacao_Aluno_HistoricoEscolar():
    with driver.session() as session:
        for ra, id_he in zip(ra_aluno_formatado, lista_hist_escolar):
            session.run(
                "MATCH (a:Aluno {ID_Aluno: $ID_Aluno}), (he:HistóricoEscolar {ID_HistoricoEscolar: $ID_HistoricoEscolar})"
                "CREATE (a)-[:TEM]->(he)",
                ID_Aluno = ra, ID_HistoricoEscolar = id_he
            )

# Criação da Relação Histórico Escolar com Matéria
def relacao_HistoricoEscolar_Materia():
    with driver.session() as session:
        for id_he, id_ma in zip(lista_hist_escolar, lista_materias):
            session.run(
                "MATCH (he:HistóricoEscolar {ID_HistoricoEscolar: $ID_HistoricoEscolar}), (m:Matéria {ID_Materia: $ID_Materia})"
                "CREATE (he)-[:REFERENTE]->(m)",
                ID_HistoricoEscolar = id_he, ID_Materia = id_ma 
            )

# Criação da Relação Professor com Histórico Professor
def relacao_Professor_HistoricoProfessor():
    with driver.session() as session:
        for ra, id_hp in zip(ra_professor_formatado, lista_hist_professor):
            session.run(
                "MATCH (p:Professor {ID_Professor: $ID_Professor}), (hp:HistóricoProfessor {ID_HistoricoProfessor: $ID_HistoricoProfessor})"
                "CREATE (p)-[:POSSUI]->(hp)",
                ID_Professor = ra, ID_HistoricoProfessor = id_hp
            )
            
# Criação da Relação Histórico Professor com Matéria
def relacao_HistoricoProfessor_Materias():
    with driver.session() as session:
        for id_hp, id_ma in zip(lista_hist_professor, lista_materias):
            session.run(
                        "MATCH (hp:HistóricoProfessor {ID_HistoricoProfessor: $ID_HistoricoProfessor}), (m:Matéria {ID_Materia: $ID_Materia})"
                        "CREATE (hp)-[:REFERENCIA]->(m)",
                        ID_HistoricoProfessor = id_hp, ID_Materia = id_ma 
                    )

# Criação da Relação Aluno com Curso
def relacao_Aluno_Curso():
    with driver.session() as session:
        for ra in ra_aluno_formatado:
            id = random.choice(primary_keys["id_curso"]) # Vai pegar um aleatório, o que permite com que alunos cursem o mesmo curso
            session.run(
                """
                MATCH (a:Aluno {ID_Aluno: $ID_Aluno}), (c:Curso {ID_Curso: $ID_Curso})
                CREATE (a)-[:CURSOU]->(c)
                """,
                ID_Aluno = ra, ID_Curso = id
            )

# Criação da Relação Departamento com Professor
def relacao_Departamento_Professor():
    with driver.session() as session:
        for ra in ra_professor_formatado:
            name = random.choice(primary_keys["nome_departamento"])
            session.run(
                """
                MATCH (d:Departamento {Nome_Departamento: $Nome_Departamento}), (p:Professor {ID_Professor: $ID_Professor})
                CREATE (d)-[:ORGANIZA]->(p)
                """,
                Nome_Departamento = name, ID_Professor = ra
            )
        session.run(
            """
            MATCH (d:Departamento {Nome_Departamento: $Nome_Departamento}), (p:Professor {ID_Professor: $ID_Professor})
            CREATE (d)-[:ORGANIZA]->(p)
            """,
            Nome_Departamento = "Engenharia de Produção", ID_Professor = "24.122.055-7"
        )

# Criação da Relação Professor com TCC
def relacao_Professor_TCC():
    with driver.session() as session:
        for id_tcc in range(len(ra_aluno_formatado)):
            ra = random.choice(ra_professor_formatado)
            session.run(
                """
                MATCH (p:Professor {ID_Professor: $ID_Professor}), (t:TCC {ID_TCC: $ID_TCC})
                CREATE (p)-[:ORIENTADO]->(t)
                """,
            ID_TCC = id_tcc, ID_Professor = ra
            )

# Criação da Relação Aluno com TCC
def relacao_Aluno_TCC():
    with driver.session() as session:
        for id_tcc, ra in enumerate(ra_aluno_formatado):
                session.run(
                    """
                    MATCH (a:Aluno {ID_Aluno: $ID_Aluno}), (t:TCC {ID_TCC: $ID_TCC})
                    CREATE (a)-[:FAZ]->(t)
                    """,
                ID_Aluno = ra, ID_TCC = id_tcc
                )

 
# ----- RESOLUÇÃO DAS QUERIES -----

# 1- Histórico escolar de qualquer aluno, retornando o código e nome da disciplina, semestre e ano que a disciplina foi cursada e nota final
def query1():
    with driver.session() as session:
        query1 = session.run(
            """
            MATCH (a:Aluno)-[:TEM]->(he:HistóricoEscolar)-[:REFERENTE]->(m:Matéria)
            RETURN a.Nome_Aluno AS Nome_Aluno, 
                m.ID_Materia AS ID_Materia, 
                m.Nome_Materia AS Nome_Materia, 
                he.Semestre AS Semestre, 
                he.Ano AS Ano, 
                he.Nota AS Nota
            LIMIT 1
            """
        )
        for resultado in query1:
            print(f'Nome do Aluno: {resultado["Nome_Aluno"]}, ID da Matéria: {resultado["ID_Materia"]}, Nome da Matéria: {resultado["Nome_Materia"]}, Semestre: {resultado["Semestre"]}, Ano: {resultado["Ano"]}, Nota: {resultado["Nota"]}')

# 2- Histórico de disciplinas ministradas por qualquer professor, com semestre e ano
def query2():
    with driver.session() as session:
        query2 = session.run(
        """
        MATCH (p:Professor)-[:POSSUI]->(hp:HistóricoProfessor)-[:REFERENCIA]->(m:Matéria)
        RETURN p.Nome_Professor AS Nome_Professor,
            m.Nome_Materia AS Nome_Materia,
            m.ID_Materia AS ID_Materia,
            hp.Semestre AS Semestre,
            hp.Ano AS Ano
        LIMIT 1
        """
        )
        for resultado in query2:
            print(f'Nome do Professor: {resultado["Nome_Professor"]}, Nome da Matéria: {resultado["Nome_Materia"]}, ID da Matéria: {resultado["ID_Materia"]}, Semestre: {resultado["Semestre"]}, Ano: {resultado["Ano"]}')

# 3- Listar alunos que já se formaram (foram aprovados em todos os cursos de uma matriz curricular) em um determinado semestre de um ano
def query3():
    with driver.session() as session:
        numero_aleatorio = random.randint(0, 7) # Pega um número aleatório para buscar na lista Semestre
        semestre_aleatorio = semestre[numero_aleatorio] # Para pegar essa variável dentro da Query é preciso colocar o '$' antes
        query3 = session.run(
        """
        MATCH (a:Aluno)-[:TEM]->(he:HistóricoEscolar), (a:Aluno)-[:CURSOU]->(c:Curso)
        WHERE he.Nota > 5 AND he.Semestre = $semestre_aleatorio AND he.Ano = 2020
        RETURN a.Nome_Aluno AS Nome_Aluno,
            c.Nome_Curso AS Nome_Curso,
            c.ID_Curso AS ID_Curso,
            he.Semestre AS Semestre,
            he.Ano AS Ano,
            he.Nota AS Nota
        """, 
        semestre_aleatorio = semestre_aleatorio # E agora eu digo para a Query qual o parâmetro que eu dei
        )
        for resultado in query3:
            print(f'Nome do Aluno: {resultado["Nome_Aluno"]}, Nome do Curso: {resultado["Nome_Curso"]}, ID do Curso: {resultado["ID_Curso"]}, Semestre: {resultado["Semestre"]}, Ano: {resultado["Ano"]}, Nota: {resultado["Nota"]}')

# 4- Listar todos os professores que são chefes de departamento, junto com o nome do departamento
def query4():
    with driver.session() as session:
        query4 = session.run(
            """
            MATCH (d:Departamento)-[:ORGANIZA]->(p:Professor)
            WHERE d.Chefe_Departamento = p.Nome_Professor
            RETURN d.Nome_Departamento AS Nome_Departamento,
                p.Nome_Professor AS Nome_Professor
            """
        )
        for resultado in query4:
            print(f'Nome do Departamento: {resultado["Nome_Departamento"]}, Nome do Professor: {resultado["Nome_Professor"]}')

# 5- Saber quais alunos formaram um grupo de TCC e qual professor foi o orientador
def query5():
    with driver.session() as session:
        query5 = session.run(
            """
            MATCH (a:Aluno)-[:FAZ]->(t:TCC)<-[:ORIENTADO]-(p:Professor)
            RETURN a.Nome_Aluno AS Nome_Aluno,
                p.Nome_Professor AS Nome_Professor,
                t.ID_TCC AS ID_TCC
            """
        )
        for resultado in query5:
            print(f'Nome do Aluno: {resultado["Nome_Aluno"]}, Nome do Professor: {resultado["Nome_Professor"]}, ID do TCC: {resultado["ID_TCC"]}')


# ----- CHAMANDO TODAS AS FUNÇÕES -----

# Chamando todas as funções que cria cada Grafo
try:
    removeNos()
    criaAluno()
    criaHistoricoEscolar()
    criaMateria()
    criaProfessor()
    adicionaProfessor()
    criaHistoricoProfessor()
    criaCurso()
    criaDepartamento()
    adicionaDepartamento()
    criaTCC()
    print("----- Grafos criados -----")
finally:
    driver.close()

# Chamando todas as funções que criam as relações entre os Grafos
try:
    relacao_Aluno_HistoricoEscolar()
    relacao_HistoricoEscolar_Materia()
    relacao_Professor_HistoricoProfessor()
    relacao_HistoricoProfessor_Materias()
    relacao_Aluno_Curso()
    relacao_Departamento_Professor()
    relacao_Professor_TCC()
    relacao_Aluno_TCC()
    print("\n----- Relação dos Grafos criadas -----")
finally:
    driver.close()

# Chamando todas as funções que criam as Queries
try:
    print('\n----- RESOLUÇÃO DAS QUERIES -----\n')
    print("----- QUERY 1 -----")
    query1()
    print("\n----- QUERY 2 -----")
    query2()
    print("\n----- QUERY 3 -----")
    query3()
    print("\n----- QUERY 4 -----")
    query4()
    print("\n----- QUERY 5 -----")
    query5()
    print("\n ----- Programa finalizado -----")
finally:
    driver.close()
