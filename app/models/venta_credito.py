from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.database import Base

class VentaCredito(Base):
    __tablename__ = 'VENTA_CREDITO'

    ID_Venta_Credito = Column(Integer, primary_key=True, autoincrement=True)
    Max_Credito = Column(Float, nullable=False)
    Total_Deuda = Column(Float, nullable=False)
    Saldo_Pendiente = Column(Float, nullable=False)
    Fecha_Registro = Column(DateTime, default=func.now())
    Fecha_Limite = Column(DateTime, nullable=True)
    
    ID_Cliente = Column(Integer, ForeignKey('CLIENTES.ID_Cliente'))
    ID_Detalle_Factura = Column(Integer, ForeignKey('DETALLE_FACTURA.ID_Detalle_Factura'))

    # Relaciones
    cliente = relationship('Clientes', back_populates='VentaCredito')
    detalle_factura = relationship('DetalleFactura', back_populates='VentaCredito')
    pago_credito = relationship('PagoCredito', back_populates='VentaCredito')
