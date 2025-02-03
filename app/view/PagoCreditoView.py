from PyQt5.QtWidgets import (
    QWidget,
    QMessageBox,
)
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QRegularExpression
from PyQt5.QtGui import QRegularExpressionValidator

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
        self.id_VentaCredito = None
        configurar_validador_numerico(self.InputPago)
        
        self.InputPago.setPlaceholderText("$")
        self.MetodoPagoBox.addItems(self.metodo_pago())
        self.MetodoPagoBox.currentIndexChanged.connect(self.configuracion_pago)
        
        self.BtnAbonar.clicked.connect(self.abonar)

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
            
            pago_credito =crear_pago_credito(db=self.db, id_venta_credito=self.id_VentaCredito, monto=abono_total, id_metodo_pago=id_metodo_pago, id_tipo_pago=tipo_pago)
            actualizar_venta = actualizar_venta_credito(db=self.db, id_venta_credito=self.id_VentaCredito, saldo_pendiente=saldo_pendiente)
            actualizar_factura(db=self.db, id_factura=id_factura, monto_efectivo=efectivo, monto_transaccion=tranferencia, id_metodo_pago=id_metodo_pago, estado=estado)
            
            tipo_ingreso = crear_tipo_ingreso(db=self.db, tipo_ingreso="Abono", id_pago_credito=pago_credito.ID_Pago_Credito)
            crear_ingreso(db=self.db, id_tipo_ingreso=tipo_ingreso.ID_Tipo_Ingreso)
            
            
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