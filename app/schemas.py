from pydantic import BaseModel, EmailStr
from datetime import datetime

class PostBase(BaseModel):
    title :  str
    content : str
    published : bool = True
   
class UserBase(BaseModel):
    email : EmailStr
    password : str
    
class CreatePost(PostBase):
    pass

class CreateUser(UserBase):
    pass

class Post(PostBase):
   id: int
   created_at: datetime
   class Config:
       orm_mode = True

class User(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

class UpdateUserPassword(BaseModel):
    password: str

class UpdateUserEmail(BaseModel):
    email:EmailStr

class UserLogin(BaseModel):
    email : EmailStr
    password : str