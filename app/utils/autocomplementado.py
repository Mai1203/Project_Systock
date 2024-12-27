from PyQt5.QtWidgets import QCompleter
from PyQt5 import QtCore

def configurar_autocompletado(input_widget, obtener_datos_func, columna, db_session):
    """
    Configura el autocompletado de un campo de entrada.

    Args:
        input_widget (QLineEdit): El widget de entrada donde se configurará el autocompletado.
        obtener_datos_func (function): La función para obtener los datos de la base de datos.
        columna (str): La columna o atributo que se desea usar para el autocompletado.
        db_session (Session): Sesión activa de la base de datos.
    """
    # Obtener datos desde la base de datos
    items = [getattr(item, columna) for item in obtener_datos_func(db_session)]
    
    # Configurar el autocompletado
    completer = QCompleter(items)
    completer.setCaseSensitivity(False)
    completer.setFilterMode(QtCore.Qt.MatchContains)
    input_widget.setCompleter(completer)

