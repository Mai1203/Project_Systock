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

        #Inicialización y configuración
        self.validar_campos()

        self.TablaClientes.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows
        )
        self.TablaClientes.setSelectionMode(
            QtWidgets.QAbstractItemView.MultiSelection
        )
        self.TablaClientes.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers
        )
        self.TablaClientes.cellClicked.connect(self.cargar_datos_fila)

        # Enfocar el primer input al iniciar
        QTimer.singleShot(0, self.InputCedula.setFocus)

        #Evento de tecla enter para guardar cambios
        self.InputNombre.returnPressed.connect(self.editar_cliente)
        self.InputApellido.returnPressed.connect(self.editar_cliente)
        self.InputTelefono.returnPressed.connect(self.editar_cliente)
        self.InputDireccion.returnPressed.connect(self.editar_cliente)
        self.lineEditBuscador.textChanged.connect(self.buscar_cliente)

        # Placeholder
        self.InputCedula.setPlaceholderText("Ej: # Cedula")
        self.InputNombre.setPlaceholderText("Ej: Pepito")
        self.InputApellido.setPlaceholderText("Ej: Perex")
        self.InputTelefono.setPlaceholderText("Ej: 3185339876")
        self.InputDireccion.setPlaceholderText("Ej: Calle 1, 123 - Piso 1")
        self.lineEditBuscador.setPlaceholderText("Buscar por C.C, Nombre o Apellido")

        # Lista ordenada de los campos
        self.campos = [
            self.InputCedula,
            self.InputNombre,
            self.InputApellido,
            self.InputTelefono,
            self.InputDireccion
        ]

        #Acciones de los botones
        self.BtnEliminar.clicked.connect(self.eliminar_cliente)
        self.BtnRegistrar.clicked.connect(self.registrar_cliente)

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

        self.actualizar_tabla_clientes(rows)

        self.db.close()

    def actualizar_tabla_clientes(self, rows):
        if not rows:
            print("No hay filas para mostrar.")
            self.TablaClientes.setRowCount(0)
            return

        try:
            self.TablaClientes.setRowCount(0)

            # rows.sort(key=lambda x: x.ID_Cliente, reverse=False)
            
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

    def cargar_datos_fila(self):
        """
        Muestra los productos en los campos de entredada.
        """
        fila_seleccionada = self.TablaClientes.currentRow()
        datos_fila = []
        for columna in range(self.TablaClientes.columnCount()):
            item = self.TablaClientes.item(fila_seleccionada, columna)
            datos_fila.append(item.text() if item else "")

        self.InputCedula.setText(datos_fila[0])
        self.InputNombre.setText(datos_fila[1])
        self.InputApellido.setText(datos_fila[2])
        self.InputTelefono.setText(datos_fila[3])
        self.InputDireccion.setText(datos_fila[4])

    def editar_cliente(self):
        #Obtener los datos de los campos
        id_cliente = int(self.InputCedula.text())
        nombre = self.InputNombre.text()
        apellido = self.InputApellido.text()
        telefono = self.InputTelefono.text()
        direccion = self.InputDireccion.text()

        if (
            not nombre
            or not id_cliente
            or not apellido
            or not telefono
            or not direccion
        ):
            enviar_notificacion("Advertencia", "Por favor, rellene todos los campos")
            return
        
        reply = QMessageBox.question(
            self,
            "Confirmación",
            "¿Desea guardar los cambios?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            try:
                self.db = SessionLocal()

                actualizar_cliente(
                    self.db, 
                    id_cliente=id_cliente,
                    nombre=nombre,
                    apellido=apellido,
                    direccion=direccion,
                    telefono=telefono
                )
                self.mostrar_clientes()
                self.limpiar_campos()
            except Exception as e:
                enviar_notificacion("Error", e)

    def validar_campos(self):
        rx_telefono = QRegularExpression(
            r"^[0-9]{10}$"
        ) 
        validator_telefono = QRegularExpressionValidator(rx_telefono)
        self.InputTelefono.setValidator(validator_telefono)
        
        rx_cedula = QRegularExpression(
            r"^[0-9]{12}$"
        ) 
        validator_cedula = QRegularExpressionValidator(rx_cedula)
        self.InputCedula.setValidator(validator_cedula)

        rx_letras = QRegularExpression(r"^[a-zA-Z]+$")
        validator_letras = QRegularExpressionValidator(rx_letras)
        self.InputNombre.setValidator(validator_letras)
        self.InputApellido.setValidator(validator_letras)

    def obtener_ids_seleccionados(self):
        """
        Obtiene los IDs de los clientes seleccionados en la tabla.
        """
        filas_seleccionadas = self.TablaClientes.selectionModel().selectedRows()
        ids = []

        for fila in filas_seleccionadas:
            id_cliente = self.TablaClientes.item(
                fila.row(), 0
            ).text()  # Columna 0: ID del producto
            ids.append(int(id_cliente))

        return ids

    def eliminar_cliente(self):
        
        ids = self.obtener_ids_seleccionados()
        if not ids:
            enviar_notificacion(
                "Advertencia", "No se seleccionaron productos para eliminar."
            )
            return
        
        respuesta = QtWidgets.QMessageBox.question(
            self,
            "Confirmar Eliminación",
            f"¿Está seguro de que desea eliminar {len(ids)} cliente(s)?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
        )

        if respuesta == QtWidgets.QMessageBox.Yes:
            try:
                self.db = SessionLocal()

                # Eliminar los productos de la base de datos
                for id_producto in ids:
                    eliminar_cliente(self.db, id_producto)

                self.db.commit()
                enviar_notificacion("Éxito", "Cliente(s) eliminado(s) correctamente.")

                # Actualizar la tabla
                self.mostrar_clientes()
                self.limpiar_campos()
            except Exception as e:
                enviar_notificacion("Error", f"Error al eliminar clientes: {e}")
            finally:
                self.db.close()

    def registrar_cliente(self):
        
        id_cliente = self.InputCedula.text()
        nombre = self.InputNombre.text()
        apellido = self.InputApellido.text()
        telefeno = self.InputTelefono.text()
        direccion = self.InputDireccion.text()

        if (
            not id_cliente
            or not nombre
            or not apellido
            or not telefeno
            or not direccion
        ):
            enviar_notificacion(
                "Advertencia", "Por favor, rellene todos los campos"
            )
            return
        
        if len(id_cliente) < 6 or len(id_cliente) > 11 or not id_cliente.isdigit():
                QMessageBox.warning(
                    self, "Cédula inválida", "La cédula debe tener entre 6 y 11 dígitos."
                )
                QTimer.singleShot(0, self.InputCedula.setFocus)
                return
        
        try:
            self.db = SessionLocal()
            id_cliente = int(id_cliente)
            
            cliente_existente = obtener_cliente_por_id(self.db, id_cliente=id_cliente)

            if cliente_existente:
                enviar_notificacion("Advertencia", "El cliente ya existe en la base de datos")
                return
            
            crear_cliente(
                db=self.db,
                id_cliente=id_cliente,
                nombre=nombre,
                apellido=apellido,
                direccion=direccion,
                telefono=telefeno
            )

            enviar_notificacion("Éxito", "Cliente Registrado exitosamente")
            self.limpiar_campos()
            self.mostrar_clientes()
        except Exception as e:
            enviar_notificacion("Error", e)
        finally:
            self.db.close()

    def buscar_cliente(self):
        busqueda = self.lineEditBuscador.text().strip()
        if not busqueda:
            self.mostrar_clientes()
            return
        
        try:
            self.db = SessionLocal()
            clientes = buscar_cliente(db=self.db, busqueda=busqueda)
            print("busqueda de clientes: ", clientes)
            self.actualizar_tabla_clientes(clientes)
        except Exception as e:
            enviar_notificacion(
                "Error", e
            )
        finally:
            self.db.close()