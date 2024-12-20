from app.database.database import init_db, SessionLocal
from app.controllers.usuario_crud import *
from app.controllers.rol_crud import *
from app.controllers.producto_crud import *


def poblar_datos_prueba():
    db = SessionLocal()
    # Crear usuarios de prueba
    try:
        print("Creando rol...")
        crear_rol(db, "Administrador")
        print("Rol creado exitosamente.")

        print("Creando usuario...")
        crear_usuario(db, "123456789", "Michael", "michael", "123456", True, 1)
        print("Usuario creado exitosamente.")

        print("Creando producto...")
        crear_producto(db, 1254, "Esmalte", 4500, 100, 10, 150, 1, 1)
        print("Producto creado exitosamente.")
    except Exception as e:
        print(f"Error al poblar datos: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    # init_db()  # Crear las tablas
    poblar_datos_prueba()  # Poblar datos de prueba
