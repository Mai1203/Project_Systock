from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, configure_mappers
from pathlib import Path
import os

# Obtener la carpeta segura para almacenar la base de datos
app_data_dir = Path(os.getenv("APPDATA") or os.path.expanduser("~/.local/share")) / "Systock"
app_data_dir.mkdir(parents=True, exist_ok=True)  # Crea el directorio si no existe

# Nueva ruta para la base de datos
DATABASE_PATH = app_data_dir / "systock.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"  # Formato correcto para SQLAlchemy

# Crear el motor de conexión
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Base para los modelos
Base = declarative_base()

# Crear una sesión para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Inicializa la base de datos (crea tablas si no existen)."""
    from app.models import (
        usuarios,
        productos,
        facturas,
        detalle_facturas,
        venta_credito,
        clientes,
        pago_credito,
        tipo_ingresos,
        ingresos,
        caja,
        egresos,
        analisis_financiero,
        reporte,
        historial,
    )  # Importar los modelos

    try:
        configure_mappers()  # Configura todos los mapeos
    except Exception as e:
        print(f"Error al configurar los mappers: {e}")

    Base.metadata.create_all(bind=engine)
