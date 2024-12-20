from sqlalchemy.orm import Session
from app.models.facturas import TipoFactura  # Ajusta la ruta según tu estructura


# Crear un tipo de factura
def crear_tipo_factura(db: Session, nombre: str):
    """
    Crea un nuevo tipo de factura.
    :param db: Sesión de base de datos.
    :param nombre: Nombre del tipo de factura (Factura A, Factura B).
    :return: Objeto de tipo de factura creado.
    """
    nuevo_tipo = TipoFactura(Nombre=nombre)
    db.add(nuevo_tipo)
    db.commit()
    db.refresh(nuevo_tipo)
    return nuevo_tipo


# Obtener todos los tipos de factura
def obtener_tipos_factura(db: Session):
    """
    Obtiene la lista de todos los tipos de factura.
    :param db: Sesión de base de datos.
    :return: Lista de tipos de factura.
    """
    return db.query(TipoFactura).all()


# Obtener un tipo de factura por ID
def obtener_tipo_factura_por_id(db: Session, id_tipo_factura: int):
    """
    Obtiene un tipo de factura por su ID.
    :param db: Sesión de base de datos.
    :param id_tipo_factura: ID del tipo de factura.
    :return: Objeto de tipo de factura o None si no existe.
    """
    return (
        db.query(TipoFactura)
        .filter(TipoFactura.ID_Tipo_Factura == id_tipo_factura)
        .first()
    )


# Actualizar un tipo de factura
def actualizar_tipo_factura(db: Session, id_tipo_factura: int, nombre: str = None):
    """
    Actualiza un tipo de factura existente.
    :param db: Sesión de base de datos.
    :param id_tipo_factura: ID del tipo de factura a actualizar.
    :param nombre: Nuevo nombre del tipo de factura.
    :return: Objeto de tipo de factura actualizado o None si no existe.
    """
    tipo_existente = (
        db.query(TipoFactura)
        .filter(TipoFactura.ID_Tipo_Factura == id_tipo_factura)
        .first()
    )
    if not tipo_existente:
        return None

    if nombre:
        tipo_existente.Nombre = nombre

    db.commit()
    db.refresh(tipo_existente)
    return tipo_existente


# Eliminar un tipo de factura
def eliminar_tipo_factura(db: Session, id_tipo_factura: int):
    """
    Elimina un tipo de factura por su ID.
    :param db: Sesión de base de datos.
    :param id_tipo_factura: ID del tipo de factura a eliminar.
    :return: True si se eliminó correctamente, False si no se encontró.
    """
    tipo_existente = (
        db.query(TipoFactura)
        .filter(TipoFactura.ID_Tipo_Factura == id_tipo_factura)
        .first()
    )
    if not tipo_existente:
        return False

    db.delete(tipo_existente)
    db.commit()
    return True
