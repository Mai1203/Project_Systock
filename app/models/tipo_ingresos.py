from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from app.database.database import Base

class TipoIngreso(Base):
    __tablename__ = 'TIPO_INGRESO'

    ID_Tipo_Ingreso = Column(Integer, primary_key=True, autoincrement=True)
    Tipo_Ingreso = Column(String, nullable=False)

    __table_args__ = (
        CheckConstraint("Tipo_Ingreso IN ('Venta', 'Abono')"),
    )
    
    ID_Pago_Credito = Column(Integer, ForeignKey('PAGO_CREDITO.ID_Pago_Credito'))
    ID_Detalle_Factura = Column(Integer, ForeignKey('DETALLE_FACTURAS.ID_Detalle_Factura'))

    # Relaciones
    pagocredito = relationship('PagoCredito', back_populates='tipoingreso')
    detallefacturas = relationship('DetalleFacturas', back_populates='tipoingreso')
    ingresos = relationship('Ingresos', back_populates='tipoingreso')
    analisisfinanciero = relationship('AnalisisFinanciero', back_populates='tipoingreso')