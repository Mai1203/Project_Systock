from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base

class DetalleFacturas(Base):
    __tablename__ = 'DETALLE_FACTURA'

    ID_Detalle_Factura = Column(Integer, primary_key=True, autoincrement=True)
    Cantidad = Column(Integer, nullable=False)
    Precio_unitario = Column(Float, nullable=False)
    Subtotal = Column(Float, nullable=False)
    Descuento = Column(Float, nullable=False)
    
    ID_Producto = Column(Integer, ForeignKey('PRODUCTOS.ID_Producto'))
    ID_Cliente = Column(Integer, ForeignKey('CLIENTES.ID_Cliente'))

    # Relaciones
    producto = relationship('Productos', back_populates='DetalleFactura')
    cliente = relationship('Clientes', back_populates='DetalleFactura')
    facturas = relationship('Facturas', back_populates='DetalleFactura')
    tipo_ingreso = relationship('TipoIngreso', back_populates='DetalleFactura')