from PyQt5.QtWidgets import (
    QMainWindow,
    # QApplication,
    QHBoxLayout,
    QWidget,
    QStackedWidget,
)

# import sys
from app.view import (
    NavbarView,
    RespaldoView,
    ControlUsuarioView,
    VentasAView,
    VentasCreditoView,
    FacturasView,
    CrediFacturaView,
    CajaView,
    EgresoView,
    ProductosView,
    ReportesView,
)

# from ..ui import Ui_Navbar

# class NavbarView(QWidget, Ui_Navbar):
#     def __init__(self, parent=None):
#         super(NavbarView, self).__init__(parent)
#         self.setupUi(self)


# Clase principal
class MainApp(QMainWindow):
    def __init__(self):
        super(MainApp, self).__init__()

        # Configurar la ventana principal
        self.setWindowTitle("Aplicación Principal")
        self.resize(800, 600)
        # self.center_window()

        self.setStyleSheet("background-color: white;")

        # Widget central que contiene el diseño principal
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Crear el diseño principal
        layout = QHBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)  # Sin márgenes
        layout.setSpacing(0)

        # Crear el Navbar
        self.navbar = NavbarView()
        layout.addWidget(self.navbar)  # Agregar el Navbar al lado izquierdo

        # Crear el QStackedWidget para el contenido
        self.stacked_widget = QStackedWidget()
        layout.addWidget(
            self.stacked_widget
        )  # Agregar el QStackedWidget al lado derecho

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

        self.stacked_widget.addWidget(self.ventasA)  # Índice 0
        self.stacked_widget.addWidget(self.ventasCredito)  # Índice 1
        self.stacked_widget.addWidget(self.facturas)  # Índice 2
        self.stacked_widget.addWidget(self.crediFactura)  # Índice 3
        self.stacked_widget.addWidget(self.caja)  # Índice 4
        self.stacked_widget.addWidget(self.egreso)  # Índice 5
        self.stacked_widget.addWidget(self.productos)  # Índice 6
        self.stacked_widget.addWidget(self.respaldo_view)  # Índice 7
        self.stacked_widget.addWidget(self.control_usuario_view)  # Índice 8
        self.stacked_widget.addWidget(self.reportes)  # Índice 9

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

    # def center_window(self):
    #     screen = QApplication.primaryScreen()
    #     screen_geometry = screen.availableGeometry()
    #     window_geometry = self.frameGeometry()

    #     # Calcular la posición del centro
    #     print(f"Screen geometry: {screen_geometry}")
    #     print(f"Window geometry (before centering): {window_geometry}")

    #     window_geometry.moveCenter(screen_geometry.center())

    #     print(f"Window geometry (after centering): {window_geometry}")
    #     print(f"Top-left position to move: {window_geometry.topLeft()}")

    #     self.move(window_geometry.topLeft())


# Ejecución de la aplicación
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     main_window = MainApp()
#     main_window.show()
#     sys.exit(app.exec_())
