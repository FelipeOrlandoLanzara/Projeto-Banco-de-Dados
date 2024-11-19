# Projeto Banco de Dados
 Projetar uma faculdade utilizando banco de dados para salvar os dados.

# Integrantes
Enzo Pacheco Porfirio R.A.: 24.122.003-7

Felipe Orlando Lanzara R.A.: 24.122.055-7

João Vitor Governatore R.A.: 24.122.027-6

Pedro Henrique Lega Kramer Costa R.A.: 24.122.049-0



# Diagrama Relacional(MER)
![image](https://github.com/jvgoverna/Projeto-Banco-de-Dados/blob/main/Diagrama%20Relacional%20(MER).png)

# Passos para executar o programa
- Antes de fazer o download do arquivo zip do projeto, deve-se primeiro, fazer a instalação das bibliotecas ```psycopg2``` e ```Faker``` através do comando ```pip install```
- Criar um ```acess.json``` com as seguintes instruções (o nome do ```database``` deve ser "projeto"):

![image](https://github.com/jvgoverna/Projeto-Banco-de-Dados/blob/main/Imagem%20do%20acess%20do%20json.png)

# Explicação das querys:
- Query 1: Dentre todos os alunos que foram colocados aleatoriamente, um deles será escolhido (também aleatoriamente).
- Query 2: Dentre todos os professores que foram colocados aleatoriamente, um deles será escolhido (também aleatoriamente).
- Query 3: Dentre todos os anos (pré-definido como 2020 para facilitar) e semestres (indo de 'Primeiro' até 'Oitavo') que foram colocados aleatoriamente, um de cada será escolhido (também aleatoriamente). Caso o aluno apresente uma nota maior do que a média (5), ele será aprovado.
- Query 4: No modelo de faculdade optamos pelo chefe de departamento não necessáriamente lecionar aulas, visto que seu papel principal é organizar o seu respectivo departamento. Por isso, tanto o nome dos professores, quanto o nome dos chefes de departamento são escolhidos aleatoriamente, tornando as chances deles coincidirem muito baixa. Por conta desse fator, adicionamos manualmente uma nova professora (Julia), que também será chefe de um novo departamento (Astrofísica), apenas para demonstrar que a query de fato funciona. (Esse departamente e professora foram exclusivamentes criados para essa querry, em outros itens não há o departamento de astrofísica ).
- Query 5: Todos os alunos terão um id de TCC já definido junto a um professor que será o orientador.

# Banco Document Store (MongoDB)

## Passos para executar o programa
- Antes de fazer o download do arquivo zip do projeto, deve-se primeiro, fazer a instalação das bibliotecas ```pymongo``` e ```Faker``` através do comando ```pip install```.
- Criar um ```acessMongo.json``` na pasta ```Banco Document Store``` com as seguintes instruções: ```connect``` e o ```database``` do seu servidor:

![image](https://github.com/jvgoverna/Projeto-Banco-de-Dados/blob/main/Conexao%20MongoDB.png)

## Descrição da Criação das Coleções
- Materia:
```python
{
  ID_Materia: int
  Nome_Materia: string
  Prova: boolean
}
```
- Estudante:
```python
{
  ID_Aluno: string
  Nome_Aluno: string
  Idade_Aluno: int
  ID_Curso: string
  ID_TCC: int
  Historico_Escolar: {
                        ID_Historico_Escolar: int
                        Nota: float
                        Semestre: string
                        Ano: int
                        ID_Materia: int
                     }
}
```
- Professor:
```python
{
  ID_Professor: string
  Nome_Professor: string
  Salario: int
  Nome_Departamento: string
  Historico_Professor: {
                          ID_Historico_Professor: int
                          Semestre: string
                          Ano: int
                          Quantidade_Aulas: int
                          ID_Materia: int
                       }
}
```
- Curso:
```python
{
  ID_Curso: string
  Nome_Curso: string
  Horas_Extras: int
  Nome_Departamento: string
}
```
- Departamento:
```python
{
  Nome_Departamento: string
  Chefe_Departamento: string
}
```

# Banco Wide-column Store (Cassandra)

## Passos para executar o programa
- Antes de fazer o download do arquivo zip do projeto, deve-se primeiro, fazer a instalação das bibliotecas ```cassandra-driver``` e ```Faker``` através do comando ```pip install```.
- Criar um ```acessCassandra.json``` na pasta ```Wide-ColumnStore``` com as seguintes instruções: ```clientId```, ```secret``` e o ```token``` do seu servidor.
- Fazer o Dowload do arquivo zip de conexão do servidor (DataStax), Ex.: secure-connect-faculdade.zip
- Nome do keyspace do servidor: ```faculdade``` o servidor deverá ser criado do tipo ```Serverless (Non-Vector)```.

![image](https://github.com/jvgoverna/Projeto-Banco-de-Dados/blob/main/Conexao%20Cassandra.png)

- No ```secure_connect_bundle```, acrescentar o nome de arquivo zip de conexão do servidor

![image](https://github.com/jvgoverna/Projeto-Banco-de-Dados/blob/main/Nome%20Arquivo%20ZIP%20conexao%20Cassandra.png)

## Descrição da Criação das Tabelas
- Aluno:
```python
{
  ID_Aluno: string
  Nome_Aluno: string
  Idade_Aluno: int
  Nome_Curso: string
  ID_Curso: string
  Semestre: string
  Ano: int
  Nota: float
  PRIMARY KEY (ID_Aluno, Nome_Aluno, Idade_Aluno)
}
```
- HistoricoEscolar:
```python
{
  ID_HistoricoEscolar: int
  Semestre: string
  Ano: int
  Nota: float
  Nome_Aluno: string
  ID_Materia: int
  Nome_Materia: string
  PRIMARY KEY (ID_HistoricoEscolar, Semestre, Ano, Nota)
}
```
- Materia:
```python
{
  ID_Materia: int
  Nome_Materia: string
  Prova: boolean
  PRIMARY KEY (ID_Materia, Nome_Materia, Prova)
}
```
- Professor:
```python
{
  ID_Professor: string
  Nome_Professor: string
  Salario: int
  Nome_Departamento: string
  Chefe_Departamento: string
  PRIMARY KEY (ID_Professor, Nome_Professor, Salario)
}
```
- HistoricoProfessor:
```python
{
  ID_HistoricoProfessor: int
  Semestre: string
  Ano: int
  Quantidade_Aulas: int
  Nome_Professor: string
  ID_Materia: int
  Nome_Materia: string
  PRIMARY KEY (ID_HistoricoProfessor, Semestre, Ano, Quantidade_Aulas)
}
```
- Curso:
```python
{
  ID_Curso: string
  Nome_Curso: string
  Horas_Extras: int
  PRIMARY KEY (ID_Curso, Nome_Curso, Horas_Extras)
}
```
- Departamento:
```python
{
  Nome_Departamento: string
  Chefe_Departamento: string
  PRIMARY KEY (Nome_Departamento, Chefe_Departamento)
}
```
- TCC:
```python
{
  ID_TCC: int
  Titulo: string
  Nome_Aluno: string
  Nome_Professor: string
  PRIMARY KEY (ID_TCC, Titulo)
}
```

# Banco GraphDatabase (Neo4j)

## Passos para executar o programa
- Antes de fazer o download do arquivo zip do projeto, deve-se primeiro, fazer a instalação das bibliotecas ```neo4j``` e ```Faker``` através do comando ```pip install```.
- Criar um ```acessNeo4j``` na pasta ```GraphDatabase``` com as seguintes instruções: ```uri```, ```user``` e ```password```do seu servidor.
- Protocolo de Conexão: ```neo4j+```.

![image](https://github.com/jvgoverna/Projeto-Banco-de-Dados/blob/main/Conexao%20Neo4j.png)

## Descrição da Criação dos Nós
- Aluno:
```python
{
  ID_Aluno: string
  Nome_Aluno: string
  Idade_Aluno: int
}
```
- HistoricoEscolar:
```python
{
  ID_HistoricoEscolar: int
  Nota: float
  Semestre: string
  Ano: int
}
```
- Materia:
```python
{
  ID_Materia: int
  Nome_Materia: string
  Prova: boolean
}
```
- Professor:
```python
{
  ID_Professor: string
  Nome_Professor: string
  Salario: int
}
```
- HistoricoProfessor:
```python
{
  ID_HistoricoProfessor: int
  Semestre: string
  Ano: int
  Quantidade_Aulas: int
}
```
- Curso:
```python
{
  ID_Curso: string
  Nome_Curso: string
  Horas_Extras: int
}
```
- Departamento:
```python
{
  Nome_Departamento: string
  Chefe_Departamento: string
}
```
- TCC:
```python
{
  ID_TCC: int
  Titulo: string
}
```

## Descrição das Relações entre os Nós
- a:Aluno -TEM-> he:HistoricoEscolar
```python
(a)-[:TEM]->(he)
```
- he:HistoricoEscolar -REFERENTE-> m:Materia
```python
(he)-[:REFERENTE]->(m)
```
- p:Professor -POSSUI-> hp:HistoricoProfessor
```python
(p)-[:POSSUI]->(hp)
```
- hp:HistoricoProfessor -REFERENCIA-> m:Materia
```python
(hp)-[:REFERENCIA]->(m)
```
- a:Aluno -CURSOU-> c:Curso
```python
(a)-[:CURSOU]->(c)
```
- d:Departamento -ORGANIZA-> p:Professor
```python
(d)-[:ORGANIZA]->(p)
```
- p:Professor -ORIENTADO-> t:TCC
```python
(p)-[:ORIENTADO]->(t)
```
- a:Aluno -FAZ-> t:TCC
```python
(a)-[:FAZ]->(t)
```
## Descrição das Relações nas Queries
- Query 1: a:Aluno -TEM-> he:HistoricoEscolar -REFERENTE-> m:Materia
```python
(a:Aluno)-[:TEM]->(he:HistóricoEscolar)-[:REFERENTE]->(m:Matéria)
```
- Query 2: p:Professor -POSSUI-> hp:HistoricoProfessor -REFERENCIA-> m:Materia
```python
(p:Professor)-[:POSSUI]->(hp:HistóricoProfessor)-[:REFERENCIA]->(m:Matéria)
```
- Query 3: a:Aluno -TEM-> he:HistoricoEscolar -CURSOU-> c:Curso
```python
(a:Aluno)-[:TEM]->(he:HistóricoEscolar), (a:Aluno)-[:CURSOU]->(c:Curso)
```
- Query 4: d:Departamento -ORGANIZA-> p:Professor
```python
(d:Departamento)-[:ORGANIZA]->(p:Professor)
```
- Query 5: a:Aluno -FAZ-> t:TCC <-ORIENTADO- p:Professor
```python
(a:Aluno)-[:FAZ]->(t:TCC)<-[:ORIENTADO]-(p:Professor)
```





