import sqlite3 as sql


def createDB():
    conn = sql.connect("ladynails.db")
    conn.commit()
    conn.close()   

def createTable():
    conn = sql.connect("ladynails.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS productos (id INTEGER PRIMARY KEY, nombre TEXT, precio REAL, stock INTEGER)")
    conn.commit()
    conn.close()
    

def insertProduct(id, nombre, precio, stock):
    conn = sql.connect("ladynails.db")
    c = conn.cursor()
    c.execute("INSERT INTO productos VALUES (?, ?, ?, ?)", (id, nombre, precio, stock))
    conn.commit()
    conn.close()
    

if __name__ == "__main__":
    # createDB()
    # createTable()
    insertProduct(1, "Producto A", 100, 50)
    insertProduct(2, "Producto B", 150, 40)
    insertProduct(3, "Producto C", 200, 30)