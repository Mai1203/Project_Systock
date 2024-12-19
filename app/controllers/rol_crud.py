from sqlalchemy.orm import Session
from app.models.usuarios import Rol


# Crear un rol
def crear_rol(db: Session, nombre: str):
    """
    Crea un nuevo rol.
    :param db: Sesión de base de datos.
    :param nombre: Nombre del rol.
    :return: Objeto del rol creado.
    """
    nuevo_rol = Rol(Nombre=nombre)
    db.add(nuevo_rol)
    db.commit()
    db.refresh(nuevo_rol)
    return nuevo_rol


# Obtener todos los roles
def obtener_roles(db: Session):
    """
    Obtiene la lista de todos los roles.
    :param db: Sesión de base de datos.
    :return: Lista de roles.
    """
    return db.query(Rol).all()


# Obtener un rol por ID
def obtener_rol_por_id(db: Session, id_rol: int):
    """
    Obtiene un rol por su ID.
    :param db: Sesión de base de datos.
    :param id_rol: ID del rol.
    :return: Objeto del rol o None si no existe.
    """
    return db.query(Rol).filter(Rol.ID_Rol == id_rol).first()


# Actualizar un rol
def actualizar_rol(db: Session, id_rol: int, nombre: str):
    """
    Actualiza un rol existente.
    :param db: Sesión de base de datos.
    :param id_rol: ID del rol a actualizar.
    :param nombre: Nuevo nombre del rol.
    :return: Objeto del rol actualizado o None si no existe.
    """
    rol_existente = db.query(Rol).filter(Rol.ID_Rol == id_rol).first()
    if not rol_existente:
        return None

    rol_existente.Nombre = nombre
    db.commit()
    db.refresh(rol_existente)
    return rol_existente


# Eliminar un rol
def eliminar_rol(db: Session, id_rol: int):
    """
    Elimina un rol por su ID.
    :param db: Sesión de base de datos.
    :param id_rol: ID del rol a eliminar.
    :return: True si se eliminó correctamente, False si no se encontró.
    """
    rol_existente = db.query(Rol).filter(Rol.ID_Rol == id_rol).first()
    if not rol_existente:
        return False

    db.delete(rol_existente)
    db.commit()
    return True
