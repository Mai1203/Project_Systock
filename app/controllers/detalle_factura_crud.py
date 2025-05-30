from sqlalchemy.orm import Session
from app.models.detalle_facturas import DetalleFacturas


# Crear un detalle de factura
def crear_detalle_factura(
    db: Session,
    cantidad: int,
    precio_unitario: float,
    subtotal: float,
    id_producto: int,
    id_factura: int,
):
    """
    Crea un nuevo registro de detalle de factura.
    :param db: Sesión de base de datos.
    :param cantidad: Cantidad de productos.
    :param precio_unitario: Precio unitario del producto.
    :param subtotal: Subtotal del detalle.
    :param id_producto: ID del producto relacionado.
    :param id_factura: ID de la factura relacionada.
    :return: Objeto del detalle de factura creado.
    """
    nuevo_detalle = DetalleFacturas(
        Cantidad=cantidad,
        Precio_unitario=precio_unitario,
        Subtotal=subtotal,
        ID_Producto=id_producto,
        ID_Factura=id_factura,
    )
    db.add(nuevo_detalle)
    db.commit()
    db.refresh(nuevo_detalle)
    return nuevo_detalle


# Obtener todos los detalles de facturas
def obtener_detalles_facturas(db: Session):
    """
    Obtiene todos los registros de detalles de facturas.
    :param db: Sesión de base de datos.
    :return: Lista de detalles de facturas.
    """
    return db.query(DetalleFacturas).all()


# Obtener un detalle de factura por ID
def obtener_detalle_factura_por_id(db: Session, id_detalle_factura: int):
    """
    Obtiene un registro de detalle de factura por su ID.
    :param db: Sesión de base de datos.
    :param id_detalle_factura: ID del detalle de factura.
    :return: Objeto del detalle de factura o None si no existe.
    """
    return (
        db.query(DetalleFacturas)
        .filter(DetalleFacturas.ID_Detalle_Factura == id_detalle_factura)
        .first()
    )


# Actualizar un detalle de factura
def actualizar_detalle_factura(
    db: Session,
    id_detalle_factura: int,
    cantidad: int = None,
    precio_unitario: float = None,
    subtotal: float = None,
    id_producto: int = None,
    id_factura: int = None,
):
    """
    Actualiza un registro de detalle de factura existente.
    :param db: Sesión de base de datos.
    :param id_detalle_factura: ID del detalle de factura a actualizar.
    :param cantidad: Nueva cantidad de productos.
    :param precio_unitario: Nuevo precio unitario.
    :param subtotal: Nuevo subtotal.
    :param id_producto: Nuevo ID de producto relacionado.
    :param id_factura: Nuevo ID de factura relacionada.
    :return: Objeto del detalle de factura actualizado o None si no existe.
    """
    detalle_existente = (
        db.query(DetalleFacturas)
        .filter(DetalleFacturas.ID_Detalle_Factura == id_detalle_factura)
        .first()
    )
    if not detalle_existente:
        return None

    if cantidad is not None:
        detalle_existente.Cantidad = cantidad
    if precio_unitario is not None:
        detalle_existente.Precio_unitario = precio_unitario
    if subtotal is not None:
        detalle_existente.Subtotal = subtotal
    if id_producto is not None:
        detalle_existente.ID_Producto = id_producto
    if id_factura is not None:
        detalle_existente.ID_Factura = id_factura

    db.commit()
    db.refresh(detalle_existente)
    return detalle_existente


# Eliminar un detalle de factura
def eliminar_detalle_factura(db: Session, id_producto: int, id_factura: int):
    """
    Elimina un registro de detalle de factura por su ID.
    :param db: Sesión de base de datos.
    :param id_detalle_factura: ID del detalle de factura a eliminar.
    :return: True si se eliminó correctamente, False si no se encontró.
    """
    detalle_existente = (
        db.query(DetalleFacturas)
        .filter(
            DetalleFacturas.ID_Factura == id_factura,
            DetalleFacturas.ID_Producto == id_producto,
        )
        .first()
    )
    if not detalle_existente:
        return False

    db.delete(detalle_existente)
    db.commit()
    return True
