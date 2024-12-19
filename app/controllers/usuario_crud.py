from sqlalchemy.orm import Session
from app.models.usuarios import Usuarios

# Crear un usuario
def crear_usuario(db: Session, Id_Usuario: str, nombre: str, usuario: str, contraseña: str, estado: bool, id_rol: int):
    """
    Crea un nuevo usuario.
    :param db: Sesión de base de datos.
    :param nombre: Nombre completo del usuario.
    :param usuario: Nombre de usuario único.
    :param contraseña: Contraseña en texto plano.
    :param estado: Estado del usuario (activo o inactivo).
    :param id_rol: ID del rol asociado al usuario.
    :return: Objeto de usuario creado.
    """
    # Hash de la contraseña para mayor seguridad

    nuevo_usuario = Usuarios(
        ID_Usuario=Id_Usuario,
        Nombre=nombre,
        Usuario=usuario,
        Contraseña=contraseña,
        Estado=estado,
        ID_Rol=id_rol
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

# Obtener todos los usuarios
def obtener_usuarios(db: Session):
    """
    Obtiene la lista de todos los usuarios.
    :param db: Sesión de base de datos.
    :return: Lista de usuarios.
    """
    return db.query(Usuarios).all()

# Obtener un usuario por ID
def obtener_usuario_por_id(db: Session, id_usuario: int):
    """
    Obtiene un usuario por su ID.
    :param db: Sesión de base de datos.
    :param id_usuario: ID del usuario.
    :return: Objeto de usuario o None si no existe.
    """
    return db.query(Usuarios).filter(Usuarios.ID_Usuario == id_usuario).first()

# Actualizar un usuario
def actualizar_usuario(db: Session, id_usuario: int, nombre: str = None, usuario: str = None, contraseña: str = None, estado: bool = None, id_rol: int = None):
    """
    Actualiza un usuario existente.
    :param db: Sesión de base de datos.
    :param id_usuario: ID del usuario a actualizar.
    :param nombre: Nuevo nombre del usuario.
    :param usuario: Nuevo nombre de usuario.
    :param contraseña: Nueva contraseña en texto plano.
    :param estado: Nuevo estado del usuario.
    :param id_rol: Nuevo ID de rol asociado.
    :return: Objeto de usuario actualizado o None si no existe.
    """
    usuario_existente = db.query(Usuarios).filter(Usuarios.ID_Usuario == id_usuario).first()
    if not usuario_existente:
        return None

    if nombre:
        usuario_existente.Nombre = nombre
    if usuario:
        usuario_existente.Usuario = usuario
    if contraseña:
        usuario_existente.Contraseña =contraseña
    if estado is not None:
        usuario_existente.Estado = estado
    if id_rol:
        usuario_existente.ID_Rol = id_rol

    db.commit()
    db.refresh(usuario_existente)
    return usuario_existente

# Eliminar un usuario
def eliminar_usuario(db: Session, id_usuario: int):
    """
    Elimina un usuario por su ID.
    :param db: Sesión de base de datos.
    :param id_usuario: ID del usuario a eliminar.
    :return: True si se eliminó correctamente, False si no se encontró.
    """
    usuario_existente = db.query(Usuarios).filter(Usuarios.ID_Usuario == id_usuario).first()
    if not usuario_existente:
        return False

    db.delete(usuario_existente)
    db.commit()
    return True
