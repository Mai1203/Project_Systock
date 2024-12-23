from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QHBoxLayout,
    QWidget,
    QStackedWidget,
    QSizePolicy,
    QMessageBox,
)
from PyQt5 import QtWidgets
from ..ui import Ui_Navbar, Ui_Respaldo, Ui_ControlUsuario, Ui_VentasA, Ui_VentasCredito, Ui_Facturas, Ui_Egreso, Ui_Productos, Ui_FacturasCredito, Ui_Caja, Ui_Reportes
from ..database.database import SessionLocal
from ..controllers.producto_crud import *
import sys


class Navbar(QWidget, Ui_Navbar):
    def __init__(self, parent=None):
        super(Navbar, self).__init__(parent)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.setupUi(self)

class RespaldoView(QWidget, Ui_Respaldo):
    def __init__(self, parent=None):
        super(RespaldoView, self).__init__(parent)
        self.setupUi(self)

class ControlUsuarioView(QWidget, Ui_ControlUsuario):
    def __init__(self, parent=None):
        super(ControlUsuarioView, self).__init__(parent)
        self.setupUi(self)
        
class VentasAView(QWidget, Ui_VentasA):
    def __init__(self, parent=None):
        super(VentasAView, self).__init__(parent)
        self.setupUi(self)

class VentasCreditoView(QWidget, Ui_VentasCredito):
    def __init__(self, parent=None):
        super(VentasCreditoView, self).__init__(parent)
        self.setupUi(self)

class FacturasView(QWidget, Ui_Facturas):
    def __init__(self, parent=None):
        super(FacturasView, self).__init__(parent)
        self.setupUi(self)
        
class CajaView(QWidget, Ui_Caja):
    def __init__(self, parent=None):
        super(CajaView, self).__init__(parent)
        self.setupUi(self)

class EgresoView(QWidget, Ui_Egreso):
    def __init__(self, parent=None):
        super(EgresoView, self).__init__(parent)
        self.setupUi(self)

class ProductosView(QWidget, Ui_Productos):
    def __init__(self, parent=None):
        super(ProductosView, self).__init__(parent)
        self.setupUi(self)
        
        self.BtnIngresarProducto.clicked.connect(self.ingresar_producto)
        self.BtnEliminar.clicked.connect(self.eliminar_producto)
        self.limpiar_tabla_productos()
        self.mostrar_productos()
    
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
      
        
class ReportesView(QWidget, Ui_Reportes):    
    def __init__(self, parent=None):
        super(ReportesView, self).__init__(parent)
        self.setupUi(self)

class CrediFacturaView(QWidget, Ui_FacturasCredito):
    def __init__(self, parent=None):
        super(CrediFacturaView, self).__init__(parent)
        self.setupUi(self)

# Clase principal
class MainApp(QMainWindow):
    def __init__(self):
        super(MainApp, self).__init__()

        # Configurar la ventana principal
        self.setWindowTitle("Aplicación Principal")
        self.resize(800, 600)

        self.setStyleSheet("background-color: white;")
        
        # Widget central que contiene el diseño principal
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Crear el diseño principal
        layout = QHBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)  # Sin márgenes
        layout.setSpacing(0)

        # Crear el Navbar
        self.navbar = Navbar()
        layout.addWidget(self.navbar)  # Agregar el Navbar al lado izquierdo

        # Crear el QStackedWidget para el contenido
        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)  # Agregar el QStackedWidget al lado derecho

        # Crear y agregar vistas al QStackedWidget
        self.ventasA = VentasAView()
        self.ventasCredito = VentasCreditoView()
        self.facturas = FacturasView()
        self.caja = CajaView()
        self.egreso = EgresoView()
        self.productos = ProductosView()
        self.respaldo_view = RespaldoView()
        self.control_usuario_view = ControlUsuarioView()
        self.reportes = ReportesView()
        self.crediFactura = CrediFacturaView()

        self.stacked_widget.addWidget(self.ventasA)       # Índice 0
        self.stacked_widget.addWidget(self.ventasCredito) # Índice 1
        self.stacked_widget.addWidget(self.facturas)      # Índice 2
        self.stacked_widget.addWidget(self.crediFactura)   # Índice 3
        self.stacked_widget.addWidget(self.caja)          # Índice 4
        self.stacked_widget.addWidget(self.egreso)        # Índice 5
        self.stacked_widget.addWidget(self.productos)     # Índice 6
        self.stacked_widget.addWidget(self.respaldo_view)       # Índice 7
        self.stacked_widget.addWidget(self.control_usuario_view) # Índice 8
        self.stacked_widget.addWidget(self.reportes)       # Índice 9

        # Conectar los botones del Navbar para cambiar las vistas del contenido
        self.navbar.BtnVentas.clicked.connect(
            lambda: self.stacked_widget.setCurrentWidget(self.ventasA)
        )
        self.navbar.BtnCaja.clicked.connect(
            lambda: self.stacked_widget.setCurrentWidget(self.caja)
        )
        self.navbar.BtnCredito.clicked.connect(
            lambda: self.stacked_widget.setCurrentWidget(self.ventasCredito)
        )
        self.navbar.BtnEgreso.clicked.connect(
            lambda: self.stacked_widget.setCurrentWidget(self.egreso)
        )
        self.navbar.BtnRespaldo.clicked.connect(
            lambda: self.stacked_widget.setCurrentWidget(self.respaldo_view)
        )
        self.navbar.BtnProductos.clicked.connect(
            lambda: self.stacked_widget.setCurrentWidget(self.productos)
        )
        self.navbar.BtnCrediFactura.clicked.connect(
            lambda: self.stacked_widget.setCurrentWidget(self.crediFactura)
        )
        self.navbar.BtnFacturas.clicked.connect(
            lambda: self.stacked_widget.setCurrentWidget(self.facturas)
        )
        self.navbar.BtnReportes.clicked.connect(
            lambda: self.stacked_widget.setCurrentWidget(self.reportes)
        )
        self.navbar.BtnControlUsuario.clicked.connect(
            lambda: self.stacked_widget.setCurrentWidget(self.control_usuario_view)
        )

# Ejecución de la aplicación
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec_())
