from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QStackedWidget,
)
from PyQt5.QtGui import QIcon
from app.view import (
    Navbar_View,
    Respaldo_View,
    ControlUsuario_View,
    VentasCredito_View,
    Facturas_View,
    CrediFactura_View,
    VentasA_View,
    VentasB_View,
    Caja_View,
    Egreso_View,
    Productos_View,
    Reportes_View,
)

class MainApp(QWidget):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)

        # Configurar la ventana principal
        self.setWindowTitle("Systock")
        self.setWindowIcon(QIcon("assets/logo.ico"))
        self.resize(800, 600)
        
        self.setStyleSheet("background-color: white;")
        
        # Widget central que contiene el diseño principal
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)  # Sin márgenes
        layout.setSpacing(0)

        # Crear el Navbar
        self.navbar = Navbar_View()
        layout.addWidget(self.navbar)  # Agregar el Navbar al lado izquierdo

        # Crear el QStackedWidget para el contenido
        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)  # Agregar el QStackedWidget al lado derecho

        # Crear y agregar vistas al QStackedWidget
        self.ventasA = VentasA_View()
        self.ventasB = VentasB_View()
        self.ventasCredito = VentasCredito_View()
        self.facturas = Facturas_View()
        self.caja = Caja_View()
        self.egreso = Egreso_View()
        self.productos = Productos_View()
        self.respaldo_view = Respaldo_View()
        self.control_usuario_view = ControlUsuario_View()
        self.reportes = Reportes_View()
        self.crediFactura = CrediFactura_View()

        self.stacked_widget.addWidget(self.ventasA)       # Índice 0
        self.stacked_widget.addWidget(self.ventasB)       # Índice 1
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
        self.ventasA.cambiar_a_ventanab.connect(
            lambda: self.stacked_widget.setCurrentWidget(self.ventasB)
        )
        
        self.ventasB.cambiar_a_ventanaA.connect(
            lambda: self.stacked_widget.setCurrentWidget(self.ventasA)
        )