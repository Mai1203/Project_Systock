import sqlite3


class DatabaseManager:
    def __init__(self, db_path):
        self.connection = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        """Crea la tabla para almacenar los códigos de barra si no existe."""
        with self.connection:
            self.connection.execute("""
                CREATE TABLE IF NOT EXISTS barcodes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code TEXT UNIQUE
                )
            """)

    def insert_data(self, code):
        """Inserta un nuevo código en la base de datos."""
        with self.connection:
            self.connection.execute("INSERT INTO barcodes (code) VALUES (?)", (code,))

    def fetch_all_data(self):
        """Obtiene todos los datos almacenados."""
        with self.connection:
            return self.connection.execute("SELECT * FROM barcodes").fetchall()

    def check_if_exists(self, code):
        """Verifica si un código ya existe en la base de datos."""
        with self.connection:
            result = self.connection.execute("SELECT 1 FROM barcodes WHERE code = ?", (code,)).fetchone()
            return result is not None
