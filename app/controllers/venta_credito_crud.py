from sqlalchemy.orm import Session
from app.models.venta_credito import (
    VentaCredito,
)


# Crear una venta a crédito
def crear_venta_credito(
    db: Session,
    max_credito: float,
    total_deuda: float,
    saldo_pendiente: float,
    fecha_limite: str,
    id_cliente: int,
    id_detalle_factura: int,
):
    """
    Crea una nueva venta a crédito.
    :param db: Sesión de base de datos.
    :param max_credito: El monto máximo de crédito disponible.
    :param total_deuda: El total de la deuda del cliente.
    :param saldo_pendiente: El saldo pendiente del cliente.
    :param fecha_limite: La fecha límite para el pago.
    :param id_cliente: El ID del cliente relacionado.
    :param id_detalle_factura: El ID del detalle de factura relacionado.
    :return: Objeto de venta a crédito creado.
    """
    nueva_venta = VentaCredito(
        Max_Credito=max_credito,
        Total_Deuda=total_deuda,
        Saldo_Pendiente=saldo_pendiente,
        Fecha_Limite=fecha_limite,
        ID_Cliente=id_cliente,
        ID_Detalle_Factura=id_detalle_factura,
    )
    db.add(nueva_venta)
    db.commit()
    db.refresh(nueva_venta)
    return nueva_venta


# Obtener todas las ventas a crédito
def obtener_ventas_credito(db: Session):
    """
    Obtiene la lista de todas las ventas a crédito.
    :param db: Sesión de base de datos.
    :return: Lista de ventas a crédito.
    """
    return db.query(VentaCredito).all()


# Obtener una venta a crédito por ID
def obtener_venta_credito_por_id(db: Session, id_venta_credito: int):
    """
    Obtiene una venta a crédito por su ID.
    :param db: Sesión de base de datos.
    :param id_venta_credito: ID de la venta a crédito.
    :return: Objeto de venta a crédito o None si no existe.
    """
    return (
        db.query(VentaCredito)
        .filter(VentaCredito.ID_Venta_Credito == id_venta_credito)
        .first()
    )


# Actualizar una venta a crédito
def actualizar_venta_credito(
    db: Session,
    id_venta_credito: int,
    max_credito: float = None,
    total_deuda: float = None,
    saldo_pendiente: float = None,
    fecha_limite: str = None,
):
    """
    Actualiza una venta a crédito existente.
    :param db: Sesión de base de datos.
    :param id_venta_credito: ID de la venta a crédito a actualizar.
    :param max_credito: Nuevo monto máximo de crédito.
    :param total_deuda: Nueva deuda total.
    :param saldo_pendiente: Nuevo saldo pendiente.
    :param fecha_limite: Nueva fecha límite.
    :return: Objeto de venta a crédito actualizado o None si no existe.
    """
    venta_existente = (
        db.query(VentaCredito)
        .filter(VentaCredito.ID_Venta_Credito == id_venta_credito)
        .first()
    )
    if not venta_existente:
        return None

    if max_credito is not None:
        venta_existente.Max_Credito = max_credito
    if total_deuda is not None:
        venta_existente.Total_Deuda = total_deuda
    if saldo_pendiente is not None:
        venta_existente.Saldo_Pendiente = saldo_pendiente
    if fecha_limite is not None:
        venta_existente.Fecha_Limite = fecha_limite

    db.commit()
    db.refresh(venta_existente)
    return venta_existente


# Eliminar una venta a crédito
def eliminar_venta_credito(db: Session, id_venta_credito: int):
    """
    Elimina una venta a crédito por su ID.
    :param db: Sesión de base de datos.
    :param id_venta_credito: ID de la venta a crédito a eliminar.
    :return: True si se eliminó correctamente, False si no se encontró.
    """
    venta_existente = (
        db.query(VentaCredito)
        .filter(VentaCredito.ID_Venta_Credito == id_venta_credito)
        .first()
    )
    if not venta_existente:
        return False

    db.delete(venta_existente)
    db.commit()
    return True
