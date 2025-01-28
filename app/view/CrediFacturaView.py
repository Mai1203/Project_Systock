from PyQt5.QtWidgets import (
    QWidget,
)
from PyQt5 import QtWidgets, QtCore

from ..ui import Ui_FacturasCredito
from ..database.database import SessionLocal
from ..controllers.venta_credito_crud import *


class CrediFactura_View(QWidget, Ui_FacturasCredito):
    def __init__(self, parent=None):
        super(CrediFactura_View, self).__init__(parent)
        self.setupUi(self)
    
    def showEvent(self, event):
        super().showEvent(event)
        self.mostrar_productos()
    
    def mostrar_productos(self):
        """
        Obtener todos los productos de la base de datos y mostrarlos en la tabla.
        """
        self.db = SessionLocal()
        rows = obtener_ventas_credito(self.db)

        self.actualizar_tabla_facturas(rows)

        self.db.close()
    
    def actualizar_tabla_facturas(self, rows):
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
                