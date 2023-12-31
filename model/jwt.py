import os
from dotenv import load_dotenv
load_dotenv()
import jwt
import datetime

jwt_secret_key = os.getenv("JWT_SECRET_KEY")
jwt_algorithm = os.getenv("JWT_ALGORITHM")

def jwt_encode(person_information):
    idPerson = person_information["id_people"]
    name = person_information["name"]
    email = person_information["email"]
    secret_key = jwt_secret_key
    payload = {"data": {
        "id": idPerson, "email": email, "name": name},
        "iat": datetime.datetime.utcnow(),
        "exp": (datetime.datetime.utcnow() + datetime.timedelta(days = 7))
    }
    token = jwt.encode(payload, secret_key, algorithm=jwt_algorithm)
    return token

def jwt_decode(get_token):
    secret_key = jwt_secret_key
    decode_token = jwt.decode(get_token, secret_key, algorithms = jwt_algorithm)
    return decode_token