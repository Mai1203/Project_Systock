from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.database import Base
from datetime import datetime
from pytz import timezone


def get_local_time():
    # Cambia 'America/Bogota' por tu zona horaria local
    local_tz = timezone("America/Bogota")
    now = datetime.now(local_tz)
    return now.replace(microsecond=0)



class HistorialModificacion(Base):
    __tablename__ = "HISTORIAL_MODIFICACION"

    ID_Modificacion = Column(Integer, primary_key=True, autoincrement=True)
    Fecha_Modificacion = Column(DateTime, default=get_local_time)
    Descripcion = Column(String(255), nullable=True)

    ID_Factura = Column(Integer, ForeignKey("FACTURA.ID_Factura"))
    ID_Usuario = Column(String, ForeignKey("USUARIOS.ID_Usuario"))

    # Relaciones
    facturas = relationship("Facturas", back_populates="historialmodificacion")
    usuarios = relationship("Usuarios", back_populates="historialmodificacion")


class HistorialInicio(Base):
    __tablename__ = "HISTORIAL_INICIO"

    ID_Inicio = Column(Integer, primary_key=True, autoincrement=True)
    # Fecha de inicio de sesion (Coreccion)
    Inicio_Sesion = Column(DateTime, default=func.now())
    Cierre_Sesion = Column(DateTime, default=func.now())

    ID_Usuario = Column(String, ForeignKey("USUARIOS.ID_Usuario"))

    # Relaciones
    usuarios = relationship("Usuarios", back_populates="historialinicio")
