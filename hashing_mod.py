from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    """Hashing de password recibida en texto plano para su almacenaminto en DB

    Args:
        password (str): Password en texto plano

    Returns:
        srt: Password hasheada 
    """
    return bcrypt_context.hash(password)
