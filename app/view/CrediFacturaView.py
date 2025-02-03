from PyQt5.QtWidgets import (
    QWidget,
    QMessageBox,
)
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSignal

from ..ui import Ui_FacturasCredito
from ..database.database import SessionLocal
from ..controllers.venta_credito_crud import *
from ..controllers.facturas_crud import *
from ..controllers.pago_credito_crud import *
from ..utils.enviar_notifi import enviar_notificacion
from ..utils.restructura_ticket import *
from datetime import datetime

class CrediFactura_View(QWidget, Ui_FacturasCredito):
    enviar_facturas_Credito = pyqtSignal(dict, int)
    enviar_ventaCredito = pyqtSignal(int)

    def __init__(self, parent=None):
        super(CrediFactura_View, self).__init__(parent)
        self.setupUi(self)
        
        self.TablaFacturasCredito.setColumnWidth(4, 120)
        self.TablaFacturasCredito.setColumnWidth(5, 120)

        self.InputBuscador.setPlaceholderText(
            "Buscar por ID, Cliente, o Fecha de Registro"
        )
        self.InputBuscador.textChanged.connect(self.buscar_ventasCredito)

        self.TablaFacturasCredito.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows
        )
        self.TablaFacturasCredito.setSelectionMode(
            QtWidgets.QAbstractItemView.MultiSelection
        )
        self.TablaFacturasCredito.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers
        )

        self.BtnEliminarFactura.clicked.connect(self.eliminar_factura)
        self.BtnEditarFactura.clicked.connect(self.editar_ventaCredito)
        self.BtnAgregarAbono.clicked.connect(self.agregar_abono)
        self.BtnGenerarTicket.clicked.connect(self.generar_ticket)

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
            fecha_limite = row.Fecha_Limite
            total_deuda = str(row.Total_Deuda)
            saldo_pendiente = str(row.Saldo_Pendiente)
            estado = "Pagado" if row.estado else "Pendiente"

            # Convertir la fecha límite a datetime
            fecha_actual = datetime.now()
            
            # Configurar items de la tabla
            items = [
                (id_venta_credito, 0),
                (usuario, 1),
                (id_factura, 2),
                (cliente, 3),
                (fecha_registro, 4),
                (str(fecha_limite), 5),
                (total_deuda, 6),
                (saldo_pendiente, 7),
                (estado, 8),
            ]

            # Determinar color de texto
            color = QtGui.QColor("red") if fecha_actual > fecha_limite else QtGui.QColor("black")
            
            # Añadir items a la tabla
            for value, col_idx in items:
                item = QtWidgets.QTableWidgetItem(value)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setForeground(QtGui.QBrush(color))  # Aplicar color
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
                    venta_credito = obtener_ventaCredito_id(self.db, id_ventaCredito)
                    if venta_credito:
                        venta = venta_credito[0]
                        id_factura = venta.ID_Factura
                    eliminar_pagoCredito_VentaCredito(self.db, id_ventaCredito)
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
            venta_credito = obtener_ventaCredito_id(self.db, ids[0])
            venta = venta_credito[0]
            
            if venta.estado == True:
                QMessageBox.warning(self, "Error", "La venta a crédito ya está pagada.")
                return
            factura_completa = obtener_factura_completa(self.db, venta.ID_Factura)

            if not factura_completa:
                QMessageBox.showerror(
                    "Error", f"No se encontró la factura con ID {venta.ID_Factura}."
                )
                return

            self.enviar_facturas_Credito.emit(factura_completa, ids[0])

        except Exception as e:
            print(f"Error al abrir ventana de ventas: {e}")

    def agregar_abono(self):
        try:
            ids = self.obtener_ids_seleccionados()

            if not ids:
                QMessageBox.warning(
                    self,
                    "Advertencia",
                    "No se seleccionaron facturas para agregar abono.",
                )
                return

            self.enviar_ventaCredito.emit(ids[0])

        except Exception as e:
            print(f"Error al agregar abono: {e}")

    def generar_ticket(self):
        """
        Genera un ticket de venta para la factura seleccionada.
        """
        ids = self.obtener_ids_seleccionados()

        if not ids:
            enviar_notificacion(
                "Advertencia", "No se seleccionaron facturas para generar ticket."
            )
            return

        db = SessionLocal()

        venta_credito = obtener_ventaCredito_id(self.db, ids[0])
        
        venta = venta_credito[0]
        # Obtener la factura completa
        factura_completa = obtener_factura_completa(db, venta.ID_Factura)

        if not factura_completa:
            print(f"No se encontró la factura con ID {ids[0]}")
            return
        # Extraer los datos de la factura
        factura = factura_completa["Factura"]
        cliente = factura_completa["Cliente"]  # Acceder al primer elemento de la lista
        detalles = factura_completa["Detalles"]

        # Calcular subtotal y descuento
        subtotal = sum(detalle["Subtotal"] for detalle in detalles)
        delivery_fee = factura["Descuento"]

        # Extraer información necesaria para el ticket
        client_name = f"{cliente['Nombre']} {cliente['Apellido']}"
        client_id = cliente["ID_Cliente"]
        client_address = cliente["Direccion"]
        client_phone = cliente["Teléfono"]
        items = [
            {
                "quantity": detalle["Cantidad"],
                "name": detalle.get(
                    "Producto", "Producto sin nombre"
                ),  # Asegúrate de incluir el nombre del producto en la consulta
                "unit_price": (
                    float(detalle["Precio_Unitario"])
                    if isinstance(detalle["Precio_Unitario"], (int, float))
                    else 0.0
                ),
            }
            for detalle in detalles
        ]

        items2 = []
        for item in items:
            quantity = item["quantity"]
            description = item["name"]
            value = float(item["unit_price"])

            items2.append((quantity, description, value))

        # Calcular el total
        total = subtotal - delivery_fee

        # Extraer información adicional de la factura
        payment_method = factura["MetodoPago"]
        invoice_number = factura["ID_Factura"]

        if payment_method == "Efectivo":
            pago = f"{factura["Monto_efectivo"]}"
        elif payment_method == "Transferencia":
            pago = f"{factura["Monto_TRANSACCION"]}"
        else:
            pago = f"{factura['Monto_efectivo']}/{factura['Monto_TRANSACCION']}"

        pan = "123456789"  # Número fijo de ejemplo, cámbialo si es necesario

        bandera = generate_ticket(
            client_name=client_name,
            client_id=client_id,
            client_address=client_address,
            client_phone=client_phone,
            items=items2,
            subtotal=subtotal,
            delivery_fee=delivery_fee,
            total=total,
            payment_method=payment_method,
            invoice_number=invoice_number,
            pan=pan,
            pago=pago,
            filename=None,  # Puedes cambiar esto según tu necesidad
        )

        if bandera:
            QMessageBox.warning(self, "Ticket", f"Factura generada exitosamente.")
