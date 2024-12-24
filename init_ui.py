from PyQt5 import QtWidgets
from init_db import conectar_base
from app.controllers.usuario_crud import verificar_credenciales
from app.ui import Ui_CONTENEDEDOR1, Ui_Form
import sys


class MainWindow(QtWidgets.QWidget, Ui_CONTENEDEDOR1):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()

        self.BtnLogin.clicked.connect(self.iniciar_sesion)

        self.db = conectar_base()

    def iniciar_sesion(self):
        # Obtener los datos ingresados por el usuario
        usuario = self.InputNombreUsuario.text()
        contraseña = self.InputPassword.text()

        # Verificar credenciales en la base de datos
        usuario_autenticado = verificar_credenciales(self.db, usuario, contraseña)

        if usuario_autenticado:
            # Si las credenciales son válidas, mostrar la ventana principal
            QtWidgets.QMessageBox.information(self, "Éxito", "Inicio de sesión exitoso")
            self.abrir_ventana_principal()
        else:
            # Si las credenciales son inválidas, mostrar un mensaje de error
            QtWidgets.QMessageBox.warning(
                self, "Error", "Usuario o contraseña incorrectos"
            )

    def abrir_ventana_principal(self):
        # Cerrar la ventana de login y abrir la ventana principal
        self.ventana_principal = VentanaPrincipal()
        self.ventana_principal.show()
        self.close()

    def closeEvent(self, event):
        # Cerrar la sesión de base de datos al salir
        self.db.close()


class VentanaPrincipal(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
