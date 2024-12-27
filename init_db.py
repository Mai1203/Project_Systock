from app.database.database import init_db, SessionLocal
from app.controllers.usuario_crud import *
from app.controllers.rol_crud import *
from app.controllers.producto_crud import *
from app.controllers.marca_crud import *
from app.controllers.categorias_crud import *

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
        print("Creando marcas de prueba...")
        crear_marca(db, "Neutrogena")
        crear_marca(db, "La Roche-Posay")
        crear_marca(db, "Maybelline")
        crear_marca(db, "Revlon")
        crear_marca(db, "L'Oréal")
        crear_marca(db, "Garnier")
        crear_marca(db, "Pantene")
        crear_marca(db, "Dove")
        crear_marca(db, "Moroccanoil")
        crear_marca(db, "Olay")
        crear_marca(db, "St. Ives")
        crear_marca(db, "Vaseline")
        crear_marca(db, "Chanel")
        crear_marca(db, "Nivea")
        crear_marca(db, "OPI")
        crear_marca(db, "The Body Shop")
        crear_marca(db, "Estée Lauder")
        crear_marca(db, "Tangle Teezer")
        crear_marca(db, "Sally Hansen")
        crear_marca(db, "Rexona")
        print("marcas de prueba creados exitosamente.")
    except Exception as e:
        print(f"Error al poblar datos: {e}")
        
    try:
        print("Creando categorias de prueba...")
        crear_categoria(db, "Cuidado Facial")
        crear_categoria(db, "Maquillaje")
        crear_categoria(db, "Cuidado Capilar")
        crear_categoria(db, "Cuidado Corporal")
        crear_categoria(db, "Perfumería")
        print("categorias de prueba creados exitosamente.")
    except Exception as e:
        print(f"Error al poblar datos: {e}")
        
    try:
        print("Creando productos de prueba...")
        crear_producto(db, 1001, "Crema Hidratante Facial", 25000, 50, 5, 100, 1, 1)
        crear_producto(db, 1002, "Protector Solar SPF 50", 35000, 75, 10, 150, 2, 1)
        crear_producto(db, 1003, "Labial Mate", 12000, 200, 20, 300, 3, 2)
        crear_producto(db, 1004, "Base de Maquillaje", 40000, 60, 5, 100, 4, 2)
        crear_producto(db, 1005, "Rímel Waterproof", 18000, 120, 10, 200, 5, 2)
        crear_producto(db, 1006, "Toallitas Desmaquillantes", 8000, 150, 10, 250, 6, 1)
        crear_producto(db, 1007, "Shampoo Anticaída", 30000, 80, 10, 120, 7, 3)
        crear_producto(db, 1008, "Acondicionador Hidratante", 32000, 70, 10, 150, 8, 3)
        crear_producto(db, 1009, "Aceite para el Cabello", 45000, 40, 5, 80, 9, 3)
        crear_producto(db, 1010, "Crema Antiedad", 60000, 30, 5, 60, 10, 1)
        crear_producto(db, 1011, "Exfoliante Corporal", 28000, 90, 10, 150, 11, 4)
        crear_producto(db, 1012, "Loción Hidratante Corporal", 22000, 100, 10, 200, 12, 4)
        crear_producto(db, 1013, "Perfume Floral", 85000, 50, 5, 100, 13, 5)
        crear_producto(db, 1014, "Crema para Manos", 15000, 120, 10, 200, 14, 4)
        crear_producto(db, 1015, "Pintura de Uñas", 10000, 300, 30, 500, 15, 2)
        crear_producto(db, 1016, "Mascarilla Facial", 20000, 60, 5, 100, 16, 1)
        crear_producto(db, 1017, "Sérum Reparador", 55000, 40, 5, 80, 17, 1)
        crear_producto(db, 1018, "Peine Desenredante", 18000, 80, 10, 150, 18, 3)
        crear_producto(db, 1019, "Esmalte en Gel", 20000, 150, 20, 300, 19, 2)
        crear_producto(db, 1020, "Desodorante Roll-on", 12000, 200, 20, 400, 20, 4)
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

if __name__ == "__main__":
    init_db()
    poblar_datos_prueba()
    # editar()