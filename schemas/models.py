# Pydantic
from pydantic import BaseModel, Field, PositiveInt, EmailStr, validator, ValidationError
from typing import Optional, List
from enum import Enum
from datetime import date,datetime


def normalize_user_names(name: str) -> str:
    return name.title()

class UserType(str, Enum):
    admin = "admin"
    staff = "staff"
    basic = "basic"


class User(BaseModel):
    id: Optional[int] = Field()
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr = Field(..., title="Email")
    password: str = Field(..., min_length=8, max_length=50, title="Constraseña")
    
    curp: Optional[str] = Field(None, title="Clave Unica de Registro de Poblacion")
    rfc: Optional[str] = Field(None, title="Registro Federal del Contribuyente")
    cp: Optional[str] = Field(None, title="Codigo Postal")
    telephone: Optional[str] = Field(None, max_length=10)
    user_type: Optional[UserType] = Field(UserType.basic, title="Tipo de usuario")
    date: Optional[datetime] = Field(datetime.now(), title="Fecha")
    age: Optional[PositiveInt] = Field(None,title="Edad")

    _normalize_first_name = validator("first_name", allow_reuse=True, always=True)(normalize_user_names)
    _normalize_last_name = validator("last_name", allow_reuse=True, always=True)(normalize_user_names)
    

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
    
    @validator('cp')
    def validate_first_2_chars(cls, v):
        if v is None: return None
        
        if v[:2] == '00':
            raise ValueError("Los primeros dos caracteres no deben ser '00'")
        if len(v) < 5 or len(v) > 5:
            raise ValueError("La longitud requerida son 5 caracteres")
        
        return v
    


        



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
