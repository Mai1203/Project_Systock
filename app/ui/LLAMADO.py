from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QToolButton, QStackedWidget
from PyQt5.uic import loadUi
import sys

class MainApp(QMainWindow):
    def __init__(self):
        super(MainApp, self).__init__()

        # Cargar el archivo Navbar.ui
        loadUi("Navbar.ui", self)

        # Asegurarse de que el widget Navbar existe
        self.navbar_widget = self.findChild(QWidget, "Navbar")
        if not self.navbar_widget:
            print("Error: No se encontró el widget 'Navbar' en Navbar.ui")
            return

        # Verificar la existencia de los botones
        self.BtnControlUsuario = self.navbar_widget.findChild(QToolButton, "BtnControlUsuario")
        self.BtnRespaldo = self.navbar_widget.findChild(QToolButton, "BtnRespaldo")

        # Confirmar si los botones existen o no
        if self.BtnControlUsuario:
            print("Botón 'BtnControlUsuario' encontrado.")
        else:
            print("Error: Botón 'BtnControlUsuario' no encontrado.")

        if self.BtnRespaldo:
            print("Botón 'BtnRespaldo' encontrado.")
            # Conectar el botón BtnRespaldo a la función que maneja la acción
            self.BtnRespaldo.clicked.connect(self.mostrar_contenido)
        else:
            print("Error: Botón 'BtnRespaldo' no encontrado.")
    
    def mostrar_contenido(self):
        # Verificar si se encuentra el widget 'Contenido' en la ventana principal
        contenido_widget = self.findChild(QStackedWidget, "Contenido")
        
        if contenido_widget:
            print("¡Widget 'Contenido' encontrado en la ventana principal!")
            # Aquí puedes cambiar la vista que deseas mostrar en el QStackedWidget
            contenido_widget.setCurrentIndex(0)  # Cambiar a la página de Respaldo (índice 0)
        else:
            print("Error: No se encontró el 'QStackedWidget' llamado 'Contenido' en la ventana principal.")
        
        # Ahora buscamos el widget 'Contenido' en la ventana Respaldo.ui
        # Cargar la ventana Respaldo.ui
        loadUi("Respaldo.ui", self)
        
        # Verificar nuevamente si el widget 'Contenido' existe en Respaldo.ui
        contenido_respaldo_widget = self.findChild(QStackedWidget, "Contenido")
        
        if contenido_respaldo_widget:
            print("¡Widget 'Contenido' encontrado en Respaldo.ui!")
        else:
            print("Error: No se encontró el 'QStackedWidget' llamado 'Contenido' en Respaldo.ui.")

# Ejecución de la aplicación
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec_())
