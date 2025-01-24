from PyQt5.QtCore import QTimer, QDate
from PyQt5.QtWidgets import QWidget, QFileDialog, QMessageBox
from ..ui import Ui_Respaldo
import shutil
import os
from datetime import datetime


class Respaldo_View(QWidget, Ui_Respaldo):
    def __init__(self, parent=None):
        super(Respaldo_View, self).__init__(parent)
        self.setupUi(self)
        # Configuración inicial
        self.ruta_base_de_datos = "./systock.db"  # Definido correctamente como un atributo de instancia
        self.ruta_carpeta_respaldos = os.path.join(os.path.expanduser("~"), "Desktop", "Respaldos")
        self.intentos_respaldo = 0  # Contador de intentos de respaldo en el día
        self.ultima_fecha_respaldo = None  # Última fecha de respaldo registrado

        self.BtnRespaldoExportar.clicked.connect(self.exportar_base_datos)
        self.BtnRespaldoImportar.clicked.connect(self.importar_base_datos)

        # Configuración del temporizador (verifica cada hora)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.respaldo_automatico)
        self.timer.start(1 * 60 * 1000)  # Verificar cada hora (60 minutos)
        # self.timer.start(3600000)  # Cada hora en milisegundos (1 hora = 3600000 ms)

    def exportar_base_datos(self):
        ruta_base_de_datos = "./systock.db"
        if not os.path.exists(ruta_base_de_datos):
            QMessageBox.warning(self, "Error", "No se encontró la base de datos.")
            return
        fecha_actual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # Cambié ":" por "-" para nombres válidos
        nombre_archivo = f"LadyNailShop_{fecha_actual}.db"
        ruta_exportar, _ = QFileDialog.getSaveFileName(
            self,
            "Exportar Base de Datos",
            nombre_archivo,
            "Archivos de Base de Datos (*.db)"
        )
        if ruta_exportar:
            try:
                shutil.copy(ruta_base_de_datos, ruta_exportar)
                QMessageBox.information(self, "Éxito", "Base de datos exportada correctamente.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al exportar la base de datos:\n{str(e)}")

    def importar_base_datos(self):
        ruta_importar, _ = QFileDialog.getOpenFileName(
            self,
            "Importar Base de Datos",
            "",
            "Archivos de Base de Datos (*.db)"
        )
        if not ruta_importar:
            return
        if not os.path.exists(ruta_importar):
            QMessageBox.warning(self, "Error", "El archivo seleccionado no existe.")
            return
        ruta_base_de_datos = os.path.abspath(os.path.join(".", "systock.db"))
        try:
            shutil.copy(ruta_importar, ruta_base_de_datos)
            QMessageBox.information(self, "Éxito", "Base de datos importada correctamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al importar la base de datos:\n{str(e)}")

    def respaldo_automatico(self):
        """Verifica si ya se realizó un respaldo hoy y lo realiza si no existe. Máximo 2 intentos por día."""
        if not os.path.exists(self.ruta_base_de_datos):
            print("No se encontró la base de datos para el respaldo automático.")
            return

        # Fecha actual
        fecha_actual = QDate.currentDate().toString("yyyy-MM-dd")

        # Verificar si ya se hizo el respaldo para hoy
        if self.ultima_fecha_respaldo == fecha_actual:
            print("Ya existe un respaldo para hoy. No se hará otro respaldo.")
            self.timer.stop() 
            
            return

        # Límite de intentos de respaldo
        if self.intentos_respaldo >= 2:
            print("Se alcanzó el límite de intentos de respaldo para hoy.")
            return

        # Intentar realizar respaldo (máximo 2 veces por día)
        for _ in range(2):  # Solo permite ejecutar una iteración
            # Verificar si ya hay un archivo de respaldo con la fecha actual
            nombre_respaldo_hoy = f"Backup_{fecha_actual}.db"
            ruta_respaldo_hoy = os.path.join(self.ruta_carpeta_respaldos, nombre_respaldo_hoy)
            if os.path.exists(ruta_respaldo_hoy):
                print(f"Ya existe un respaldo para hoy en: {ruta_respaldo_hoy}")
                self.ultima_fecha_respaldo = fecha_actual  # Actualizar para evitar bucles
                return

            # Crear carpeta de respaldos si no existe
            os.makedirs(self.ruta_carpeta_respaldos, exist_ok=True)

            # Crear respaldo
            try:
                shutil.copy(self.ruta_base_de_datos, ruta_respaldo_hoy)
                print(f"Respaldo automático creado: {ruta_respaldo_hoy}")
                self.ultima_fecha_respaldo = fecha_actual
                self.intentos_respaldo += 1  # Incrementar contador de intentos
                return  # Salir después de un respaldo exitoso
            except Exception as e:
                print(f"Error al crear el respaldo automático: {str(e)}")
                self.intentos_respaldo += 1  # Incrementar contador en caso de error