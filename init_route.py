from PyQt5.QtWidgets import QApplication
from app.ventanasView import MainApp
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec_())
