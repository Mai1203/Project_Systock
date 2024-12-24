from PyQt5.QtWidgets import (
    QWidget,
)
from ..ui import Ui_VentasCredito


class VentasCreditoView(QWidget, Ui_VentasCredito):
    def __init__(self, parent=None):
        super(VentasCreditoView, self).__init__(parent)
        self.setupUi(self)
