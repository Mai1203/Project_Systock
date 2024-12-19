from app.database.database import init_db, SessionLocal
from app.controllers.usuario_crud import crear_usuario

def poblar_datos_prueba():
    db = SessionLocal()
    # Crear usuarios de prueba
    crear_usuario(db, Nombre="Juan Pérez", Usuario="user1", contraseña="12345")
    crear_usuario(db, Nombre="María López", Usuario="user2", contraseña="67890")

    db.close()

if __name__ == "__main__":
    init_db()  # Crear las tablas
    # poblar_datos_prueba()  # Poblar datos de prueba
