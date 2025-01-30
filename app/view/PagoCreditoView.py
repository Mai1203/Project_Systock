from PyQt5.QtWidgets import (
    QWidget,
)
from PyQt5 import QtWidgets, QtCore

from ..ui import Ui_PagoCredito
from ..database.database import SessionLocal
from ..controllers.venta_credito_crud import *
from ..controllers.venta_credito_crud import *


class PagoCredito_View(QWidget, Ui_PagoCredito):
    def __init__(self, parent=None):
        super(PagoCredito_View, self).__init__(parent)
        self.setupUi(self)

    def cargar_información(self, id_ventaCredito):

        self.db = SessionLocal()
        rows = obtener_ventaCredito_id(self.db, id_ventaCredito)
        # Establecer número de filas y columnas
        self.TablaPagoCredito.setRowCount(len(rows))
        self.TablaPagoCredito.setColumnCount(7)
        print(f"Tipo de row: {type(rows)}, Valor: {rows}")
        # Iterar sobre las filas
        for row_idx, row in enumerate(rows):
            try:
                if row:  # Verificar si hay datos
                    id_factura = str(rows._mapping["ID_Factura"])
                    usuario = str(rows._mapping["usuario"])
                    fecha_registro = str(rows._mapping["Fecha_Registro"])
                    fecha_limite = str(rows._mapping["Fecha_Limite"])
                    total_deuda = str(rows._mapping["Total_Deuda"])
                    saldo_pendiente = str(rows._mapping["Saldo_Pendiente"])
                    estado = "Pagado" if rows._mapping["estado"] else "Pendiente"
                else:
                    print("No se encontró la venta a crédito.")
            except IndexError as e:
                print(f"Error: {e}. Revisa las posiciones en la consulta.")

            # Configurar items de la tabla
            items = [
                (id_factura, 0),
                (usuario, 1),
                (fecha_registro, 2),
                (fecha_limite, 3),
                (total_deuda, 4),
                (saldo_pendiente, 5),
                (estado, 6),
            ]

            # Añadir items a la tabla
            for value, col_idx in items:
                item = QtWidgets.QTableWidgetItem(value)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.TablaPagoCredito.setItem(row_idx, col_idx, item)
