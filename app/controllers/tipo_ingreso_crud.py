from sqlalchemy.orm import Session
from app.models.tipo_ingresos import (
    TipoIngreso,
)


# Crear un nuevo tipo de ingreso
def crear_tipo_ingreso(
    db: Session,
    tipo_ingreso: str,
    id_pago_credito: int = None,
    id_detalle_factura: int = None,
):
    """
    Crea un nuevo tipo de ingreso.
    :param db: Sesión de base de datos.
    :param tipo_ingreso: Tipo de ingreso ('Venta' o 'Abono').
    :param id_pago_credito: ID del pago de crédito asociado (opcional).
    :param id_detalle_factura: ID del detalle de factura asociado (opcional).
    :return: Objeto de tipo de ingreso creado.
    """
    if tipo_ingreso not in ["Venta", "Abono"]:
        raise ValueError("El tipo de ingreso debe ser 'Venta' o 'Abono'.")

    nuevo_tipo_ingreso = TipoIngreso(
        Tipo_Ingreso=tipo_ingreso,
        ID_Pago_Credito=id_pago_credito,
        ID_Detalle_Factura=id_detalle_factura,
    )
    db.add(nuevo_tipo_ingreso)
    db.commit()
    db.refresh(nuevo_tipo_ingreso)
    return nuevo_tipo_ingreso


# Obtener todos los tipos de ingreso
def obtener_tipos_ingreso(db: Session):
    """
    Obtiene la lista de todos los tipos de ingreso.
    :param db: Sesión de base de datos.
    :return: Lista de tipos de ingreso.
    """
    return db.query(TipoIngreso).all()


# Obtener un tipo de ingreso por ID
def obtener_tipo_ingreso_por_id(db: Session, id_tipo_ingreso: int):
    """
    Obtiene un tipo de ingreso por su ID.
    :param db: Sesión de base de datos.
    :param id_tipo_ingreso: ID del tipo de ingreso.
    :return: Objeto de tipo de ingreso o None si no existe.
    """
    return (
        db.query(TipoIngreso)
        .filter(TipoIngreso.ID_Tipo_Ingreso == id_tipo_ingreso)
        .first()
    )


# Actualizar un tipo de ingreso
def actualizar_tipo_ingreso(
    db: Session,
    id_tipo_ingreso: int,
    tipo_ingreso: str = None,
    id_pago_credito: int = None,
    id_detalle_factura: int = None,
):
    """
    Actualiza un tipo de ingreso existente.
    :param db: Sesión de base de datos.
    :param id_tipo_ingreso: ID del tipo de ingreso a actualizar.
    :param tipo_ingreso: Nuevo tipo de ingreso ('Venta' o 'Abono').
    :param id_pago_credito: Nuevo ID de pago de crédito (opcional).
    :param id_detalle_factura: Nuevo ID de detalle de factura (opcional).
    :return: Objeto de tipo de ingreso actualizado o None si no existe.
    """
    tipo_ingreso_existente = (
        db.query(TipoIngreso)
        .filter(TipoIngreso.ID_Tipo_Ingreso == id_tipo_ingreso)
        .first()
    )
    if not tipo_ingreso_existente:
        return None

    if tipo_ingreso:
        if tipo_ingreso not in ["Venta", "Abono"]:
            raise ValueError("El tipo de ingreso debe ser 'Venta' o 'Abono'.")
        tipo_ingreso_existente.Tipo_Ingreso = tipo_ingreso
    if id_pago_credito is not None:
        tipo_ingreso_existente.ID_Pago_Credito = id_pago_credito
    if id_detalle_factura is not None:
        tipo_ingreso_existente.ID_Detalle_Factura = id_detalle_factura

    db.commit()
    db.refresh(tipo_ingreso_existente)
    return tipo_ingreso_existente


# Eliminar un tipo de ingreso
def eliminar_tipo_ingreso(db: Session, id_tipo_ingreso: int):
    """
    Elimina un tipo de ingreso por su ID.
    :param db: Sesión de base de datos.
    :param id_tipo_ingreso: ID del tipo de ingreso a eliminar.
    :return: True si se eliminó correctamente, False si no se encontró.
    """
    tipo_ingreso_existente = (
        db.query(TipoIngreso)
        .filter(TipoIngreso.ID_Tipo_Ingreso == id_tipo_ingreso)
        .first()
    )
    if not tipo_ingreso_existente:
        return False

    db.delete(tipo_ingreso_existente)
    db.commit()
    return True
