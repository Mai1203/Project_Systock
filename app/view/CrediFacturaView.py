from PyQt5.QtWidgets import (
    QWidget,
)
from ..ui import Ui_FacturasCredito

class CrediFacturaView(QWidget, Ui_FacturasCredito):
    def __init__(self, parent=None):
        super(CrediFacturaView, self).__init__(parent)
        self.setupUi(self)