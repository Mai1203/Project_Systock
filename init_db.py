from app.database.database import init_db, SessionLocal
from app.controllers.usuario_crud import *
from app.controllers.rol_crud import *
from app.controllers.producto_crud import *

def conectar_base():
    try:
        db = SessionLocal()
        return db
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")

def poblar_datos_prueba():
    db = SessionLocal()
    # Crear usuarios de prueba
    try:
        print("Creando rol...")
        crear_rol(db, "ADMINISTRADOR")
        print("Rol creado exitosamente.")

        print("Creando usuario...")
        crear_usuario(db, 1004598203, "Michael", "michael", "314159", True, 1)
        print("Usuario creado exitosamente.")

        print("Creando producto...")
        crear_producto(db, 1254, "Esmalte", 4500, 100, 10, 150, 1, 1)
        print("Producto creado exitosamente.")
    except Exception as e:
        print(f"Error al poblar datos: {e}")
    finally:
        db.close()

