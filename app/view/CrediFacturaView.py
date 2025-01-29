from PyQt5.QtWidgets import (
    QWidget,
    QMessageBox,
)
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal

from ..ui import Ui_FacturasCredito
from ..database.database import SessionLocal
from ..controllers.venta_credito_crud import *
from ..controllers.facturas_crud import *
from ..utils.enviar_notifi import enviar_notificacion



class CrediFactura_View(QWidget, Ui_FacturasCredito):
    enviar_facturas_Credito = pyqtSignal(dict, int)
    enviar_ventaCredito = pyqtSignal()
    def __init__(self, parent=None):
        super(CrediFactura_View, self).__init__(parent)
        self.setupUi(self)
        
        self.InputBuscador.setPlaceholderText("Buscar por ID, Cliente, o Fecha de Registro")
        self.InputBuscador.textChanged.connect(self.buscar_ventasCredito)
        
        self.TablaFacturasCredito.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.TablaFacturasCredito.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.TablaFacturasCredito.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        
        self.BtnEliminarFactura.clicked.connect(self.eliminar_factura)
        self.BtnEditarFactura.clicked.connect(self.editar_ventaCredito)
        self.BtnAgregarAbono.clicked.connect(self.agregar_abono)
    
    def showEvent(self, event):
        super().showEvent(event)
        self.limpiar_tabla()
        self.mostrar_ventasCredito()
    
    def mostrar_ventasCredito(self):
        """
        Obtener todos los productos de la base de datos y mostrarlos en la tabla.
        """
        self.db = SessionLocal()
        rows = obtener_ventas_credito(self.db)

        self.actualizar_tabla_ventasCredito(rows)

        self.db.close()
    
    def limpiar_tabla(self):
        self.TablaFacturasCredito.setRowCount(0)
    
    def actualizar_tabla_ventasCredito(self, rows):
        if not rows:
            print("No hay filas para mostrar.")
            self.TablaFacturasCredito.setRowCount(0)
            return

        # Establecer número de filas y columnas
        self.TablaFacturasCredito.setRowCount(len(rows))
        self.TablaFacturasCredito.setColumnCount(9)

        # Iterar sobre las filas
        for row_idx, row in enumerate(rows):
            # Datos de la fila
            id_venta_credito = str(row.ID_Venta_Credito)
            usuario = str(row.usuario)
            id_factura = str(row.ID_Factura)
            cliente = str(row.cliente)
            fecha_registro = str(row.Fecha_Registro)
            fecha_limite = str(row.Fecha_Limite)
            total_deuda = str(row.Total_Deuda)
            saldo_pendiente = str(row.Saldo_Pendiente)
            estado = "Pagado" if row.estado else "Pendiente"

            # Configurar items de la tabla
            items = [
                (id_venta_credito, 0),
                (usuario, 1),
                (id_factura, 2),
                (cliente, 3),
                (fecha_registro, 4),
                (fecha_limite, 5),
                (total_deuda, 6),
                (saldo_pendiente, 7),
                (estado, 8),
            ]

            # Añadir items a la tabla
            for value, col_idx in items:
                item = QtWidgets.QTableWidgetItem(value)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.TablaFacturasCredito.setItem(row_idx, col_idx, item)
    
    def obtener_ids_seleccionados(self):
        """
        Obtiene los IDs de los productos seleccionados en la tabla.
        """
        filas_seleccionadas = self.TablaFacturasCredito.selectionModel().selectedRows()
        ids = []

        for fila in filas_seleccionadas:
            id_producto = self.TablaFacturasCredito.item(
                fila.row(), 0
            ).text()  # Columna 0: ID del producto
            ids.append(int(id_producto))

        return ids

    def eliminar_factura(self):
        """
        Elimina una factura.
        """
        # Obtener el ID de la factura seleccionada
        ids = self.obtener_ids_seleccionados()

        if not ids:
            enviar_notificacion(
                "Advertencia", "No se seleccionaron facturas para eliminar."
            )
            return

        respuesta = QtWidgets.QMessageBox.question(
            self,
            "Confirmar Eliminación",
            f"¿Está seguro de que desea eliminar {len(ids)} factura(s)?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
        )

        if respuesta == QtWidgets.QMessageBox.Yes:
            try:
                self.db = SessionLocal()


                for id_ventaCredito in ids:
                    ventaCredito = obtener_venta_credito_por_id(self.db, id_ventaCredito)
                    if ventaCredito:
                        id_factura =ventaCredito.ID_Factura
                        eliminar_venta_credito(self.db, id_ventaCredito)
                    eliminar_factura(self.db, id_factura)

                self.db.commit()
                enviar_notificacion("Éxito", "Factura(s) eliminada(s) correctamente.")

                # Actualizar la tabla
                self.limpiar_tabla()
                self.mostrar_ventasCredito()

            except Exception as e:
                print(f"Error al eliminar ventaCredito: {e}")
            finally:
                self.db.close()
    
    def buscar_ventasCredito(self):
        """
        Busca facturas en la base de datos y actualiza la tabla.
        """
        busqueda = self.InputBuscador.text().strip()
        if not busqueda:
            self.mostrar_ventasCredito()
            return

        self.db = SessionLocal()

        facturas = buscar_ventas_credito(self.db, busqueda)
        self.actualizar_tabla_ventasCredito(facturas)

        self.db.close()

    def editar_ventaCredito(self):
        """Abrir ventana de ventas con los datos de la factura seleccionada."""
        try:
            ids = self.obtener_ids_seleccionados()

            if not ids:
                enviar_notificacion(
                    "Advertencia", "No se seleccionaron facturas para editar."
                )
                return

            # Llamar a la función para obtener todos los datos de la factura
            id_factura = obtener_venta_credito_por_id(self.db, ids[0]).ID_Factura
            
            factura_completa = obtener_factura_completa(self.db, id_factura)
        
            if not factura_completa:
                QMessageBox.showerror("Error", f"No se encontró la factura con ID {id_factura}.")
                return
            
            self.enviar_facturas_Credito.emit(factura_completa, ids[0])

        except Exception as e:
            print(f"Error al abrir ventana de ventas: {e}")
    
    def agregar_abono(self):
        try:
            ids = self.obtener_ids_seleccionados()
            
            if not ids:
                QMessageBox.warning(self, "Advertencia", "No se seleccionaron facturas para agregar abono.")
                return
            
            self.enviar_ventaCredito.emit()
            
        except Exception as e:
            print(f"Error al agregar abono: {e}")
                