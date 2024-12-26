from PyQt5.QtWidgets import (
    QWidget,
)
from ..ui import Ui_Respaldo

class Respaldo_View(QWidget, Ui_Respaldo):
    def __init__(self, parent=None):
        super(Respaldo_View, self).__init__(parent)
        self.setupUi(self)