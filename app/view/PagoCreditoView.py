from PyQt5.QtWidgets import (
    QWidget,
    QMessageBox,
)
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QRegularExpression
from PyQt5.QtGui import QRegularExpressionValidator
from datetime import datetime, timedelta
import win32print
import win32ui
import win32con

from ..ui import Ui_PagoCredito
from ..database.database import SessionLocal
from ..controllers.venta_credito_crud import *
from ..controllers.facturas_crud import *
from ..controllers.metodo_pago_crud import *
from ..controllers.pago_credito_crud import *
from ..controllers.tipo_ingreso_crud import *
from ..controllers.ingresos_crud import *
from ..utils.validar_campos import *


class PagoCredito_View(QWidget, Ui_PagoCredito):
    def __init__(self, parent=None):
        super(PagoCredito_View, self).__init__(parent)
        self.setupUi(self)
        
        self.invoice_number = None
        
        self.TablaPagoCredito.setColumnWidth(2, 120)
        self.TablaPagoCredito.setColumnWidth(3, 120)
        self.TablaPagoCredito.setColumnWidth(4, 120)
        self.id_VentaCredito = None
        configurar_validador_numerico(self.InputPago)
        
        self.InputPago.setPlaceholderText("$")
        self.MetodoPagoBox.addItems(self.metodo_pago())
        self.MetodoPagoBox.currentIndexChanged.connect(self.configuracion_pago)
        
        self.BtnAbonar.clicked.connect(self.abonar)

    def calcular_fecha_futura(self, dias):
        # Obtener la fecha y hora actual
        fecha_actual = datetime.now()
        # Sumar los días a la fecha actual
        fecha_futura = fecha_actual + timedelta(days=dias)
        return fecha_futura.replace(microsecond=0)
    
    def cargar_información(self, id_ventaCredito):

        self.id_VentaCredito = id_ventaCredito
        self.db = SessionLocal()
        ventaCreditos = obtener_ventaCredito_id(self.db, id_ventaCredito)
        pago_credito = obtener_pagos_credito(self.db, id_ventaCredito)
        ventaCredito = ventaCreditos[0]
        
        self.LabelDeuda.setText(f"${ventaCredito.Total_Deuda:,}")
        self.LabelPendiente.setText(f"${ventaCredito.Saldo_Pendiente:,}")
        
        estado = ventaCredito.estado
        
        if estado:
            self.LabelEstado.setText("Pagada")
            self.LabelEstado.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.LabelEstado.setText("Pendiente")
            self.LabelEstado.setStyleSheet("color: red; font-weight: bold;")  
        
        self.TablaPagoCredito.setRowCount(len(pago_credito))
        self.TablaPagoCredito.setColumnCount(7)
        
        for row, pago in enumerate(pago_credito):
            id_venta = str(pago.ID_Pago_Credito)
            cliente = str(ventaCredito.cliente)
            fecha_registro = str(pago.Fecha_Registro)
            id_ventacredito = str(ventaCredito.ID_Venta_Credito)
            metodo_pago = str(pago.metodopago)
            tipo_pago = str(pago.tipopago)
            monto = str(pago.Monto)
            
            # Configurar items de la tabla
            items = [
                (id_venta, 0),
                (cliente, 1),
                (fecha_registro, 2),
                (id_ventacredito, 3),
                (metodo_pago, 4),
                (tipo_pago, 5),
                (monto, 6),
            ]
            
            for value, col_idx in items:
                item = QtWidgets.QTableWidgetItem(value)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.TablaPagoCredito.setItem(row, col_idx, item)
                
            self.db.close()
            
    def metodo_pago(self):
        try:
            db = SessionLocal()

            if db:
                metodos = obtener_metodos_pago(db)
                
                if metodos:
                    nombres_metodos = [metodo.Nombre for metodo in metodos]
                else:
                    nombres_metodos = []
            else:
                nombres_metodos = []

            return nombres_metodos  # Retorna los nombres de los métodos de pago

        except Exception as e:
            return []

        finally:
            db.close()

    def configuracion_pago(self):
        metodo_seleccionado = self.MetodoPagoBox.currentText()
        self.InputPago.clear()
        if metodo_seleccionado == "Efectivo" or metodo_seleccionado == "Transferencia":
            # Si el método de pago es Efectivo o Transferencia, mostramos solo el símbolo $
            self.InputPago.setPlaceholderText("$")
            
            # Configurar la validación para solo números y puntos
            rx_inpago = QRegularExpression(r"^\d+\.\d+$")  # Expresión para solo números y puntos
            validator_inpago = QRegularExpressionValidator(rx_inpago)
            self.InputPago.setValidator(validator_inpago)
        elif metodo_seleccionado == "Mixto":
            # Si el método de pago es Mixto, mostramos el placeholder con la barra /
            self.InputPago.setPlaceholderText("$Efectivo / $Transferencia")
            
            # Expresión regular para permitir el formato 50000 / 30000 (con espacio antes y después de la barra)
            rx_inpago = QRegularExpression(r"^\d+(\.\d{1,2})?\s*/\s*\d+(\.\d{1,2})?$")  # Formato: 50000.00 / 30000.00
            validator_inpago = QRegularExpressionValidator(rx_inpago)
            self.InputPago.setValidator(validator_inpago)
        else:
            # Si no es Efectivo, Transferencia ni Mixto, mostramos solo el símbolo $
            self.InputPago.setText("$")

    def abonar(self):
        try:
            #Obtener datos 
            
            abono = self.InputPago.text().strip()
            metodo_pago = self.MetodoPagoBox.currentText().strip()
            id_metodo_pago = obtener_metodo_pago_por_nombre(self.db, metodo_pago).ID_Metodo_Pago
            
            if not abono:
                QMessageBox.warning(self, "Error", "Por favor, ingrese un valor válido para el abono.")
                return
            
            venta_credito  = obtener_ventaCredito_id(self.db, self.id_VentaCredito)
            
            if not venta_credito:
                QMessageBox.warning(self, "Error", "No se pudo obtener la venta a crédito.")
                return
            
            venta = venta_credito[0]
            
            if venta.estado == True:
                QMessageBox.warning(self, "Error", "La venta a crédito ya está pagada.")
                return
            
            if metodo_pago == "Efectivo":
                efectivo = float(abono)
                tranferencia = 0.0
                saldo_pendiente = float(venta.Saldo_Pendiente) - float(abono)
            elif metodo_pago == "Transferencia":
                efectivo = 0.0
                tranferencia = float(abono)
                saldo_pendiente = float(venta.Saldo_Pendiente) - float(abono)
            else:
                total = abono.split("/")
                efectivo = float(total[0])
                tranferencia = float(total[1])
                saldo_pendiente = float(venta.Saldo_Pendiente) - (efectivo + tranferencia)

            
            abono_total = efectivo + tranferencia
            
            if abono_total > venta.Saldo_Pendiente:
                QMessageBox.warning(self, "Error", "El abono no puede ser mayor al saldo pendiente.")
                return
            
            
            id_factura = int(venta.ID_Factura)
            
            factura_antigua = obtener_factura_por_id(self.db, id_factura)
            
            monto_efectivo = float(factura_antigua.Monto_efectivo)
            monto_transaccion = float(factura_antigua.Monto_TRANSACCION)
            
            efectivo += monto_efectivo
            tranferencia += monto_transaccion
            
            total_abonar = efectivo + tranferencia
            
            if total_abonar == venta.Total_Deuda:
                estado = True
                tipo_pago = 2
            else:
                estado = False
                tipo_pago = 1
                
            fecha_registro = venta.Fecha_Registro
            fecha_limite = venta.Fecha_Limite
            
            dias = fecha_limite - fecha_registro
                
            limite_pago = self.calcular_fecha_futura(dias.days)
            
            pago_credito =crear_pago_credito(db=self.db, id_venta_credito=self.id_VentaCredito, monto=abono_total, id_metodo_pago=id_metodo_pago, id_tipo_pago=tipo_pago)
            actualizar_venta = actualizar_venta_credito(db=self.db, id_venta_credito=self.id_VentaCredito, saldo_pendiente=saldo_pendiente, fecha_limite=limite_pago)
            actualizar_factura(db=self.db, id_factura=id_factura, monto_efectivo=efectivo, monto_transaccion=tranferencia, id_metodo_pago=id_metodo_pago, estado=estado)
            
            tipo_ingreso = crear_tipo_ingreso(db=self.db, tipo_ingreso="Abono", id_pago_credito=pago_credito.ID_Pago_Credito)
            crear_ingreso(db=self.db, id_tipo_ingreso=tipo_ingreso.ID_Tipo_Ingreso)
            
            id_factura = int(venta.ID_Factura)
            factura_completa = obtener_factura_completa(self.db, id_factura)
            
            productos = factura_completa["Detalles"]
            clientes = factura_completa["Cliente"]
            factura = factura_completa["Factura"]
            
            client_name = f"{clientes['Nombre']} {clientes['Apellido']}"
            client_id = clientes["ID_Cliente"]
            client_address = clientes["Direccion"]
            client_phone = clientes["Teléfono"]
            
            items = []
            for producto in productos:
                cantidad = producto["Cantidad"]
                nombre = producto["Producto"]
                precio = producto["Subtotal"]
                
                items.append((cantidad, nombre, precio))
                
            subtotal = sum(item[2] for item in items)
            delivery_fee = factura["Descuento"]
                
            pagos = obtener_pagos_credito(self.db, self.id_VentaCredito)
            
            abonos = []
            for pago in pagos:
                fecha = pago.Fecha_Registro
                metodo = pago.metodopago
                monto = pago.Monto
                abonos.append((fecha, metodo, monto))
                
                
            
                
            #----------------------------------------------------------------------------------------
            # Configuración inicial
            max_lines_per_page = 30  # Límite de líneas por página
            current_line = 0  # Contador de líneas
            empresa_nombre = "LadyNailShop"
            empresa_direccion = "Pasto, Colombia"
            empresa_telefono = "+57 316-144-44-74"

            # Obtener la fecha actual
            fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")  # ✅ Correcto

            # Formatear valores monetarios
            subtotal_formateado = f"${subtotal:,.2f}"
            total_formateado = f"${subtotal:,.2f}"
            

            # Formatear el costo de envío
            delivery_fee = float(delivery_fee)
            if delivery_fee.is_integer():
                delivery_fee_formateado = f"${int(delivery_fee):,.0f}"
            else:
                delivery_fee_formateado = f"${delivery_fee:,.2f}"

            # Limitar la dirección del cliente a 25 caracteres por línea
            direccion = client_address
            direccion_linea1 = direccion[:25]
            direccion_linea2 = direccion[25:] if len(direccion) > 25 else ""


            # Obtener la impresora predeterminada
            impresora = win32print.GetDefaultPrinter()
            print(f"Impresora predeterminada: {impresora}")
            hDC = win32ui.CreateDC()
            hDC.CreatePrinterDC(impresora)

            # Crear un documento de impresión
            hDC.StartDoc("Ticket de Venta")
            hDC.StartPage()

            # Configurar la fuente
            font_size = 26
            line_height = font_size + 10
            font = win32ui.CreateFont({
                "name": "Helvetica-Bold",
                "height": font_size,
                "weight": win32con.FW_BOLD
            })
            hDC.SelectObject(font)

            # Obtener el tamaño del papel para centrar el texto
            printer_width = hDC.GetDeviceCaps(win32con.HORZRES)
            center_x = printer_width // 2  # Punto central

            # Imprimir los datos de la empresa
            hDC.TextOut(center_x - (len(empresa_nombre) * 6), 50, empresa_nombre)
            hDC.TextOut(center_x - (len(empresa_direccion) * 6), 50 + line_height, empresa_direccion)
            hDC.TextOut(center_x - (len(empresa_telefono) * 6), 50 + 2 * line_height, empresa_telefono)

            # Imprimir la fecha actual
            hDC.TextOut(center_x - (len(fecha_actual) * 6), 50 + 3 * line_height, fecha_actual)

            # Línea separadora
            hDC.TextOut(50, 50 + 4 * line_height, "----------------------------------------")
            
            # Ajuste de coordenadas iniciales para el contenido del ticket
            x, y = 2, 2 + 5 * line_height  # Espacio después de la información de la empresa, la línea y la fecha
            # Imprimir la información del cliente
            y += line_height

            hDC.TextOut(x, y, "Ticket de venta credito")  # Imprime el título "Productos:"
            y += line_height
            hDC.TextOut(x, y, f"Ticket No. {id_factura}")# Aquí se agrega el número de factura
            y += line_height
            hDC.TextOut(x, y, f"Cliente: {client_name}")
            y += line_height
            hDC.TextOut(x, y, f"Cédula: {client_id}")
            y += line_height
            hDC.TextOut(x, y, f"Teléfono: {client_phone}")
            y += line_height
            hDC.TextOut(x, y, f"Dirección: {direccion_linea1}")
            y += line_height
            if direccion_linea2:  # Si hay una segunda línea de dirección, imprimirla
                hDC.TextOut(x, y, direccion_linea2)
                y += line_height

            # 🔹 Imprimir "Productos:" y la línea separadora
            
            hDC.TextOut(x, y, "-----------------------------------------------------------------------------------------------------------------")  # Imprime la línea separadora
            y += line_height  # Mueve la posición para empezar a imprimir los productos
            # Imprimir los productos
            hDC.TextOut(x, y, "Productos:")  # Imprime el título "Productos:"
            y += line_height  # Mueve la posición de la siguiente línea hacia abajo

            for item in items:
                producto_linea = f"{item[0]} x {item[1]} - {item[2]}"
                hDC.TextOut(x, y, producto_linea)
                y += line_height
                current_line += 1

                # Si se alcanza el límite de líneas, crear una nueva página
                if current_line >= max_lines_per_page:
                    hDC.EndPage()  # Finalizar la página actual
                    hDC.StartPage()  # Iniciar una nueva página
                    y = 2  # Reiniciar la posición Y
                    current_line = 0  # Reiniciar el contador de líneas

            # Imprimir los totales y el mensaje final
            totales = f"""
            -----------------------------------------------------------------------------------------------------
            Deuda Total: {subtotal_formateado}
            Fecha Limite: {limite_pago}
            -----------------------------------------------------------------------------------------------------
            """
            for line in totales.split("\n"):
                hDC.TextOut(x, y, line.strip())
                y += line_height

            hDC.TextOut(x, y, "Abonos:")  # Imprime el título "Productos:"
            y += line_height  # Mueve la posición de la siguiente línea hacia abajo
            
            for abono in abonos:
                abono_linea = f"{abono[0]} x {abono[1]} - {abono[2]}"
                
                # Dividir la línea en fragmentos de 25 caracteres
                while len(abono_linea) > 0:
                    abono_linea_parte = abono_linea[:35]  # Tomar los primeros 25 caracteres
                    hDC.TextOut(x, y, abono_linea_parte)
                    abono_linea = abono_linea[35:]  # Eliminar los primeros 25 caracteres ya impresos
                    y += line_height  # Salto de línea
                    current_line += 1
            hDC.TextOut(x, y, "-----------------------------------------------------------------------------------------------------------------")  # Imprime la línea separadora
            y += line_height  
            hDC.TextOut(x, y, "!Gracias Por cumplir con tu pago!")  # Imprime la línea separadora
            y += line_height  # Mueve la posición para empezar a imprimir los productos
                
            # Finalizar la impresión
            hDC.EndPage()
            hDC.EndDoc()
            hDC.DeleteDC()
            
            # Fina
            
            if actualizar_venta:
                QMessageBox.information(self, "Venta a crédito", "La venta a crédito ha sido actualizada exitosamente.")
                self.InputPago.clear()
                
                self.limpiar_tabla()
                self.cargar_información(self.id_VentaCredito)
                
        except Exception as e:
            print(f"Error al actualizar la venta a crédito: {e}")
        finally:
            self.db.close()
                
    def limpiar_tabla(self):
        self.TablaPagoCredito.setRowCount(0)