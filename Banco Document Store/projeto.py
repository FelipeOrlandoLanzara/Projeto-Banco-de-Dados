from pymongo import MongoClient
import json
from faker import Faker
from faker.providers import DynamicProvider
import random

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


with open ('./Banco Document Store/acessMongo.json') as file:
    config = json.load(file)

mongo_uri = config['connect']
db_name = config['database']

connection = MongoClient(mongo_uri)

db = connection[db_name]

#Dropar todas as tabelas:
drop_collections(db)

fake = Faker()
#Criar as coleções
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

#inicialização dos providers:
fake.add_provider(nome_materia)


ra_aluno = random.sample(range(100000000, 500000000), 50)
ra_professor = random.sample(range(500000001, 999999999), 20)
lista_materias = [num for num in random.sample(range(100000, 999999), 60)]

ra_aluno_formatado = []
ra_professor_formatado = []

for i in ra_aluno:
    ra_aluno_formatado.append(f"{str(i)[:2]}.{str(i)[:3]}.{str(i)[:3]}-{str(i)[:1]}")

for i in ra_professor:
    ra_professor_formatado.append(f"{str(i)[:2]}.{str(i)[:3]}.{str(i)[:3]}-{str(i)[:1]}")


# valores chaves de variaveis para quando for criar valores ficticios
primary_keys = {
    "nome_departamento" : ["Matemática", "Física", "Ciência da Computação", "Engenharia Elétrica", "Engenharia Mecânica"],
    "id_curso" : ['MA', 'FI', 'CC', 'EE', 'EM'],
    "id_materia" : ['452645', '745234', '258452', '123254', '123456', '545236'],
}
semestre = ["Primeiro","Segundo","Terceiro","Quarto","Quinto","Sexto","Setimo","oitavo"]

materias = []
for i in range(len(lista_materias)):
    materia = {
        "ID_Materia" : random.choice(primary_keys["id_materia"]),
        "Nome_Materia" : fake.materias_random(),
        "Prova" : fake.pybool() 
    }
    materias.append(materia)
collection_materia.insert_many(materias)

students = []
for i in range(len(ra_aluno)):
    student = {
        "ID_Aluno" : ra_aluno_formatado[i],
        "Nome_Aluno" : fake.first_name(), #nome atribuido aleatoriamente pela biblioteca faker
        "Idade_Aluno" : random.randint(18,65),
        "ID_Curso" : primary_keys["id_curso"][random.randint(0, 4)],
        "ID_TCC" : (i+1),
        "Historico_Escolar": {
            "ID_Historico_Escolar" : 1,
            "Nota" : round(random.uniform(0.0,10.0),2),
            "Semestre" : random.choice(semestre),
            "Ano" : 2020,
            "ID_Materia" : random.choice(primary_keys["id_materia"])
        }
    }
    students.append(student)
collection_student.insert_many(students)

pipeline = [
    {
        "$lookup" : {
            "from" : "students",
            "localField" : "ID_Materia",
            "foreignField" : "Historico_Escolar.ID_Materia",
            "as" : "Materias_Info"
        }
    },
    {
        "$unwind" : "$Materias_Info"
    }
]

result = db.collection_materia.aggregate(pipeline)
print(result)


teachers = []
for i in range(len(ra_professor)):
    teacher = {
        "ID_Professor" : ra_professor_formatado[i],
        "Nome_Professor" : fake.first_name(),
        "Salario" : random.randint(2000, 20000),
        "Nome_Departamento" : random.choice(primary_keys["nome_departamento"]),
        "Historico_Professor" : {
            "Semestre" : random.choice(semestre),
            "Ano" : 2020,
            "Quantidade_Aulas" : random.randint(1, 100),
            "ID_Materia" : random.choice(primary_keys["id_materia"]) 
        }
    }
    teachers.append(teacher)
collection_teacher.insert_many(teachers)

# for i in collection_student.find():
#     print(i)

#querie para retornar a nota de cada aluno

#{} -> busque todas as collections sem filtro
#nome_aluno = collection_student.find({}, {"Nome_Aluno": 1, "_id": 0, "Idade_Aluno" : 1, "Historico_Escolar.Nota" : 1})

#nota_especifica = collection_student.find({"Historico_Escolar.Nota": {"$lt": 2} }, {"Nome_Aluno": 1, "_id": 0, "Historico_Escolar.Nota" : 1})

#for i in nota_especifica:
   #print("nota especifica: ", i)

#resultado = collection_test.find_one({"nome" : document["nome"]})

# if resultado:
#     print('O documento ja exite', document)

# else:
#     collection_test.insert_one(document)
#     print("Inserção realizada com sucesso")

#QUERIES
# 1- histórico escolar de qualquer aluno, retornando o código e nome da disciplina, semestre e ano que a disciplina foi cursada e nota final
#hist_esc = collection_student.find_one({"Nome_Aluno":0, "_id":1})


# 2- histórico de disciplinas ministradas por qualquer professor, com semestre e ano
hist_prof = collection_teacher.find_one({}, {"Nome_Professor":1, "Historico_Professor.ID_Materia":1, "Historico_Professor.Semestre":1, "Historico_Professor.Ano":1})
print(hist_prof)


# 3- listar alunos que já se formaram (foram aprovados em todos os cursos de uma matriz curricular) em um determinado semestre de um ano



# 4- listar todos os professores que são chefes de departamento, junto com o nome do departamento



# 5- saber quais alunos formaram um grupo de TCC e qual professor foi o orientador

