from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QWidget,
    QHBoxLayout,
    QStackedWidget,
)
from PyQt5.QtGui import QIcon, QScreen
from PyQt5 import QtWidgets
from init_db import conectar_base
from app.utils.enviar_notifi import enviar_notificacion
from app.controllers.usuario_crud import verificar_credenciales
from app.ventanasView import MainApp
from app.view import Login_View
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.setWindowTitle("Systock")
        self.setWindowIcon(QIcon("assets/logo.ico"))
        self.resize(800, 600)
        
        self.setStyleSheet("background-color: white;")
        
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Crear el diseño principal
        layout = QHBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)  # Sin márgenes
        layout.setSpacing(0)
        
        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)
        
        self.Login = Login_View()
        self.MainApp = MainApp()
        
        self.stacked_widget.addWidget(self.Login)
        self.stacked_widget.addWidget(self.MainApp)
        
        self.Login.BtnLogin.clicked.connect(self.iniciar_sesion)
        self.Login.InputPassword.returnPressed.connect(self.iniciar_sesion) 
        
        self.db = conectar_base()
        
    def closeEvent(self, event):
        """
        Sobrescribe el evento de cierre para mostrar una ventana de confirmación.
        """
        respuesta = QtWidgets.QMessageBox.question(
            self,
            "Salir del programa",
            "¿Estás seguro de que deseas cerrar el programa?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )

        if respuesta == QtWidgets.QMessageBox.Yes:
            event.accept()  # Permite cerrar la ventana
        else:
            event.ignore()  # Cancela el cierre de la ventana
    
    def showEvent(self, event):
        super(MainWindow, self).showEvent(event)
        self.center_window()
    
    def center_window(self):
        screen_geometry = QScreen.availableGeometry(QApplication.primaryScreen())
        acreen_width = screen_geometry.width()
        acreen_height = screen_geometry.height()
        
        window_width = self.width()
        window_height = self.height()
        
        # Calcular la posición del centro
        x = (acreen_width - window_width) // 2
        y = (acreen_height - window_height) // 2
        
        self.move(x, y)
        
        
    def iniciar_sesion(self):
        # Obtener los datos ingresados por el usuario
        usuario = self.Login.InputNombreUsuario.text()
        contraseña = self.Login.InputPassword.text()
        
        if not usuario or not contraseña:
            # Si no se ingresaron los datos, mostrar un mensaje de error
            enviar_notificacion("Error","Por favor, ingresa tus credenciales")
            return

        # Verificar credenciales en la base de datos
        usuario_autenticado = verificar_credenciales(self.db, usuario, contraseña)

        if usuario_autenticado:
            # Si las credenciales son válidas, mostrar la ventana principal
            enviar_notificacion("Inicio de sesión exitoso","Puedes continuar con tus operaciones")
            self.stacked_widget.setCurrentWidget(self.MainApp)
        else:
            # Si las credenciales son inválidas, mostrar un mensaje de error
            enviar_notificacion("Error al ingresar","Usuario o contraseña incorrectos")
        
        self.db.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())