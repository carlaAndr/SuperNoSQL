import pandas 
import requests
import pymongo
from pymongo import MongoClient
import json


token=1##Aqui se debe incluir el token proporcionado
url= 'https://www.superheroapi.com/api.php/'+token


try:
    mongo_client = MongoClient("mongodb://supernosql-mongo-1:27017/")
    print("Conexión exitosa a MongoDB")
except Exception as e:
    print(f"Error en la conexión a MongoDB: {e}")
# Conexión a MongoDB

super_db = mongo_client["super"]
super_col = super_db["supers"]

# Obtener datos de la API
superheroes=[requests.get(f"{url}/{i}") for i in range(1,152)]

# Insertar datos en MongoDB
for super in superheroes:
    print(super.json())
    super_col.insert_one(super.json())
                         
