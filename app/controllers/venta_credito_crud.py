from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime
from app.models.venta_credito import (
    VentaCredito,
)
from app.models.facturas import Facturas
from app.models.usuarios import Usuarios
from app.models.clientes import Clientes


# Crear una venta a crédito
def crear_venta_credito(
    db: Session,
    total_deuda: float,
    saldo_pendiente: float,
    fecha_limite: datetime,
    id_factura: int,
):
    """
    Crea una nueva venta a crédito.
    :param db: Sesión de base de datos.
    :param total_deuda: El total de la deuda del cliente.
    :param saldo_pendiente: El saldo pendiente del cliente.
    :param fecha_limite: La fecha límite para el pago.
    :param id_factura: El ID de la factura relacionada.
    :return: Objeto de venta a crédito creado.
    """
    nueva_venta = VentaCredito(
        Total_Deuda=total_deuda,
        Saldo_Pendiente=saldo_pendiente,
        Fecha_Limite=fecha_limite,
        ID_Factura=id_factura,
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
    ventas_credito = (
        db.query(
            VentaCredito.ID_Venta_Credito,
            VentaCredito.Total_Deuda,
            VentaCredito.Saldo_Pendiente,
            VentaCredito.Fecha_Registro,
            VentaCredito.Fecha_Limite,
            Facturas.ID_Factura,
            
            Usuarios.Nombre.label("usuario"),
            Clientes.Nombre.label("cliente"),
            Facturas.Estado.label("estado"),
        )
        .join(Facturas, VentaCredito.ID_Factura == Facturas.ID_Factura)
        .join(Usuarios, Facturas.ID_Usuario == Usuarios.ID_Usuario)
        .join(Clientes, Facturas.ID_Cliente == Clientes.ID_Cliente)
        .all()
    )
    
    return ventas_credito


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
    total_deuda: float = None,
    saldo_pendiente: float = None,
    fecha_limite: str = None,
):
    """
    Actualiza una venta a crédito existente.
    :param db: Sesión de base de datos.
    :param id_venta_credito: ID de la venta a crédito a actualizar.
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

    if total_deuda is not None:
        venta_existente.Total_Deuda = total_deuda
    if saldo_pendiente is not None:
        venta_existente.Saldo_Pendiente = saldo_pendiente
    if fecha_limite is not None:
        venta_existente.Fecha_Limite = fecha_limite

    db.commit()
    db.refresh(venta_existente)
    return venta_existente

def buscar_ventas_credito(db: Session, busqueda: str):
    """
    Busca facturas en la base de datos.
    :param db: Sesión de base de datos.
    :param busqueda: Texto a buscar.
    :return: Lista de facturas.
    """
    if not busqueda:
        return None

    ventas_credito = (
        db.query(
            VentaCredito.ID_Venta_Credito,
            VentaCredito.Total_Deuda,
            VentaCredito.Saldo_Pendiente,
            VentaCredito.Fecha_Registro,
            VentaCredito.Fecha_Limite,
            Facturas.ID_Factura,
            
            Usuarios.Nombre.label("usuario"),
            Clientes.Nombre.label("cliente"),
            Facturas.Estado.label("estado"),
        )
        .join(Facturas, VentaCredito.ID_Factura == Facturas.ID_Factura)
        .join(Usuarios, Facturas.ID_Usuario == Usuarios.ID_Usuario)
        .join(Clientes, Facturas.ID_Cliente == Clientes.ID_Cliente)
        .filter(
            or_(
                VentaCredito.ID_Venta_Credito.like(f"%{busqueda}%"),
                VentaCredito.Fecha_Registro.like(f"%{busqueda}%"),
                Clientes.Nombre.like(f"%{busqueda}%"),
            )
        )
        .all()
    )
    
    return ventas_credito
   

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
