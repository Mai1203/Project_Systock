import sqlite3 as sql

def createDB():
  conn = sql.connect("ladynails.db")
  conn.commit()
  conn.close()
  
def createTable():
  conn = sql.connect("ladynails.db")
  cursor = conn.cursor()
  cursor.execute("CREATE TABLE IF NOT EXISTS productos (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT, precio REAL, stock INTEGER)")
  conn.commit()
  conn.close()
  
def insertRow(nombre, precio, stock):
  conn = sql.connect("ladynails.db")
  cursor = conn.cursor()
  cursor.execute("INSERT INTO productos (nombre, precio, stock) VALUES (?,?,?)", (nombre, precio, stock))
  conn.commit()
  conn.close()

if __name__ == "__main__":
  #createDB()
  #createTable()
  insertRow("Producto A", 100, 50)