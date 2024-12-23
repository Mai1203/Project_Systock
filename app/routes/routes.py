from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QHBoxLayout,
    QWidget,
    QStackedWidget,
    QSizePolicy,
)
from ..ui import Ui_Navbar, Ui_Respaldo, Ui_ControlUsuario, Ui_VentasA, Ui_VentasCredito, Ui_Facturas, Ui_Egreso, Ui_Productos, Ui_FacturasCredito, Ui_Caja, Ui_Reportes
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
