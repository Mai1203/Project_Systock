from sqlalchemy.orm import Session
from app.models.egresos import Egresos
from app.models.facturas import MetodoPago


# Crear un egreso
def crear_egreso(
    db: Session,
    tipo_egreso: str,
    descripcion: str,
    monto_egreso: float,
    id_metodo_pago: int,
):
    """
    Crea un nuevo registro de egreso.
    :param db: Sesión de base de datos.
    :param tipo_egreso: Tipo de egreso (por ejemplo, 'Pago', 'Compra').
    :param descripcion: Descripción del egreso.
    :param monto_egreso: Monto del egreso.
    :param id_metodo_pago: ID del método de pago utilizado.
    :return: Objeto de egreso creado.
    """
    nuevo_egreso = Egresos(
        Tipo_Egreso=tipo_egreso,
        Descripcion=descripcion,
        Monto_Egreso=monto_egreso,
        ID_Metodo_Pago=id_metodo_pago,
    )
    db.add(nuevo_egreso)
    db.commit()
    db.refresh(nuevo_egreso)
    return nuevo_egreso


# Obtener todos los egresos
def obtener_egresos(db: Session):
    """
    Obtiene todos los registros de egresos.
    :param db: Sesión de base de datos.
    :return: Lista de egresos.
    """
    egresos = (
        db.query(
            Egresos.ID_Egreso,
            Egresos.Tipo_Egreso,
            Egresos.Fecha_Egreso,
            Egresos.Descripcion,
            Egresos.Monto_Egreso,
            Egresos.ID_Metodo_Pago,
            
            MetodoPago.Nombre.label("metodopago"),
        )
        .join(MetodoPago, Egresos.ID_Metodo_Pago == MetodoPago.ID_Metodo_Pago)
        .all()
    )
    
    return egresos


# Obtener un egreso por ID
def obtener_egreso_por_id(db: Session, id_egreso: int):
    """
    Obtiene un registro de egreso por su ID.
    :param db: Sesión de base de datos.
    :param id_egreso: ID del egreso.
    :return: Objeto de egreso o None si no existe.
    """
    return db.query(Egresos).filter(Egresos.ID_Egreso == id_egreso).first()


# Actualizar un egreso
def actualizar_egreso(
    db: Session,
    id_egreso: int,
    tipo_egreso: str = None,
    descripcion: str = None,
    monto_egreso: float = None,
    id_metodo_pago: int = None,
):
    """
    Actualiza un registro de egreso existente.
    :param db: Sesión de base de datos.
    :param id_egreso: ID del egreso a actualizar.
    :param tipo_egreso: Nuevo tipo de egreso.
    :param descripcion: Nueva descripción del egreso.
    :param monto_egreso: Nuevo monto del egreso.
    :param id_metodo_pago: Nuevo ID del método de pago utilizado.
    :return: Objeto de egreso actualizado o None si no existe.
    """
    egreso_existente = db.query(Egresos).filter(Egresos.ID_Egreso == id_egreso).first()
    if not egreso_existente:
        return None

    if tipo_egreso:
        egreso_existente.Tipo_Egreso = tipo_egreso
    if descripcion:
        egreso_existente.Descripcion = descripcion
    if monto_egreso is not None:
        egreso_existente.Monto_Egreso = monto_egreso
    if id_metodo_pago is not None:
        egreso_existente.ID_Metodo_Pago = id_metodo_pago

    db.commit()
    db.refresh(egreso_existente)
    return egreso_existente


# Eliminar un egreso
def eliminar_egreso(db: Session, id_egreso: int):
    """
    Elimina un registro de egreso por su ID.
    :param db: Sesión de base de datos.
    :param id_egreso: ID del egreso a eliminar.
    :return: True si se eliminó correctamente, False si no se encontró.
    """
    egreso_existente = db.query(Egresos).filter(Egresos.ID_Egreso == id_egreso).first()
    if not egreso_existente:
        return False

    db.delete(egreso_existente)
    db.commit()
    return True
