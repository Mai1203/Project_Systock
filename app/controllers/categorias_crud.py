from sqlalchemy.orm import Session
from app.models.productos import Categorias


# Crear una nueva categoría
def crear_categoria(db: Session, nombre: str):
    """
    Crea una nueva categoría.
    :param db: Sesión de base de datos.
    :param nombre: Nombre de la categoría.
    :return: Objeto Categorias creado.
    """
    nueva_categoria = Categorias(Nombre=nombre)
    db.add(nueva_categoria)
    db.commit()
    db.refresh(nueva_categoria)
    return nueva_categoria

def obtener_o_crear_categoria(db: Session, nombre_categoria):
    """
    Busca una categoría por su nombre. Si no existe, la crea y devuelve su ID.
    """
    # Buscar la categoría por nombre
    categoria = db.query(Categorias).filter(Categorias.Nombre == nombre_categoria).first()
    if categoria:
        return categoria.ID_Categoria  # Devolver ID si ya existe
    
    # Crear nueva categoría si no existe
    nueva_categoria = Categorias(Nombre=nombre_categoria)
    db.add(nueva_categoria)
    db.commit()  # Confirmar los cambios
    db.refresh(nueva_categoria)  # Actualizar el objeto para obtener el ID
    return nueva_categoria.ID_Categoria

# Obtener todas las categorías
def obtener_categorias(db: Session):
    """
    Obtiene todas las categorías.
    :param db: Sesión de base de datos.
    :return: Lista de objetos Categorias.
    """
    return db.query(Categorias).all()


# Obtener una categoría por ID
def obtener_categoria_por_id(db: Session, id_categoria: int):
    """
    Obtiene una categoría por su ID.
    :param db: Sesión de base de datos.
    :param id_categoria: ID de la categoría.
    :return: Objeto Categorias o None si no existe.
    """
    return db.query(Categorias).filter(Categorias.ID_Categoria == id_categoria).first()


# Actualizar una categoría
def actualizar_categoria(db: Session, id_categoria: int, nombre: str = None):
    """
    Actualiza una categoría existente.
    :param db: Sesión de base de datos.
    :param id_categoria: ID de la categoría a actualizar.
    :param nombre: Nuevo nombre de la categoría (opcional).
    :return: Objeto Categorias actualizado o None si no existe.
    """
    categoria_existente = (
        db.query(Categorias).filter(Categorias.ID_Categoria == id_categoria).first()
    )
    if not categoria_existente:
        return None

    if nombre is not None:
        categoria_existente.Nombre = nombre

    db.commit()
    db.refresh(categoria_existente)
    return categoria_existente


# Eliminar una categoría
def eliminar_categoria(db: Session, id_categoria: int):
    """
    Elimina una categoría por su ID.
    :param db: Sesión de base de datos.
    :param id_categoria: ID de la categoría a eliminar.
    :return: True si se eliminó correctamente, False si no se encontró.
    """
    categoria_existente = (
        db.query(Categorias).filter(Categorias.ID_Categoria == id_categoria).first()
    )
    if not categoria_existente:
        return False

    db.delete(categoria_existente)
    db.commit()
    return True
