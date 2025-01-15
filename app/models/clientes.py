from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.database import Base


class Clientes(Base):
    __tablename__ = "CLIENTES"

   #ID_Cliente = Column(Integer, primary_key=True, index=True)
    ID_Cliente = Column(String(100), primary_key=True, index=True)
    Nombre = Column(String(100), nullable=False)
    Apellido = Column(String(100), nullable=False)
    Direccion = Column(String(255), nullable=False)
    Teléfono = Column(String(100), nullable=False)

    # Relación con Producto
    facturas = relationship("Facturas", back_populates="clientes")
    ventacredito = relationship("VentaCredito", back_populates="clientes")
