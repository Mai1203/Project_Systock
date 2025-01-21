from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    DateTime,
    Boolean,
    CheckConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.database import Base
from datetime import datetime
from pytz import timezone

def get_local_time():
    # Cambia 'America/Bogota' por tu zona horaria local
    local_tz = timezone('America/Bogota')
    now =datetime.now(local_tz)
    return now.replace(microsecond=0)

class Facturas(Base):
    __tablename__ = "FACTURA"

    ID_Factura = Column(Integer, primary_key=True, autoincrement=True)
    Fecha_Factura = Column(DateTime(timezone=True), default=get_local_time)
    Monto_efectivo = Column(Float, nullable=False)
    Monto_TRANSACCION = Column(Float, nullable=False)
    Estado = Column(Boolean, nullable=False)
    
    ID_Metodo_Pago = Column(Integer, ForeignKey("METODO_PAGO.ID_Metodo_Pago"))
    ID_Tipo_Factura = Column(Integer, ForeignKey("TIPO_FACTURA.ID_Tipo_Factura"))
    ID_Cliente = Column(Integer, ForeignKey("CLIENTES.ID_Cliente"))
    ID_Usuario = Column(Integer, ForeignKey("USUARIOS.ID_Usuario"))

    # Relaciones
    metodopago = relationship("MetodoPago", back_populates="facturas")
    tipofactura = relationship("TipoFactura", back_populates="facturas")
    detallefacturas = relationship("DetalleFacturas", back_populates="facturas")
    clientes = relationship("Clientes", back_populates="facturas")
    usuarios = relationship("Usuarios", back_populates="facturas")
    historialmodificacion = relationship(
        "HistorialModificacion", back_populates="facturas"
    )


class MetodoPago(Base):
    __tablename__ = "METODO_PAGO"

    ID_Metodo_Pago = Column(Integer, primary_key=True, autoincrement=True)
    Nombre = Column(String, nullable=False)

    __table_args__ = (
        CheckConstraint("Nombre IN ('Transferencia', 'Efectivo', 'Mixto')"),
    )

    # Relación con Factura
    facturas = relationship("Facturas", back_populates="metodopago")
    pagocredito = relationship("PagoCredito", back_populates="metodopago")
    egresos = relationship("Egresos", back_populates="metodopago")


class TipoFactura(Base):
    __tablename__ = "TIPO_FACTURA"

    ID_Tipo_Factura = Column(Integer, primary_key=True, autoincrement=True)
    Nombre = Column(String, nullable=False)

    __table_args__ = (CheckConstraint("Nombre IN ('Factura A', 'Factura B')"),)

    # Relación con Factura
    facturas = relationship("Facturas", back_populates="tipofactura")
