import json
from typing import Optional, List
from datetime import datetime, timedelta

from utils.exceptions import user_not_found_excep
from utils.auth import authenticate_user, generate_access_token
from utils.utils import update_obj_from_dict

from fastapi import APIRouter, Response, status
from fastapi import Body, Query, Path, Form, Cookie, Header, UploadFile, File, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from config.db import session
from config.models import UserTable

from schemas.models import User, UserType, LoginResponse, UserResponse, UserPatch

from hashing_mod import get_password_hash



user_router = APIRouter()

@user_router.post(path="/upload-imge", status_code=status.HTTP_201_CREATED)
def upload_image(image: UploadFile = File(...)):

    return {
        "filename": image.filename,
        "type": image.content_type,
        "size(kb)": round(len(image.file.read()) / 1024, 2) 
    }

@user_router.post(path="/login",status_code=status.HTTP_202_ACCEPTED, response_model=LoginResponse, response_model_exclude=["password"], tags=["Auth"])
async def login(email: str = Form(...), password: str = Form(...)):   
    return LoginResponse(email=email, password=password)

@user_router.post("/token", tags=["Auth"], status_code=status.HTTP_200_OK)
async def login_for_access_token(email: str = Form(...), password: str = Form(...)):
    """

    Autentificacion del usuario, generacion y devolucion del token jwt

    Args:
        email (str, mandatory): Email en texto plano. Defaults to Form(...).
        password (str, mandatory): Password en texto plano. Defaults to Form(...).

    Raises:
        user_not_found_excep: Si el usuario no es encontrado

    Returns:
        dict: Devolver json con el token jwt
    """
    user = authenticate_user(email=email, password=password, session=session)

    if not user:
        raise user_not_found_excep()
    
    token_expires = timedelta(minutes=30)
    token = generate_access_token(email=user.email, id=user.id, expires=token_expires)

    return {"token": token}

@user_router.get(path="/users", status_code=status.HTTP_200_OK, tags=["Users"], summary="Show All Users", response_model=List[UserResponse], response_model_exclude=["password"])
async def get_all_users(user_agent: Optional[str] = Cookie(None), header: Optional[str] = Header(None)):
    """
    Consultar todos los usuario registrados en la base de datos

    Returns:
        List[User]: Devolver lista de usuarios
    """
    return session.query(UserTable).all()

@user_router.post(path="/users/create", response_model=UserResponse, response_model_exclude=['password'], status_code=status.HTTP_201_CREATED, tags=["Users"])
async def create_user(
    user: User = Body(
        ...
        )
    ):
    """

    Creacion y almacenamiento de un nuevo usuario en la base de datos

    Args:
        user (User, mandatory): Defaults to Body( ... ).

    Returns:
        UserResponse: Usuario recien creado
    """
    user = user.dict()
    user["password"] = get_password_hash(user["password"])

    if user["user_type"] not in ["basic", "admin", "staff"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="MAL")

    try:
        new_user = UserTable(**user)
        session.add(new_user)
        session.commit()
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No pudimos crear el usuario")
    
    return new_user

@user_router.get(path="/users/{id}", status_code=status.HTTP_200_OK, tags=["Users"], summary="Show User", response_model=UserResponse, response_model_exclude=["password"])
async def get_user(
    id: int = Path(
        ...,
        title="Numeric User ID",
        gt=0,
        example=1
    )
    ):
    """
    Consultar un unico usuario en la base de datos

    Args:
        id (int, optional): ID del usuario. Defaults to Path( ..., title="Numeric User ID", gt=0, example=1 ).

    Raises:
        user_not_found_excep: Excepcion levantada si el usuario no es encontrada

    Returns:
        UserResponse:  
    """
    user = session.query(UserTable).filter(UserTable.id == id).one_or_none()

    if not user:
        raise user_not_found_excep()
        
    return user

@user_router.patch(path="/users/{id}/update", status_code=status.HTTP_202_ACCEPTED, tags=["Users"], summary="Update User", response_model=UserResponse, response_model_exclude=["password"])
async def update_user(
    id: int = Path(
        ...,
        title="Numeric User ID",
        gt=0,
        example=1
        ),
    request: UserPatch = Body(
        ...
        )
    ):
    """

    Actualización parcial de un usuario den la base de datos

    Args:
        id (int, optional): ID del usuario a actualizar. Defaults to Path( ..., title="Numeric User ID", gt=0, example=1 ).
        request (UserPatch, optional): Cuerpo de la peticion del clienta con los atributos a actualizar. Defaults to Body( ... ).

    Raises:
        user_not_found_excep: Excepcion leventada si el usuario no es encontrado en la base de datos

    Returns:
        UserResponse: Usuario actualizado
    """
    user = session.query(UserTable).filter(UserTable.id == id).one_or_none()

    if not user:
        raise user_not_found_excep()

    update_obj_from_dict(user, request.dict(), excl=["id"])
    
    session.commit()
    
    return user

@user_router.delete(path="/users/{id}/delete", status_code=status.HTTP_204_NO_CONTENT, tags=["Users"], summary="Show User")
async def delete_user(
    id: int = Path(
        ...,
        title="Numeric User ID",
        gt=0,
        example=1
    )
    ):
    """
    Eliminar un usuario de la base de datos

    Args:
        id (int, optional): ID del usuario. Defaults to Path( ..., title="Numeric User ID", gt=0, example=1 ).

    Raises:
        user_not_found_excep: Excepcion leventada si el usuario no es encontrado en la base de datos
    """
    user = session.query(UserTable).filter(UserTable.id == id).one_or_none()

    if not user:
        raise user_not_found_excep()
    
    session.delete(user)
    session.commit()