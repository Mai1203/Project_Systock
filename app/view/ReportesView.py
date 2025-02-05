from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QDate

from ..ui import Ui_Reportes

class Reportes_View(QWidget, Ui_Reportes):
    def __init__(self, parent=None):
        super(Reportes_View, self).__init__(parent)
        self.setupUi(self)

        # Variables para almacenar fechas
        self.fecha_inicio_caja = None
        self.fecha_fin_caja = None
        self.fecha_inicio_analisis = None
        self.fecha_fin_analisis = None
        self.modo_intervalo_caja = False
        self.modo_intervalo_analisis = False

        # Configurar calendarios
        self.CalendarioCaja.selectionChanged.connect(lambda: self.obtener_fecha(self.CalendarioCaja, "caja"))
        self.CalendarioAnalisis.selectionChanged.connect(lambda: self.obtener_fecha(self.CalendarioAnalisis, "analisis"))

        # Configurar ComboBox
        self.TipoCajaComboBox.addItems(["Ingresos", "Egresos"])
        self.TiempoCajaComboBox.addItems(["Diario", "Intervalo de días"])
        self.TipoProductosComboBox.addItems(["Bajo Stock", "Más  Vendidos - Menos Vendidos", "Inactivos"])
        self.ReporteAnalisisComboBox.addItems(["Comparación Financiera", "Análisis de crédito"])
        self.TiempoAnalisisComboBox.addItems(["Diario", "Intervalo de días"])

        # Conectar ComboBox de tiempo con la función de habilitar/deshabilitar el calendario
        self.TiempoCajaComboBox.currentIndexChanged.connect(lambda: self.cambiar_estado_calendario("caja"))
        self.TiempoAnalisisComboBox.currentIndexChanged.connect(lambda: self.cambiar_estado_calendario("analisis"))

        # Deshabilitar calendarios por defecto
        self.CalendarioCaja.setEnabled(False)
        self.CalendarioAnalisis.setEnabled(False)

    def obtener_fecha(self, calendario, tipo):
        """Guarda la fecha seleccionada para Caja o Análisis."""
        fecha = calendario.selectedDate()

        if tipo == "caja":
            if self.modo_intervalo_caja:
                if not self.fecha_inicio_caja:
                    self.fecha_inicio_caja = fecha
                    print(f"[Caja] Fecha de inicio: {self.fecha_inicio_caja.toString('yyyy-MM-dd')}")
                elif not self.fecha_fin_caja:
                    self.fecha_fin_caja = fecha
                    print(f"[Caja] Fecha de fin: {self.fecha_fin_caja.toString('yyyy-MM-dd')}")
                    calendario.setEnabled(False)
            else:
                self.fecha_inicio_caja = fecha
                self.fecha_fin_caja = None
                print(f"[Caja] Fecha seleccionada: {self.fecha_inicio_caja.toString('yyyy-MM-dd')}")
                calendario.setEnabled(False)

        elif tipo == "analisis":
            if self.modo_intervalo_analisis:
                if not self.fecha_inicio_analisis:
                    self.fecha_inicio_analisis = fecha
                    print(f"[Análisis] Fecha de inicio: {self.fecha_inicio_analisis.toString('yyyy-MM-dd')}")
                elif not self.fecha_fin_analisis:
                    self.fecha_fin_analisis = fecha
                    print(f"[Análisis] Fecha de fin: {self.fecha_fin_analisis.toString('yyyy-MM-dd')}")
                    calendario.setEnabled(False)
            else:
                self.fecha_inicio_analisis = fecha
                self.fecha_fin_analisis = None
                print(f"[Análisis] Fecha seleccionada: {self.fecha_inicio_analisis.toString('yyyy-MM-dd')}")
                calendario.setEnabled(False)

    def cambiar_estado_calendario(self, tipo):
        """Habilita/deshabilita el calendario según la opción seleccionada en los ComboBox."""
        if tipo == "caja":
            opcion = self.TiempoCajaComboBox.currentText()
            if opcion == "Diario":
                self.modo_intervalo_caja = False
                self.fecha_inicio_caja = None
                self.fecha_fin_caja = None
                self.CalendarioCaja.setEnabled(True)
                print("[Caja] Modo Diario: Selecciona una sola fecha.")
            elif opcion == "Intervalo de días":
                self.modo_intervalo_caja = True
                self.fecha_inicio_caja = None
                self.fecha_fin_caja = None
                self.CalendarioCaja.setEnabled(True)
                print("[Caja] Modo Intervalo: Selecciona dos fechas.")
            else:
                self.CalendarioCaja.setEnabled(False)

        elif tipo == "analisis":
            opcion = self.TiempoAnalisisComboBox.currentText()
            if opcion == "Diario":
                self.modo_intervalo_analisis = False
                self.fecha_inicio_analisis = None
                self.fecha_fin_analisis = None
                self.CalendarioAnalisis.setEnabled(True)
                print("[Análisis] Modo Diario: Selecciona una sola fecha.")
            elif opcion == "Intervalo de días":
                self.modo_intervalo_analisis = True
                self.fecha_inicio_analisis = None
                self.fecha_fin_analisis = None
                self.CalendarioAnalisis.setEnabled(True)
                print("[Análisis] Modo Intervalo: Selecciona dos fechas.")
            else:
                self.CalendarioAnalisis.setEnabled(False)
