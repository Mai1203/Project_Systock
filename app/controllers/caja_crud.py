from sqlalchemy.orm import Session
from app.models.caja import Caja


# Crear una nueva caja
def crear_caja(
    db: Session,
    monto_base: float,
    monto_efectivo: float,
    monto_transaccion: float,
    monto_final_calculado: float,
    estado: bool,
    fecha_apertura=None,
    fecha_cierre=None,
    id_ingreso=None,
    id_egreso=None,
    id_usuario=None,
):
    """
    Crea un nuevo registro en la tabla Caja.
    :param db: Sesión de base de datos.
    :param monto_base: Monto base de la caja.
    :param monto_efectivo: Monto en efectivo en la caja.
    :param monto_transaccion: Monto de transacciones en la caja.
    :param monto_final_calculado: Monto final calculado de la caja.
    :param estado: Estado de la caja (abierta/cerrada).
    :param fecha_apertura: Fecha de apertura de la caja (opcional).
    :param fecha_cierre: Fecha de cierre de la caja (opcional).
    :param id_ingreso: ID de ingreso asociado (opcional).
    :param id_egreso: ID de egreso asociado (opcional).
    :param id_usuario: ID del usuario asociado (opcional).
    :return: Objeto Caja creado.
    """
    nueva_caja = Caja(
        Monto_Base=monto_base,
        Monto_Efectivo=monto_efectivo,
        Monto_Transaccion=monto_transaccion,
        Monto_Final_calculado=monto_final_calculado,
        Estado=estado,
        Fecha_Apertura=fecha_apertura,
        Fecha_Cierre=fecha_cierre,
        ID_Ingreso=id_ingreso,
        ID_Egreso=id_egreso,
        ID_Usuario=id_usuario,
    )
    db.add(nueva_caja)
    db.commit()
    db.refresh(nueva_caja)
    return nueva_caja


# Obtener todos los registros de caja
def obtener_cajas(db: Session):
    """
    Obtiene todos los registros de caja.
    :param db: Sesión de base de datos.
    :return: Lista de objetos Caja.
    """
    return db.query(Caja).all()


# Obtener un registro de caja por ID
def obtener_caja_por_id(db: Session, id_caja: int):
    """
    Obtiene un registro de caja por su ID.
    :param db: Sesión de base de datos.
    :param id_caja: ID del registro de caja.
    :return: Objeto Caja o None si no existe.
    """
    return db.query(Caja).filter(Caja.ID_Caja == id_caja).first()


# Actualizar un registro de caja
def actualizar_caja(
    db: Session,
    id_caja: int,
    monto_base: float = None,
    monto_efectivo: float = None,
    monto_transaccion: float = None,
    monto_final_calculado: float = None,
    estado: bool = None,
    fecha_apertura=None,
    fecha_cierre=None,
    id_ingreso=None,
    id_egreso=None,
    id_usuario=None,
):
    """
    Actualiza un registro de caja existente.
    :param db: Sesión de base de datos.
    :param id_caja: ID del registro de caja a actualizar.
    :param monto_base: Nuevo monto base (opcional).
    :param monto_efectivo: Nuevo monto en efectivo (opcional).
    :param monto_transaccion: Nuevo monto de transacciones (opcional).
    :param monto_final_calculado: Nuevo monto final calculado (opcional).
    :param estado: Nuevo estado de la caja (opcional).
    :param fecha_apertura: Nueva fecha de apertura (opcional).
    :param fecha_cierre: Nueva fecha de cierre (opcional).
    :param id_ingreso: Nuevo ID de ingreso asociado (opcional).
    :param id_egreso: Nuevo ID de egreso asociado (opcional).
    :param id_usuario: Nuevo ID de usuario asociado (opcional).
    :return: Objeto Caja actualizado o None si no existe.
    """
    caja_existente = db.query(Caja).filter(Caja.ID_Caja == id_caja).first()
    if not caja_existente:
        return None

    if monto_base is not None:
        caja_existente.Monto_Base = monto_base
    if monto_efectivo is not None:
        caja_existente.Monto_Efectivo = monto_efectivo
    if monto_transaccion is not None:
        caja_existente.Monto_Transaccion = monto_transaccion
    if monto_final_calculado is not None:
        caja_existente.Monto_Final_calculado = monto_final_calculado
    if estado is not None:
        caja_existente.Estado = estado
    if fecha_apertura is not None:
        caja_existente.Fecha_Apertura = fecha_apertura
    if fecha_cierre is not None:
        caja_existente.Fecha_Cierre = fecha_cierre
    if id_ingreso is not None:
        caja_existente.ID_Ingreso = id_ingreso
    if id_egreso is not None:
        caja_existente.ID_Egreso = id_egreso
    if id_usuario is not None:
        caja_existente.ID_Usuario = id_usuario

    db.commit()
    db.refresh(caja_existente)
    return caja_existente


# Eliminar un registro de caja
def eliminar_caja(db: Session, id_caja: int):
    """
    Elimina un registro de caja por su ID.
    :param db: Sesión de base de datos.
    :param id_caja: ID del registro de caja a eliminar.
    :return: True si se eliminó correctamente, False si no se encontró.
    """
    caja_existente = db.query(Caja).filter(Caja.ID_Caja == id_caja).first()
    if not caja_existente:
        return False

    db.delete(caja_existente)
    db.commit()
    return True
