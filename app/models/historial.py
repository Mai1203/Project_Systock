from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.database import Base

class HistorialModificacion(Base):
    __tablename__ = 'HISTORIAL_MODIFICACION'

    ID_Modificacion = Column(Integer, primary_key=True, autoincrement=True)
    Fecha_Modificacion = Column(DateTime, default=func.now())
    Descripcion = Column(String(255), nullable=True)
    
    ID_Factura = Column(Integer, ForeignKey('FACTURA.ID_Factura'))
    ID_Usuario = Column(Integer, ForeignKey('USUARIOS.ID_Usuario'))

    # Relaciones
    factura = relationship('Facturas', back_populates='HistorialModificacion')
    usuario = relationship('Usuarios', back_populates='HistorialModificacion')

class HistorialInicio(Base):
    __tablename__ = 'HISTORIAL_INICIO'

    ID_Inicio = Column(Integer, primary_key=True, autoincrement=True)
    #Fecha de inicio de sesion (Coreccion)
    Inicio_Sesion = Column(DateTime, default=func.now())
    Cierre_Sesion = Column(DateTime, default=func.now())
    
    ID_Usuario = Column(Integer, ForeignKey('USUARIOS.ID_Usuario'))

    # Relaciones
    usuario = relationship('Usuarios', back_populates='HistorialInicio')