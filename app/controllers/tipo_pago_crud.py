from sqlalchemy.orm import Session
from app.models.pago_credito import (
    TipoPago,
)  # Asegúrate de ajustar la importación de acuerdo a tu estructura de proyecto


# Crear un nuevo tipo de pago
def crear_tipo_pago(db: Session, nombre: str):
    """
    Crea un nuevo tipo de pago.
    :param db: Sesión de base de datos.
    :param nombre: Nombre del tipo de pago ('Abono' o 'Pago Total').
    :return: Objeto de tipo de pago creado.
    """
    if nombre not in ["Abono", "Pago Total"]:
        raise ValueError("El nombre del tipo de pago debe ser 'Abono' o 'Pago Total'")

    nuevo_tipo_pago = TipoPago(Nombre=nombre)
    db.add(nuevo_tipo_pago)
    db.commit()
    db.refresh(nuevo_tipo_pago)
    return nuevo_tipo_pago


# Obtener todos los tipos de pago
def obtener_tipos_pago(db: Session):
    """
    Obtiene la lista de todos los tipos de pago.
    :param db: Sesión de base de datos.
    :return: Lista de tipos de pago.
    """
    return db.query(TipoPago).all()


# Obtener un tipo de pago por ID
def obtener_tipo_pago_por_id(db: Session, id_tipo_pago: int):
    """
    Obtiene un tipo de pago por su ID.
    :param db: Sesión de base de datos.
    :param id_tipo_pago: ID del tipo de pago.
    :return: Objeto de tipo de pago o None si no existe.
    """
    return db.query(TipoPago).filter(TipoPago.ID_Tipo_Pago == id_tipo_pago).first()


# Actualizar un tipo de pago
def actualizar_tipo_pago(db: Session, id_tipo_pago: int, nombre: str = None):
    """
    Actualiza un tipo de pago existente.
    :param db: Sesión de base de datos.
    :param id_tipo_pago: ID del tipo de pago a actualizar.
    :param nombre: Nuevo nombre del tipo de pago ('Abono' o 'Pago Total').
    :return: Objeto de tipo de pago actualizado o None si no existe.
    """
    tipo_pago_existente = (
        db.query(TipoPago).filter(TipoPago.ID_Tipo_Pago == id_tipo_pago).first()
    )
    if not tipo_pago_existente:
        return None

    if nombre:
        if nombre not in ["Abono", "Pago Total"]:
            raise ValueError(
                "El nombre del tipo de pago debe ser 'Abono' o 'Pago Total'"
            )
        tipo_pago_existente.Nombre = nombre

    db.commit()
    db.refresh(tipo_pago_existente)
    return tipo_pago_existente


# Eliminar un tipo de pago
def eliminar_tipo_pago(db: Session, id_tipo_pago: int):
    """
    Elimina un tipo de pago por su ID.
    :param db: Sesión de base de datos.
    :param id_tipo_pago: ID del tipo de pago a eliminar.
    :return: True si se eliminó correctamente, False si no se encontró.
    """
    tipo_pago_existente = (
        db.query(TipoPago).filter(TipoPago.ID_Tipo_Pago == id_tipo_pago).first()
    )
    if not tipo_pago_existente:
        return False

    db.delete(tipo_pago_existente)
    db.commit()
    return True
