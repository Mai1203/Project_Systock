from PyQt5.QtWidgets import (
    QWidget,
)
from ..ui import Ui_FacturasCredito

class CrediFactura_View(QWidget, Ui_FacturasCredito):
    def __init__(self, parent=None):
        super(CrediFactura_View, self).__init__(parent)
        self.setupUi(self)