from PyQt5.QtWidgets import (
    QWidget,
)
from ..ui import Ui_Caja


class CajaView(QWidget, Ui_Caja):
    def __init__(self, parent=None):
        super(CajaView, self).__init__(parent)
        self.setupUi(self)
