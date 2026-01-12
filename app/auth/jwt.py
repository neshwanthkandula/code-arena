from jose import jwt 
from datetime import datetime, timedelta

SECRET_KEY = "super_secret_key"
AlGORITHM = "HS256"
EXPIRE_HOURS = 24

def create_jwt(user_id : int)->str:
    payload  = {
        "sub" : str(user_id),
        "exp" : datetime.utcnow() + timedelta(hours=EXPIRE_HOURS)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=AlGORITHM)


def decode_jwt(token : str)->int:
    return jwt.decode(token, SECRET_KEY , algorithms=[AlGORITHM])