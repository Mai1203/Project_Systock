from sqlalchemy import Column, Integer, Float, DateTime, Boolean, ForeignKey, String
from sqlalchemy.orm import relationship
from app.database.database import Base
from datetime import datetime
from pytz import timezone


def get_local_time():
    # Cambia 'America/Bogota' por tu zona horaria local
    local_tz = timezone("America/Bogota")
    now = datetime.now(local_tz)
    return now.replace(microsecond=0)

class Caja(Base):
    __tablename__ = "CAJA"

    ID_Caja = Column(Integer, primary_key=True, autoincrement=True)
    Monto_Base = Column(Float, nullable=False)
    Monto_Efectivo = Column(Float, nullable=True)
    Monto_Transaccion = Column(Float, nullable=True)
    Monto_Final_calculado = Column(Float, nullable=True)
    # Las fechas se generan con el sistema de apertura?
    Fecha_Apertura = Column(DateTime, default=get_local_time)
    Fecha_Cierre = Column(DateTime, nullable=True)
    Estado = Column(Boolean, nullable=False)

    ID_Usuario = Column(String, ForeignKey("USUARIOS.ID_Usuario"))

    # Relaciones
    usuarios = relationship("Usuarios", back_populates="caja")
    analisisfinanciero = relationship("AnalisisFinanciero", back_populates="caja")
