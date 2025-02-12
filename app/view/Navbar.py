from PyQt5.QtGui import QIcon
import os
from PyQt5.QtWidgets import (
    QWidget,
    QButtonGroup,
)
from ..ui import Ui_Navbar


class Navbar_View(QWidget, Ui_Navbar):
    def __init__(self, parent=None):
        super(Navbar_View, self).__init__(parent)
        self.setupUi(self)

        self.BtnCaja.setStyleSheet("background-color: #f2f2f2;\n")

        self.button_group = QButtonGroup(self)
        self.button_group.addButton(self.BtnVentas)
        self.button_group.addButton(self.BtnCredito)
        self.button_group.addButton(self.BtnProductos)
        self.button_group.addButton(self.BtnCaja)
        self.button_group.addButton(self.BtnCrediFactura)
        self.button_group.addButton(self.BtnControlUsuario)
        self.button_group.addButton(self.BtnEgreso)
        self.button_group.addButton(self.BtnFacturas)
        self.button_group.addButton(self.BtnReportes)
        self.button_group.addButton(self.BtnRespaldo)

        self.button_group.buttonClicked.connect(self.cambiar_color_boton)

        self.estilo_normal = """QToolButton {
            background-color: white; /* Fondo blanco */
            border: none; /* Sin borde ni decoración inicial */
            color:  rgb(50, 50, 50); /* Color del texto */
            border-radius: 15px; /* Bordes circulares */
            padding: 5px 10px; /* Espaciado interno para mejor apariencia */
            height: 40px; /* Altura del botón */
            text-align: left; /* Alinea el texto del botón a la izquierda */
            font-size: 18px; /* Tamaño de fuente */
            cursor: pointer;
        }

        QToolButton:hover {
            background-color: #f2f2f2; /* Gris claro al pasar el mouse */
            cursor: pointer;
        }"""

        self.estilo_seleccionado = " background-color: #f2f2f2;"

        self.icon_asesor = "./assets/iconos/asesor.png"
        self.icon_admin = "./assets/iconos/perfil.png"

    def cambiar_color_boton(self, boton_seleccionado):
        """
        Cambia el color del botón seleccionado en función de su estado.
        """
        # Restaurar el estilo normal a todos los botones
        for button in self.button_group.buttons():
            button.setStyleSheet(self.estilo_normal)

        # Aplicar el estilo seleccionado al botón que fue presionado
        boton_seleccionado.setStyleSheet(self.estilo_seleccionado)

    def actualizar_usuario_rol(self, usuario):
        """
        Actualiza el texto del botón con el nombre de usuario
        """
        nombre = usuario.Nombre
        if " " in nombre:
            nombre = nombre.split(" ")[0]
        self.BtnUsuario.setText(f"{nombre}")

        # Si el usuario no es "ADMIN", cambia el ícono
        if usuario.ID_Rol != 1:
            # Verifica si el archivo existe antes de asignar el ícono
            if os.path.exists(self.icon_asesor):
                self.BtnUsuario.setIcon(
                    QIcon(self.icon_asesor)
                )  # Cambia el ícono a asesor
            else:
                print("Error: No se encuentra el archivo de ícono.")
        else:
            self.BtnUsuario.setIcon(QIcon(self.icon_admin))  # Cambia el ícono a asesor
