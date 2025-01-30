from app.database.database import init_db, SessionLocal
from app.controllers.usuario_crud import *
from app.controllers.rol_crud import *
from app.controllers.producto_crud import *
from app.controllers.marca_crud import *
from app.controllers.categorias_crud import *
from app.controllers.metodo_pago_crud import *
from app.controllers.tipo_factura_crud import *
from app.controllers.clientes_crud import *


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
        print("creando cliente default")
        crear_cliente(
            db, 111, "Predeterminado", "Predeterminado", "Predeterminado", "1234567890"
        )
        print("cliente default creado exitosamente.")
    except Exception as e:
        print(f"Error al poblar datos: {e}")

    try:
        print("creando Tipo Facturas")
        crear_tipo_factura(db, "Factura A")
        crear_tipo_factura(db, "Factura B")
        crear_tipo_factura(db, "Credito")
        print("Tipo Facturas creados exitosamente.")
    except Exception as e:
        print(f"Error al poblar datos: {e}")

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
        crear_producto(
            db, 1001, "Crema Hidratante Facial", 25000, 50, 3, 99, 50000, 48000, 1, 1
        )
        crear_producto(
            db, 1002, "Protector Solar SPF 50", 35000, 75, 10, 150, 70000, 68000, 2, 1
        )
        crear_producto(db, 1003, "Labial Mate", 12000, 200, 20, 300, 24000, 20000, 3, 2)
        crear_producto(
            db, 1004, "Base de Maquillaje", 40000, 60, 5, 100, 80000, 70000, 4, 2
        )
        crear_producto(
            db, 1005, "Rímel Waterproof", 18000, 120, 10, 200, 36000, 30000, 5, 2
        )
        crear_producto(
            db,
            1006,
            "Toallitas Desmaquillantes",
            8000,
            150,
            10,
            250,
            16000,
            12000,
            6,
            1,
        )
        crear_producto(
            db, 1007, "Shampoo Anticaída", 30000, 80, 10, 120, 60000, 50000, 7, 3
        )
        crear_producto(
            db,
            1008,
            "Acondicionador Hidratante",
            32000,
            70,
            10,
            150,
            64000,
            56000,
            8,
            3,
        )
        crear_producto(
            db, 1009, "Aceite para el Cabello", 45000, 40, 5, 80, 90000, 80000, 9, 3
        )
        crear_producto(db, 1010, "Crema Antiedad", 6000, 30, 5, 60, 12000, 10000, 10, 1)
        crear_producto(
            db, 1011, "Exfoliante Corporal", 28000, 90, 10, 150, 56000, 48000, 11, 4
        )
        crear_producto(
            db,
            1012,
            "Loción Hidratante Corporal",
            22000,
            100,
            10,
            200,
            44000,
            36000,
            12,
            4,
        )
        crear_producto(
            db, 1013, "Perfume Floral", 85000, 50, 5, 100, 90000, 87000, 13, 5
        )
        crear_producto(
            db, 1014, "Crema para Manos", 15000, 120, 10, 200, 30000, 24000, 14, 4
        )
        crear_producto(
            db, 1015, "Pintura de Uñas", 10000, 300, 30, 500, 20000, 18000, 15, 2
        )
        crear_producto(
            db, 1016, "Mascarilla Facial", 10000, 60, 5, 100, 20000, 18000, 16, 1
        )
        crear_producto(
            db, 1017, "Base de Maquillaje", 12000, 40, 5, 80, 24000, 16200, 2, 2
        )
        crear_producto(
            db, 1018, "Shampoo Fortificante", 8000, 70, 20, 150, 16000, 10800, 3, 3
        )
        crear_producto(
            db, 1019, "Loción Corporal", 10000, 60, 15, 120, 20000, 13500, 4, 4
        )
        crear_producto(
            db, 1020, "Perfume Exclusivo", 50000, 30, 5, 70, 100000, 67500, 5, 5
        )
        crear_producto(db, 1021, "Sérum Facial", 25000, 45, 10, 90, 50000, 33750, 6, 1)
        crear_producto(
            db, 1022, "Corrector de Ojeras", 18000, 35, 8, 70, 36000, 24300, 7, 2
        )
        crear_producto(
            db, 1023, "Acondicionador Nutritivo", 9000, 80, 25, 200, 18000, 12150, 8, 3
        )
        crear_producto(
            db, 1024, "Jabón Corporal", 7000, 100, 30, 250, 14000, 9450, 9, 4
        )
        crear_producto(
            db, 1025, "Esencia Aromática", 40000, 20, 5, 60, 80000, 54000, 10, 5
        )
        crear_producto(
            db, 1026, "Exfoliante Facial", 14000, 50, 10, 120, 28000, 18900, 11, 1
        )
        crear_producto(
            db, 1027, "Rubor Compacto", 11000, 30, 5, 70, 22000, 14850, 12, 2
        )
        crear_producto(
            db, 1028, "Spray Capilar", 9500, 65, 20, 140, 19000, 12825, 13, 3
        )
        crear_producto(
            db, 1029, "Aceite Corporal", 20000, 40, 10, 90, 40000, 27000, 14, 4
        )
        crear_producto(
            db, 1030, "Colonia Premium", 45000, 25, 5, 60, 90000, 60750, 15, 5
        )
        crear_producto(
            db, 1031, "Mascarilla Facial", 16000, 45, 10, 100, 32000, 21600, 16, 1
        )
        crear_producto(
            db, 1032, "Delineador de Ojos", 12500, 35, 5, 80, 25000, 16875, 17, 2
        )
        crear_producto(
            db, 1033, "Espuma Capilar", 8700, 75, 25, 180, 17400, 11745, 18, 3
        )
        crear_producto(
            db, 1034, "Loción Refrescante", 13000, 60, 20, 140, 26000, 17550, 19, 4
        )
        crear_producto(
            db, 1035, "Perfume Femenino", 55000, 20, 5, 50, 110000, 74250, 20, 5
        )
        crear_producto(
            db, 1036, "Tónico Facial", 17000, 55, 15, 120, 34000, 22950, 1, 1
        )
        crear_producto(db, 1037, "Polvo Compacto", 14000, 30, 8, 70, 28000, 18900, 2, 2)
        crear_producto(db, 1038, "Gel Capilar", 8000, 85, 20, 200, 16000, 10800, 3, 3)
        crear_producto(
            db, 1039, "Crema Corporal", 10000, 50, 15, 120, 20000, 13500, 4, 4
        )
        crear_producto(
            db, 1040, "Perfume Deluxe", 60000, 15, 5, 40, 120000, 81000, 5, 5
        )
        crear_producto(db, 1041, "Aceite Facial", 30000, 35, 8, 90, 60000, 40500, 6, 1)
        crear_producto(db, 1042, "Lápiz Labial", 18000, 40, 10, 80, 36000, 24300, 7, 2)
        crear_producto(
            db, 1043, "Crema Anti-Frizz", 12000, 65, 20, 140, 24000, 16200, 8, 3
        )
        crear_producto(db, 1044, "Jabón Líquido", 8000, 95, 30, 250, 16000, 10800, 9, 4)
        crear_producto(
            db, 1045, "Fragancia Exclusiva", 55000, 18, 5, 50, 110000, 74250, 10, 5
        )
        print("Productos de prueba creados exitosamente.")
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


if __name__ == "__main__":
    init_db()
    print("Base de datos inicializada exitosamente.")
    poblar_datos_prueba()
