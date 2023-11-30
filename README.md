# Superhéroe
Proyecto Otoño 2023

![Superhéroe](super.jpg)

# Equipo 

Carla

Santiago Villaseñor Ramírez

Santiago Olvera Moreno

# Objetivo

Que los alumnos muestren el entendimiento y capacidad de manejo de las diferentes bases de datos que vimos en el semestre, así como los conceptos relacionados con API's, ETL's, etc.

# Planteamiento

Buscar alguna API que llame la atención al equipo, con esta API, conectarla através de python con una base de datos MongoDB. Posteriormente, hacer un ETL que cargue la base de datos procesada  a una base de datos estilo grafo y una base columnar; evidentemente las transformaciones y los subconjuntos de datos ocupados serán diferentes para cada base de datos ya que tienen fines diferentes cada una.

# Implementacion

## API usada

Utilizamos la API : Superhéroes
 ```bash
  https://superheroapi.com
 ```
## Extracción y Load en Mongo (SuperMongo2.py)
1. Utilzamos la libreria request para conectamos al API usando un private key que esta en el archivo de python.
2. Extrajimos de froma local un json de la información, nos conectamos al contenedor de Mongo y vaciamos los datos en la colección llamada super_col.

## Extract Transform y Load en Cassandra (SuperCassandra.py)
1. Ya que la base datos esta en el contenedor de Mongo DB, nos conectamos al puerto de del contenedor de Mongo y extrajimos la base datos que contenia en la colección 'super_col'
2. Estandarizamos los datos para que no hubiera datos tipo null, '-' o vacios. Los remplazamos por un valor numérico de 0 o con el lable de 'Unknown en caso de ser necesario.
3. Eliminamos las columnas que contenian mucho texto, como lo son 'connections.group-affiliation' y 'connections.relatives'. También eliminamos columnas que no nos proporcionaban información como la de 'image.url'
4. Cambiamos los nombres de la columnas de 'powerstats.intelligence' a 'Intelligence. Esto para que pudiera ser más fácil la lectura.
5. Por último, nos conectamos al contenedor de cassandra y vaciamos la base de datos usando el Key de supers y nombrando a la tabla columnar superheros.

   
## Extract Transform y Load en Neo4J (updataneo.py)
1.v 
2.
  

# ¿Cómo utilizarla?
1. Clonar el repo.
2. Posicionarse en ese directorio.
3. Descarga los CSV al mismo directorio (los quitamos de Git para que fuera más ligero)
  ```bash
  https://itam2-my.sharepoint.com/:f:/g/personal/csosaper_itam_mx/EuiY9jdQ0e9Lm2R2HQC9xoEBWzgDw7w6Fbqpp4YBBYd_3A?e=9GAthD
  ```
4. Correr el comando
  ```bash
  docker compose up -d
  ```
5. Ejecutar mongo
  ```bash
  docker exec -it supernosql-mongo-1 mongosh
  ```
   
6. Realizar las consultas (Se encuentren en Queries Final para MongoDB).

7. Ejecutar Cassandra con el comando
  ```bash
  #Comando para ejecutar Cassandra
  docker exec -it supernosql-cassandra-1 cqlsh
  #Entra a la base de datos
  use supers;
  ```
8. Realizar las consultas (Se encuentren en Queries Final para Cassandra).

9. Ejecutar Neo 4J con el comando en un buscador (TARDA)
  ```bash
localhost:7474  
  ```
user neo4j
pasword 12345678

10. Realizar las consultas (Se encuentren en Queries Final para Neo4j).
   
 

