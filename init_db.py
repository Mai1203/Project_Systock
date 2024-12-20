from app.database.database import init_db, SessionLocal
from app.controllers.usuario_crud import *
from app.controllers.rol_crud import *
from app.controllers.producto_crud import *

def poblar_datos_prueba():
    db = SessionLocal()
    # Crear usuarios de prueba
    try:
        print("Eliminando rol...")
        rol = eliminar_rol(db, 2)
        if(rol):
            print("rol eliminado exitosamente.")
        else:
            print("No se encontro el rol")
            
            
        
        print("Eliminando cliente...")
        cli = eliminar_usuario(db, 987654321)
        if(cli):
            print("usuario eliminado exitosamente.")
        else:
            print("No se encontro el usuario.")
            
            
        
        print("Eliminando producto...")
        pro = eliminar_producto(db, 1254)
        if(pro):
            print("Producto eliminado exitosamente.")
        else:
            print("No se encontro el producto.")
            
        
    except Exception as e:
        print(f"Error al poblar datos: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    # init_db()  # Crear las tablas
    poblar_datos_prueba()  # Poblar datos de prueba
