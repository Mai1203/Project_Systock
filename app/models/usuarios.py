from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base

class Usuarios(Base):
    __tablename__ = 'USUARIOS'

    ID_Usuario = Column(Integer, primary_key=True, index=True)
    Nombre = Column(String(100), nullable=False)
    Usuario = Column(String(100), unique=True, nullable=False)
    Contraseña = Column(String(255), nullable=False)
    Estado = Column(Boolean, nullable=False)
    
    ID_Rol = Column(Integer, ForeignKey('ROL.ID_Rol'))
    # Relación con las tablas MARCA y CATEGORIA
    rol = relationship('Rol', back_populates='Usuarios')
    cajas = relationship('Cajas', back_populates='Usuarios')
    reportes = relationship('Reportes', back_populates='Usuarios')
    historial_modificacion = relationship('HistorialModificacion', back_populates='Usuarios')
    historial_inicios = relationship('HistorialInicio', back_populates='Usuarios')
    
class Rol(Base):
    __tablename__ = 'ROL'
    
    ID_Rol = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Nombre = Column(String(50), nullable=False)
    
     # Relación con usuarios
    usuarios = relationship('Usuarios', back_populates='Rol')
    
