from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.database import Base

class Facturas(Base):
    __tablename__ = 'FACTURA'

    ID_Factura = Column(Integer, primary_key=True, autoincrement=True)
    Fecha_Factura = Column(DateTime, default=func.now())
    Monto_efectivo = Column(Float, nullable=False)
    Monto_TRANSACCION = Column(Float, nullable=False)
    Estado = Column(Boolean, nullable=False)
    ID_Metodo_Pago = Column(Integer, ForeignKey('METODO_PAGO.ID_Metodo_Pago'))
    ID_Tipo_Factura = Column(Integer, ForeignKey('TIPO_FACTURA.ID_Tipo_Factura'))
    ID_Detalle_Factura = Column(Integer, ForeignKey('DETALLE_FACTURA.ID_Detalle_Factura'))

    # Relaciones
    metodo_pago = relationship('MetodoPago', back_populates='Facturas')
    tipo_factura = relationship('TipoFactura', back_populates='Facturas')
    detalle_factura = relationship('DetalleFactura', back_populates='Facturas')
    historial_modificacion = relationship('HistorialModificacion', back_populates='Facturas')


class MetodoPago(Base):
    __tablename__ = 'METODO_PAGO'

    ID_Metodo_Pago = Column(Integer, primary_key=True, autoincrement=True)
    Nombre = Column(String, nullable=False)
    
    __table_args__ = (
        CheckConstraint("Nombre IN ('Transferencia', 'Pago en efectivo')"),
    )

    # Relación con Factura
    facturas = relationship('Facturs', back_populates='MetodoPago')
    pago_credito = relationship('PagoCredito', back_populates='MetodoPago')
    egreso = relationship('Egresos', back_populates='MetodoPago')


class TipoFactura(Base):
    __tablename__ = 'TIPO_FACTURA'

    ID_Tipo_Factura = Column(Integer, primary_key=True, autoincrement=True)
    Nombre = Column(String, nullable=False)

    __table_args__ = (
        CheckConstraint("Nombre IN ('Factura A', 'Factura B')"),
    )

    # Relación con Factura
    facturas = relationship('Facturas', back_populates='TipoFactura')