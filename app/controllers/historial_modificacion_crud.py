from sqlalchemy.orm import Session
from app.models.historial import HistorialModificacion


# Crear un historial de modificación
def crear_historial_modificacion(
    db: Session, descripcion: str, id_factura: int, id_usuario: str
):
    """
    Crea un nuevo historial de modificación.
    :param db: Sesión de base de datos.
    :param descripcion: Descripción de la modificación realizada.
    :param id_factura: ID de la factura asociada.
    :param id_usuario: ID del usuario que realizó la modificación.
    :return: Objeto de historial de modificación creado.
    """
    nuevo_historial = HistorialModificacion(
        Descripcion=descripcion, ID_Factura=id_factura, ID_Usuario=id_usuario
    )
    db.add(nuevo_historial)
    db.commit()
    db.refresh(nuevo_historial)
    return nuevo_historial


# Obtener todos los historiales de modificación
def obtener_historiales_modificacion(db: Session):
    """
    Obtiene la lista de todos los historiales de modificación.
    :param db: Sesión de base de datos.
    :return: Lista de historiales de modificación.
    """
    return db.query(HistorialModificacion).all()


# Obtener un historial de modificación por ID
def obtener_historial_modificacion_por_id(db: Session, id_modificacion: int):
    """
    Obtiene un historial de modificación por su ID.
    :param db: Sesión de base de datos.
    :param id_modificacion: ID del historial de modificación.
    :return: Objeto de historial de modificación o None si no existe.
    """
    return (
        db.query(HistorialModificacion)
        .filter(HistorialModificacion.ID_Modificacion == id_modificacion)
        .first()
    )


# Actualizar un historial de modificación
def actualizar_historial_modificacion(
    db: Session, id_modificacion: int, descripcion: str = None
):
    """
    Actualiza un historial de modificación existente.
    :param db: Sesión de base de datos.
    :param id_modificacion: ID del historial de modificación a actualizar.
    :param descripcion: Nueva descripción de la modificación.
    :return: Objeto de historial de modificación actualizado o None si no existe.
    """
    historial_existente = (
        db.query(HistorialModificacion)
        .filter(HistorialModificacion.ID_Modificacion == id_modificacion)
        .first()
    )
    if not historial_existente:
        return None

    if descripcion:
        historial_existente.Descripcion = descripcion

    db.commit()
    db.refresh(historial_existente)
    return historial_existente


# Eliminar un historial de modificación
def eliminar_historial_modificacion(db: Session, id_modificacion: int):
    """
    Elimina un historial de modificación por su ID.
    :param db: Sesión de base de datos.
    :param id_modificacion: ID del historial de modificación a eliminar.
    :return: True si se eliminó correctamente, False si no se encontró.
    """
    historial_existente = (
        db.query(HistorialModificacion)
        .filter(HistorialModificacion.ID_Modificacion == id_modificacion)
        .first()
    )
    if not historial_existente:
        return False

    db.delete(historial_existente)
    db.commit()
    return True
