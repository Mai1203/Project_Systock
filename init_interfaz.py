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
from app.controllers.usuario_crud import verificar_credenciales, obtener_usuario_por_id
from app.ventanasView import MainApp
from app.view import Login_View
from dotenv import load_dotenv
import os
import sys
import jwt
import datetime


load_dotenv()  # Carga las variables de entorno desde el archivo .env
SECRET_KEY = os.getenv("SECRET_KEY")
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.usuario_actual_id = None
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
        
        self.MainApp.navbar.BtnCerrarSesion.clicked.connect(self.cerrar_sesion)
        
        self.Login.BtnLogin.clicked.connect(self.iniciar_sesion)
        self.Login.InputPassword.returnPressed.connect(self.iniciar_sesion) 
        
        self.db = conectar_base()
     
    def cerrar_sesion(self):
        """
        Manejar el evento de cierre de sesión.
        """
        enviar_notificacion("Sesión cerrada", "Puedes iniciar sesión nuevamente")
        self.stacked_widget.setCurrentWidget(self.Login)
        self.limpiar_campos()
        
    def limpiar_campos(self):
        """
        Limpiar los campos de entrada del formulario de login.
        """
        self.Login.InputNombreUsuario.clear()
        self.Login.InputPassword.clear()
        
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
        """
        Maneja el inicio de sesión y genera un token JWT.
        """
        # Obtener los datos ingresados por el usuario
        usuario = self.Login.InputNombreUsuario.text()
        contraseña = self.Login.InputPassword.text()
        rol = self.Login.BtnRol.text()  # Asegúrate de obtener el rol del usuario
        
        if not usuario or not contraseña:
            enviar_notificacion("Error", "Por favor, ingresa tus credenciales")
            return

        # Verificar las credenciales
        usuario_autenticado = verificar_credenciales(self.db, usuario, contraseña)
        if not usuario_autenticado:
            enviar_notificacion("Error", "Usuario o contraseña incorrectos")
            return

        # Verificar que el rol sea correcto
        usuario_data = obtener_usuario_por_id(self.db, usuario_autenticado.ID_Usuario)
        if usuario_data.rol != rol:
            enviar_notificacion("Error", "El rol seleccionado no coincide con tus permisos")
            return

        # Generar el token JWT
        self.usuario_actual_id = usuario_autenticado.ID_Usuario
        self.MainApp.ventasA.usuario_actual_id = usuario_autenticado.ID_Usuario
        self.MainApp.ventasB.usuario_actual_id = usuario_autenticado.ID_Usuario
        token = self.generar_token(usuario_autenticado.ID_Usuario, rol)

        # Almacenar el token en el objeto MainWindow
        self.token_actual = token

        # Mostrar la ventana principal
        enviar_notificacion("Inicio de sesión exitoso", "Bienvenido")
        self.stacked_widget.setCurrentWidget(self.MainApp)

        # Configurar accesos por rol
        self.configurar_accesos_por_rol(rol)

        # Actualizar el nombre del usuario en la barra de navegación
        self.MainApp.navbar.actualizar_usuario_rol(usuario.upper())
        self.db.close()    
    
    def generar_token(self, usuario_id, rol):
        """
        Genera un token JWT con el ID del usuario y su rol.
        """
        payload = {
            "id_usuario": usuario_id,
            "rol": rol,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),  # Expira en 1 hora
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return token
    
    def configurar_accesos_por_rol(self, rol):
        """
        Configurar accesos según el rol del usuario autenticado.
        """
        self.MainApp.stacked_widget.setCurrentIndex(0)
        navbar = self.MainApp.navbar
        
        if rol == "ADMINISTRADOR":
            navbar.BtnVentas.setEnabled(True)
            navbar.BtnCaja.setEnabled(True)
            navbar.BtnCredito.setEnabled(True)
            navbar.BtnEgreso.setEnabled(True)
            navbar.BtnRespaldo.setEnabled(True)
            navbar.BtnProductos.setEnabled(True)
            navbar.BtnCrediFactura.setEnabled(True)
            navbar.BtnFacturas.setEnabled(True)
            navbar.BtnReportes.setEnabled(True)
            navbar.BtnControlUsuario.setEnabled(True)
        elif rol == "ASESOR":
            navbar.BtnVentas.setEnabled(True)
            navbar.BtnCaja.setEnabled(True)
            navbar.BtnCredito.setEnabled(True)
            navbar.BtnEgreso.setEnabled(True)
            navbar.BtnRespaldo.setEnabled(False)
            navbar.BtnProductos.setEnabled(False)
            navbar.BtnCrediFactura.setEnabled(True)
            navbar.BtnFacturas.setEnabled(True)
            navbar.BtnReportes.setEnabled(False)
            navbar.BtnControlUsuario.setEnabled(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())