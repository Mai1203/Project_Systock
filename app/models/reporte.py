from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.database import Base

class Reporte(Base):
    __tablename__ = 'REPORTE'

    ID_Reporte = Column(Integer, primary_key=True, autoincrement=True)
    Fecha_Reporte = Column(DateTime, default=func.now())
    
    ID_Usuario = Column(String, ForeignKey('USUARIOS.ID_Usuario'))
    ID_Analisis_Financiero = Column(Integer, ForeignKey('ANALISIS_FINANCIERO.ID_Analisis_Financiero'))

    # Relaciones
    usuarios = relationship('Usuarios', back_populates='reporte')
    analisisfinanciero = relationship('AnalisisFinanciero', back_populates='reporte')