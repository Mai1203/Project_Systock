from PyQt5.QtWidgets import (
    QWidget,
)
from ..ui import Ui_VentasCredito

class VentasCredito_View(QWidget, Ui_VentasCredito):
    def __init__(self, parent=None):
        super(VentasCredito_View, self).__init__(parent)
        self.setupUi(self)

