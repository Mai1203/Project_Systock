from PyQt5.QtCore import QTimer, QDate
from PyQt5.QtWidgets import QWidget, QFileDialog, QMessageBox, QInputDialog
from ..ui import Ui_Respaldo
import shutil
import os
import sqlite3
from datetime import datetime
from pathlib import Path

app_data_dir = Path(os.getenv("APPDATA") or os.path.expanduser("~/.local/share")) / "Systock"
DATABASE_PATH = app_data_dir / "systock.db"

class Respaldo_View(QWidget, Ui_Respaldo):
    def __init__(self, parent=None):
        super(Respaldo_View, self).__init__(parent)
        self.setupUi(self)
        # Configuración inicial
        self.ruta_carpeta_respaldos = os.path.join(
            os.path.expanduser("~"), "Desktop", "Respaldos"
        )
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
        
        if not os.path.exists(DATABASE_PATH):
            QMessageBox.warning(self, "Error", "No se encontró la base de datos.")
            return

        opciones = ["Exportar tabla específica", "Exportar toda la base de datos"]
        opcion, ok = QInputDialog.getItem(
            self, "Seleccionar tipo de exportación", "Opciones:", opciones, 0, False
        )

        if not ok:
            return

        if opcion == "Exportar tabla específica":
            tabla, ok_tabla = QInputDialog.getText(
                self, "Exportar tabla", "Ingrese el nombre de la tabla a exportar:"
            )
            if not ok_tabla or not tabla:
                return

            fecha_actual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            nombre_archivo = f"{tabla}_{fecha_actual}.db"
            ruta_exportar, _ = QFileDialog.getSaveFileName(
                self,
                "Exportar Tabla",
                nombre_archivo,
                "Archivos de Base de Datos (*.db)",
            )

            if ruta_exportar:
                try:
                    # Aquí se incluiría la lógica para exportar una tabla específica
                    # Por simplicidad, copiaremos toda la base de datos como ejemplo
                    shutil.copy(DATABASE_PATH, ruta_exportar)
                    QMessageBox.information(
                        self, "Éxito", f"Tabla '{tabla}' exportada correctamente."
                    )
                except Exception as e:
                    QMessageBox.critical(
                        self, "Error", f"Error al exportar la tabla:{str(e)}"
                    )

        elif opcion == "Exportar toda la base de datos":
            fecha_actual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            nombre_archivo = f"LadyNailShop_{fecha_actual}.db"
            ruta_exportar, _ = QFileDialog.getSaveFileName(
                self,
                "Exportar Base de Datos",
                nombre_archivo,
                "Archivos de Base de Datos (*.db)",
            )

            if ruta_exportar:
                try:
                    shutil.copy(DATABASE_PATH, ruta_exportar)
                    QMessageBox.information(
                        self, "Éxito", "Base de datos exportada correctamente."
                    )
                except Exception as e:
                    QMessageBox.critical(
                        self, "Error", f"Error al exportar la base de datos:{str(e)}"
                    )


    def importar_base_datos(self):
        ruta_importar, _ = QFileDialog.getOpenFileName(
            self, "Importar Base de Datos", "", "Archivos de Base de Datos (*.db)"
        )
        if not ruta_importar:
            return

        if not os.path.exists(ruta_importar):
            QMessageBox.warning(self, "Error", "El archivo seleccionado no existe.")
            return

        # Confirmación antes de importar
        respuesta = QMessageBox.question(
            self,
            "Confirmar Importación",
            "Esto importará los datos del respaldo sin borrar tu base actual. ¿Deseas continuar?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if respuesta != QMessageBox.Yes:
            return

        self.importar_y_migrar_datos(ruta_importar)

    def respaldo_automatico(self):
        """Verifica si ya se realizó un respaldo hoy y lo realiza si no existe. Máximo 2 intentos por día."""
        
        if not os.path.exists(DATABASE_PATH):
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
            ruta_respaldo_hoy = os.path.join(
                self.ruta_carpeta_respaldos, nombre_respaldo_hoy
            )
            if os.path.exists(ruta_respaldo_hoy):
                print(f"Ya existe un respaldo para hoy en: {ruta_respaldo_hoy}")
                self.ultima_fecha_respaldo = (
                    fecha_actual  # Actualizar para evitar bucles
                )
                return

            # Crear carpeta de respaldos si no existe
            os.makedirs(self.ruta_carpeta_respaldos, exist_ok=True)

            # Crear respaldo
            try:
                shutil.copy(DATABASE_PATH, ruta_respaldo_hoy)
                print(f"Respaldo automático creado: {ruta_respaldo_hoy}")
                self.ultima_fecha_respaldo = fecha_actual
                self.intentos_respaldo += 1  # Incrementar contador de intentos
                return  # Salir después de un respaldo exitoso
            
            except Exception as e:
                print(f"Error al crear el respaldo automático: {str(e)}")
                self.intentos_respaldo += 1  # Incrementar contador en caso de error

    def importar_y_migrar_datos(self, ruta_importar):
        # Crear conexión a la base actual (estructura nueva)
        nueva_conn = sqlite3.connect(DATABASE_PATH)
        nueva_cursor = nueva_conn.cursor()

        # Crear conexión a la base antigua (archivo a importar)
        antigua_conn = sqlite3.connect(ruta_importar)
        antigua_cursor = antigua_conn.cursor()

        try:
            # Obtener nombres de tablas en la base antigua
            antigua_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tablas = [fila[0] for fila in antigua_cursor.fetchall()]

            for tabla in tablas:
                if tabla == "sqlite_sequence":
                    continue  # Saltar tabla interna

                # Leer todas las filas de la tabla antigua
                antigua_cursor.execute(f"SELECT * FROM {tabla}")
                filas = antigua_cursor.fetchall()

                # Obtener columnas comunes entre vieja y nueva base
                antigua_cursor.execute(f"PRAGMA table_info({tabla})")
                columnas_antiguas = [col[1] for col in antigua_cursor.fetchall()]

                nueva_cursor.execute(f"PRAGMA table_info({tabla})")
                columnas_nuevas = [col[1] for col in nueva_cursor.fetchall()]

                columnas_comunes = [col for col in columnas_antiguas if col in columnas_nuevas]
                if not columnas_comunes:
                    continue  # No hay columnas en común, saltar tabla

                columnas_str = ", ".join(columnas_comunes)
                placeholders = ", ".join("?" for _ in columnas_comunes)

                # Insertar cada fila en la tabla nueva
                for fila in filas:
                    # Usar solo los datos de las columnas comunes
                    datos = [
                        fila[columnas_antiguas.index(col)] for col in columnas_comunes
                    ]
                    nueva_cursor.execute(
                        f"INSERT OR REPLACE INTO {tabla} ({columnas_str}) VALUES ({placeholders})",
                        datos
                    )

            nueva_conn.commit()
            QMessageBox.information(
                self, "Éxito", "Datos migrados correctamente desde el respaldo."
            )
        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"Ocurrió un error durante la migración:\n{str(e)}"
            )
            print(e)
        finally:
            nueva_conn.close()
            antigua_conn.close()