# Pydantic
from pydantic import BaseModel, Field, PositiveInt, EmailStr
from typing import Optional, List
from enum import Enum
from datetime import date,datetime

class UserType(str, Enum):
    admin = "admin"
    staff = "staff"
    basic = "basic"


class User(BaseModel):
    id: Optional[int] = Field()
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr = Field(..., title="User email")
    password: str = Field(..., min_length=8, max_length=50)
    
    curp: Optional[str] = Field(None, max_length=18)
    rfc: Optional[str] = Field(None, max_length=13)
    cp: Optional[str] = Field(None, max_length=5)
    telephone: Optional[str] = Field(None, max_length=10)
    user_type: Optional[UserType] = Field(UserType.basic, title="User Type")
    date: Optional[datetime] = Field(default=datetime.now())
    age: Optional[PositiveInt] = Field(default=None,title="User age")

    class Config:
        schema_extra = {
            "example": {
                "first_name": "Juan",
                "last_name": "Perez",
                "password": "password",
                "email": "juanp@ejemplo.com",
                
                "age": 20,
                "user_type": UserType.basic,
                "curp": "ARDFC123456098HGTY",
                "cp": "12345",
                "telephone": "5567678987",
                "rfc": "6543276787612"
            }
        }
        orm_mode = True


class LoginResponse(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field() 


class UserPatch(User):
    first_name: Optional[str] = Field(min_length=1, max_length=50)
    last_name: Optional[str] = Field(min_length=1, max_length=50)
    email: Optional[EmailStr] = Field(title="User email")
    password: Optional[str] = Field(min_length=8, max_length=50)
    curp: Optional[str] = Field(max_length=18)
    rfc: Optional[str] = Field(max_length=13)
    cp: Optional[str] = Field(max_length=5)
    telephone: Optional[str] = Field(max_length=10)
    date: Optional[datetime] = Field()
    user_type: Optional[str] = Field(title="User Type")
    age: Optional[PositiveInt] = Field(title="User age")


class UserResponse(User):
    password: str = Field()
