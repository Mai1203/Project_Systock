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
    ID_Detalle_Factura = Column(Integer, ForeignKey('DETALLE_FACTURA.ID_Detalle_Factura'))

    # Relaciones
    pago_credito = relationship('PagoCredito', back_populates='TipoIngreso')
    detalle_factura = relationship('DetalleFactura', back_populates='TipoIngreso')
    ingreso = relationship('Ingresos', back_populates='TipoIngreso')
    analisis_financiero = relationship('AnalisisFinanciero', back_populates='TipoIngreso')