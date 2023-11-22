import pandas 
import requests
import pymongo
from pymongo import MongoClient
import json

url="https://api.thedogapi.com/v1/images/search?limit=100&api_key=live_5OtO3lqVASaXYYhkRjxgj7JV3rHrxrcA4pCJvG7SobwVUpUVuvw4Vp4iRrjblhQk"
#Análisis de las bases de datos: images/id/analisis?api_key
# Conexión a MongoDB
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
doggo_db = mongo_client["Doggo"]
doggo_col = doggo_db["dogs"]

# Obtener datos de la API
response = requests.get(url)
dogs_data = response.json()

# Insertar datos en MongoDB
for dog in dogs_data:
    print("Inserting:", dog)
    doggo_col.insert_one(dog)
