from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt, QTimer
from ..ui import Ui_ControlCliente
from ..database.database import SessionLocal
from ..controllers.clientes_crud import *
from ..utils import *

class Cliente_View(QWidget, Ui_ControlCliente):
    def __init__(self, parent=None):
        super(Cliente_View, self).__init__(parent)
        self.setupUi(self)

        # Enfocar el primer input al iniciar
        QTimer.singleShot(0, self.InputCedula.setFocus)

        # Validaciones
        configurar_validador_numerico(self.InputCedula)
        configurar_validador_texto(self.InputNombre)
        configurar_validador_texto(self.InputApellido)
        configurar_validador_numerico(self.InputTelefono)

        # Placeholder
        self.InputCedula.setPlaceholderText("Ej: # Cedula")
        self.InputNombre.setPlaceholderText("Ej: Pepito")
        self.InputApellido.setPlaceholderText("Ej: Perex")
        self.InputTelefono.setPlaceholderText("Ej: 3185339876")
        self.InputDireccion.setPlaceholderText("Ej: Calle 1, 123 - Piso 1")

        # Lista ordenada de los campos
        self.campos = [
            self.InputCedula,
            self.InputNombre,
            self.InputApellido,
            self.InputTelefono,
            self.InputDireccion
        ]

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Down:
            self.navegar_anterior()
        elif event.key() == Qt.Key_Up:
            self.navegar_siguiente()
        else:
            super().keyPressEvent(event)

    def navegar_siguiente(self):
        actual = self.focusWidget()
        if actual in self.campos:
            index = self.campos.index(actual)
            siguiente = self.campos[(index + 1) % len(self.campos)]
            siguiente.setFocus()

    def navegar_anterior(self):
        actual = self.focusWidget()
        if actual in self.campos:
            index = self.campos.index(actual)
            anterior = self.campos[(index - 1) % len(self.campos)]
            anterior.setFocus()
