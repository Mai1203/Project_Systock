import sqlite3 as sql


# Función para crear la base de datos
def createDB():
    conn = sql.connect("systock.db")
    conn.commit()
    conn.close()


# Función para crear las tablas principales
def createTables():
    conn = sql.connect("systock.db")
    cursor = conn.cursor()

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS CLIENTE (
        ID_Cliente VARCHAR(25) PRIMARY KEY,
        Nombre TEXT,
        Apellido TEXT,
        Dirección TEXT,
        Teléfono TEXT
    )"""
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS MARCA (
        ID_Marca INTEGER PRIMARY KEY AUTOINCREMENT,
        Nombre TEXT
    )"""
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS CATEGORIA (
        ID_Categoria INTEGER PRIMARY KEY AUTOINCREMENT,
        Nombre TEXT
    )"""
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS PRODUCTOS (
        ID_Producto INTEGER PRIMARY KEY,
        Nombre TEXT,
        Precio_costo DECIMAL(10,2),
        Precio_venta_mayor DECIMAL(10,2),
        Precio_venta_normal DECIMAL(10,2),
        Ganancia_Producto_mayor DECIMAL(10,2),
        Ganancia_Producto_normal DECIMAL(10,2),
        Stock_actual INTEGER,
        Stock_min INTEGER,
        Stock_max INTEGER,
        ID_Marca INTEGER,
        ID_Categoria INTEGER,
        FOREIGN KEY (ID_Marca) REFERENCES MARCA(ID_Marca),
        FOREIGN KEY (ID_Categoria) REFERENCES CATEGORIA(ID_Categoria)
    )"""
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS USUARIO (
        ID_Usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        Nombre TEXT,
        Usuario TEXT,
        Contraseña TEXT,
        Estado bollean,
        ID_Rol INTEGER,
        FOREIGN KEY (ID_Rol) REFERENCES ROL(ID_Rol)
    )"""
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS ROL (
        ID_Rol INTEGER PRIMARY KEY AUTOINCREMENT,
        Nombre TEXT NOT NULL CHECK (Nombre IN ('Administrador', 'Asesor'))
    )"""
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS FACTURA (
        ID_Factura INTEGER PRIMARY KEY AUTOINCREMENT,
        Fecha_Factura DATETIME DEFAULT CURRENT_TIMESTAMP,
        Monto_efectivo DECIMAL(10,2),
        Monto_TRANSACCION DECIMAL(10,2),
        Estado bollean,
        ID_Metodo_Pago INTEGER,
        ID_Tipo_Factura INTEGER,
        ID_Detalle_Factura INTEGER,
        FOREIGN KEY (ID_Detalle_Factura) REFERENCES DETALLE_FACTURA(ID_Detalle_Factura),
        FOREIGN KEY (ID_Metodo_Pago) REFERENCES METODO_PAGO(ID_Metodo_Pago),
        FOREIGN KEY (ID_Tipo_Factura) REFERENCES TIPO_FACTURA(ID_Tipo_Factura)
    )"""
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS METODO_PAGO (
        ID_Metodo_Pago INTEGER PRIMARY KEY AUTOINCREMENT,
        Nombre TEXT NOT NULL CHECK (Nombre IN ('Transferencia', 'Pago en efectivo'))
    )"""
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS TIPO_FACTURA(
        ID_Tipo_Factura INTEGER PRIMARY KEY AUTOINCREMENT,
        Nombre TEXT NOT NULL CHECK (Nombre IN ('Factura A', 'Factura B'))
    )"""
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS DETALLE_FACTURA(
        ID_Detalle_Factura INTEGER PRIMARY KEY AUTOINCREMENT,
        ID_Producto INTEGER,
        ID_Cliente INTEGER,
        Cantidad INTEGER,
        Precio_unitario DECIMAL(10,2),
        Subtotal DECIMAL(10,2),
        Descuento DECIMAL(10,2),
        FOREIGN KEY (ID_Producto) REFERENCES PRODUCTOS(ID_Producto),
        FOREIGN KEY (ID_Cliente) REFERENCES CLIENTE(ID_Cliente)
    )               
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS VENTA_CREDITO(
        ID_Venta_Credito INTEGER PRIMARY KEY AUTOINCREMENT,
        ID_Cliente INTEGER,
        ID_Detalle_Factura INTEGER,
        Max_Credito DECIMAL(10,2),
        Total_Deuda DECIMAL(10,2),
        Saldo_Pendiente DECIMAL(10,2),
        Fecha_Registro DATETIME DEFAULT CURRENT_TIMESTAMP,
        Fecha_Limite DATETIME,
        FOREIGN KEY (ID_Cliente) REFERENCES CLIENTE(ID_Cliente),
        FOREIGN KEY (ID_Detalle_Factura) REFERENCES DETALLE_FACTURA(ID_Detalle_Factura)
    )"""
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS PAGO_CREDITO(
        ID_Pago_Credito INTEGER PRIMARY KEY AUTOINCREMENT,
        ID_Venta_Credito INTEGER,
        ID_Metodo_Pago INTEGER,
        ID_Tipo_Pago INTEGER,
        Monto DECIMAL(10,2),
        Fecha_Registro DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (ID_Venta_Credito) REFERENCES VENTA_CREDITO(ID_Venta_Credito),
        FOREIGN KEY (ID_Metodo_Pago) REFERENCES METODO_PAGO(ID_Metodo_Pago),
        FOREIGN KEY (ID_Tipo_Pago) REFERENCES TIPO_PAGO(ID_Tipo_Pago)
    )"""
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS TIPO_INGRESO(
        ID_Tipo_Ingreso INTEGER PRIMARY KEY AUTOINCREMENT,
        ID_Pago_Credito INTEGER,
        ID_Detalle_Factura INTEGER,
        Tipo_Ingreso TEXT NOT NULL CHECK (Tipo_Ingreso IN ('Venta', 'Abono')),
        FOREIGN KEY (ID_Pago_Credito) REFERENCES PAGO_CREDITO(ID_Pago_Credito),
        FOREIGN KEY (ID_Detalle_Factura) REFERENCES DETALLE_FACTURA(ID_Detalle_Factura)
    )"""
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS INGRESOS(
        ID_Ingreso INTEGER PRIMARY KEY AUTOINCREMENT,
        ID_Tipo_Ingreso INTEGER,
        FOREIGN KEY (ID_Tipo_Ingreso) REFERENCES TIPO_INGRESO(ID_Tipo_Ingreso)
    )"""
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS CAJA(
        ID_Caja INTEGER PRIMARY KEY AUTOINCREMENT,
        ID_Ingreso INTEGER,
        ID_Egreso INTEGER,
        ID_Usuario INTEGER,
        Monto_Base DECIMAL(10,2),
        Monto_Efectivo DECIMAL(10,2),
        Monto_Transaccion DECIMAL(10,2),
        Monto_Final_calculado DECIMAL(10,2),
        Fecha_Apertura DATETIME,
        Fecha_Cierre DATETIME,
        Estado BOOLEAN,
        FOREIGN KEY (ID_Ingreso) REFERENCES INGRESOS(ID_Ingreso),
        FOREIGN KEY (ID_Usuario) REFERENCES USUARIO(ID_Usuario),
        FOREIGN KEY (ID_Egreso) REFERENCES EGRESOS(ID_Egreso)
    )"""
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS EGRESOS(
        ID_Egreso INTEGER PRIMARY KEY AUTOINCREMENT,
        ID_Metodo_Pago INTEGER,
        Tipo_Egreso VARCHAR(50),
        Fecha_Egreso DATETIME DEFAULT CURRENT_TIMESTAMP,
        Descripcion VARCHAR(255),
        Monto_Egreso DECIMAL(10,2),
        FOREIGN KEY (ID_Metodo_Pago) REFERENCES METODO_PAGO(ID_Metodo_Pago)
    )"""
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS ANALISIS_FINANCIERO(
        ID_Analisis_Financiero INTEGER PRIMARY KEY AUTOINCREMENT,
        ID_Egreso INTEGER,
        ID_Tipo_Ingreso INTEGER,
        ID_Caja INTEGER,
        Ganancia DECIMAL(10,2),
        FOREIGN KEY (ID_Egreso) REFERENCES EGRESOS(ID_Egreso),
        FOREIGN KEY (ID_Tipo_Ingreso) REFERENCES TIPO_INGRESO(ID_Tipo_Ingreso),
        FOREIGN KEY (ID_Caja) REFERENCES CAJA(ID_Caja)
    )"""
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS REPORTE(
        ID_Reporte INTEGER PRIMARY KEY AUTOINCREMENT,
        ID_Usuario INTEGER,
        ID_Analisis_Financiero INTEGER,
        Fecha_Reporte DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (ID_Usuario) REFERENCES USUARIO(ID_Usuario),
        FOREIGN KEY (ID_Analisis_Financiero) REFERENCES ANALISIS_FINANCIERO(ID_Analisis_Financiero)
    )"""
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS HISTORIAL_MODIFICACION(
        ID_Modificacion INTEGER PRIMARY KEY AUTOINCREMENT,
        ID_Factura INTEGER,
        ID_Usuario INTEGER,
        Fecha_Modificacion DATETIME DEFAULT CURRENT_TIMESTAMP,
        Descripcion VARCHAR(255),
        FOREIGN KEY (ID_Factura) REFERENCES FACTURA(ID_Factura),
        FOREIGN KEY (ID_Usuario) REFERENCES USUARIO(ID_Usuario)
    )"""
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS HISTORIAL_INICIO(
        ID_Inicio INTEGER PRIMARY KEY AUTOINCREMENT,
        ID_Usuario INTEGER,
        Inicio_Sesion DATETIME DEFAULT CURRENT_TIMESTAMP,
        Cierre_Sesion DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (ID_Usuario) REFERENCES USUARIO(ID_Usuario)
    )"""
    )

    conn.commit()
    conn.close()


# Ejecución de las funciones
if __name__ == "__main__":
    createDB()
    createTables()
