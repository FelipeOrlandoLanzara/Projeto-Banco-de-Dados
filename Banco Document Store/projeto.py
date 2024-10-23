from pymongo import MongoClient
import json
from faker import Faker
from faker.providers import DynamicProvider
import random

# Def para dropas todas as coleções
def drop_collections(db):
    collections_to_drop = [
        'Departamento',
        'Curso',
        'Professores',
        'Materia',
        'Aluno',
        'Query1',
        'Query2',
        'Query3',
        'Query4',
        'Query5'
    ]
    
    for collection_name in collections_to_drop:
        db[collection_name].drop()
        #print(f"Coleção '{collection_name}' removida.")
    #print("Operação drop terminada.")


# Abrir o arquivo json e conectar com o banco
with open ('./Banco Document Store/acessMongo.json') as file:
    config = json.load(file)

mongo_uri = config['connect']
db_name = config['database']

connection = MongoClient(mongo_uri)

db = connection[db_name]

# Dropar todas as tabelas:
drop_collections(db)

# Inicialização do Faker
fake = Faker()



# Criação das Coleções 
collection_departamento = db['Departamento']
collection_curso = db['Curso']
collection_teacher = db['Professores']
collection_materia = db['Materia']
collection_student = db['Aluno']

# Criação das Coleções das Queries
collection_query1 = db['Query1']
collection_query2 = db['Query2']
collection_query3 = db['Query3']
collection_query4 = db['Query4']
collection_query5 = db['Query5']

# Geracao de nomes de departamento de maneira aleatoria
nome_materia = DynamicProvider(
    provider_name = "materias_random",
    elements = ["Calculo 1", "Calculo 2", "Calculo 3", "Calculo 4", "Probabilidade e Estatística", "Desenvolvimento de Projetos", "Introdução a Computação"],
)

# inicialização dos providers:
fake.add_provider(nome_materia)

# Criação das variáveis que serão usadas nas coleçõe - serão gerados números aleatórios
ra_aluno = random.sample(range(100000000, 500000000), 60)
ra_professor = random.sample(range(500000001, 999999999), 20)
lista_materias = [num for num in random.sample(range(100000, 999999), 60)]


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
    
# Criação da Coleção Matéria
materias = []
for i in range(len(lista_materias)):
    chave = random.choice(list(materias_ids.keys())) # Pega uma chave aleatoria
    materia = {
        "ID_Materia" : chave,
        "Nome_Materia" : materias_ids[chave],
        "Prova" : fake.pybool() 
    }
    materias.append(materia)
collection_materia.insert_many(materias)


# Criação da Coleção Estudante 
students = []
for i, ra in enumerate(ra_aluno_formatado):
    chave = random.choice(list(materias_ids.keys())) # Pega uma chave aleatoria
    student = {
        "ID_Aluno" : ra,
        "Nome_Aluno" : fake.first_name(), # Nome atribuido aleatoriamente pela biblioteca faker
        "Idade_Aluno" : random.randint(18,65),
        "ID_Curso" : primary_keys["id_curso"][random.randint(0, 4)],
        "ID_TCC" : (i+1),
        "Historico_Escolar": { # Criação do Histórico Escolar junto a Coleção de Estudante
            "ID_Historico_Escolar" : 1,
            "Nota" : round(random.uniform(0.0,10.0),2),
            "Semestre" : random.choice(semestre),
            "Ano" : 2020,
            "ID_Materia" : chave,
        },
        "TCC" : { # Criação do TCC junto a Coleção de Estudante
            "Titulo" : "Título: " + str(i),
            "ID_Professor" : random.choice(ra_professor_formatado)
        }
    }
    students.append(student)
collection_student.insert_many(students)


