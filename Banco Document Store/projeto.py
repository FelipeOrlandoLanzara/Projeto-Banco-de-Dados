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
        'Matriz Curricular',
        'TCC',
        'Aluno',
        'Horas Complementares',
        'Historico Escolar',
        'Historico Professor'
    ]
    
    for collection_name in collections_to_drop:
        db[collection_name].drop()
        print(f"Coleção '{collection_name}' removida.")
    print("Operação drop terminada.")


# Abrir o arquivo json e conectar com o banco
with open ('./Banco Document Store/acessMongo.json') as file:
    config = json.load(file)

mongo_uri = config['connect']
db_name = config['database']

connection = MongoClient(mongo_uri)

db = connection[db_name]

# Dropar todas as tabelas:
drop_collections(db)

fake = Faker()
# Criar as coleções
collection_departamento = db['Departamento']
collection_curso = db['Curso']
collection_teacher = db['Professores']
collection_materia = db['Materia']
collection_matriz_curricular = db['Matriz Curricular']
collection_tcc = db['TCC']
collection_student = db['Aluno']
collection_horas_coplementares = db['Horas Complementares']
collection_historico_escolar = db['Historico Escolar']
collection_historico_professor = db['Historico Professor']

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
semestre = ["Primeiro","Segundo","Terceiro","Quarto","Quinto","Sexto","Setimo","oitavo"]


# Cria um dicionario de ids de materias, onde cada id vai referenciar uma materia - assim podemos ter varios alunos fazendo aquela mesma materia (com mesmo id, logo mesma sala de aula)
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
        "Historico_Escolar": {
            "ID_Historico_Escolar" : 1,
            "Nota" : round(random.uniform(0.0,10.0),2),
            "Semestre" : random.choice(semestre),
            "Ano" : 2020,
            "ID_Materia" : chave,
        }
    }
    students.append(student)
collection_student.insert_many(students)


# Agregação entre a Coleção Estudante e a Coleção Matéria a partir do ID_Materia ser igual
resultados = collection_student.aggregate([
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
        "$sample": { "size": 1 } # pega apenas um resultado (não aleatório, sempre o primeiro da lista)
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
collection_teacher.insert_many(teachers)


#QUERIES
# 1- histórico escolar de qualquer aluno, retornando o código e nome da disciplina, semestre e ano que a disciplina foi cursada e nota final
print("----- QUERY 1 -----")
resultados_dif = [] # pega apenas os que nao forem repetidos (remove quando object_id é a unica coisa diferente)
nome_dif = [] # colocar todos os nomes que nao forem iguais
for resultado in resultados:
    if resultado['Nome_Aluno'] not in nome_dif:
        nome_dif.append(resultado['Nome_Aluno'])
        resultados_dif.append(resultado)
        
for resultado in resultados_dif:
    print(resultado)

# 2- histórico de disciplinas ministradas por qualquer professor, com semestre e ano
print("\n----- QUERY 2 -----")
hist_prof = collection_teacher.find_one({}, {"Nome_Professor":1, "Historico_Professor.ID_Materia":1, "Historico_Professor.Semestre":1, "Historico_Professor.Ano":1})
print(hist_prof)


# 3- listar alunos que já se formaram (foram aprovados em todos os cursos de uma matriz curricular) em um determinado semestre de um ano
#print("\n----- QUERY 3 -----")


# 4- listar todos os professores que são chefes de departamento, junto com o nome do departamento
#print("\n----- QUERY 4 -----")


# 5- saber quais alunos formaram um grupo de TCC e qual professor foi o orientador
#print("\n----- QUERY 5 -----")

