from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt, QTimer

from ..ui import Ui_ControlCliente
from ..database.database import SessionLocal
from ..controllers.clientes_crud import *
from ..utils import *

class Cliente_View(QWidget, Ui_ControlCliente):
    def __init__(self, parent=None):
        super(Cliente_View, self).__init__(parent)
        self.setupUi(self)

        # Enfocar el primer input al iniciar
        QTimer.singleShot(0, self.InputCedula.setFocus)

        # Validaciones
        configurar_validador_numerico(self.InputCedula)
        configurar_validador_texto(self.InputNombre)
        configurar_validador_texto(self.InputApellido)
        configurar_validador_numerico(self.InputTelefono)

        # Placeholder
        self.InputCedula.setPlaceholderText("Ej: # Cedula")
        self.InputNombre.setPlaceholderText("Ej: Pepito")
        self.InputApellido.setPlaceholderText("Ej: Perex")
        self.InputTelefono.setPlaceholderText("Ej: 3185339876")
        self.InputDireccion.setPlaceholderText("Ej: Calle 1, 123 - Piso 1")

        # Lista ordenada de los campos
        self.campos = [
            self.InputCedula,
            self.InputNombre,
            self.InputApellido,
            self.InputTelefono,
            self.InputDireccion
        ]

    def showEvent(self, event):
        super().showEvent(event)
        self.limpiar_campos()
        self.mostrar_clientes()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Down:
            self.navegar_anterior()
        elif event.key() == Qt.Key_Up:
            self.navegar_siguiente()
        else:
            super().keyPressEvent(event)

    def navegar_siguiente(self):
        actual = self.focusWidget()
        if actual in self.campos:
            index = self.campos.index(actual)
            siguiente = self.campos[(index + 1) % len(self.campos)]
            siguiente.setFocus()

    def navegar_anterior(self):
        actual = self.focusWidget()
        if actual in self.campos:
            index = self.campos.index(actual)
            anterior = self.campos[(index - 1) % len(self.campos)]
            anterior.setFocus()

    def limpiar_campos(self):
        self.InputApellido.clear()
        self.InputCedula.clear()
        self.InputDireccion.clear()
        self.InputNombre.clear()
        self.InputTelefono.clear()

    def mostrar_clientes(self):
        self.db = SessionLocal()
        rows = obtener_clientes(self.db)

        self.actualizar_tabla_ventasCredito(rows)

        self.db.close()

    def actualizar_tabla_ventasCredito(self, rows):
        if not rows:
            print("No hay filas para mostrar.")
            self.TablaClientes.setRowCount(0)
            return

        try:
            self.TablaClientes.setRowCount(0)

            rows.sort(key=lambda x: x.ID_Cliente, reverse=False)
            
            for row_idx, row in enumerate(rows):
                
                id_cliente = str(row.ID_Cliente)
                nombre = str(row.Nombre)
                apellido = str(row.Apellido)
                direccion = str(row.Direccion)
                telefono = str(row.Teléfono)

                self.TablaClientes.insertRow(0)
                
                # Configurar items de la tabla
                items = [
                    (id_cliente, 0),
                    (nombre, 1),
                    (apellido, 2),
                    (telefono, 3),
                    (direccion, 4)
                ]

                # Añadir items a la tabla
                for value, col_idx in items:
                    item = QtWidgets.QTableWidgetItem(value)
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.TablaClientes.setItem(0, col_idx, item)
        except Exception as e:
            print(f"Error al mostrar tabla clientes: {e}")
