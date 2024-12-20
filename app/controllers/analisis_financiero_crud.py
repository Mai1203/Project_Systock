from sqlalchemy.orm import Session
from app.models.analisis_financiero import AnalisisFinanciero


# Crear un nuevo análisis financiero
def crear_analisis_financiero(
    db: Session,
    ganancia: float,
    id_egreso: int = None,
    id_tipo_ingreso: int = None,
    id_caja: int = None,
):
    """
    Crea un nuevo registro en la tabla AnalisisFinanciero.
    :param db: Sesión de base de datos.
    :param ganancia: Monto de la ganancia calculada.
    :param id_egreso: ID del egreso asociado (opcional).
    :param id_tipo_ingreso: ID del tipo de ingreso asociado (opcional).
    :param id_caja: ID de la caja asociada (opcional).
    :return: Objeto AnalisisFinanciero creado.
    """
    nuevo_analisis = AnalisisFinanciero(
        Ganancia=ganancia,
        ID_Egreso=id_egreso,
        ID_Tipo_Ingreso=id_tipo_ingreso,
        ID_Caja=id_caja,
    )
    db.add(nuevo_analisis)
    db.commit()
    db.refresh(nuevo_analisis)
    return nuevo_analisis


# Obtener todos los análisis financieros
def obtener_analisis_financieros(db: Session):
    """
    Obtiene todos los registros de análisis financiero.
    :param db: Sesión de base de datos.
    :return: Lista de objetos AnalisisFinanciero.
    """
    return db.query(AnalisisFinanciero).all()


# Obtener un análisis financiero por ID
def obtener_analisis_financiero_por_id(db: Session, id_analisis: int):
    """
    Obtiene un análisis financiero por su ID.
    :param db: Sesión de base de datos.
    :param id_analisis: ID del análisis financiero.
    :return: Objeto AnalisisFinanciero o None si no existe.
    """
    return (
        db.query(AnalisisFinanciero)
        .filter(AnalisisFinanciero.ID_Analisis_Financiero == id_analisis)
        .first()
    )


# Actualizar un análisis financiero
def actualizar_analisis_financiero(
    db: Session,
    id_analisis: int,
    ganancia: float = None,
    id_egreso: int = None,
    id_tipo_ingreso: int = None,
    id_caja: int = None,
):
    """
    Actualiza un registro de análisis financiero existente.
    :param db: Sesión de base de datos.
    :param id_analisis: ID del análisis financiero a actualizar.
    :param ganancia: Nueva ganancia calculada (opcional).
    :param id_egreso: Nuevo ID de egreso asociado (opcional).
    :param id_tipo_ingreso: Nuevo ID de tipo de ingreso asociado (opcional).
    :param id_caja: Nuevo ID de caja asociado (opcional).
    :return: Objeto AnalisisFinanciero actualizado o None si no existe.
    """
    analisis_existente = (
        db.query(AnalisisFinanciero)
        .filter(AnalisisFinanciero.ID_Analisis_Financiero == id_analisis)
        .first()
    )
    if not analisis_existente:
        return None

    if ganancia is not None:
        analisis_existente.Ganancia = ganancia
    if id_egreso is not None:
        analisis_existente.ID_Egreso = id_egreso
    if id_tipo_ingreso is not None:
        analisis_existente.ID_Tipo_Ingreso = id_tipo_ingreso
    if id_caja is not None:
        analisis_existente.ID_Caja = id_caja

    db.commit()
    db.refresh(analisis_existente)
    return analisis_existente


# Eliminar un análisis financiero
def eliminar_analisis_financiero(db: Session, id_analisis: int):
    """
    Elimina un análisis financiero por su ID.
    :param db: Sesión de base de datos.
    :param id_analisis: ID del análisis financiero a eliminar.
    :return: True si se eliminó correctamente, False si no se encontró.
    """
    analisis_existente = (
        db.query(AnalisisFinanciero)
        .filter(AnalisisFinanciero.ID_Analisis_Financiero == id_analisis)
        .first()
    )
    if not analisis_existente:
        return False

    db.delete(analisis_existente)
    db.commit()
    return True
