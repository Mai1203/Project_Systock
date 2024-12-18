from sqlalchemy import Column, Integer, String, Boolean
from app.database.database import Base

class Usuarios(Base):
    __tablename__ = 'USUARIOS'

    ID_Usuario = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Nombre = Column(String(100), nullable=False)
    Usuario = Column(String(100), unique=True, nullable=False)
    Contraseña = Column(String(255), nullable=False)
    Estado = Column(Boolean, nullable=False)
    ID_Rol = Column(Integer, nullable=False)
    
    
