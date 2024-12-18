from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.database import Base

class Categorias(Base):
    __tablename__ = 'CATEGORIAS'

    ID_Categoria = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Nombre = Column(String, nullable=False)

    # Relación con Producto
    productos = relationship('Producto', back_populates='categoria')