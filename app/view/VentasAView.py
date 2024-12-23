from PyQt5.QtWidgets import (
    QWidget,
)
from ..ui import Ui_VentasA

class VentasAView(QWidget, Ui_VentasA):
    def __init__(self, parent=None):
        super(VentasAView, self).__init__(parent)
        self.setupUi(self)