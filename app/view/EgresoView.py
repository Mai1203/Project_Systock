from PyQt5.QtWidgets import (
    QWidget,
)
from ..ui import Ui_Egreso

class EgresoView(QWidget, Ui_Egreso):
    def __init__(self, parent=None):
        super(EgresoView, self).__init__(parent)
        self.setupUi(self)