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
        print("Creando usuarios de prueba...")
        crear_usuario(db, 1004598203, "Michael", "maicol", "12032003", True, 1)
        print("usuarios de prueba creados exitosamente.")
    except Exception as e:
        print(f"Error al poblar datos: {e}")
    finally:
        db.close()
        
def editar():
    db = SessionLocal()
    try:
        print("Editando producto...")
        actualizar_producto(db, 852, "Teclado_Mecanico", 4500, 100, 150, 10, 10, 150, 1, 1)
        print("Producto editado exitosamente.")
    except Exception as e:
        print(f"Error al editar: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    # init_db()
    poblar_datos_prueba()
    # editar()