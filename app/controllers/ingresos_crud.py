from sqlalchemy.orm import Session


from app.models.ingresos import (Ingresos,) 
from app.models.tipo_ingresos import (TipoIngreso)
from app.models.facturas import Facturas, MetodoPago
from app.models.pago_credito import PagoCredito

# Crear un nuevo ingreso
def crear_ingreso(db: Session, id_tipo_ingreso: int):
    """
    Crea un nuevo ingreso.
    :param db: Sesión de base de datos.
    :param id_tipo_ingreso: ID del tipo de ingreso.
    :return: Objeto de ingreso creado.
    """
    nuevo_ingreso = Ingresos(ID_Tipo_Ingreso=id_tipo_ingreso)
    db.add(nuevo_ingreso)
    db.commit()
    db.refresh(nuevo_ingreso)
    return nuevo_ingreso


# Obtener todos los ingresos
def obtener_ingresos(db: Session):
    """
    Obtiene la lista de todos los ingresos.
    :param db: Sesión de base de datos.
    :return: Lista de ingresos.
    """
    ingresos = (
        db.query(
            Ingresos.ID_Ingreso,
            Ingresos.ID_Tipo_Ingreso,
            
            TipoIngreso.Tipo_Ingreso.label("tipo_ingreso"),
            Facturas.Monto_efectivo.label("monto_efectivo"),
            Facturas.Monto_TRANSACCION.label("monto_transaccion"),
            Facturas.Fecha_Factura.label("fecha_venta"),
            PagoCredito.Monto.label("monto"),
            PagoCredito.Fecha_Registro.label("fecha_abono"),
            MetodoPago.Nombre.label("metodo_pago"),
        )
        .outerjoin(TipoIngreso, Ingresos.ID_Tipo_Ingreso == TipoIngreso.ID_Tipo_Ingreso)
        .outerjoin(Facturas, TipoIngreso.ID_Factura == Facturas.ID_Factura)
        .outerjoin(PagoCredito, TipoIngreso.ID_Pago_Credito == PagoCredito.ID_Pago_Credito)
        .outerjoin(MetodoPago, PagoCredito.ID_Metodo_Pago == MetodoPago.ID_Metodo_Pago)
        .all()
    )
    
    return ingresos


# Obtener un ingreso por ID
def obtener_ingreso_por_id(db: Session, id_ingreso: int):
    """
    Obtiene un ingreso por su ID.
    :param db: Sesión de base de datos.
    :param id_ingreso: ID del ingreso.
    :return: Objeto de ingreso o None si no existe.
    """
    return db.query(Ingresos).filter(Ingresos.ID_Ingreso == id_ingreso).first()


# Actualizar un ingreso
def actualizar_ingreso(db: Session, id_ingreso: int, id_tipo_ingreso: int = None):
    """
    Actualiza un ingreso existente.
    :param db: Sesión de base de datos.
    :param id_ingreso: ID del ingreso a actualizar.
    :param id_tipo_ingreso: Nuevo ID del tipo de ingreso.
    :return: Objeto de ingreso actualizado o None si no existe.
    """
    ingreso_existente = (
        db.query(Ingresos).filter(Ingresos.ID_Ingreso == id_ingreso).first()
    )
    if not ingreso_existente:
        return None

    if id_tipo_ingreso:
        ingreso_existente.ID_Tipo_Ingreso = id_tipo_ingreso

    db.commit()
    db.refresh(ingreso_existente)
    return ingreso_existente


# Eliminar un ingreso
def eliminar_ingreso(db: Session, id_ingreso: int):
    """
    Elimina un ingreso por su ID.
    :param db: Sesión de base de datos.
    :param id_ingreso: ID del ingreso a eliminar.
    :return: True si se eliminó correctamente, False si no se encontró.
    """
    ingreso_existente = (
        db.query(Ingresos).filter(Ingresos.ID_Ingreso == id_ingreso).first()
    )
    if not ingreso_existente:
        return False

    db.delete(ingreso_existente)
    db.commit()
    return True
