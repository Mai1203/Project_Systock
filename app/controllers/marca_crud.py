from sqlalchemy.orm import Session
from app.models.productos import Marcas


# Crear una nueva marca
def crear_marca(db: Session, nombre: str):
    """
    Crea una nueva marca.
    :param db: Sesión de base de datos.
    :param nombre: Nombre de la marca.
    :return: Objeto Marcas creado.
    """
    nueva_marca = Marcas(Nombre=nombre)
    db.add(nueva_marca)
    db.commit()
    db.refresh(nueva_marca)
    return nueva_marca


# Obtener todas las marcas
def obtener_marcas(db: Session):
    """
    Obtiene todas las marcas.
    :param db: Sesión de base de datos.
    :return: Lista de objetos Marcas.
    """
    return db.query(Marcas).all()


# Obtener una marca por ID
def obtener_marca_por_id(db: Session, id_marca: int):
    """
    Obtiene una marca por su ID.
    :param db: Sesión de base de datos.
    :param id_marca: ID de la marca.
    :return: Objeto Marcas o None si no existe.
    """
    return db.query(Marcas).filter(Marcas.ID_Marca == id_marca).first()


# Actualizar una marca
def actualizar_marca(db: Session, id_marca: int, nombre: str = None):
    """
    Actualiza una marca existente.
    :param db: Sesión de base de datos.
    :param id_marca: ID de la marca a actualizar.
    :param nombre: Nuevo nombre de la marca (opcional).
    :return: Objeto Marcas actualizado o None si no existe.
    """
    marca_existente = db.query(Marcas).filter(Marcas.ID_Marca == id_marca).first()
    if not marca_existente:
        return None

    if nombre is not None:
        marca_existente.Nombre = nombre

    db.commit()
    db.refresh(marca_existente)
    return marca_existente


# Eliminar una marca
def eliminar_marca(db: Session, id_marca: int):
    """
    Elimina una marca por su ID.
    :param db: Sesión de base de datos.
    :param id_marca: ID de la marca a eliminar.
    :return: True si se eliminó correctamente, False si no se encontró.
    """
    marca_existente = db.query(Marcas).filter(Marcas.ID_Marca == id_marca).first()
    if not marca_existente:
        return False

    db.delete(marca_existente)
    db.commit()
    return True
