from sqlalchemy.orm import Session
from app.models.facturas import Facturas


# Crear una factura
def crear_factura(
    db: Session,
    monto_efectivo: float,
    monto_transaccion: float,
    estado: bool,
    id_metodo_pago: int,
    id_tipo_factura: int,
    id_detalle_factura: int,
):
    """
    Crea una nueva factura.
    :param db: Sesión de base de datos.
    :param monto_efectivo: Monto pagado en efectivo.
    :param monto_transaccion: Monto pagado mediante transacción.
    :param estado: Estado de la factura (True: Activa, False: Cancelada).
    :param id_metodo_pago: ID del método de pago.
    :param id_tipo_factura: ID del tipo de factura.
    :param id_detalle_factura: ID del detalle de factura.
    :return: Objeto de factura creada.
    """
    nueva_factura = Facturas(
        Monto_efectivo=monto_efectivo,
        Monto_TRANSACCION=monto_transaccion,
        Estado=estado,
        ID_Metodo_Pago=id_metodo_pago,
        ID_Tipo_Factura=id_tipo_factura,
        ID_Detalle_Factura=id_detalle_factura,
    )
    db.add(nueva_factura)
    db.commit()
    db.refresh(nueva_factura)
    return nueva_factura


# Obtener todas las facturas
def obtener_facturas(db: Session):
    """
    Obtiene la lista de todas las facturas.
    :param db: Sesión de base de datos.
    :return: Lista de facturas.
    """
    return db.query(Facturas).all()


# Obtener una factura por ID
def obtener_factura_por_id(db: Session, id_factura: int):
    """
    Obtiene una factura por su ID.
    :param db: Sesión de base de datos.
    :param id_factura: ID de la factura.
    :return: Objeto de factura o None si no existe.
    """
    return db.query(Facturas).filter(Facturas.ID_Factura == id_factura).first()


# Actualizar una factura
def actualizar_factura(
    db: Session,
    id_factura: int,
    monto_efectivo: float = None,
    monto_transaccion: float = None,
    estado: bool = None,
    id_metodo_pago: int = None,
    id_tipo_factura: int = None,
    id_detalle_factura: int = None,
):
    """
    Actualiza una factura existente.
    :param db: Sesión de base de datos.
    :param id_factura: ID de la factura a actualizar.
    :param monto_efectivo: Nuevo monto pagado en efectivo.
    :param monto_transaccion: Nuevo monto pagado mediante transacción.
    :param estado: Nuevo estado de la factura.
    :param id_metodo_pago: Nuevo ID del método de pago.
    :param id_tipo_factura: Nuevo ID del tipo de factura.
    :param id_detalle_factura: Nuevo ID del detalle de factura.
    :return: Objeto de factura actualizado o None si no existe.
    """
    factura_existente = (
        db.query(Facturas).filter(Facturas.ID_Factura == id_factura).first()
    )
    if not factura_existente:
        return None

    if monto_efectivo is not None:
        factura_existente.Monto_efectivo = monto_efectivo
    if monto_transaccion is not None:
        factura_existente.Monto_TRANSACCION = monto_transaccion
    if estado is not None:
        factura_existente.Estado = estado
    if id_metodo_pago:
        factura_existente.ID_Metodo_Pago = id_metodo_pago
    if id_tipo_factura:
        factura_existente.ID_Tipo_Factura = id_tipo_factura
    if id_detalle_factura:
        factura_existente.ID_Detalle_Factura = id_detalle_factura

    db.commit()
    db.refresh(factura_existente)
    return factura_existente


# Eliminar una factura
def eliminar_factura(db: Session, id_factura: int):
    """
    Elimina una factura por su ID.
    :param db: Sesión de base de datos.
    :param id_factura: ID de la factura a eliminar.
    :return: True si se eliminó correctamente, False si no se encontró.
    """
    factura_existente = (
        db.query(Facturas).filter(Facturas.ID_Factura == id_factura).first()
    )
    if not factura_existente:
        return False

    db.delete(factura_existente)
    db.commit()
    return True
