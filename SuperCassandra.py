import pandas as pd
import requests
import pymongo
from pymongo import MongoClient
import json
from cassandra.cluster import Cluster
import tarfile
import csv
import re
import os
import time


time.sleep(50)  # Pausa la ejecución por 50 segundos para que Cassandra termine de inicializarse
# Conectando con el servidor de MongoDB
mongo_client = pymongo.MongoClient("mongodb://supernosql-mongo-1:27017/")
super_db = mongo_client["super"]
super_col = super_db["supers"]

# Obtener los documentos de la colección.
documents = super_col.find()

# Conviertiendo los documentos en diccionarios
documents_list = [doc for doc in documents]

# Convertir el JSON a un DataFrame de Pandas
df = pd.json_normalize(documents_list)

# Quitmaos las columans que consideramos que no se van a utilizar para los queries
df.drop(['_id','response','id','biography.aliases','biography.first-appearance', 'work.occupation','work.base','connections.group-affiliation','connections.relatives','image.url','biography.place-of-birth'],axis=1,inplace=True)

# Función para extraer solo los centímetros y los kilogramos
def extract_num(text):
    word=text[1]
    cm=re.findall(r'\d+', word)
    return int(cm[0]) 
# Aplicar la función a la columna 'appearance.height' para extraer solo los centímetros
df['appearance.height'] = df['appearance.height'].apply(lambda x: extract_num(x) if x != 'nan' else None)
df['appearance.weight'] = df['appearance.weight'].apply(lambda x: extract_num(x) if x != 'nan' else None)

# Función para cambiar los nulls por 0 en los power stats
def change_null(text):
    if text=='null':
        return 0
    else:
        return int(text)

columns_to_change = ['powerstats.intelligence', 'powerstats.strength', 'powerstats.speed', 'powerstats.durability', 'powerstats.power', 'powerstats.combat']
df[columns_to_change] = df[columns_to_change].apply(lambda col: col.map(change_null))

# Función para cambiar los nulls por Unknown de appearance
def change_null_txt(text):
    if text=='null':
        return 'Unknown'
    else:
        return text
df['appearance.race'] = df['appearance.race'].apply(lambda x: change_null_txt(x))

# Función para cambiar los vacios por Unknown de biography
def change_blank(text):
    if text=='':
        return 'Unknown'
    else:
        return text
columns_to_change = ['biography.full-name', 'biography.publisher']
df[columns_to_change] = df[columns_to_change].apply(lambda col: col.map(change_blank))

# Función para cambiar los - por Unknown de biography y appearance
def change_sign(text):
    if text=='-':
        return 'Unknown'
    else:
        return text
columns_to_change = ['biography.full-name','biography.alignment','appearance.gender','appearance.eye-color','appearance.hair-color']
df[columns_to_change] = df[columns_to_change].apply(lambda col: col.map(change_sign))

# Función para poner en mayuscula la primera palabra del los datos que son string
def capitalize(text):
    return text.capitalize()
columns_to_change = ['name','biography.full-name','biography.alter-egos','biography.publisher','biography.alignment','appearance.gender','appearance.race','appearance.eye-color','appearance.hair-color']
df[columns_to_change] = df[columns_to_change].apply(lambda col: col.map(capitalize))

#Funcion para poenr los nombres de las columnas con mayúscula al inicio y eliminando palabras que no brindan información
nuevos_nombres=['Name', 'Intelligence', 'Strength', 'Speed', 'Durability', 'Power', 'Combat', 'FullName', 'AlterEgos', 'Publisher', 'Alignment', 'Gender', 'Race', 'Height', 'Weight', 'EyeColor', 'HairColor']
df.columns=nuevos_nombres

print("Transfom complete")

#Mandamos el dataframe a un csv
df.to_csv('supers.csv', header=True, sep=',', index=False)
print("intentar conectar")
# Conectar al cluster de Cassandra
cluster = Cluster(['supernosql-cassandra-1'], port=9042)
session = cluster.connect()


# Crear keyspace si no existe
session.execute("CREATE KEYSPACE IF NOT EXISTS supers WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}")

# Utilizar el keyspace 'supers'
session.set_keyspace('supers')

# Crear tabla en el keyspace 'supers' si no existe
create_table_query = '''
    CREATE TABLE IF NOT EXISTS supers.superheros (
        Name TEXT PRIMARY KEY,
        Intelligence INT,
        Strength INT,
        Speed INT,
        Durability INT,
        Power INT,
        Combat INT,
        FullName TEXT,
        AlterEgos TEXT,
        Publisher TEXT,
        Alignment TEXT,
        Gender TEXT,
        Race TEXT,
        Height INT,
        Weight INT,
        EyeColor TEXT,
        HairColor TEXT
    )
'''
session.execute(create_table_query)

# Leer el archivo CSV y cargar los datos en la tabla
with open('supers.csv', 'r', newline='', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    header = next(csv_reader)  # Obtener encabezados/columnas

    for row in csv_reader:
        # Convertir valores a entero si es posible, de lo contrario, mantener el valor original
        converted_row = [int(value) if value.isdigit() else value for value in row]    
        insert_query = f"INSERT INTO supers.superheros (Name, Intelligence, Strength, Speed, Durability, Power, Combat, FullName, AlterEgos, Publisher, Alignment, Gender, Race, Height, Weight, EyeColor, HairColor) VALUES ({', '.join(['%s'] * len(header))})"
        session.execute(insert_query, converted_row)

print("Datos del archivo CSV cargados en la tabla 'superheros' de Cassandra.")
print('Load completed')



