from sqlalchemy.orm import Session
from app.models.usuarios import Usuarios, Rol


# Crear un usuario
def crear_usuario(
    db: Session,
    Id_Usuario: str,
    nombre: str,
    usuario: str,
    contrasena: str,
    estado: bool,
    id_rol: int,
):
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
        Contrasena=contrasena,
        Estado=estado,
        ID_Rol=id_rol,
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
    usuarios = (
        db.query(
            Usuarios.ID_Usuario,
            Usuarios.Nombre,
            Usuarios.Usuario,
            Usuarios.Contrasena,
            Usuarios.Estado,
            
            Rol.Nombre.label('rol')
        )
        .join(Rol, Usuarios.ID_Rol == Rol.ID_Rol)
        .all()
    )
    return usuarios

# Obtener un usuario por ID
def obtener_usuario_por_id(db: Session, id_usuario: str):
    """
    Obtiene un usuario por su ID.
    :param db: Sesión de base de datos.
    :param id_usuario: ID del usuario.
    :return: Objeto de usuario o None si no existe.
    """
    usuario = (
        db.query(
            Usuarios.ID_Usuario,
            Usuarios.Nombre,
            Usuarios.Usuario,
            Usuarios.Contrasena,
            Usuarios.Estado,
            
            Rol.Nombre.label('rol')
        )
        .join(Rol, Usuarios.ID_Rol == Rol.ID_Rol)
        .filter(Usuarios.ID_Usuario == id_usuario)
        .first()
    )
    
    return usuario


# Actualizar un usuario
def actualizar_usuario(
    db: Session,
    id_usuario: int,
    nombre: str = None,
    usuario: str = None,
    contrasena: str = None,
    estado: bool = None,
):
    """
    Actualiza un usuario existente.
    :param db: Sesión de base de datos.
    :param id_usuario: ID del usuario a actualizar.
    :param nombre: Nuevo nombre del usuario.
    :param usuario: Nuevo nombre de usuario.
    :param contraseña: Nueva contraseña en texto plano.
    :param estado: Nuevo estado del usuario.
    :return: Objeto de usuario actualizado o None si no existe.
    """
    usuario_existente = (
        db.query(Usuarios).filter(Usuarios.ID_Usuario == id_usuario).first()
    )
    if not usuario_existente:
        return None

    if nombre:
        usuario_existente.Nombre = nombre
    if usuario:
        usuario_existente.Usuario = usuario
    if contrasena:
        usuario_existente.Contrasena = contrasena
    if estado is not None:
        usuario_existente.Estado = estado

    db.commit()
    db.refresh(usuario_existente)
    return usuario_existente


# Eliminar un usuario
def eliminar_usuario(db: Session, id_usuario: str):
    """
    Elimina un usuario por su ID.
    :param db: Sesión de base de datos.
    :param id_usuario: ID del usuario a eliminar.
    :return: True si se eliminó correctamente, False si no se encontró.
    """
    usuario_existente = (
        db.query(Usuarios).filter(Usuarios.ID_Usuario == id_usuario).first()
    )
    if not usuario_existente:
        return False

    db.delete(usuario_existente)
    db.commit()
    return True

def verificar_credenciales(db: Session, usuario: str, contrasena: str):
    """
    Verifica las credenciales del usuario.
    :param db: Sesión de la base de datos.
    :param usuario: Nombre de usuario.
    :param contraseña: Contraseña ingresada por el usuario.
    :return: Objeto del usuario si las credenciales son válidas, None si no lo son.
    """
    usuario_existente = db.query(Usuarios).filter(Usuarios.Usuario == usuario).first()
    if usuario_existente and usuario_existente.Contrasena == contrasena:
        return usuario_existente
    return None

