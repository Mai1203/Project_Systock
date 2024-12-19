from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.database import Base

class Reporte(Base):
    __tablename__ = 'REPORTE'

    ID_Reporte = Column(Integer, primary_key=True, autoincrement=True)
    Fecha_Reporte = Column(DateTime, default=func.now())
    
    ID_Usuario = Column(Integer, ForeignKey('USUARIOS.ID_Usuario'))
    ID_Analisis_Financiero = Column(Integer, ForeignKey('ANALISIS_FINANCIERO.ID_Analisis_Financiero'))

    # Relaciones
    usuario = relationship('Usuarios', back_populates='Reportes')
    analisis_financiero = relationship('AnalisisFinanciero', back_populates='Reportes')