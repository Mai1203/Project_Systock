import sys
from PyQt6.QtCore import Qt, QSize  # Importación corregida
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QComboBox, QWidget, QDialog, QFrame


class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Login')
        self.setGeometry(0, 0, 500, 400)  # Tamaño más grande
        self.setStyleSheet("""
            background-color: white;
            color: black; 
        """)

        # Centrar la ventana de login
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        center = screen_geometry.center()
        frame_geometry = self.frameGeometry()
        frame_geometry.moveCenter(center)
        self.move(frame_geometry.topLeft())

        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)  # Para ventana sin bordes

        # Layouts
        layout = QVBoxLayout()

        # Título
        self.title = QLabel("Iniciar sesión")
        self.title.setStyleSheet("font-size: 24px; font-weight: bold; text-align: center; margin-bottom: 20px;")
        layout.addWidget(self.title)

        # ComboBox para los roles
        self.role_combobox = QComboBox()
        self.role_combobox.addItems(["Administrador", "Asesor Comercial"])
        self.role_combobox.setStyleSheet("""
            font-size: 16px;
            padding: 10px;
            background-color: rgba(226, 227, 221, 1);
            color: black;
        """)
        layout.addWidget(self.role_combobox)

        # Campo de contraseña
        self.password_label = QLabel("Contraseña:")
        self.password_label.setStyleSheet("font-size: 16px; margin-top: 20px;")
        layout.addWidget(self.password_label)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet("""
            font-size: 16px;
            padding: 10px;
            background-color: rgba(226, 227, 221, 1);
            color: black;
        """)
        layout.addWidget(self.password_input)

        # Botón de Login
        self.login_button = QPushButton("Iniciar sesión")
        self.login_button.setStyleSheet("""
            font-size: 18px;
            padding: 10px;
            background-color: rgba(49, 49, 47, 1);
            color: white;
            border-radius: 5px;
            margin-top: 20px;
        """)
        self.login_button.setIconSize(QSize(24, 24))  # Uso de QtCore.QSize correctamente
        layout.addWidget(self.login_button)

        # Conectar la acción del botón de login
        self.login_button.clicked.connect(self.check_credentials)

        self.setLayout(layout)

    def check_credentials(self):
        role = self.role_combobox.currentText()
        password = self.password_input.text()

        # Validar las credenciales
        if role == "Administrador" and password == "adminpass":
            print("Login como Administrador exitoso")
            self.accept()  # Cierra el diálogo
        elif role == "Asesor Comercial" and password == "asesorpass":
            print("Login como Asesor Comercial exitoso")
            self.accept()  # Cierra el diálogo
        else:
            print("Credenciales incorrectas")
            self.password_input.clear()  # Limpiar el campo de contraseña


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Aplicación Principal')
        self.setGeometry(100, 100, 600, 400)
        
        # Mostrar la ventana de login
        self.login_window = LoginWindow()
        if self.login_window.exec() == QDialog.DialogCode.Accepted:
            # Solo muestra la ventana principal si el login es exitoso
            self.init_ui()

    def init_ui(self):
        # Contenido de la aplicación principal
        layout = QVBoxLayout()
        label = QLabel("Bienvenido a la aplicación")
        layout.addWidget(label)

        # Configuración de la ventana principal
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
