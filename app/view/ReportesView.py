from PyQt5.QtWidgets import (
    QWidget,
)
from ..ui import Ui_Reportes

class Reportes_View(QWidget, Ui_Reportes):    
    def __init__(self, parent=None):
        super(Reportes_View, self).__init__(parent)
        self.setupUi(self)
