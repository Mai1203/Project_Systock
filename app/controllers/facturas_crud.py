from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from sqlalchemy import func, case
from app.models.facturas import Facturas, MetodoPago, TipoFactura
from app.models.detalle_facturas import DetalleFacturas
from app.models.clientes import Clientes
from app.models.productos import Productos, Marcas, Categorias
from app.models.usuarios import Usuarios
from app.models.historial import HistorialModificacion
from app.models.tipo_ingresos import TipoIngreso


# Crear una factura
def crear_factura(
    db: Session,
    monto_efectivo: float,
    monto_transaccion: float,
    descuento: float,
    estado: bool,
    id_metodo_pago: int,
    id_tipo_factura: int,
    id_cliente: int,
    id_usuario: int,
):
    """
    Crea una nueva factura.
    :param db: Sesión de base de datos.
    :param monto_efectivo: Monto pagado en efectivo.
    :param monto_transaccion: Monto pagado mediante transacción.
    :param descuento: Descuento aplicado.
    :param estado: Estado de la factura (True: Activa, False: Cancelada).
    :param id_metodo_pago: ID del método de pago.
    :param id_tipo_factura: ID del tipo de factura.
    :param id_cliente: ID del cliente.
    :param id_usuario: ID del usuario.
    :return: Objeto de factura creada.
    """
    nueva_factura = Facturas(
        Monto_efectivo=monto_efectivo,
        Monto_TRANSACCION=monto_transaccion,
        Descuento=descuento,
        Estado=estado,
        ID_Metodo_Pago=id_metodo_pago,
        ID_Tipo_Factura=id_tipo_factura,
        ID_Cliente=id_cliente,
        ID_Usuario=id_usuario,
    )
    db.add(nueva_factura)
    db.commit()
    db.refresh(nueva_factura)
    return nueva_factura


def obtener_factura_completa(db: Session, id_factura: int):
    """
    Obtiene todos los datos de una factura, sus detalles y el cliente asociado.
    :param db: Sesión de base de datos.
    :param id_factura: ID de la factura a buscar.
    :return: Diccionario con la información de la factura, cliente y sus detalles.
    """
    # Consulta principal para la factura y cliente
    factura = (
        db.query(
            Facturas.ID_Factura,
            Facturas.Fecha_Factura,
            Facturas.Monto_efectivo,
            Facturas.Monto_TRANSACCION,
            Facturas.Descuento,
            Facturas.Estado,
            Facturas.ID_Cliente,
            Clientes.Nombre.label("cliente"),
            Clientes.Apellido.label("apellido"),
            Clientes.Direccion.label("direccion"),
            Clientes.Teléfono.label("telefono"),
            MetodoPago.Nombre.label("metodo_pago"),
            TipoFactura.Nombre.label("tipo_factura"),
        )
        .join(MetodoPago, Facturas.ID_Metodo_Pago == MetodoPago.ID_Metodo_Pago)
        .join(TipoFactura, Facturas.ID_Tipo_Factura == TipoFactura.ID_Tipo_Factura)
        .join(Clientes, Facturas.ID_Cliente == Clientes.ID_Cliente)
        .filter(Facturas.ID_Factura == id_factura)
        .first()
    )

    if not factura:
        return None  # Si no se encuentra la factura, devolver None

    # Consulta para los detalles de la factura
    detalles = (
        db.query(
            DetalleFacturas.ID_Detalle_Factura,
            DetalleFacturas.ID_Producto,
            DetalleFacturas.Cantidad,
            DetalleFacturas.Precio_unitario,
            DetalleFacturas.Subtotal,
            Productos.Nombre.label("producto"),
            Marcas.Nombre.label("marca"),
            Categorias.Nombre.label("categoria"),
        )
        .join(Productos, DetalleFacturas.ID_Producto == Productos.ID_Producto)
        .join(Marcas, Productos.ID_Marca == Marcas.ID_Marca)
        .join(Categorias, Productos.ID_Categoria == Categorias.ID_Categoria)
        .filter(DetalleFacturas.ID_Factura == id_factura)
        .all()
    )

    # Formatear el resultado como un diccionario
    resultado = {
        "Factura": {
            "ID_Factura": factura.ID_Factura,
            "Fecha_Factura": factura.Fecha_Factura,
            "Monto_efectivo": factura.Monto_efectivo,
            "Monto_TRANSACCION": factura.Monto_TRANSACCION,
            "Descuento": factura.Descuento,
            "Estado": factura.Estado,
            "MetodoPago": factura.metodo_pago,
            "TipoFactura": factura.tipo_factura,
        },
        "Cliente": {
            "ID_Cliente": factura.ID_Cliente,
            "Nombre": factura.cliente,
            "Apellido": factura.apellido,
            "Direccion": factura.direccion,
            "Teléfono": factura.telefono,
        },
        "Detalles": [
            {
                "ID_Detalle": detalle.ID_Detalle_Factura,
                "ID_Producto": detalle.ID_Producto,
                "Cantidad": detalle.Cantidad,
                "Marca": detalle.marca,
                "Categoria": detalle.categoria,
                "Precio_Unitario": detalle.Precio_unitario,
                "Subtotal": detalle.Subtotal,
                "Producto": detalle.producto,
            }
            for detalle in detalles
        ],
    }

    return resultado


