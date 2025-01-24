from PyQt5.QtWidgets import (
    QWidget,
    QMessageBox,
)
from PyQt5 import QtWidgets, QtGui, QtCore
from ..ui import Ui_ControlUsuario
from ..database.database import SessionLocal
from ..controllers.usuario_crud import *
from ..utils import *
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer



class ControlUsuario_View(QWidget, Ui_ControlUsuario):
    def __init__(self, parent=None):
        super(ControlUsuario_View, self).__init__(parent)
        self.setupUi(self)
        QTimer.singleShot(0, self.InputIdUser.setFocus)

        
        self.BtnEliminar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.BtnRegistrarUser.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.BtnRolUser.setText("ASESOR")
        self.limpiar_tabla_usuarios()
        self.mostrar_usuarios()
        
        configurar_validador_numerico(self.InputIdUser)
        configurar_validador_texto(self.InputNombreUser)
        
        
        self.BtnRegistrarUser.clicked.connect(self.ingresar_usuario)
        self.BtnEliminar.clicked.connect(self.eliminar_usuarios)
        self.InputIdUser.returnPressed.connect(self.editar_usuario)
        self.InputNombreUser.returnPressed.connect(self.editar_usuario)
        self.InputUser.returnPressed.connect(self.editar_usuario)
        self.InputPasswordUser.returnPressed.connect(self.editar_usuario)
        
        self.TablaUser.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.TablaUser.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.TablaUser.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        
        self.TablaUser.cellClicked.connect(self.cargar_datos_fila)
    
    def showEvent(self, event):
        super().showEvent(event)
        self.limpiar_formulario()
        self.limpiar_tabla_usuarios()
        self.mostrar_usuarios()
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            self.navegar_widgets()  # Continúa con la navegación normal
        elif event.key() == Qt.Key_Down:
            self.navegar_widgets_atras()

        # Llamar al método original para procesar otros eventos
        super().keyPressEvent(event)

    def navegar_widgets(self):
        if self.focusWidget() == self.InputIdUser:
            self.InputNombreUser.setFocus()
        elif self.focusWidget() == self.InputNombreUser:
            self.InputUser.setFocus()
        elif self.focusWidget() == self.InputUser:
            self.InputPasswordUser.setFocus()
        elif self.focusWidget() == self.InputPasswordUser:
            self.InputIdUser.setFocus()  

    def navegar_widgets_atras(self):
        if self.focusWidget() == self.InputPasswordUser:
            self.InputUser.setFocus()
        elif self.focusWidget() == self.InputUser:
            self.InputNombreUser.setFocus()
        elif self.focusWidget() == self.InputNombreUser:
            self.InputIdUser.setFocus()  # Volver al inicio
        elif self.focusWidget() == self.InputIdUser:
            self.InputPasswordUser.setFocus()

        
    def ingresar_usuario(self):
        
        id_user = self.InputIdUser.text().strip()
        nombre = self.InputNombreUser.text().strip()
        usuario = self.InputUser.text().strip()
        contraseña = self.InputPasswordUser.text().strip()
        # rol = self.BtnRolUser.text()
        
        
        if not id_user or not usuario or not contraseña:
            enviar_notificacion("Error", "Por favor, rellena todos los campos")
            return
        
        try:
            self.db = SessionLocal()
            usuario_existente = obtener_usuario_por_id(self.db, id_user)
            if usuario_existente:
                enviar_notificacion("Error", "El usuario ya existe en la base de datos")
                return
            
            crear_usuario(self.db, id_user, nombre, usuario, contraseña, True, 2)
            enviar_notificacion("Éxito", "Usuario registrado exitosamente")
            
            self.BtnRolUser.setText("ASESOR")
            
            self.limpiar_formulario()
            self.limpiar_tabla_usuarios()
            self.mostrar_usuarios()
            
        except Exception as e:
            print(f"Error: {e}")
            enviar_notificacion("Error", f"Error: {e}")
            
        finally:
            if hasattr(self, "db") and self.db:
                self.db.close()
                
    def limpiar_formulario(self):
        self.InputIdUser.setText("")
        self.InputNombreUser.setText("")
        self.InputUser.setText("")
        self.InputPasswordUser.setText("")
        
    def mostrar_usuarios(self):
        self.db = SessionLocal()
        usuarios = obtener_usuarios(self.db)
        
        self.actualizar_tabla_usuarios(usuarios)
        
        self.db.close()
        
    def actualizar_tabla_usuarios(self, usuarios):
        if usuarios:
            self.TablaUser.setRowCount(len(usuarios))
            self.TablaUser.setColumnCount(6)
            
            for row_idx, row in enumerate(usuarios):
                id_item = QtWidgets.QTableWidgetItem(str(row.ID_Usuario))
                nombre_item = QtWidgets.QTableWidgetItem(str(row.Nombre))
                usuario_item = QtWidgets.QTableWidgetItem(str(row.Usuario))
                contrasena_item = QtWidgets.QTableWidgetItem(str(row.Contrasena))
                rol_item = QtWidgets.QTableWidgetItem(str(row.rol))
                estado_item = QtWidgets.QTableWidgetItem(str(row.Estado))
                
                self.TablaUser.setItem(row_idx, 0, id_item)
                self.TablaUser.setItem(row_idx, 1, nombre_item)
                self.TablaUser.setItem(row_idx, 2, usuario_item)
                self.TablaUser.setItem(row_idx, 3, contrasena_item)
                self.TablaUser.setItem(row_idx, 4, rol_item)
                self.TablaUser.setItem(row_idx, 5, estado_item)
                
    def limpiar_tabla_usuarios(self):
        self.TablaUser.setRowCount(0)
        self.TablaUser.setColumnCount(6)
        
    def eliminar_usuarios(self):
        """
        Elimina los productos seleccionados de la base de datos y actualiza la tabla.
        """
        ids = self.obtener_ids_seleccionados()
        
        if not ids:
            enviar_notificacion(
                "Advertencia", "No se seleccionaron usuarios para eliminar."
            )
            return
        self.db = SessionLocal()
        
        try:
            for id in ids:
                usuario = obtener_usuario_por_id(self.db, id)
                if usuario.rol == "ADMINISTRADOR":
                    enviar_notificacion(
                        "Advertencia", "No se puede eliminar un administrador."
                    )
                    return
        except Exception as e:
                enviar_notificacion("Error", f"Error al buscar usuarios: {e}")
                print(e)

        respuesta = QtWidgets.QMessageBox.question(
            self,
            "Confirmar Eliminación",
            f"¿Está seguro de que desea eliminar {len(ids)} usuario(s)?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
        )

        if respuesta == QtWidgets.QMessageBox.Yes:
            try:
     
                # Eliminar los usuarios de la base de datos
                for id_usuario in ids:
                    eliminar_usuario(self.db, id_usuario)

                self.db.commit()
                enviar_notificacion("Éxito", "Usuario(s) eliminado(s) correctamente.")

                # Actualizar la tabla
                self.limpiar_tabla_usuarios()
                self.mostrar_usuarios()
                self.limpiar_formulario()
            except Exception as e:
                enviar_notificacion("Error", f"Error al eliminar usuarios: {e}")
            finally:
                self.db.close()
              
    def obtener_ids_seleccionados(self):
        """
        Obtiene los IDs de los usuarios seleccionados en la tabla.
        """
        filas_seleccionadas = self.TablaUser.selectionModel().selectedRows()
        ids = []

        for fila in filas_seleccionadas:
            id_usuario = self.TablaUser.item(
                fila.row(), 0
            ).text()  # Columna 0: ID del usuario
            ids.append(int(id_usuario))
            
        return ids
    
    def cargar_datos_fila(self):
        """
        Muestra los usuarios en los campos de entredada.
        """
        fila_seleccionada = self.TablaUser.currentRow()
        datos_fila = []
        for columna in range(self.TablaUser.columnCount()):
            item = self.TablaUser.item(fila_seleccionada, columna)
            datos_fila.append(item.text() if item else "")

        self.InputIdUser.setText(datos_fila[0])
        self.InputNombreUser.setText(datos_fila[1])
        self.InputUser.setText(datos_fila[2])
        self.InputPasswordUser.setText(datos_fila[3])
        
    def editar_usuario(self):
        """
        Al presionar Enter en cualquier input, pregunta si desea guardar los cambios
        y luego edita el usuario si es confirmado.
        """
        # Obtener los nuevos datos de los inputs
        id = self.InputIdUser.text()
        nombre = self.InputNombreUser.text()
        usuario = self.InputUser.text()
        contrasena = self.InputPasswordUser.text()
        
        # Verificar que todos los campos tengan datos
        if (
            not id
            or not nombre
            or not usuario
            or not contrasena
        ):
            enviar_notificacion("Error", "Por favor, rellene todos los campos")
            return

        # Confirmar si el usuario desea realizar la edición
        reply = QMessageBox.question(
            self,
            "Confirmación",
            "¿Desea guardar los cambios?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            try:
                # Hacer la actualización en la base de datos
                self.db = SessionLocal()

                usuario_actualizado = actualizar_usuario(self.db, id, nombre, usuario, contrasena)
                
                if usuario_actualizado:
                    enviar_notificacion("Éxito", "Usuario actualizado correctamente")
                    self.limpiar_formulario()
                    self.limpiar_tabla_usuarios()
                    self.mostrar_usuarios()
                else:
                    enviar_notificacion(
                        "Error", "Hubo un problema al actualizar el usuario"
                    )
                self.db.close()
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error: {e}")
        else:
            # Si el usuario cancela la edición
            print("Edición cancelada")