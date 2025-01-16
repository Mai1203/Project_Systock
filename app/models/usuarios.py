from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base


class Usuarios(Base):
    __tablename__ = "USUARIOS"

    ID_Usuario = Column(String(100), primary_key=True, index=True)
    Nombre = Column(String(100), nullable=False)
    Usuario = Column(String(100), unique=True, nullable=False)
    Contrasena = Column(String(255), nullable=False)
    Estado = Column(Boolean, nullable=False)

    ID_Rol = Column(Integer, ForeignKey("ROL.ID_Rol"))
    # Relación con las tablas MARCA y CATEGORIA
    rol = relationship("Rol", back_populates="usuarios")
    caja = relationship("Caja", back_populates="usuarios")
    reporte = relationship("Reporte", back_populates="usuarios")
    historialmodificacion = relationship(
        "HistorialModificacion", back_populates="usuarios"
    )
    historialinicio = relationship("HistorialInicio", back_populates="usuarios")
    facturas = relationship("Facturas", back_populates="usuarios")


class Rol(Base):
    __tablename__ = "ROL"

    ID_Rol = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Nombre = Column(String(50), nullable=False)

    # Relación con usuarios
    usuarios = relationship("Usuarios", back_populates="rol")
