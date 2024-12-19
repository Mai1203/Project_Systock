from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base


class Productos(Base):
    __tablename__ = "PRODUCTOS"

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

    ID_Marca = Column(Integer, ForeignKey("MARCAS.ID_Marca"))
    ID_Categoria = Column(Integer, ForeignKey("CATEGORIAS.ID_Categoria"))

    # Relación con las tablas MARCA y CATEGORIA
    marcas = relationship("Marcas", back_populates="productos")
    categorias = relationship("Categorias", back_populates="productos")
    detallefacturas = relationship("DetalleFacturas", back_populates="productos")


class Marcas(Base):
    __tablename__ = "MARCAS"

    ID_Marca = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Nombre = Column(String, nullable=False)

    # Relación con Producto
    productos = relationship("Productos", back_populates="marcas")


class Categorias(Base):
    __tablename__ = "CATEGORIAS"

    ID_Categoria = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Nombre = Column(String, nullable=False)

    # Relación con Producto
    productos = relationship("Productos", back_populates="categorias")
