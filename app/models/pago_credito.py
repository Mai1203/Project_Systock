from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, String, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.database import Base

class PagoCredito(Base):
    __tablename__ = 'PAGO_CREDITO'

    ID_Pago_Credito = Column(Integer, primary_key=True, autoincrement=True)
    Monto = Column(Float, nullable=False)
    Fecha_Registro = Column(DateTime, default=func.now())
    
    ID_Venta_Credito = Column(Integer, ForeignKey('VENTA_CREDITO.ID_Venta_Credito'))
    ID_Metodo_Pago = Column(Integer, ForeignKey('METODO_PAGO.ID_Metodo_Pago'))
    ID_Tipo_Pago = Column(Integer, ForeignKey('TIPO_PAGO.ID_Tipo_Pago'))

    # Relaciones
    venta_credito = relationship('VentaCredito', back_populates='PagoCredito')
    metodo_pago = relationship('MetodoPago', back_populates='PagoCredito')
    tipo_pago = relationship('TipoPago', back_populates='PagoCredito')
    tipo_ingresos = relationship('TipoIngreso', back_populates='PagoCredito')
    
class TipoPago(Base):
    __tablename__ = 'TIPO_PAGO'

    ID_Tipo_Pago = Column(Integer, primary_key=True, autoincrement=True)
    Nombre = Column(String, nullable=False)

    __table_args__ = (
        CheckConstraint("Nombre IN ('Abono', 'Pago Total')"),
    )

    # Relación con PagoCredito
    pago_credito = relationship('PagoCredito', back_populates='TipoPago')