from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base

class Productos(Base):
    __tablename__ = 'PRODUCTOS'

    ID_Producto = Column(Integer, primary_key=True, index=True)
    Nombre = Column(String, nullable=False)
    Precio_costo = Column(Float, nullable=False)
    Precio_venta_mayor = Column(Float, nullable=False)
    Precio_venta_normal = Column(Float, nullable=False)
    Ganancia_Producto_mayor = Column(Float, nullable=False)
    Ganancia_Producto_normal = Column(Float, nullable=False)
    Stock_actual = Column(Integer, nullable=False)
    Stock_min = Column(Integer, nullable=False)
    Stock_max = Column(Integer, nullable=False)

    ID_Marca = Column(Integer, ForeignKey('MARCA.ID_Marca'))
    ID_Categoria = Column(Integer, ForeignKey('CATEGORIA.ID_Categoria'))

    # Relación con las tablas MARCA y CATEGORIA
    marca = relationship('Marca', back_populates='productos')
    categoria = relationship('Categoria', back_populates='productos')



