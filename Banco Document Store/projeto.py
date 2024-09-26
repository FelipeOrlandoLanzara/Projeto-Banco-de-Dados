from pymongo import MongoClient
import json
from faker import Faker
import random

with open ('./Banco Document Store/acessMongo.json') as file:
    config = json.load(file)

mongo_uri = config['connect']
db_name = config['database']

connection = MongoClient(mongo_uri)

db = connection[db_name]

fake = Faker()

collection_student = db['Aluno']

collection_student.drop()
print("Coleção Apagada com Sucesso")

ra_aluno = random.sample(range(100000000, 500000000), 50)
#ra_professor = random.sample(range(500000001, 999999999), 20)

ra_aluno_formatado = []


for i in ra_aluno:
    ra_aluno_formatado.append(f"{str(i)[:2]}.{str(i)[:3]}.{str(i)[:3]}-{str(i)[:1]}")

semestre = ["Primeiro","Segundo","Terceiro","Quarto","Quinto","Sexto","Setimo","oitavo"]

students = []
for i in range(len(ra_aluno)):
    student = {
        "ID_Aluno" : ra_aluno_formatado[i],
        "Nome_Aluno" : fake.first_name(), #nome atribuido aleatoriamente pela biblioteca faker
        "Idade_Aluno" : random.randint(18,65),
        "ID_Curso" : 2,
        "ID_TCC" : 3,
        "Historico_Escolar": {
            "ID_Historico_Escolar" : 1,
            "Nota" : round(random.uniform(0.0,10.0),2),
            "Semestre" : random.choice(semestre),
            "Ano" : 2,
            "ID_Aluno" : ra_aluno_formatado[i],
            "ID_Materia" : "ca122"
        }
    }
    students.append(student)

collection_student.insert_many(students)

for i in collection_student.find():
    print(i)

#resultado = collection_test.find_one({"nome" : document["nome"]})

# if resultado:
#     print('O documento ja exite', document)

# else:
#     collection_test.insert_one(document)
#     print("Inserção realizada com sucesso")