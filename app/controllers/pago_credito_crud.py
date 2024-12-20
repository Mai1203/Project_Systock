from sqlalchemy.orm import Session
from app.models.pago_credito import (
    PagoCredito,
)


# Crear un nuevo pago de crédito
def crear_pago_credito(
    db: Session,
    monto: float,
    id_venta_credito: int,
    id_metodo_pago: int,
    id_tipo_pago: int,
):
    """
    Crea un nuevo pago de crédito.
    :param db: Sesión de base de datos.
    :param monto: Monto del pago de crédito.
    :param id_venta_credito: ID de la venta a la que corresponde el pago.
    :param id_metodo_pago: ID del método de pago.
    :param id_tipo_pago: ID del tipo de pago.
    :return: Objeto de pago de crédito creado.
    """
    nuevo_pago_credito = PagoCredito(
        Monto=monto,
        ID_Venta_Credito=id_venta_credito,
        ID_Metodo_Pago=id_metodo_pago,
        ID_Tipo_Pago=id_tipo_pago,
    )
    db.add(nuevo_pago_credito)
    db.commit()
    db.refresh(nuevo_pago_credito)
    return nuevo_pago_credito


# Obtener todos los pagos de crédito
def obtener_pagos_credito(db: Session):
    """
    Obtiene la lista de todos los pagos de crédito.
    :param db: Sesión de base de datos.
    :return: Lista de pagos de crédito.
    """
    return db.query(PagoCredito).all()


# Obtener un pago de crédito por ID
def obtener_pago_credito_por_id(db: Session, id_pago_credito: int):
    """
    Obtiene un pago de crédito por su ID.
    :param db: Sesión de base de datos.
    :param id_pago_credito: ID del pago de crédito.
    :return: Objeto de pago de crédito o None si no existe.
    """
    return (
        db.query(PagoCredito)
        .filter(PagoCredito.ID_Pago_Credito == id_pago_credito)
        .first()
    )


# Actualizar un pago de crédito
def actualizar_pago_credito(
    db: Session,
    id_pago_credito: int,
    monto: float = None,
    id_venta_credito: int = None,
    id_metodo_pago: int = None,
    id_tipo_pago: int = None,
):
    """
    Actualiza un pago de crédito existente.
    :param db: Sesión de base de datos.
    :param id_pago_credito: ID del pago de crédito a actualizar.
    :param monto: Nuevo monto del pago de crédito.
    :param id_venta_credito: Nuevo ID de la venta a la que corresponde el pago (opcional).
    :param id_metodo_pago: Nuevo ID del método de pago (opcional).
    :param id_tipo_pago: Nuevo ID del tipo de pago (opcional).
    :return: Objeto de pago de crédito actualizado o None si no existe.
    """
    pago_credito_existente = (
        db.query(PagoCredito)
        .filter(PagoCredito.ID_Pago_Credito == id_pago_credito)
        .first()
    )
    if not pago_credito_existente:
        return None

    if monto is not None:
        pago_credito_existente.Monto = monto
    if id_venta_credito is not None:
        pago_credito_existente.ID_Venta_Credito = id_venta_credito
    if id_metodo_pago is not None:
        pago_credito_existente.ID_Metodo_Pago = id_metodo_pago
    if id_tipo_pago is not None:
        pago_credito_existente.ID_Tipo_Pago = id_tipo_pago

    db.commit()
    db.refresh(pago_credito_existente)
    return pago_credito_existente


# Eliminar un pago de crédito
def eliminar_pago_credito(db: Session, id_pago_credito: int):
    """
    Elimina un pago de crédito por su ID.
    :param db: Sesión de base de datos.
    :param id_pago_credito: ID del pago de crédito a eliminar.
    :return: True si se eliminó correctamente, False si no se encontró.
    """
    pago_credito_existente = (
        db.query(PagoCredito)
        .filter(PagoCredito.ID_Pago_Credito == id_pago_credito)
        .first()
    )
    if not pago_credito_existente:
        return False

    db.delete(pago_credito_existente)
    db.commit()
    return True
