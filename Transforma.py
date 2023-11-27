from pymongo import MongoClient

# Conexión a MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["super"]
collection = db["supers"]

# Lista de campos a convertir
fields_to_convert = ["intelligence", "strength", "speed", "durability", "power", "combat"]

# Actualizar documentos en la colección supers
docs_to_update = collection.find({"powerstats": {"$exists": True}})
for doc in docs_to_update:
    for field in fields_to_convert:
        field_value = doc["powerstats"].get(field, "0")

        # Manejar el caso en que field_value sea 'null'
        if field_value == 'null':
            updated_value = 0
        else:
            updated_value = int(field_value)

        collection.update_one(
            {"_id": doc["_id"]},
            {"$set": {f"powerstats.{field}": updated_value}}
        )

print("Actualización completada.")
