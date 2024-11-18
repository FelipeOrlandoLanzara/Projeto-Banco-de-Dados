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

# Banco Wide-column Store (Cassandra)

## Passos para executar o programa
- Antes de fazer o download do arquivo zip do projeto, deve-se primeiro, fazer a instalação das bibliotecas ```cassandra-driver``` e ```Faker``` através do comando ```pip install```.
- Criar um ```acessCassandra.json``` na pasta ```Wide-ColumnStore``` com as seguintes instruções: ```clientId```, ```secret``` e o ```token``` do seu servidor.
- Fazer o Dowload do arquivo zip de conexão do servidor (DataStax), Ex.: secure-connect-faculdade.zip
- Nome do keyspace do servidor: ```faculdade``` o servidor deverá ser criado do tipo ```Serverless (Non-Vector)```.

![image](https://github.com/jvgoverna/Projeto-Banco-de-Dados/blob/main/Conexao%20Cassandra.png)

![image](https://github.com/jvgoverna/Projeto-Banco-de-Dados/blob/main/Nome%20do%20arquivo%20ZIP%20de%20conexao%20do%20banco.png)

# Banco GraphDatabase (Neo4j)

## Passos para executar o programa
- Antes de fazer o download do arquivo zip do projeto, deve-se primeiro, fazer a instalação das bibliotecas ```neo4j``` e ```Faker``` através do comando ```pip install```.
- Criar um ```acessNeo4j``` na pasta ```GraphDatabase``` com as seguintes instruções: ```uri```, ```user``` e ```password```do seu servidor.
- Protocolo de Conexão: ```neo4j+```.

![image](https://github.com/jvgoverna/Projeto-Banco-de-Dados/blob/main/Conexao%20Neo4j.png)
