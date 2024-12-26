from PyQt5.QtWidgets import (
    QWidget,
    QLineEdit,
)
from PyQt5.QtGui import QIcon
from ..ui import Ui_Login

class Login_View(QWidget, Ui_Login):
    def __init__(self, parent=None):
        super(Login_View, self).__init__(parent)
        self.setupUi(self)
        
        self.InputPassword.setEchoMode(QLineEdit.Password)
        self.BtnRol.clicked.connect(self.Cambiar_Rol)
        self.toolButton.clicked.connect(self.mostrar_contrasena)
        self.ojo_abierto = False
        
        
    def Cambiar_Rol(self):
        if self.BtnRol.text() == "ADMINISTRADOR":
            self.BtnRol.setText("ASESOR")
        else:
            self.BtnRol.setText("ADMINISTRADOR")
            
    def mostrar_contrasena(self):
        self.cambiar_icono()
        if self.InputPassword.echoMode() == QLineEdit.Password:
            self.InputPassword.setEchoMode(QLineEdit.Normal)
        else:
            self.InputPassword.setEchoMode(QLineEdit.Password)
            
    def cambiar_icono(self):
        if not self.ojo_abierto:
            self.toolButton.setIcon(QIcon("assets/iconos/ojo_abierto.png"))
            self.ojo_abierto = True
        else:
            self.toolButton.setIcon(QIcon("assets/iconos/ojo_cerrado.png"))
            self.ojo_abierto = False
