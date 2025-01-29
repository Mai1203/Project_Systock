from PyQt5.QtWidgets import (
    QWidget,
)


from ..ui import Ui_PagoCredito

class PagoCredito_View(QWidget, Ui_PagoCredito):
    def __init__(self, parent=None):
        super(PagoCredito_View, self).__init__(parent)
        self.setupUi(self)
        
        