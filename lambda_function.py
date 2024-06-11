import json
from mongo import get_credentials, encrypt_data, decrypt_data

def lambda_handler(event, context):
    action = event.get("action")
    if action == 1:
        return credentials_bd(event, context)
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'message': 'Invalid action'
            })
        }

def credentials_bd(event, context):
    domain = event ["domain"]
    #print("DOMAIN", domain)
    if not domain:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'message': 'Domain not provided'
            })
        }
    credentials_bd  = get_credentials(domain)
    if credentials_bd:
        # Cifrar las credenciales
        encrypted_credentials_bd = encrypt_data(credentials_bd)
        print("Datos encriptados:", encrypted_credentials_bd)
        # Descifrar las credenciales (opcional)
        #decrypted_credentials_bd = decrypt_data(encrypted_credentials_bd)
        #print("Datos descifrados:", decrypted_credentials_bd)
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Hello from Lambda!',
                'data': encrypted_credentials_bd.decode('utf-8')
            })
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({
                'message': 'Credentials not found for the given domain' 
            })
        }
    
# Test the function
response = lambda_handler({"action": 1, "domain": "romario6.com.co"}, None)
print(response)
