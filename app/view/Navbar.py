from PyQt5.QtWidgets import (
    QWidget,
)
from ..ui import Ui_Navbar

class NavbarView(QWidget, Ui_Navbar):
    def __init__(self, parent=None):
        super(NavbarView, self).__init__(parent)
        self.setupUi(self)