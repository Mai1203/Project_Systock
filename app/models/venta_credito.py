from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.database import Base
from datetime import datetime
from pytz import timezone

def get_local_time():
    # Cambia 'America/Bogota' por tu zona horaria local
    local_tz = timezone('America/Bogota')
    now =datetime.now(local_tz)
    return now.replace(microsecond=0)

class VentaCredito(Base):
    __tablename__ = "VENTA_CREDITO"

    ID_Venta_Credito = Column(Integer, primary_key=True, autoincrement=True)
    Total_Deuda = Column(Float, nullable=False)
    Saldo_Pendiente = Column(Float, nullable=False)
    Fecha_Registro = Column(DateTime, default=get_local_time)
    Fecha_Limite = Column(DateTime, nullable=True)

    ID_Factura = Column(Integer, ForeignKey("FACTURA.ID_Factura"), nullable=False)

    # Relaciones
    facturas = relationship("Facturas", back_populates="ventacredito")
    pagocredito = relationship("PagoCredito", back_populates="ventacredito")
