from sqlalchemy.orm import Session
from app.models.usuarios import Usuarios

def crear_usuario(db: Session, Nombre: str, Usuario: str, contraseña: str):
    nuevo_usuario = Usuarios(Nombre=Nombre, Usuario=Usuario, Contraseña=contraseña, Estado=True, ID_Rol=1)
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

