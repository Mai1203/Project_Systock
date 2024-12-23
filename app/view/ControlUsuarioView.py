from PyQt5.QtWidgets import (
    QWidget,
)
from ..ui import Ui_ControlUsuario

class ControlUsuarioView(QWidget, Ui_ControlUsuario):
    def __init__(self, parent=None):
        super(ControlUsuarioView, self).__init__(parent)
        self.setupUi(self)