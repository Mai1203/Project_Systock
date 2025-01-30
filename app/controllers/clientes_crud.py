from sqlalchemy.orm import Session
from app.models.clientes import Clientes


# Crear un cliente
def crear_cliente(
    db: Session,
    id_cliente: str,
    nombre: str,
    apellido: str,
    direccion: str,
    telefono: str,
):
    """
    Crea un nuevo cliente en la base de datos.
    :param db: Sesión de base de datos.
    :param id_cliente: Cedula del cliente.
    :param nombre: Nombre del cliente.
    :param apellido: Apellido del cliente.
    :param direccion: Dirección del cliente.
    :param telefono: Teléfono del cliente.
    :return: Objeto del cliente creado.
    """
    nuevo_cliente = Clientes(
        ID_Cliente=id_cliente,
        Nombre=nombre,
        Apellido=apellido,
        Direccion=direccion,
        Teléfono=telefono,
    )
    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)
    return nuevo_cliente


# Obtener todos los clientes
def obtener_clientes(db: Session):
    """
    Obtiene todos los registros de clientes.
    :param db: Sesión de base de datos.
    :return: Lista de clientes.
    """
    return db.query(Clientes).all()


# Obtener un cliente por ID
def obtener_cliente_por_id(db: Session, id_cliente: int):
    """
    Obtiene un cliente específico por su ID.
    :param db: Sesión de base de datos.
    :param id_cliente: ID del cliente.
    :return: Objeto del cliente o None si no existe.
    """
    return db.query(Clientes).filter(Clientes.ID_Cliente == id_cliente).first()


# Actualizar un cliente
def actualizar_cliente(
    db: Session,
    id_cliente: int,
    nombre: str = None,
    apellido: str = None,
    direccion: str = None,
    telefono: str = None,
):
    """
    Actualiza los datos de un cliente existente.
    :param db: Sesión de base de datos.
    :param id_cliente: ID del cliente a actualizar.
    :param nombre: Nuevo nombre del cliente.
    :param apellido: Nuevo apellido del cliente.
    :param direccion: Nueva dirección del cliente.
    :param telefono: Nuevo teléfono del cliente.
    :return: Objeto del cliente actualizado o None si no existe.
    """
    cliente_existente = (
        db.query(Clientes).filter(Clientes.ID_Cliente == id_cliente).first()
    )
    if not cliente_existente:
        return None

    if nombre is not None:
        cliente_existente.Nombre = nombre
    if apellido is not None:
        cliente_existente.Apellido = apellido
    if direccion is not None:
        cliente_existente.Direccion = direccion
    if telefono is not None:
        cliente_existente.Teléfono = telefono

    db.commit()
    db.refresh(cliente_existente)
    return cliente_existente


# Eliminar un cliente
def eliminar_cliente(db: Session, id_cliente: int):
    """
    Elimina un cliente por su ID.
    :param db: Sesión de base de datos.
    :param id_cliente: ID del cliente a eliminar.
    :return: True si se eliminó correctamente, False si no se encontró.
    """
    cliente_existente = (
        db.query(Clientes).filter(Clientes.ID_Cliente == id_cliente).first()
    )
    if not cliente_existente:
        return False

    db.delete(cliente_existente)
    db.commit()
    return True
