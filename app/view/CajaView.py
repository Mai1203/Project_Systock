from PyQt5.QtWidgets import (
    QWidget,
)
from ..ui import Ui_Caja

class Caja_View(QWidget, Ui_Caja):
    def __init__(self, parent=None):
        super(Caja_View, self).__init__(parent)
        self.setupUi(self)
