from PyQt5.QtWidgets import (
    QWidget,
    QFileDialog,
    QMessageBox,
)
from ..ui import Ui_Respaldo
import shutil  # Para copiar archivos
import os      # Para comprobar la existencia de archivos
from datetime import datetime  # Para obtener la fecha actual


class Respaldo_View(QWidget, Ui_Respaldo):
    def __init__(self, parent=None):
        super(Respaldo_View, self).__init__(parent)
        self.setupUi(self)
        
        self.BtnRespaldoExportar.clicked.connect(self.exportar_base_datos)
        # 7709991003054
        # self.BtnRespaldoImportar.clicked.connect(self.importar_base_datos)
    def exportar_base_datos(self):
        # Ruta original de la base de datos
        ruta_base_de_datos = ".\systock.db"
        if not os.path.exists(ruta_base_de_datos):
            QMessageBox.warning(self, "Error", "No se encontró la base de datos.")
            return
        # Obtener la fecha actual en formato "YYYY-MM-DD"
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        # Crear el nombre por defecto del archivo de respaldo
        nombre_archivo = f"LadyNailShop_{fecha_actual}.db"
        # Mostrar un cuadro de diálogo para guardar el respaldo, con el nombre por defecto
        ruta_exportar, _ = QFileDialog.getSaveFileName(
            self,
            "Exportar Base de Datos",
            nombre_archivo,  # Usamos el nombre por defecto aquí
            "Archivos de Base de Datos (*.db)"
        )

        if ruta_exportar:
            try:
                # Copiar la base de datos al destino seleccionado
                shutil.copy(ruta_base_de_datos, ruta_exportar)
                QMessageBox.information(self, "Éxito", "Base de datos exportada correctamente.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al exportar la base de datos:\n{str(e)}")
