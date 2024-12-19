from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base

class AnalisisFinanciero(Base):
    __tablename__ = 'ANALISIS_FINANCIERO'

    ID_Analisis_Financiero = Column(Integer, primary_key=True, autoincrement=True)
    Ganancia = Column(Float, nullable=False)
    
    ID_Egreso = Column(Integer, ForeignKey('EGRESOS.ID_Egreso'))
    ID_Tipo_Ingreso = Column(Integer, ForeignKey('TIPO_INGRESO.ID_Tipo_Ingreso'))
    ID_Caja = Column(Integer, ForeignKey('CAJA.ID_Caja'))

    # Relaciones
    egreso = relationship('Egresos', back_populates='AnalisisFinanciero')
    tipo_ingreso = relationship('TipoIngreso', back_populates='AnalisisFinanciero')
    caja = relationship('Cajas', back_populates='AnalisisFinanciero')
    reportes = relationship('Reportes', back_populates='AnalisisFinanciero')