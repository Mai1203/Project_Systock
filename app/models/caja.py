from sqlalchemy import Column, Integer, Float, DateTime, Boolean, ForeignKey, String
from sqlalchemy.orm import relationship
from app.database.database import Base


class Caja(Base):
    __tablename__ = "CAJA"

    ID_Caja = Column(Integer, primary_key=True, autoincrement=True)
    Monto_Base = Column(Float, nullable=False)
    Monto_Efectivo = Column(Float, nullable=False)
    Monto_Transaccion = Column(Float, nullable=False)
    Monto_Final_calculado = Column(Float, nullable=False)
    # Las fechas se generan con el sistema de apertura?
    Fecha_Apertura = Column(DateTime, nullable=True)
    Fecha_Cierre = Column(DateTime, nullable=True)
    Estado = Column(Boolean, nullable=False)

    ID_Ingreso = Column(Integer, ForeignKey("INGRESOS.ID_Ingreso"))
    ID_Egreso = Column(Integer, ForeignKey("EGRESOS.ID_Egreso"))
    ID_Usuario = Column(String, ForeignKey("USUARIOS.ID_Usuario"))

    # Relaciones
    ingresos = relationship("Ingresos", back_populates="caja")
    egresos = relationship("Egresos", back_populates="caja")
    usuarios = relationship("Usuarios", back_populates="caja")
    analisisfinanciero = relationship("AnalisisFinanciero", back_populates="caja")
