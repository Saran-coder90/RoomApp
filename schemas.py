from pydantic import BaseModel
from typing import Optional, Dict

class Register(BaseModel):
    name : str
    email : str 
    password : str
    
class Login(BaseModel):
    email : str
    password : str

    class Config:
        orm_mode = True

class StoreTransaction(BaseModel):
    email : str
    amount : float
    reason : str

    class Config:
        orm_mode = True

class Response(BaseModel):
    status : str 
    statusCode : int
    data : dict
    message : str

    class Config:
        orm_mode = True
