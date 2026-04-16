import bcrypt
import jwt
from datetime import timezone , timedelta , datetime
import os

SECRET_KEY=os.getenv("SECRET_KEY","dev-secret-change-me")
ALGORITHM="HS256"

def hash_password(password:str)-> str:
    return bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()

def verify_password(password,hashed)->bool:
    return bcrypt.checkpw(password.encode(),hashed.encode())

def create_access_token(user_id:int)->str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub":str(user_id),
        "iat":int(now.timestamp()),
        "exp":now+timedelta(minutes=60)
    }
    return jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)