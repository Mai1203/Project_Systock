from PyQt5.QtWidgets import (
    QWidget,
)
from ..ui import Ui_Egreso

class Egreso_View(QWidget, Ui_Egreso):
    def __init__(self, parent=None):
        super(Egreso_View, self).__init__(parent)
        self.setupUi(self)