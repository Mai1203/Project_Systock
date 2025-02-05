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
        QTimer.singleShot(0, self.InputMontoCaja.setFocus)
        self.timer = QTimer(self)  # Timer para evitar consultas excesivas
        self.InputMontoCaja.setPlaceholderText("Ej : 45000")
        
        
        #placeholder
        self.InputBuscador.setPlaceholderText("Buscar por Usuario  o Fecha de Apertura AAAA/MM/DD")
        configurar_validador_numerico(self.InputMontoCaja)
        self.limpiar_tabla()
    
    def showEvent(self, event):
        super().showEvent(event)
        self.limpiar_tabla()
        self.mostrar_tabla()
        
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
            egresos = obtener_egresos(db=self.db)
            ingresos = obtener_ingresos(db=self.db)
            caja = obtener_cajas(db=self.db)
        except Exception as e:
            print(f"Error al obtener datos de la caja: {e}")
            return
        finally:
            self.db.close()
            
        self.actualizar_tabla(egresos, ingresos, caja)
        
    def actualizar_tabla(self, egresos, ingresos, caja):
        
        try:
            self.TablaEgresos.setRowCount(
                len(egresos)
            ) 
            
            for row, egreso in enumerate(egresos):
                id_egreso = str(egreso.ID_Egreso)
                metodo = str(egreso.metodopago)
                monto = str(egreso.Monto_Egreso)
                
                if metodo == "Efectivo":
                    efectivo = monto
                    trasferencia = 0.0
                elif metodo == "Transferencia":
                    trasferencia = monto
                    efectivo = 0.0
                
                items = [
                    (id_egreso, 0),
                    (str(efectivo), 1),
                    (str(trasferencia), 2),
                ]
                
                for value, col_idx in items:
                    item = QtWidgets.QTableWidgetItem(str(value))
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.TablaEgresos.setItem(row, col_idx, item)
                    
        except Exception as e:
            print(f"Error en Tabla Egresos: {e}")
        
        try:              
            self.TablaIngresos.setRowCount(
                len(ingresos)
            ) 
            for row, ingreso in enumerate(ingresos):
                id_ingreso = str(ingreso.ID_Ingreso)
                tipo = str(ingreso.tipo_ingreso)
                efectivo = str(ingreso.monto_efectivo)
                trasferencia = str(ingreso.monto_transaccion)
                
                items = [
                    (id_ingreso, 0),
                    (tipo, 1)
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
            self.TablaCaja.setRowCount(
                len(caja)
            )  
            # for row, caja in enumerate(caja):
            #     id_caja = str(caja.ID_Caja)
            #     monto = str(caja.Monto)
            #     fecha = str(caja.Fecha)
            #     usuario = str(caja.Usuario)
                
            #     items = [
            #         (id_caja, 0),
            #         (monto, 1),
            #         (fecha, 2),
            #         (usuario, 3),
            #     ]
                
            #     for value, col_idx in items:
            #         item = QtWidgets.QTableWidgetItem(value)
            #         item.setTextAlignment(QtCore.Qt.AlignCenter)
            #         self.TablaCaja.setItem(row, col_idx, item)
        except Exception as e:
            print(f"Error en Tabla caja: {e}")
            
            
        
        
        
        
        
