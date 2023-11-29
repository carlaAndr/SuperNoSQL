# Superhéroe
Proyecto Otoño 2023
Utilizando la API : Superhéroes
 ```bash
  https://www.superheroapi.com/api.php/
 ```
1. La API se vacía en un Datalake en Mongo.
   
2. Se transforma la base de datos a Cassandra.
  
3. Se crea un grafo en Neo4J.

## ¿Cómo utilizarla?
1. Clonar el repo.
2. Posicionarse en ese directorio.
3. Descarga los CSV al mismo directorio (los quitamos de Git para que fuera más ligero)
  ```bash
  https://itam2-my.sharepoint.com/:f:/g/personal/csosaper_itam_mx/EuiY9jdQ0e9Lm2R2HQC9xoEBWzgDw7w6Fbqpp4YBBYd_3A?e=9GAthD
  ```
5. Correr el comando
  ```bash
  docker compose up -d
  ```
4. Ejecutar mongo
  ```bash
  docker exec -it supernosql-mongo-1 mongosh
  ```
   
5. Realizar las consultas (Se encuentren en Queries).

6. Ejecutar Cassandra con el comando
  ```bash
  #Comando para ejecutar Cassandra
  ```
7. Ejecutar Neo 4J con el comando
  ```bash
  #Comando para ejecutar Neo 4J
  ```
   
 

