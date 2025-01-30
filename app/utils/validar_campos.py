from PyQt5.QtCore import QRegularExpression
from PyQt5.QtGui import QRegularExpressionValidator


def configurar_validador(input_widget, patron):
    """
    Configura un validador para un campo de entrada basado en una expresión regular.

    Args:
        input_widget (QLineEdit): El widget donde se aplicará el validador.
        patron (str): La expresión regular para validar la entrada.
    """
    rx = QRegularExpression(patron)
    validador = QRegularExpressionValidator(rx)
    input_widget.setValidator(validador)


def configurar_validador_numerico(input_widget):
    """
    Configura un validador para aceptar solo números en un campo de entrada.
    """
    configurar_validador(input_widget, r"^\d+$")


def configurar_validador_texto(input_widget):
    """
    Configura un validador para aceptar solo texto (letras y espacios).
    """
    configurar_validador(input_widget, r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$")


def configurar_validador_texto_y_numeros(input_widget):
    """
    Configura un validador para aceptar solo texto (letras, números y espacios).
    """
    configurar_validador(input_widget, r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ0-9\s]+$")


def configurar_validador_decimal(input_widget):
    """
    Configura un validador para aceptar números decimales.
    """
    configurar_validador(input_widget, r"^\d+(\.\d{1,2})?$")


def configurar_validador_codigo(input_widget):
    """
    Configura un validador para códigos alfanuméricos.
    """
    configurar_validador(input_widget, r"^[a-zA-Z0-9]+$")
