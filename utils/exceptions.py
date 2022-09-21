from fastapi import HTTPException, status


def user_not_found_excep():
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"El usuario no existe")