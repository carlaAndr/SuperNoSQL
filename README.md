# Superhéroe
Proyecto Otoño 2023

![Superhéroe](super.jpg)

# Equipo 

Carla Andrea Sosa Peralta 200035

Santiago Villaseñor Ramírez 201427

Santiago Olvera Moreno 194701

# Objetivo

Que los alumnos muestren el entendimiento y capacidad de manejo de las diferentes bases de datos que vimos en el semestre, así como los conceptos relacionados con API's, ETL's, etc.

# Planteamiento

Buscar alguna API que llame la atención al equipo, con esta API, conectarla através de python con una base de datos MongoDB. Posteriormente, hacer un ETL que cargue la base de datos procesada  a una base de datos estilo grafo y una base columnar; evidentemente las transformaciones y los subconjuntos de datos ocupados serán diferentes para cada base de datos ya que tienen fines diferentes cada una.

# Implementación

## API usada

Utilizamos la API : Superhéroes
 ```bash
  https://superheroapi.com
 ```
## Extract y Load en Mongo (SuperMongo2.py)
1. Utilzamos la libreria request para conectamos al API usando un private key que esta en el archivo de python.
2. Extrajimos de froma local un json de la información, nos conectamos al contenedor de Mongo y vaciamos los datos en la colección llamada super_col.

## Extract Transform y Load en Cassandra (SuperCassandra.py)
1. Ya que la base datos esta en el contenedor de Mongo DB, nos conectamos al puerto de del contenedor de Mongo y extrajimos la base datos que contenia en la colección 'super_col'
2. Estandarizamos los datos para que no hubiera datos tipo null, '-' o vacios. Los remplazamos por un valor numérico de 0 o con el lable de 'Unknown en caso de ser necesario.
3. Eliminamos las columnas que contenian mucho texto, como lo son 'connections.group-affiliation' y 'connections.relatives'. También eliminamos columnas que no nos proporcionaban información como la de 'image.url'
4. Cambiamos los nombres de la columnas de 'powerstats.intelligence' a 'Intelligence. Esto para que pudiera ser más fácil la lectura.
5. Por último, nos conectamos al contenedor de cassandra y vaciamos la base de datos usando el Key de supers y nombrando a la tabla columnar superheros.

## Extract Transform y Load en Neo4J (updataneo.py y LimpiezaNeo.ipynb)
1. Utilizamos un csv obtenido la API directamente ya normalizado.
2. De ahí se hizo una división utilizando DataFrames para cada clase de dato (character, powerstats,...) para que cada uno termine siendo un nodo en Neo4j.
3. Se agrega el id a todas las tablas para implementar la relación.
4. Cambiamos cada nombre de las columnas para que quitar información extra (ejemplo: powerstats.durability -> durability).
5. Finalmente, se suben las tablas a Neo4j (usuario: Neo4j password: 12345678), creando relaciones de cada atributo del superhéroe a su nombre.
  

# ¿Cómo utilizarla?
1. Clonar el repo.
2. Posicionarse en ese directorio.
3. Correr el comando
  ```bash
  docker compose up -d
  ```
4. Ejecutar mongo
  ```bash
  #Comando para ejecutar Cassandra
  docker exec -it supernosql-mongo-1 mongosh
  use super
  ```
   
5. Realizar las consultas (Se encuentren en Queries Final para MongoDB).

6. Ejecutar Cassandra con el comando
  ```bash
  #Comando para ejecutar Cassandra
  docker exec -it supernosql-cassandra-1 cqlsh
  #Entra a la base de datos
  use supers;
  ```
7. Realizar las consultas (Se encuentren en Queries Final para Cassandra).

8. Ejecutar Neo 4J con el comando en un buscador (TARDA)
  ```bash
localhost:7474  
  ```
- user: neo4j
- pasword: 12345678

9. Realizar las consultas (Se encuentren en Queries Final para Neo4j).
   
 

