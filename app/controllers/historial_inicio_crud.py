from sqlalchemy.orm import Session
from app.models.historial import HistorialInicio


# Crear un registro de historial de inicio de sesión
def crear_historial_inicio(db: Session, id_usuario: str, cierre_sesion: str = None):
    """
    Crea un nuevo registro de historial de inicio de sesión.
    :param db: Sesión de base de datos.
    :param id_usuario: ID del usuario que inició sesión.
    :param cierre_sesion: Fecha y hora opcional para el cierre de sesión.
    :return: Objeto de historial de inicio creado.
    """
    nuevo_historial = HistorialInicio(
        ID_Usuario=id_usuario, Cierre_Sesion=cierre_sesion
    )
    db.add(nuevo_historial)
    db.commit()
    db.refresh(nuevo_historial)
    return nuevo_historial


# Obtener todos los historiales de inicio de sesión
def obtener_historiales_inicio(db: Session):
    """
    Obtiene todos los registros de historial de inicio de sesión.
    :param db: Sesión de base de datos.
    :return: Lista de historiales de inicio.
    """
    return db.query(HistorialInicio).all()


# Obtener un historial de inicio de sesión por ID
def obtener_historial_inicio_por_id(db: Session, id_inicio: int):
    """
    Obtiene un registro de historial de inicio de sesión por su ID.
    :param db: Sesión de base de datos.
    :param id_inicio: ID del historial de inicio de sesión.
    :return: Objeto de historial de inicio o None si no existe.
    """
    return (
        db.query(HistorialInicio).filter(HistorialInicio.ID_Inicio == id_inicio).first()
    )


# Actualizar un historial de inicio de sesión
def actualizar_historial_inicio(db: Session, id_inicio: int, cierre_sesion: str = None):
    """
    Actualiza un registro de historial de inicio de sesión existente.
    :param db: Sesión de base de datos.
    :param id_inicio: ID del historial de inicio a actualizar.
    :param cierre_sesion: Nueva fecha y hora para el cierre de sesión.
    :return: Objeto de historial de inicio actualizado o None si no existe.
    """
    historial_existente = (
        db.query(HistorialInicio).filter(HistorialInicio.ID_Inicio == id_inicio).first()
    )
    if not historial_existente:
        return None

    if cierre_sesion:
        historial_existente.Cierre_Sesion = cierre_sesion

    db.commit()
    db.refresh(historial_existente)
    return historial_existente


# Eliminar un historial de inicio de sesión
def eliminar_historial_inicio(db: Session, id_inicio: int):
    """
    Elimina un registro de historial de inicio de sesión por su ID.
    :param db: Sesión de base de datos.
    :param id_inicio: ID del historial de inicio a eliminar.
    :return: True si se eliminó correctamente, False si no se encontró.
    """
    historial_existente = (
        db.query(HistorialInicio).filter(HistorialInicio.ID_Inicio == id_inicio).first()
    )
    if not historial_existente:
        return False

    db.delete(historial_existente)
    db.commit()
    return True
