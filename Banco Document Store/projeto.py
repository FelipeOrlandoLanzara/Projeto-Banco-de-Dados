from pymongo import MongoClient
import json

with open ('./Banco Document Store/acessMongo.json') as file:
    config = json.load(file)

mongo_uri = config['connect']
db_name = config['database']

connection = MongoClient(mongo_uri)

db = connection[db_name]

collection_student = db['Aluno']

collection_student.drop()
print("Coleção Apagada com Sucesso")


student = {
    "ID_Aluno" : 40,
    "Nome_Aluno" : "Joao",
    "Idade_Aluno" : 18,
    "ID_Curso" : 2,
    "ID_TCC" : 3
}

collection_student.insert_one(student)

for i in collection_student.find():
    print(i)

#resultado = collection_test.find_one({"nome" : document["nome"]})

# if resultado:
#     print('O documento ja exite', document)

# else:
#     collection_test.insert_one(document)
#     print("Inserção realizada com sucesso")