# Obtener todas las facturas
def obtener_facturas(db: Session):
    """
    Obtiene la lista de todas las facturas.
    :param db: Sesión de base de datos.
    :return: Lista de facturas.
    """
    facturas = (
        db.query(
            Facturas.ID_Factura,
            Facturas.Fecha_Factura,
            Facturas.Monto_efectivo,
            Facturas.Monto_TRANSACCION,
            Facturas.Estado,
            Clientes.Nombre.label("cliente"),
            Usuarios.Usuario.label("usuario"),
            MetodoPago.Nombre.label("metodopago"),
            TipoFactura.Nombre.label("tipofactura"),
            HistorialModificacion.Fecha_Modificacion.label("fecha_modificacion"),
        )
        .join(Usuarios, Facturas.ID_Usuario == Usuarios.ID_Usuario)
        .join(MetodoPago, Facturas.ID_Metodo_Pago == MetodoPago.ID_Metodo_Pago)
        .join(TipoFactura, Facturas.ID_Tipo_Factura == TipoFactura.ID_Tipo_Factura)
        .outerjoin(HistorialModificacion, Facturas.ID_Factura == HistorialModificacion.ID_Factura)
        .join(Clientes, Facturas.ID_Cliente == Clientes.ID_Cliente)
        .all()
    )

    return facturas


def buscar_facturas(db: Session, busqueda: str):
    """
    Busca facturas en la base de datos.
    :param db: Sesión de base de datos.
    :param busqueda: Texto a buscar.
    :return: Lista de facturas.
    """
    if not busqueda:
        return None

    facturas = (
        db.query(
            Facturas.ID_Factura,
            Facturas.Fecha_Factura,
            Facturas.Monto_efectivo,
            Facturas.Monto_TRANSACCION,
            Facturas.Estado,
            Clientes.Nombre.label("cliente"),
            Usuarios.Nombre.label("usuario"),
            MetodoPago.Nombre.label("metodopago"),
            TipoFactura.Nombre.label("tipofactura"),
        )
        .join(MetodoPago, Facturas.ID_Metodo_Pago == MetodoPago.ID_Metodo_Pago)
        .join(TipoFactura, Facturas.ID_Tipo_Factura == TipoFactura.ID_Tipo_Factura)
        .join(Clientes, Facturas.ID_Cliente == Clientes.ID_Cliente)
        .join(Usuarios, Facturas.ID_Usuario == Usuarios.ID_Usuario)
        .filter(
            or_(
                Facturas.ID_Factura.like(f"%{busqueda}%"),
                Facturas.Fecha_Factura.like(f"%{busqueda}%"),
                TipoFactura.Nombre.like(f"%{busqueda}%"),
                Clientes.Nombre.like(f"%{busqueda}%"),
                MetodoPago.Nombre.like(f"%{busqueda}%"),
                Facturas.Estado.like(f"%{busqueda}%"),
            )
        )
        .all()
    )
    return facturas


# Obtener una factura por ID
def obtener_factura_por_id(db: Session, id_factura: int):
    """
    Obtiene una factura por su ID.
    :param db: Sesión de base de datos.
    :param id_factura: ID de la factura.
    :return: Objeto de factura o None si no existe.
    """
    facturas = (
        db.query(
            Facturas.ID_Factura,
            Facturas.Fecha_Factura,
            Facturas.Monto_efectivo,
            Facturas.Monto_TRANSACCION,
            Facturas.Estado,
            Clientes.Nombre.label("cliente"),
            Usuarios.Usuario.label("usuario"),
            MetodoPago.Nombre.label("metodopago"),
            TipoFactura.Nombre.label("tipofactura"),
        )
        .join(Usuarios, Facturas.ID_Usuario == Usuarios.ID_Usuario)
        .join(MetodoPago, Facturas.ID_Metodo_Pago == MetodoPago.ID_Metodo_Pago)
        .join(TipoFactura, Facturas.ID_Tipo_Factura == TipoFactura.ID_Tipo_Factura)
        .join(Clientes, Facturas.ID_Cliente == Clientes.ID_Cliente)
        .filter(Facturas.ID_Factura == id_factura)
        .first()
    )

    return facturas

def obtener_reporte_facturas(db: Session, fecha_inicio, fecha_fin=None):
    query = (
        db.query(
            Facturas.ID_Factura,
            TipoIngreso.Tipo_Ingreso,
            Facturas.Monto_efectivo,
            Facturas.Monto_TRANSACCION,
            Facturas.Fecha_Factura,
            func.sum(
                DetalleFacturas.Cantidad * 
                case(
                    (Facturas.ID_Tipo_Factura == 1, Productos.Ganancia_Producto_normal),
                    (Facturas.ID_Tipo_Factura == 2, Productos.Ganancia_Producto_mayor),
                    else_=0
                )-Facturas.Descuento
            ).label("ganancia_por_factura")
        )
        .join(TipoIngreso, TipoIngreso.ID_Factura == Facturas.ID_Factura)
        .join(DetalleFacturas, DetalleFacturas.ID_Factura == Facturas.ID_Factura)
        .join(Productos, Productos.ID_Producto == DetalleFacturas.ID_Producto)
    )

    # Filtrar por fecha
    if fecha_fin:
        query = query.filter(and_(Facturas.Fecha_Factura >= fecha_inicio, Facturas.Fecha_Factura <= fecha_fin))
    else:
        query = query.filter(func.date(Facturas.Fecha_Factura) == fecha_inicio)

    query = query.group_by(Facturas.ID_Factura, TipoIngreso.Tipo_Ingreso, Facturas.Descuento)

    return query.all()


# Actualizar una factura
def actualizar_factura(
    db: Session,
    id_factura: int,
    monto_efectivo: float = None,
    monto_transaccion: float = None,
    descuento: float = None,
    estado: bool = None,
    id_metodo_pago: int = None,
    id_tipo_factura: int = None,
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
    if descuento is not None:
        factura_existente.Descuento = descuento
    if estado is not None:
        factura_existente.Estado = estado
    if id_metodo_pago:
        factura_existente.ID_Metodo_Pago = id_metodo_pago
    if id_tipo_factura:
        factura_existente.ID_Tipo_Factura = id_tipo_factura

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
