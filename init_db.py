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
        print("Creando rols de prueba...")
        crear_rol(db, "ADMINISTRADOR")
        crear_rol(db, "ASESOR")
        print("Rols de prueba creados exitosamente.")
    except Exception as e:
        print(f"Error al poblar datos: {e}")
        
    
    try:
        print("Creando usuarios de prueba...")
        crear_usuario(db, 1004, "Admin", "admin", "admin", True, 1)
        print("usuarios de prueba creados exitosamente.")
    except Exception as e:
        print(f"Error al poblar datos: {e}")
        
    try:
        print("Creando productos de prueba...")
        crear_producto(db, 852, "Teclado_Mecanico", 4500, 100, 10, 150, 1, 1)
        crear_producto(db, 853, "Teclado_Mecanico", 3200, 100, 10, 150, 1, 1)
        crear_producto(db, 854, "Teclado_Mecanico", 1200, 100, 10, 150, 1, 1)
        crear_producto(db, 855, "Teclado_Mecanico", 2000, 100, 10, 150, 1, 1)
        crear_producto(db, 856, "Teclado_Mecanico", 80000, 100, 10, 150, 1, 1)
        print("Productos de prueba creados exitosamente.")
    except Exception as e:
        print(f"Error al poblar datos: {e}")
    
       
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

# if __name__ == "__main__":
#     init_db()
#     poblar_datos_prueba()
#     editar()