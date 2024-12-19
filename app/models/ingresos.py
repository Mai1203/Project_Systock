from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base


class Ingresos(Base):
    __tablename__ = "INGRESOS"

    ID_Ingreso = Column(Integer, primary_key=True, autoincrement=True)
    ID_Tipo_Ingreso = Column(Integer, ForeignKey("TIPO_INGRESO.ID_Tipo_Ingreso"))

    # Relaciones
    tipoingreso = relationship("TipoIngreso", back_populates="ingresos")
    caja = relationship("Caja", back_populates="ingresos")