# Criando a Coleção Professor
teachers = []
for i in range(len(ra_professor)):
    chave = random.choice(list(materias_ids.keys())) # Pega uma chave aleatoria
    teacher = {
        "ID_Professor" : ra_professor_formatado[i],
        "Nome_Professor" : fake.first_name(),
        "Salario" : random.randint(2000, 20000),
        "Nome_Departamento" : random.choice(primary_keys["nome_departamento"]),
        "Historico_Professor" : {
            "Semestre" : random.choice(semestre),
            "Ano" : 2020,
            "Quantidade_Aulas" : random.randint(1, 100),
            "ID_Materia" : chave
        }
    }
    teachers.append(teacher)

# Cria um professor isolado, com nome e nome de departamento já estabelecido para mostrar que a query 4 está correta
teacher_solo = {
    "ID_Professor" : '24.122.049-0',
    "Nome_Professor" : "Julia",
    "Salario" : random.randint(2000, 20000),
    "Nome_Departamento" : "Engenharia de Produção",
    "Historico_Professor" : {
        "Semestre" : random.choice(semestre),
        "Ano" : 2020,
        "Quantidade_Aulas" : random.randint(1, 100),
        "ID_Materia" : chave
    }
}
teachers.append(teacher_solo)
collection_teacher.insert_many(teachers)

# Criando a Coleção Curso
cursos = []
for i in primary_keys["id_curso"]:
    curso = {
        "ID_Curso" : i,
        "Nome_Curso" : cursos_ids[i],
        "Horas_Extras" : random.randint(120, 360),
        "Nome_Departamento" : cursos_ids[i]
    }
    cursos.append(curso)
collection_curso.insert_many(cursos)

#Criando a Coleção Departamento
departamentos = []
for i in primary_keys["nome_departamento"]:
    departamento = {
        "Nome_Departamento": i,
        "Chefe_Departamento": fake.first_name()
    }
    departamentos.append(departamento)

# Cria um departamento isolado, com nome de departamento e chefe de departamento já estabelecido para provar que a query 4 funciona
departamento_solo = {
    "Nome_Departamento": "Engenharia de Produção",
    "Chefe_Departamento": "Julia"
}
departamentos.append(departamento_solo)
collection_departamento.insert_many(departamentos)

#QUERIES
print('----- RESOLUÇÃO DAS QUERIES -----N\n')

# 1- Histórico escolar de qualquer aluno, retornando o código e nome da disciplina, semestre e ano que a disciplina foi cursada e nota final
# Agregação entre a Coleção Estudante e a Coleção Matéria a partir do ID_Materia ser igual
print("----- QUERY 1 -----")
query1 = collection_student.aggregate([
    {
        "$lookup": {
            "from": "Materia",  # Nome da coleção que vai agregar
            "localField": "Historico_Escolar.ID_Materia",  # Campo da outra coleção
            "foreignField": "ID_Materia",  # Campo da coleção que vou agregar
            "as": "materia_info"  # É onde vai armazenar todas essas informações
        }
    },
    {
        "$unwind": "$materia_info"  # Muda o nome - serve para poder chamar qualquer variável da Coleção Matéria
    },
    {
        "$sample": { "size": 1 } # Pega apenas um resultado (não aleatório, sempre o primeiro da lista)
    },
    {
        "$project": { # Adiciona em resultados apenas as variáveis que eu quiser
            "Nome_Aluno": 1,
            "ID_Curso": 1,
            "materia_info.Nome_Materia": 1,
            "Historico_Escolar.Semestre": 1,
            "Historico_Escolar.Ano": 1,
            "Historico_Escolar.Nota": 1,
            "_id": 0
        }
    }
])

# resultados_dif = [] # Pega apenas os que nao forem repetidos (remove quando object_id é a unica coisa diferente)
# nome_dif = [] # Colocar todos os nomes que nao forem iguais
# for resultado in query1:
#     if resultado['Nome_Aluno'] not in nome_dif:
#         nome_dif.append(resultado['Nome_Aluno'])
#         resultados_dif.append(resultado)
        
# for resultado in resultados_dif:
#     print(resultado)

