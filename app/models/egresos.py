from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String, func
from sqlalchemy.orm import relationship
from app.database.database import Base

class Egresos(Base):
    __tablename__ = 'EGRESOS'

    ID_Egreso = Column(Integer, primary_key=True, autoincrement=True)
    Tipo_Egreso = Column(String(50), nullable=False)
    Fecha_Egreso = Column(DateTime, default=func.now())
    Descripcion = Column(String(255), nullable=True)
    Monto_Egreso = Column(Float, nullable=False)
    
    ID_Metodo_Pago = Column(Integer, ForeignKey('METODO_PAGO.ID_Metodo_Pago'))

    # Relaciones
    metodo_pago = relationship('MetodoPago', back_populates='Egresos')
    cajas = relationship('Cajas', back_populates='Egresos')
    analisis_financiero = relationship('AnalisisFinanciero', back_populates='Egresos')