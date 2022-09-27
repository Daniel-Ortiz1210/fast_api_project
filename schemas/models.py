from typing import Optional, List
from enum import Enum
from datetime import date,datetime
import re

from pydantic import BaseModel, Field, PositiveInt, EmailStr, validator, ValidationError


def normalize_user_names(name: str) -> str:
    if re.findall("[+]", name):
        return ValueError("Nombre inválido")
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
    
    curp: Optional[str] = Field(None, title="Clave Unica de Registro de Poblacion", max_length=18, min_length=18)
    rfc: Optional[str] = Field(None, title="Registro Federal del Contribuyente", max_length=13, min_length=13)
    cp: Optional[str] = Field(None, title="Codigo Postal", max_length=5, min_length=5)
    telephone: Optional[str] = Field(None, max_length=10, min_length=10)
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
    
    @validator('cp', pre=True)
    def validate_cp(cls, v) -> str:
        if len(v) != 5:
            raise ValueError("El formato oficial son 5 caracteres")

        if re.findall("^00", v) or re.findall("[+]", v) or re.findall("[a-zA-Z]", v):
            raise ValueError("Codigo Postal inválido")
        
        return v
    
    @validator("curp", pre=True)
    def validate_curp(cls, v):

        if len(v) != 18:
            raise ValueError("El formato oficial son 18 caracteres")

        first_4_chars = v[:4]
        intermediate_chars = v[4:10]

        if re.findall("[0-9]", first_4_chars) or re.findall("[a-zA-Z]", intermediate_chars) or re.findall("[$&+,:;=?@#|'<>.^*()%!-]", v):
            raise ValueError("CURP no cumple con el formato oficial")
        
        return v

    @validator("rfc", pre=True)
    def validate_rfc(cls, v):
        if len(v) != 13:
            raise ValueError("El formato ofical son 13 caracteres")
        
        first_4_chars = v[:4]
        intermediate_chars = v[4:10]

        if re.findall("[0-9]", first_4_chars) or re.findall("[a-zA-Z]", intermediate_chars) or re.findall("[$&+,:;=?@#|'<>.^*()%!-]", v):
            raise ValueError("CURP no cumple con el formato oficial")
        
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
