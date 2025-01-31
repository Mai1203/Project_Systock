from sqlalchemy.orm import Session
from app.models.facturas import MetodoPago


# Crear un método de pago
def crear_metodo_pago(db: Session, nombre: str):
    """
    Crea un nuevo método de pago.
    :param db: Sesión de base de datos.
    :param nombre: Nombre del método de pago (Transferencia, Pago en efectivo).
    :return: Objeto de método de pago creado.
    """
    nuevo_metodo = MetodoPago(Nombre=nombre)
    db.add(nuevo_metodo)
    db.commit()
    db.refresh(nuevo_metodo)
    return nuevo_metodo


# Obtener todos los métodos de pago
def obtener_metodos_pago(db: Session):
    """
    Obtiene la lista de todos los métodos de pago.
    :param db: Sesión de base de datos.
    :return: Lista de métodos de pago.
    """
    return db.query(MetodoPago).all()


# Obtener un método de pago por ID
def obtener_metodo_pago_por_id(db: Session, id_metodo_pago: int):
    """
    Obtiene un método de pago por su ID.
    :param db: Sesión de base de datos.
    :param id_metodo_pago: ID del método de pago.
    :return: Objeto de método de pago o None si no existe.
    """
    return (
        db.query(MetodoPago).filter(MetodoPago.ID_Metodo_Pago == id_metodo_pago).first()
    )


def obtener_metodo_pago_por_nombre(db: Session, nombre_metodo_pago: str):
    """
    Obtiene un método de pago por su nombre.
    :param db: Sesión de base de datos.
    :param nombre_metodo_pago: Nombre del método de pago.
    :return: Objeto de método de pago o None si no existe.
    """
    return (
        db.query(MetodoPago)
        .filter(MetodoPago.Nombre.ilike(f"%{nombre_metodo_pago}%"))
        .first()
    )


# Actualizar un método de pago
def actualizar_metodo_pago(db: Session, id_metodo_pago: int, nombre: str = None):
    """
    Actualiza un método de pago existente.
    :param db: Sesión de base de datos.
    :param id_metodo_pago: ID del método de pago a actualizar.
    :param nombre: Nuevo nombre del método de pago.
    :return: Objeto de método de pago actualizado o None si no existe.
    """
    metodo_existente = (
        db.query(MetodoPago).filter(MetodoPago.ID_Metodo_Pago == id_metodo_pago).first()
    )
    if not metodo_existente:
        return None

    if nombre:
        metodo_existente.Nombre = nombre

    db.commit()
    db.refresh(metodo_existente)
    return metodo_existente


# Eliminar un método de pago
def eliminar_metodo_pago(db: Session, id_metodo_pago: int):
    """
    Elimina un método de pago por su ID.
    :param db: Sesión de base de datos.
    :param id_metodo_pago: ID del método de pago a eliminar.
    :return: True si se eliminó correctamente, False si no se encontró.
    """
    metodo_existente = (
        db.query(MetodoPago).filter(MetodoPago.ID_Metodo_Pago == id_metodo_pago).first()
    )
    if not metodo_existente:
        return False

    db.delete(metodo_existente)
    db.commit()
    return True

def obtener_metodos_pago_por_ids(db: Session, window):
    """
    Obtiene los métodos de pago con IDs 0 y 1 y muestra los resultados en un QMessageBox.
    :param db: Sesión de base de datos.
    :param window: Ventana principal de la aplicación (usada para mostrar el QMessageBox).
    :return: None
    """
    # Buscar métodos de pago con ID 0 y 1
    metodo_pago_0 = db.query(MetodoPago).filter(MetodoPago.ID_Metodo_Pago == 0).first()
    metodo_pago_1 = db.query(MetodoPago).filter(MetodoPago.ID_Metodo_Pago == 1).first()
    
    # Crear el mensaje a mostrar
    mensaje = "Métodos de Pago Encontrados:\n"
    
    if metodo_pago_0:
        mensaje += f"ID 0: {metodo_pago_0.Nombre}\n"
    else:
        mensaje += "ID 0: No encontrado\n"
        
    if metodo_pago_1:
        mensaje += f"ID 1: {metodo_pago_1.Nombre}\n"
    else:
        mensaje += "ID 1: No encontrado\n"
    
    # Mostrar el mensaje en un QMessageBox
    msg_box = QMessageBox(window)
    msg_box.setIcon(QMessageBox.Information)
    msg_box.setWindowTitle("Resultado de Búsqueda de Métodos de Pago")
    msg_box.setText(mensaje)
    msg_box.exec_()
