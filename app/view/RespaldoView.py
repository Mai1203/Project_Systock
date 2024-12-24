from PyQt5.QtWidgets import (
    QWidget,
)
from ..ui import Ui_Respaldo


class RespaldoView(QWidget, Ui_Respaldo):
    def __init__(self, parent=None):
        super(RespaldoView, self).__init__(parent)
        self.setupUi(self)