# if resultados_dif:
#     collection_query1.insert_many(resultados_dif)

query_1 = [] # Lista para colocar os resultados da Query 1 e poder jogar em uma nova Coleção
for resultado in query1:
    query_1.append(resultado)
    print(resultado)

if query_1:
    collection_query1.insert_many(query_1) # Cria uma nova Coleção da Query 1


# 2- Histórico de disciplinas ministradas por qualquer professor, com semestre e ano
print("\n----- QUERY 2 -----")
query2 = collection_teacher.find_one({}, {
    "Historico_Professor.ID_Materia":1,
    "Historico_Professor.Semestre":1,
    "Historico_Professor.Ano":1,
    "_id": 0
})
print(query2)

if query2:
    collection_query2.insert_one(query2)

# 3- Listar alunos que já se formaram (foram aprovados em todos os cursos de uma matriz curricular) em um determinado semestre de um ano
print("\n----- QUERY 3 -----")
semestre_aleatorio = random.randint(0, 7)

query3 = collection_student.aggregate([
    {
        "$lookup": {
            "from": "Curso",
            "localField": "ID_Curso",
            "foreignField": "ID_Curso",
            "as": "curso_info"
        }
    },
    {
        "$unwind": "$curso_info"
    },
    {
        "$match": {
            "Historico_Escolar.Nota": { "$gt": 5 },
            "Historico_Escolar.Semestre": { "$eq": semestre[semestre_aleatorio] },
            "Historico_Escolar.Ano": { "$eq": 2020 }
        }
    },
    {
        "$project": {
            "Nome_Aluno": 1,
            "curso_info.Nome_Curso": 1,
            "ID_Curso": 1,
            "Historico_Escolar.Nota": 1,
            "Historico_Escolar.Semestre": 1,
            "Historico_Escolar.Ano": 1,
            "_id": 0
        }
    },
])

query_3 = [] # Lista para colocar os resultados da Query 3 e poder jogar em uma nova Coleção
for resultado in query3:
    query_3.append(resultado)
    print(resultado)

if query_3:
    collection_query3.insert_many(query_3) # Cria uma nova Coleção da Query 3


# 4- Listar todos os professores que são chefes de departamento, junto com o nome do departamento
print("\n----- QUERY 4 -----")
query4 = collection_teacher.aggregate([ # Nome professor = a Chefe de Departamento
    {
        "$lookup": {
            "from": "Departamento",
            "localField": "Nome_Professor", 
            "foreignField": "Chefe_Departamento",
            "as": "departamento_info"
        }
    },
    
    {
        "$unwind": "$departamento_info"
    },

    {
        "$project": {
            "Nome_Departamento": 1,
            "Nome_Professor": 1,
            "_id": 0
        }
    },
])

query_4 = [] # Lista para colocar os resultados da Query 4 e poder jogar em uma nova Coleção
for resultado in query4:
    query_4.append(resultado)
    print(resultado)
 
if query4:
    collection_query4.insert_many(query_4) # Cria uma nova Coleção da Query 4


# 5- Saber quais alunos formaram um grupo de TCC e qual professor foi o orientador
print("\n----- QUERY 5 -----")
query5 = collection_student.aggregate([
    {
        "$lookup": {
            "from": "Professores",
            "localField": "TCC.ID_Professor",
            "foreignField": "ID_Professor",
            "as": "tcc_info"
        }
    },
    {
        "$unwind": "$tcc_info" # Remove de uma lista
    },
    {
        "$project": {
            "Nome_Aluno": 1,
            "tcc_info.Nome_Professor": 1,
            "_id": 0
        }
    },
])

query_5 = [] # Lista para colocar os resultados da Query 5 e poder jogar em uma nova Coleção
for resultado in query5:
    query_5.append(resultado)
    print(resultado)

if query5:
    collection_query5.insert_many(query_5) # Cria uma nova Coleção da Query 5

