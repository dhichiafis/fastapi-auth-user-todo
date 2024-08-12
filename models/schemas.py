from typing import List 
from pydantic import BaseModel 


class ItemCreate(BaseModel):
    title:str 
    description:str 
    
class ItemList(ItemCreate):
    id:int 
    owner_id:int 
    
    class Config:
        orm_mode=True 
        
        
class UserCreate(BaseModel):
    username:str 
    password:str 
    
class UserList(UserCreate):
    id:int 
    items:list[ItemList]=[]
    
    class Config:
        orm_mode=True 
        
        

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
        