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
from ..utils.validar_campos import *


class Caja_View(QWidget, Ui_Caja):
    def __init__(self, parent=None):
        super(Caja_View, self).__init__(parent)
        self.setupUi(self)
        QTimer.singleShot(0, self.InputMontoCaja.setFocus)
        self.timer = QTimer(self)  # Timer para evitar consultas excesivas
        
        #placeholder
        self.InputBuscador.setPlaceholderText("Buscar por Usuario  o Fecha de Apertura AAAA/MM/DD")
        configurar_validador_numerico(self.InputMontoCaja)
        self.limpiar_tabla()
        
    def limpiar_tabla(self):

        self.TablaCaja.setRowCount(
            0
        ) 
        self.TablaEgresos.setRowCount(
            0
        ) 
        self.TablaIngresos.setRowCount(
            0
        ) 
        
    def mostrar_tabla(self):
        
        self.db = SessionLocal()
        
        egresos = obtener_egresos(db=self.db)
        ingresos = obtener_ingresos(db=self.db)
        
        
    
    def actualizar_tabla(self, egresos, ingresos):
        
        self.TablaEgresos.setRowCount(
            len(egresos)
        ) 
        self.TablaIngresos.setRowCount(
            len(ingresos)
        )
        
        
        
        
        
