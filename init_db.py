from app.database.database import init_db, SessionLocal
from app.controllers.usuario_crud import *
from app.controllers.rol_crud import *
from app.controllers.producto_crud import *
from app.controllers.marca_crud import *
from app.controllers.categorias_crud import *
from app.controllers.metodo_pago_crud import *
from app.controllers.tipo_factura_crud import *
from app.controllers.clientes_crud import *
from app.controllers.tipo_pago_crud import *
from app.controllers.tipo_ingreso_crud import *
from app.controllers.ingresos_crud import *


def conectar_base():
    try:
        db = SessionLocal()
        return db
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")

def inicializar_db():
    try:
        init_db()
        print("Base de datos Inicializada")
        
    except Exception as e:
        print(f"Error al inicializar base de datos: {e}")
    
    poblar_datos_prueba()

def poblar_datos_prueba():
    db = SessionLocal()
    # Crear usuarios de prueba
    try:
        print("creando cliente default")
        crear_cliente(
            db, 111, "Predeterminado", "Predeterminado", "Predeterminado", "1234567890"
        )
        print("cliente default creado exitosamente.")
    except Exception as e:
        print(f"Error al crear cliente: {e}")
        
    try:
        print("Crear Tipo Pago")
        crear_tipo_pago(db, "Abono")
        crear_tipo_pago(db, "Pago Total")
        print("Tipo Pago creado exitosamente.")
    except Exception as e:
        print(f"Error al crear Tipo Pago: {e}")

    try:
        print("creando Tipo Facturas")
        crear_tipo_factura(db, "Factura A")
        crear_tipo_factura(db, "Factura B")
        crear_tipo_factura(db, "Credito")
        print("Tipo Facturas creados exitosamente.")
    except Exception as e:
        print(f"Error al crear Tipo Facturas: {e}")

    try:
        print("Creando rols de prueba...")
        crear_rol(db, "ADMINISTRADOR")
        crear_rol(db, "ASESOR")
        print("Rols de prueba creados exitosamente.")
    except Exception as e:
        print(f"Error al poblar datos: {e}")

    try:
        print("Creando usuarios de prueba...")
        crear_usuario(db, 87068087, "John Jairo Uribe", "admin", "admin", True, 1)
        print("usuarios de prueba creados exitosamente.")
    except Exception as e:
        print(f"Error al poblar datos: {e}")

    try:
        print("Creando metodos de pago ...")
        crear_metodo_pago(db, "Transferencia")
        crear_metodo_pago(db, "Efectivo")
        crear_metodo_pago(db, "Mixto")
    except Exception as e:
        print(f"Error al poblar datos: {e}")
    db.close()

    
