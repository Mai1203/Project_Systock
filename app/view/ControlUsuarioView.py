from PyQt5.QtWidgets import (
    QWidget,
)
from ..ui import Ui_ControlUsuario

class ControlUsuario_View(QWidget, Ui_ControlUsuario):
    def __init__(self, parent=None):
        super(ControlUsuario_View, self).__init__(parent)
        self.setupUi(self)