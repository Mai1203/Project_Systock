# PyQt5 imports
from PyQt5.QtWidgets import QMessageBox, QWidget, QTableWidgetItem
from PyQt5.QtCore import QRegularExpression, QTimer, QUrl
from PyQt5.QtGui import QRegularExpressionValidator
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from ..utils.Estructura_Reporte import *

from ..ui import Ui_Caja
from ..database.database import *
from ..controllers.caja_crud import *
from ..controllers.egresos_crud import *
from ..controllers.ingresos_crud import *
from ..controllers.caja_crud import *
from ..utils.validar_campos import *
from PyQt5.QtGui import QColor 
from PyQt5.QtWidgets import QMessageBox  
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
        self.TablaCaja.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        
        self.BtnCajaApertura.clicked.connect(self.crear_caja)
        self.BtnCajaCierre.clicked.connect(self.cerrar_caja)
        self.InputBuscador.textChanged.connect(self.buscar_caja)
        self.TablaCaja.itemSelectionChanged.connect(self.seleccionar_fila)
        self.BtnCajaImprimir.clicked.connect(self.generar_reporte)

        #placeholder
        self.InputBuscador.setPlaceholderText("Buscar por Usuario  o Fecha de Apertura AAAA/MM/DD")
        configurar_validador_numerico(self.InputMontoCaja)
        self.limpiar_tabla()
    
    def showEvent(self, event):
        super().showEvent(event)
        self.InputMontoCaja.clear()
        self.limpiar_tabla()
        self.mostrar_tabla()
        self.sumar_total()
        
    def seleccionar_fila(self):
        selected_row = self.TablaCaja.currentRow()
        if selected_row == -1:
            print("No hay una fila seleccionada.")
            return
        
        # Resetear colores de todas las filas
        for row in range(self.TablaCaja.rowCount()):
            for col in range(self.TablaCaja.columnCount()):
                self.TablaCaja.item(row, col).setBackground(QColor(255, 255, 255))  # Blanco

        # Cambiar color de la fila seleccionada
        for col in range(self.TablaCaja.columnCount()):
            self.TablaCaja.item(selected_row, col).setBackground(QColor(173, 216, 230))  # Azul claro

        # Obtener datos de la fila seleccionada
        id_caja = self.TablaCaja.item(selected_row, 0).text()  # ID_Caja
        id_usuario = self.TablaCaja.item(selected_row, 1).text()  # ID_Usuar
        monto_base = self.TablaCaja.item(selected_row, 2).text()  # Monto_Base
        fecha_apertura = self.TablaCaja.item(selected_row, 3).text()  # Fecha_Apertura
        fecha_cierre = self.TablaCaja.item(selected_row, 4).text()  # Fecha_Cierre
        monto_efectivo = self.TablaCaja.item(selected_row, 5).text()  # Monto_Efectivo
        monto_transaccion = self.TablaCaja.item(selected_row, 6).text()  # Monto_Transaccion
        monto_final = self.TablaCaja.item(selected_row, 7).text()  # Monto_Final_calculado
        estado = self.TablaCaja.item(selected_row, 8).text()  # Estado

        print(f"Fila seleccionada: ID Caja {id_caja}, Apertura: {fecha_apertura}, Cierre: {fecha_cierre}")

        # Guardar datos en atributos de la clase
        self.fecha_inicio = fecha_apertura
        self.fecha_fin = fecha_cierre
        self.id_caja = id_caja
        self.monto_base = monto_base
        self.monto_efectivo = monto_efectivo
        self.monto_transaccion = monto_transaccion
        self.monto_final = monto_final
        self.estado = estado
        self.id_usuario = id_usuario

    def generar_reporte(self):
        """ Filtra los ingresos según la fecha de la caja seleccionada y envía los datos a la función del PDF. """
        db = SessionLocal()
        try:
            if not hasattr(self, 'fecha_inicio') or not hasattr(self, 'fecha_fin'):
                QMessageBox.warning(self, "Error", "No se ha seleccionado una caja correctamente.")
                return

            fecha_inicio = self.fecha_inicio
            fecha_fin = self.fecha_fin

            # Consultar ingresos en el rango de fechas
            ingresos = obtener_ingresos(db, fecha_inicio, fecha_fin)

            if ingresos:
                # Crear un objeto caja con los datos de la fila seleccionada
                caja = Caja(
                    Monto_Base=self.monto_base,
                    Monto_Efectivo=self.monto_efectivo,
                    Monto_Transaccion=self.monto_transaccion,
                    Monto_Final_calculado=self.monto_final,
                    Fecha_Apertura=fecha_inicio,
                    Fecha_Cierre=fecha_fin,
                    Estado=self.estado,
                    ID_Usuario=self.id_usuario
                )

                # Enviar los datos a la función de generación de PDF
                generar_pdf_caja_ingresos(caja, ingresos)

            else:
                QMessageBox.information(self, "Sin resultados", "No se encontraron ingresos en el rango de fechas seleccionado.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al generar el reporte: {e}")
            print(f"Error al generar el reporte: {e}")

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
                
                ingresos.sort(key=lambda x: x.ID_Ingreso, reverse=False)
                
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
                        self.TablaIngresos.insertRow(0)
                        
                        items = [
                            (id_ingreso, 0),
                            (tipo, 1),
                            (efectivo, 2),
                            (trasferencia, 3),
                        ]
                        
                        for value, col_idx in items:
                            item = QtWidgets.QTableWidgetItem(value)
                            item.setTextAlignment(QtCore.Qt.AlignCenter)
                            self.TablaIngresos.setItem(0, col_idx, item)
        except Exception as e:
            print(f"Error en Tabla Ingreso: {e}")
        
        try:
            if caja:
                
                caja.sort(key=lambda x: x.ID_Caja, reverse=False)
                 
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
                    
                    self.TablaCaja.insertRow(0)
                    
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
                        self.TablaCaja.setItem(0, col_idx, item)
                    
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