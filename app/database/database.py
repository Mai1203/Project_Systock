from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuración de la conexión a la base de datos
# Cambiar aquí entre SQLite o MySQL según la necesidad
DATABASE_URL = "sqlite:///./systock.db"  # Base de datos SQLite en el archivo local "inventario.db"
# Para MySQL, usarías algo como:
# DATABASE_URL = "mysql+pymysql://root:tu_contraseña@localhost/inventario_db"

# Crear el motor de conexión
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Base para los modelos
Base = declarative_base()

# Crear una sesión para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Inicializa la base de datos (crea tablas si no existen)."""
    from app.models import usuarios, productos, facturas, detalle_facturas, venta_credito, clientes, pago_credito, tipo_ingresos, ingresos, caja, egresos, analisis_financiero, reporte, historial  # Importar los modelos
    Base.metadata.create_all(bind=engine)
