import bcrypt
import jwt
from datetime import timezone , timedelta , datetime
import os
from fastapi.security import HTTPBearer

http_bearer=HTTPBearer()
http_bearer_optional=HTTPBearer(auto_error=False)
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

def get_current_user_id_from_token(token:str)->int:
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise ValueError("Invalid token: missing subject")
        return int(user_id)
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, ValueError) as e:
        raise ValueError(f"Invalid token: {str(e)}")