from PyQt5.QtWidgets import (
    QWidget,
)
from ..ui import Ui_Facturas


class FacturasView(QWidget, Ui_Facturas):
    def __init__(self, parent=None):
        super(FacturasView, self).__init__(parent)
        self.setupUi(self)
