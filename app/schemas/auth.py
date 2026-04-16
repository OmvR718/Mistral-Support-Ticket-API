from pydantic import BaseModel,EmailStr

class SignUpRequest(BaseModel):
    email:EmailStr
    username:str
    password:str
    
class LoginRequest(BaseModel):
    email:EmailStr
    password:str