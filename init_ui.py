from PyQt5 import QtWidgets
from init_db import conectar_base
from app.utils.enviar_notifi import enviar_notificacion
from app.controllers.usuario_crud import verificar_credenciales
from app.ventanasView import MainApp
from app.ui.Login import Ui_Login
import sys

class MainWindow(QtWidgets.QWidget, Ui_Login):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
          
        self.BtnRol.clicked.connect(self.Cambiar_Rol)
        self.InputPassword.returnPressed.connect(self.iniciar_sesion) 
        self.BtnLogin.clicked.connect(self.iniciar_sesion)
        
        self.db = conectar_base()
        
    def Cambiar_Rol(self):
        if self.BtnRol.text() == "ADMINISTRADOR":
            self.BtnRol.setText("ASESOR")
        else:
            self.BtnRol.setText("ADMINISTRADOR")
        
    def iniciar_sesion(self):
        # Obtener los datos ingresados por el usuario
        usuario = self.InputNombreUsuario.text()
        contraseña = self.InputPassword.text()
        
        if not usuario or not contraseña:
            # Si no se ingresaron los datos, mostrar un mensaje de error
            enviar_notificacion("Error","Por favor, ingresa tus credenciales")

        # Verificar credenciales en la base de datos
        usuario_autenticado = verificar_credenciales(self.db, usuario, contraseña)

        if usuario_autenticado:
            # Si las credenciales son válidas, mostrar la ventana principal
            enviar_notificacion("Inicio de sesión exitoso","Puedes continuar con tus operaciones")
            self.abrir_ventana_principal()
        else:
            # Si las credenciales son inválidas, mostrar un mensaje de error
            enviar_notificacion("Error al ingresar","Usuario o contraseña incorrectos")
        
        self.db.close()

    def abrir_ventana_principal(self):
        # Cerrar la ventana de login y abrir la ventana principal
        self.close()
        self.main_window = MainApp()
        self.main_window.show()



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
