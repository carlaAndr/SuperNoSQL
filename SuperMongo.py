import pandas 
import requests
import pymongo
from pymongo import MongoClient
import json


token='6622488331213745'
url= 'https://www.superheroapi.com/api.php/'+token

# Conexión a MongoDB
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
super_db = mongo_client["super"]
super_col = doggo_db["supers"]

# Obtener datos de la API
superheroes=[requests.get(f"{base_url}/{i}") for i in range(1,152)]

# Insertar datos en MongoDB
for super in superh:
    print(supers.json())
    super_col.insert_one(supers.json())
                         
