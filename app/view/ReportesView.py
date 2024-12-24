from PyQt5.QtWidgets import (
    QWidget,
)
from ..ui import Ui_Reportes


class ReportesView(QWidget, Ui_Reportes):
    def __init__(self, parent=None):
        super(ReportesView, self).__init__(parent)
        self.setupUi(self)
