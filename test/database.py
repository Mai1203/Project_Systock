from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

# Configuración de la cadena de conexión
DATABASE_URL = "mysql+pymysql://root:12032003@localhost/ladynail"

# Crear el motor de conexión
engine = create_engine(DATABASE_URL, echo=True)

# Crear una clase Base para las clases de modelo
Base = declarative_base()

# Definir un modelo simple (una tabla de prueba) con longitud para las columnas VARCHAR
class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), index=True)  # Especificar longitud de 255
    correo = Column(String(255), unique=True, index=True)  # Especificar longitud de 255

# Crear una sesión para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_connection():
    """ Verificar si SQLAlchemy está conectado a la base de datos y crear tablas """
    try:
        # Intentamos conectar a la base de datos y crear las tablas
        Base.metadata.create_all(bind=engine)
        print("Conexión exitosa y tablas creadas (si no existen).")
    except OperationalError as e:
        print(f"Error al conectar con la base de datos: {e}")
        return False
    return True

def create_user():
    """ Crear un usuario en la base de datos """
    db = SessionLocal()
    new_user = Usuario(nombre="Juan Pérez", correo="juan@example.com")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print(f"Usuario creado: {new_user.nombre} con correo: {new_user.correo}")
    db.close()

def get_users():
    """ Obtener todos los usuarios desde la base de datos """
    db = SessionLocal()
    users = db.query(Usuario).all()
    print("Usuarios en la base de datos:")
    for user in users:
        print(f"{user.id}: {user.nombre}, {user.correo}")
    db.close()

if __name__ == "__main__":
    # Verificar conexión
    if test_connection():
        # Crear un usuario como ejemplo
        create_user()
        # Obtener los usuarios
        get_users()
