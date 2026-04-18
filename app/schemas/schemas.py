from pydantic import BaseModel,EmailStr,Field

class SignUpRequest(BaseModel):
    email:EmailStr
    username:str
    password:str
    
class LoginRequest(BaseModel):
    email:EmailStr
    password:str

class TicketCreate(BaseModel):
    subject:str = Field(...,max_length=100)
    body:str = Field(...,max_length=10000)