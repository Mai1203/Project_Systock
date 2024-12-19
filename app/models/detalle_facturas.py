from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base

class DetalleFacturas(Base):
    __tablename__ = 'DETALLE_FACTURAS'

    ID_Detalle_Factura = Column(Integer, primary_key=True, autoincrement=True)
    Cantidad = Column(Integer, nullable=False)
    Precio_unitario = Column(Float, nullable=False)
    Subtotal = Column(Float, nullable=False)
    Descuento = Column(Float, nullable=False)
    
    ID_Producto = Column(Integer, ForeignKey('PRODUCTOS.ID_Producto'))
    ID_Cliente = Column(Integer, ForeignKey('CLIENTES.ID_Cliente'))

    # Relaciones
    productos = relationship('Productos', back_populates='detallefacturas')
    clientes = relationship('Clientes', back_populates='detallefacturas')
    facturas = relationship('Facturas', back_populates='detallefacturas')
    tipoingreso = relationship('TipoIngreso', back_populates='detallefacturas')
    ventacredito = relationship('VentaCredito', back_populates='detallefacturas')