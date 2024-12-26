from PyQt5.QtWidgets import (
    QWidget,
)
from ..ui import Ui_Facturas

class Facturas_View(QWidget, Ui_Facturas):
    def __init__(self, parent=None):
        super(Facturas_View, self).__init__(parent)
        self.setupUi(self)