import jwt

key = 'something_secret_key'

def generate_access_token(payload):
    return jwt.encode(payload, key, algorithm='HS256')

def get_payload_from_access_token(token):
    return jwt.decode(token, key, algorithms='HS256')
