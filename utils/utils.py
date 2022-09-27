from hashing_mod import get_password_hash, bcrypt_context

def update_obj_from_dict(obj, dict, excl=[]):
    """
    Funcion para actualizar un objeto a partir de un diccionario.
    El objeto debe ser del tipo de un modelo de la base de datos.
    Las llaves del diccionario deben coincidir con los atributos (columnas) del modelo.
    El parametro excl es una lista con los atributos a ignorar, ej: id de un usuario.

    Args:
        obj (Query): Objeto a actualizar
        dict (Dict): Diccionario con los atributos a actualizar del obj
        excl (list, optional): Lista de atributos a ignorar. Defaults to [].
    """
    
    for k, v in dict.items():
        if k in excl or v == None: continue
        if k == "password": v = get_password_hash(v)
        setattr(obj, k, v)