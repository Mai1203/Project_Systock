from PyQt5.QtWidgets import (
    QMessageBox,
    QWidget
)
from PyQt5 import QtWidgets
from ..database.database import SessionLocal
from ..controllers.producto_crud import *
from ..ui import Ui_Productos

class ProductosView(QWidget, Ui_Productos):
    def __init__(self, parent=None):
        super(ProductosView, self).__init__(parent)
        self.setupUi(self)
        # Enfocar automáticamente el campo de entrada al abrir
        self.InputCodigo.setFocus()

        # Conectar el evento de tecla Enter para procesar el código
        self.InputCodigo.returnPressed.connect(self.procesar_codigo)
        
        self.BtnIngresarProducto.clicked.connect(self.ingresar_producto)
        self.BtnEliminar.clicked.connect(self.eliminar_producto)
        self.limpiar_tabla_productos()
        self.mostrar_productos()
        
    def procesar_codigo(self):
        codigo = self.InputCodigo.text().strip()
    
        # Validar si el código es válido
      
    
         # Aquí puedes agregar la lógica para buscar el producto usando el código
        self.buscar_producto_por_codigo(codigo)

        # Limpiar el campo InputCodigo para que se pueda escanear otro código
        self.InputCodigo.clear()

        
    def procesar_codigo(self):
        """
        Procesa el código ingresado en el campo InputCodigo.
        """
        codigo = self.InputCodigo.text().strip()
    def obtener_id_producto(self):
        """
        Obtiene el id del producto seleccionado en la tabla.
        """
        fila_seleccionada = self.TablaProductos.currentRow()
        
        if fila_seleccionada == -1:
            QtWidgets.QMessageBox.warning(self, "Error", "Selecciona un producto")
            return None
        
        id = self.TablaProductos.item(fila_seleccionada, 0).text()
        if id:
            return id
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "No se pudo obtener el ID del producto")
            return None
    
        
    def eliminar_producto(self):
        """
        Elimina el producto seleccionado en la tabla.
        """
        id = self.obtener_id_producto()
        if id is None:
            return
        respuesta = QMessageBox.question(
            self,
            "Confirmar Eliminación",
            f"¿Estás seguro de que deseas eliminar el producto con ID {id}?",
            QMessageBox.Yes | QMessageBox.No
        )
        if respuesta == QMessageBox.No:
            return
        
        try:
            self.db = SessionLocal()
            eliminar_producto(self.db, id)  # Llamar a la función de base de datos
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo eliminar el producto: {str(e)}")
            return

        QMessageBox.information(self, "Éxito", "Producto eliminado correctamente.")
        
        self.db.close()
        self.limpiar_tabla_productos()
        self.mostrar_productos()
    
    def mostrar_productos(self):
        """
        Obtener todos los productos de la base de datos y mostrarlos en la tabla.
        """
        self.db = SessionLocal()
        rows = obtener_productos(self.db)
        
        if rows:
            self.TablaProductos.setRowCount(len(rows))
            self.TablaProductos.setColumnCount(12)
            
            for row_idx, row in enumerate(rows):
                id_producto = str(row.ID_Producto)
                nombre = str(row.Nombre)
                precio_compra = str(row.Precio_costo)
                precio_venta_mayor = str(row.Precio_venta_mayor)
                precio_venta_normal = str(row.Precio_venta_normal)
                ganancia_producto_mayor = str(row.Ganancia_Producto_mayor)
                ganancia_producto_normal = str(row.Ganancia_Producto_normal)
                cantidad = str(row.Stock_actual)
                cantidad_min = str(row.Stock_min)
                cantidad_max = str(row.Stock_max)
                marca = str(row.ID_Marca)
                categoria = str(row.ID_Categoria)
                
                self.TablaProductos.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(id_producto))
                self.TablaProductos.setItem(row_idx, 1, QtWidgets.QTableWidgetItem(nombre))
                self.TablaProductos.setItem(row_idx, 2, QtWidgets.QTableWidgetItem(marca))
                self.TablaProductos.setItem(row_idx, 3, QtWidgets.QTableWidgetItem(categoria))
                self.TablaProductos.setItem(row_idx, 4, QtWidgets.QTableWidgetItem(cantidad))
                self.TablaProductos.setItem(row_idx, 5, QtWidgets.QTableWidgetItem(cantidad_min))
                self.TablaProductos.setItem(row_idx, 6, QtWidgets.QTableWidgetItem(cantidad_max))
                self.TablaProductos.setItem(row_idx, 7, QtWidgets.QTableWidgetItem(precio_compra))
                self.TablaProductos.setItem(row_idx, 9, QtWidgets.QTableWidgetItem(precio_venta_normal))
                self.TablaProductos.setItem(row_idx, 8, QtWidgets.QTableWidgetItem(precio_venta_mayor))
                self.TablaProductos.setItem(row_idx, 10, QtWidgets.QTableWidgetItem(ganancia_producto_normal))
                self.TablaProductos.setItem(row_idx, 11, QtWidgets.QTableWidgetItem(ganancia_producto_mayor))
        
        self.db.close()
    
    def limpiar_tabla_productos(self):
        """
        Limpia la tabla de productos.
        """
        self.TablaProductos.setRowCount(0)
        self.TablaProductos.setColumnCount(12)
        
    def ingresar_producto(self):
        """
        Captura los datos del formulario y los registra en la base de datos.
        """
        self.db = SessionLocal()
        id = self.InputCodigo.text()
        nombre = self.InputNombre.text()
        precio_compra = self.InputPrecioCompra.text()
        cantidad = self.InputCantidad.text()
        cantidad_min = self.InputCantidadMin.text()
        cantidad_max = self.InputCantidadMax.text()
        marca = self.InputMarca.text()
        categoria = self.InputCategoria.text()
        
        if not id or not nombre or not precio_compra or not cantidad or not cantidad_min or not cantidad_max or not marca or not categoria:
            QtWidgets.QMessageBox.warning(self, "Error", "Por favor, rellene todos los campos")
            return
        
        try:
            id = int(id)
            precio_compra = float(precio_compra)
            cantidad = int(cantidad)
            cantidad_min = int(cantidad_min)
            cantidad_max = int(cantidad_max)
            marca = int(marca)
            categoria = int(categoria)
            
            crear_producto(self.db, id, nombre, precio_compra, cantidad, cantidad_min, cantidad_max, marca, categoria)
            QtWidgets.QMessageBox.information(self, "Éxito", "Producto registrado exitosamente")
            self.limpiar_formulario()
            self.limpiar_tabla_productos()
            self.mostrar_productos()
            self.db.close()
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Error", "Por favor, ingrese valores numéricos")
        
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Error: {e}")
            
    def limpiar_formulario(self):
        """
        Limpia el formulario de todos los campos.
        """
        self.InputCodigo.setText("")
        self.InputNombre.setText("")
        self.InputPrecioCompra.setText("")
        self.InputCantidad.setText("")
        self.InputCantidadMin.setText("")
        self.InputCantidadMax.setText("")
        self.InputMarca.setText("")
        self.InputCategoria.setText("")