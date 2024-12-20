from sqlalchemy.orm import Session
from app.models.reporte import (
    Reporte,
)


# Crear un nuevo reporte
def crear_reporte(db: Session, id_usuario: str, id_analisis_financiero: int):
    """
    Crea un nuevo reporte.
    :param db: Sesión de base de datos.
    :param id_usuario: ID del usuario que generó el reporte.
    :param id_analisis_financiero: ID del análisis financiero relacionado.
    :return: Objeto de reporte creado.
    """
    nuevo_reporte = Reporte(
        ID_Usuario=id_usuario, ID_Analisis_Financiero=id_analisis_financiero
    )
    db.add(nuevo_reporte)
    db.commit()
    db.refresh(nuevo_reporte)
    return nuevo_reporte


# Obtener todos los reportes
def obtener_reportes(db: Session):
    """
    Obtiene la lista de todos los reportes.
    :param db: Sesión de base de datos.
    :return: Lista de reportes.
    """
    return db.query(Reporte).all()


# Obtener un reporte por ID
def obtener_reporte_por_id(db: Session, id_reporte: int):
    """
    Obtiene un reporte por su ID.
    :param db: Sesión de base de datos.
    :param id_reporte: ID del reporte.
    :return: Objeto de reporte o None si no existe.
    """
    return db.query(Reporte).filter(Reporte.ID_Reporte == id_reporte).first()


# Actualizar un reporte
def actualizar_reporte(
    db: Session,
    id_reporte: int,
    id_usuario: str = None,
    id_analisis_financiero: int = None,
):
    """
    Actualiza un reporte existente.
    :param db: Sesión de base de datos.
    :param id_reporte: ID del reporte a actualizar.
    :param id_usuario: Nuevo ID de usuario (opcional).
    :param id_analisis_financiero: Nuevo ID de análisis financiero (opcional).
    :return: Objeto de reporte actualizado o None si no existe.
    """
    reporte_existente = (
        db.query(Reporte).filter(Reporte.ID_Reporte == id_reporte).first()
    )
    if not reporte_existente:
        return None

    if id_usuario:
        reporte_existente.ID_Usuario = id_usuario
    if id_analisis_financiero:
        reporte_existente.ID_Analisis_Financiero = id_analisis_financiero

    db.commit()
    db.refresh(reporte_existente)
    return reporte_existente


# Eliminar un reporte
def eliminar_reporte(db: Session, id_reporte: int):
    """
    Elimina un reporte por su ID.
    :param db: Sesión de base de datos.
    :param id_reporte: ID del reporte a eliminar.
    :return: True si se eliminó correctamente, False si no se encontró.
    """
    reporte_existente = (
        db.query(Reporte).filter(Reporte.ID_Reporte == id_reporte).first()
    )
    if not reporte_existente:
        return False

    db.delete(reporte_existente)
    db.commit()
    return True
