# PyQt5 imports
from PyQt5.QtWidgets import QMessageBox, QWidget, QTableWidgetItem
from PyQt5.QtCore import QRegularExpression, QTimer, QUrl
from PyQt5.QtGui import QRegularExpressionValidator
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtGui
from PyQt5.QtCore import Qt

from ..ui import Ui_Caja
from ..database.database import *
from ..controllers.caja_crud import *
from ..controllers.egresos_crud import *
from ..controllers.ingresos_crud import *
from ..controllers.caja_crud import *
from ..utils.validar_campos import *


class Caja_View(QWidget, Ui_Caja):
    def __init__(self, parent=None):
        super(Caja_View, self).__init__(parent)
        self.setupUi(self)
        
        self.usuario_actual_id = None
        
        QTimer.singleShot(0, self.InputMontoCaja.setFocus)
        self.timer = QTimer(self)  # Timer para evitar consultas excesivas
        self.InputMontoCaja.setPlaceholderText("Ej : 45000")
        
        self.TablaCaja.setColumnWidth(3, 180)
        self.TablaCaja.setColumnWidth(4, 180)
        
        self.BtnCajaApertura.clicked.connect(self.crear_caja)
        self.BtnCajaCierre.clicked.connect(self.cerrar_caja)
        self.InputBuscador.textChanged.connect(self.buscar_caja)
        
        #placeholder
        self.InputBuscador.setPlaceholderText("Buscar por Usuario  o Fecha de Apertura AAAA/MM/DD")
        configurar_validador_numerico(self.InputMontoCaja)
        self.limpiar_tabla()
    
    def showEvent(self, event):
        super().showEvent(event)
        self.limpiar_tabla()
        self.mostrar_tabla()
        self.TablaIngresos.sortItems(0, QtCore.Qt.DescendingOrder)
        self.sumar_total()
        
    def limpiar_tabla(self):

        self.TablaCaja.setRowCount(
            0
        )  
        self.TablaIngresos.setRowCount(
            0
        ) 
        
    def mostrar_tabla(self):
        
        self.db = SessionLocal()
        
        try:
            ingresos = None
            cajas = obtener_cajas(db=self.db)
            
            for caja in cajas:
                if caja.Estado == True:
                    fecha_apertura = caja.Fecha_Apertura
                    fecha_cierre = caja.Fecha_Cierre
                    ingresos = obtener_ingresos(db=self.db, FechaInicio=fecha_apertura, FechaFin=fecha_cierre)
                    
        except Exception as e:
            print(f"Error al obtener datos de la caja: {e}")
            return
        finally:
            self.db.close()
            
        self.actualizar_tabla(ingresos, cajas)
        
    def actualizar_tabla(self, ingresos=None, caja=None):
        
        try: 
                 
            if ingresos:
                
                self.TablaIngresos.setRowCount(
                    len(ingresos)
                ) 
                for row, ingreso in enumerate(ingresos):
                        id_ingreso = str(ingreso.ID_Ingreso)
                        tipo = str(ingreso.tipo_ingreso)
                        if tipo == "Venta":
                            efectivo = str(ingreso.monto_efectivo)
                            trasferencia = str(ingreso.monto_transaccion)
                        else:
                            if ingreso.metodo_pago == "Efectivo":
                                efectivo = str(ingreso.monto)
                                trasferencia = "0.0"
                            else:
                                trasferencia = str(ingreso.monto)
                                efectivo = "0.0"
                        
                        items = [
                            (id_ingreso, 0),
                            (tipo, 1),
                            (efectivo, 2),
                            (trasferencia, 3),
                        ]
                        
                        for value, col_idx in items:
                            item = QtWidgets.QTableWidgetItem(value)
                            item.setTextAlignment(QtCore.Qt.AlignCenter)
                            self.TablaIngresos.setItem(row, col_idx, item)
        except Exception as e:
            print(f"Error en Tabla Ingreso: {e}")
        
        try:
            if caja:
                self.TablaCaja.setRowCount(
                    len(caja)
                )  
                for row, caja in enumerate(caja):
                    id_caja = str(caja.ID_Caja)
                    usuario = str(caja.usuario)
                    monto = str(caja.Monto_Base)
                    fechaA = str(caja.Fecha_Apertura)
                    fechaC = str(caja.Fecha_Cierre)
                    efectivo = str(caja.Monto_Efectivo)
                    trasferencia = str(caja.Monto_Transaccion)
                    total = str(caja.Monto_Final_calculado)
                    estado = "Abierta" if caja.Estado else "Cerrada"
                    
                    items = [
                        (id_caja, 0),
                        (usuario, 1),
                        (monto, 2),
                        (fechaA, 3),
                        (fechaC, 4),
                        (efectivo, 5),
                        (trasferencia, 6),
                        (total, 7),
                        (estado, 8),
                    ]
                    
                    for value, col_idx in items:
                        item = QtWidgets.QTableWidgetItem(value)
                        item.setTextAlignment(QtCore.Qt.AlignCenter)
                        self.TablaCaja.setItem(row, col_idx, item)
                    
        except Exception as e:
            print(f"Error en Tabla caja: {e}")
            
    def sumar_total(self):
        
        try:
            monto = []
            for row in range(self.TablaIngresos.rowCount()):  
                
                efectivo = self.TablaIngresos.item(row, 2).text()
                trasferencia = self.TablaIngresos.item(row, 3).text()
                monto.append((float(efectivo), float(trasferencia)))
                
            efectivo = sum(monto[0] for monto in monto)
            trasferencia = sum(monto[1] for monto in monto)
            
            self.OutEfectivo.setText(f"{efectivo:,.2f}")
            self.OutTransferencia.setText(f"{trasferencia:,.2f}")
            self.OutTotal.setText(f"{efectivo + trasferencia:,.2f}")
        except Exception as e:
            print(f"Error al sumar total: {e}")
        
    def crear_caja(self):

        for row in range(self.TablaCaja.rowCount()):
            if self.TablaCaja.item(row, 8).text() == "Abierta":
                QMessageBox.warning(self, "Error", "Ya existe una caja abierta.")
                return
        
        try:
            base = self.InputMontoCaja.text().strip()
            
            if not base:
                QMessageBox.warning(self, "Error", "Ingrese un monto válido.")
                return
            
            if float(base) < 0:
                QMessageBox.warning(self, "Error", "El monto no puede ser negativo.")
                return
            
            self.db = SessionLocal()
            try:
                id_usuario = self.usuario_actual_id
                base = float(base)
                estado = True
                
                caja = crear_caja(db=self.db, monto_base=base, id_usuario=id_usuario, estado=estado)
                self.limpiar_tabla()
                self.mostrar_tabla()
                QMessageBox.information(self, "Caja creada", "La caja ha sido creada exitosamente.")
        
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al crear la cajaen bd: {str(e)}")
            finally:
                self.db.close()
                
        except Exception as e:
            print(f"Error al crear la caja: {e}")
       
        self.InputMontoCaja.clear()     
        
    def cerrar_caja(self):
        
        count = 0
        for row in range(self.TablaCaja.rowCount()):    
            if self.TablaCaja.item(row, 8).text() == "Cerrada":
                count += 1
                if count == self.TablaCaja.rowCount():
                    QMessageBox.warning(self, "Error", "No se encontró ninguna caja Abierta.")
                    return
            
            if self.TablaCaja.item(row, 8).text() == "Abierta":
                
                efectivo = self.OutEfectivo.text().strip()
                efectivo = float(efectivo.replace(",", ""))
                trasferencia = self.OutTransferencia.text().strip()
                trasferencia = float(trasferencia.replace(",", ""))
                total = self.OutTotal.text().strip()
                total = float(total.replace(",", ""))
        
                id_caja = self.TablaCaja.item(row, 0).text()
                self.db = SessionLocal()
                try:
                    actualizar_caja(db=self.db, id_caja=id_caja, estado=False, monto_efectivo=efectivo, monto_transaccion=trasferencia, monto_final_calculado=total, fecha_cierre=datetime.now().replace(microsecond=0))
                    self.limpiar_tabla()
                    self.mostrar_tabla()
                    QMessageBox.information(self, "Caja cerrada", "La caja ha sido cerrada exitosamente.")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Error al cerrar la caja en bd: {str(e)}")
                finally:
                    self.db.close()
        
    def buscar_caja(self):
        buscar = self.InputBuscador.text().strip()
        
        if not buscar:
            self.limpiar_tabla()
            self.mostrar_tabla()
            return
        
        self.db = SessionLocal()
        
        try:
            caja = buscar_cajas(db=self.db, buscar=buscar)
            self.actualizar_tabla(caja=caja)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al buscar la caja en bd: {str(e)}")
            
        finally:
            self.db.close()