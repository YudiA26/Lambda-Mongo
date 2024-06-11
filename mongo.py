from pymongo import MongoClient
import json
from cryptography.fernet import Fernet
from bson import ObjectId

# Generar una clave de cifrado: key
key = b'generated key for encryption'
#key = Fernet.generate_key()
#print("key criptografía", key)
# Cifrar la clave con la clave de cifrado
cipher_suite = Fernet(key)

# Conexión a MongoDB
client = MongoClient('url connection with mongo')
# Selecciona la base de datos
db = client['name bd']

def get_credentials(domain): 
    # Define el pipeline
    pipeline = [
      {
          "$lookup": {
            "from": "db_connections",
            "localField": "connection_id",
            "foreignField": "_id",
            "as": "connection_data"
          }
      },
      { "$match" : { "domain" : domain } },
      { "$unwind": "$connection_data" },
      {
          "$project": {
            "schema_db": 1,
            "tenancy_id": 1,
            "connection_data.host": 1,
            "connection_data.port": 1,
            "connection_data.database": 1,
            "connection_data.user": 1,
            "connection_data.password": 1,
          }
      }
    ]
    # Ejecuta aggregate
    result = db.tenancy_db_connections.aggregate(pipeline)
    first_result = next(result, None)
    if first_result:
        data = first_result
        return data
    else:
        print("No se encontraron credenciales para el dominio dado.")
        return None

def encrypt_data(data):
    # Convertir ObjectId a cadenas
    data = convert_objectid_to_str(data)
    # Convierte el diccionario a una cadena JSON
    json_data = json.dumps(data)
    # Codifica la cadena JSON a bytes
    byte_data = json_data.encode('utf-8')
    # Cifra los bytes
    encrypted_data = cipher_suite.encrypt(byte_data)
    return encrypted_data

def decrypt_data(encrypted_data):
    cipher_suite = Fernet(key)
    # Descifrar los bytes
    decrypted_data = cipher_suite.decrypt(encrypted_data)
    # Decodificar los bytes a una cadena JSON
    json_data = decrypted_data.decode('utf-8')
    # Convertir la cadena JSON a un diccionario
    data = json.loads(json_data)
    return data

def convert_objectid_to_str(doc):