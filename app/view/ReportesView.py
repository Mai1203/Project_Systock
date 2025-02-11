from PyQt5.QtWidgets import QWidget, QFileDialog
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QMessageBox
from ..database.database import SessionLocal
from ..ui import Ui_Reportes
from..controllers.tipo_pago_crud import *
from ..controllers.metodo_pago_crud import *
from ..controllers.pago_credito_crud import *
from ..controllers.venta_credito_crud import *
from ..controllers.producto_crud import * 
from ..controllers.ingresos_crud import *
from ..controllers.egresos_crud import *
from ..utils.Estructura_Reporte import crear_pdf
from ..utils.Credito__Reporte import generar_pdf_creditos
from ..utils.Estructura_Reporte import crear_pdf, generar_pdf_productos_mas_vendidos
from ..utils import Ingresos_egresos_reporte
from sqlalchemy import and_
import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from sqlalchemy import and_, func



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
        self.BtnTicketProducto.clicked.connect(lambda: self.generar_pdf())
        self.BtnTicketCaja.clicked.connect(lambda: self.obtener_ingresos_egresos(self.TipoCajaComboBox.currentText()))
        self.BtnTicketAnalisis.clicked.connect(
        lambda: self.obtener_creditos_analisis(self.ReporteAnalisisComboBox.currentText()))

        # Deshabilitar calendarios por defecto
        self.CalendarioCaja.setEnabled(True)
        self.CalendarioAnalisis.setEnabled(True)
    def obtener_creditos(self, tipo):
        tipo = "Análisis de crédito"
        resultado = self.obtener_creditos_analisis(tipo)
        if resultado:
            # Aquí podrías hacer algo con el resultado, como mostrarlo en una nueva ventana
            messagebox.showinfo("Resultado", f"Análisis: {resultado}")
        else:
            messagebox.showwarning("Error", "No se pudo obtener el análisis.")
    
    
    def obtener_creditos_analisis(self, tipo):
        db = SessionLocal()  # Iniciamos la sesión de base de datos
        try:
            if tipo == "Análisis de crédito":
                # Obtener las ventas a crédito
                ventas = obtener_ventas_credito(db)
                resultado = []  # Lista para almacenar el resultado

                for venta in ventas:
                    # Obtener los pagos asociados a cada venta usando el ID_Venta_Credito
                    pagos = db.query(PagoCredito).filter(PagoCredito.ID_Venta_Credito == venta.ID_Venta_Credito).all()

                    # Agregar los datos de la venta y sus pagos al resultado
                    resultado.append({
                        "venta": {
                            "ID_Venta_Credito": venta.ID_Venta_Credito,
                            "Total_Deuda": venta.Total_Deuda,
                            "Saldo_Pendiente": venta.Saldo_Pendiente,
                            "Fecha_Registro": venta.Fecha_Registro
                        },
                        "pagos": [{
                            "ID_Pago_Credito": pago.ID_Pago_Credito,
                            "Monto": pago.Monto,
                            "Fecha_Registro": pago.Fecha_Registro,
                            "Metodo_Pago": self.obtener_metodo_pago(db, pago.ID_Metodo_Pago),
                            "Tipo_Pago": self.obtener_tipo_pago(db, pago.ID_Tipo_Pago)
                        } for pago in pagos]
                    })

                # Enviar el resultado a la función que genera el reporte (por ejemplo, generar_pdf_creditos)
                generar_pdf_creditos(self, resultado)

                # Retornar los resultados para ser utilizados en el reporte PDF
                return resultado
            else:
                print("Tipo no válido:", tipo)
                return None
        finally:
            db.close()  # Cerrar la sesión

    # Funciones auxiliares para obtener los detalles del método de pago y tipo de pago
    def obtener_metodo_pago(self, db, id_metodo_pago):
        # Obtiene el nombre o detalle del método de pago
        metodo_pago = db.query(MetodoPago).filter(MetodoPago.ID_Metodo_Pago == id_metodo_pago).first()
        return metodo_pago.Nombre if metodo_pago else "Desconocido"

    def obtener_tipo_pago(self, db, id_tipo_pago):
        # Obtiene el nombre o detalle del tipo de pago
        tipo_pago = db.query(TipoPago).filter(TipoPago.ID_Tipo_Pago == id_tipo_pago).first()
        return tipo_pago.Nombre if tipo_pago else "Desconocido"

    def obtener_ingresos_egresos(self, tipo):
       
        db = SessionLocal()
        try:
            if not self.fecha_inicio_caja:
                QMessageBox.warning(self, "Error", "Debes seleccionar una fecha inicial")
            
            if tipo == "Egresos":
                query = db.query(Egresos)  # Asegúrate de que "Egresos" es el nombre de tu modelo

                # Depurar: Verificar las fechas seleccionadas
                print(f"Fecha inicio seleccionada: {self.fecha_inicio_caja}")
                print(f"Fecha fin seleccionada: {self.fecha_fin_caja}")

                # Filtramos por las fechas si están definidas
                if self.fecha_inicio_caja and self.fecha_fin_caja:
                    fecha_inicio = self.fecha_inicio_caja.toString('yyyy-MM-dd')
                    fecha_fin = self.fecha_fin_caja.toString('yyyy-MM-dd')
                    
                    # Asegurarse de que la fecha fin tenga la hora hasta el último minuto
                    fecha_fin += " 23:59:59"  # Añadir las horas al final de la fecha de fin
                    query = query.filter(and_(
                        func.date(Egresos.Fecha_Egreso) >= fecha_inicio, 
                        func.date(Egresos.Fecha_Egreso) <= fecha_fin))
                    
                elif self.fecha_inicio_caja:
                    fecha_inicio = self.fecha_inicio_caja.toString('yyyy-MM-dd')
                    fecha_fin = None
                    # Ajustar la fecha de inicio para considerar solo el día, sin hora
                    query = query.filter(func.date(Egresos.Fecha_Egreso) == fecha_inicio)

                egresos = query.all()                    
                datos = [(e.ID_Egreso, e.Tipo_Egreso, e.Monto_Egreso, e.Fecha_Egreso) for e in egresos]

                Ingresos_egresos_reporte.generar_pdf_transacciones(datos, "egresos", fecha_inicio, fecha_fin)

            else:
                print(f"Fecha inicio seleccionada: {self.fecha_inicio_caja}")
                print(f"Fecha fin seleccionada: {self.fecha_fin_caja}")
                ingresos = []
                # Filtramos por las fechas si están definidas
                if self.fecha_inicio_caja and self.fecha_fin_caja:
                    fecha_inicio = self.fecha_inicio_caja.toString('yyyy-MM-dd')
                    fecha_fin = self.fecha_fin_caja.toString('yyyy-MM-dd')
                    # Asegurarse de que la fecha fin tenga la hora hasta el último minuto
                    fecha_fin += " 23:59:59"  # Añadir las horas al final de la fecha de fin
                    ingresos = obtener_ingresos_reportes(db=db, FechaInicio=fecha_inicio, FechaFin=fecha_fin)
                    
                elif self.fecha_inicio_caja:
                    fecha_inicio = self.fecha_inicio_caja.toString('yyyy-MM-dd')
                    fecha_fin = None
                    # Ajustar la fecha de inicio para considerar solo el día, sin hora
                    ingresos = obtener_ingresos_reportes(db=db, FechaInicio=fecha_inicio)

                datos = []
                for e in ingresos:
                    if e.tipo_ingreso == "Venta":
                        datos.append((e.ID_Ingreso, e.tipo_ingreso, e.monto_efectivo, e.monto_transaccion, e.fecha_venta))
                    else:
                        if e.metodo_pago == "Efectivo":
                            efectivo = str(e.monto)
                            tranferencia = "0.0"
                        else:
                            tranferencia = str(e.monto)
                            efectivo = "0.0"
                        datos.append((e.ID_Ingreso, e.tipo_ingreso, efectivo, tranferencia, e.fecha_abono))
                Ingresos_egresos_reporte.generar_pdf_transacciones(datos, "ingresos", fecha_inicio, fecha_fin)

        finally:
            db.close()
    
    def mostrar_mensaje(self, titulo, mensaje):
        """
        Muestra un mensaje emergente en caso de error o advertencia.
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(titulo)
        msg.setText(mensaje)
        msg.exec_()
    
    def obtener_productos(self, tipo):
        """
        Obtiene productos según el tipo seleccionado (Bajo Stock o Inactivos).
        """
        db = SessionLocal()
        try:
            if tipo == "Bajo Stock":
                productos = (
                    db.query(Productos.ID_Producto, Productos.Nombre, Productos.Stock_actual)
                    .order_by(Productos.Stock_actual)
                    .all()
                )
                return [(p.ID_Producto, p.Nombre, p.Stock_actual) for p in productos]
            
            elif tipo == "Más  Vendidos - Menos Vendidos":
                return []

            elif tipo == "Inactivos":
                productos = (
                    db.query(Productos.ID_Producto, Productos.Nombre, Productos.Estado)
                    .filter(Productos.Estado.in_(['0', '1']))  # Filtramos por estado
                    .order_by(Productos.Estado)  # Ordenamos por estado (inactivos primero)
                    .all()
                )
                # Mapear los valores de Estado de 0/1 a Inactivo/Activo
                # Mapear los valores de Estado de 0/1 a Inactivo/Activo
                productos_transformados = [
                    (p.ID_Producto, p.Nombre, "Activo" if p.Estado == 1 else "Inactivo") for p in productos
                ]

                # Retornar los productos transformados
                return productos_transformados

            else:
                # Si se selecciona otra opción, podemos incluir lógica adicional si es necesario
                return []

        finally:
            db.close()

    def generar_pdf(self):
        # Obtener el tipo de productos seleccionado en el ComboBox
        tipo_seleccionado = self.TipoProductosComboBox.currentText()  # Obtener el valor del ComboBox
        
        if tipo_seleccionado == "Más  Vendidos - Menos Vendidos":
            db = SessionLocal()
            productos =obtener_productos_mas_vendidos(db=db, limite=30)
            generar_pdf_productos_mas_vendidos(productos)
        
        else:
            # Obtener los productos de la base de datos según el tipo seleccionado
            productos = self.obtener_productos(tipo_seleccionado)  

            # Nombre por defecto para el archivo (BajoStock_fecha)
            fecha_actual = datetime.now().strftime("%Y-%m-%d")
            nombre_pdf_por_defecto = f"{tipo_seleccionado}_{fecha_actual}.pdf"

            # Usar un diálogo para que el usuario elija dónde guardar el archivo
            ruta_archivo, _ = QFileDialog.getSaveFileName(self, "Guardar PDF", nombre_pdf_por_defecto, "PDF Files (*.pdf)")

            # Verificar si se ha seleccionado una ruta y proceder con la creación del PDF
            if ruta_archivo:  
                crear_pdf(ruta_archivo, productos, tipo_seleccionado)

                # Mostrar mensaje de confirmación
                messagebox.showinfo("PDF Generado", f"El archivo PDF ha sido generado en: {ruta_archivo}")
            else:
                # Si no se seleccionó ninguna ruta (es decir, el usuario cerró el cuadro de diálogo sin seleccionar archivo),
                # se evita proceder a guardar el archivo.
                messagebox.showinfo("Operación cancelada", "No se ha seleccionado ninguna ruta para guardar el archivo.")

    def closeEvent(self, event):
        # Verificar si el cuadro de diálogo de guardado ha sido abierto y no se ha seleccionado un archivo
        respuesta = messagebox.askyesno("Salir", "¿Estás seguro de que deseas salir sin guardar?")

        if respuesta == "yes":
            event.accept()  # Cerrar la ventana si el usuario acepta
        else:
            event.ignore()  # No cerrar la ventana si el usuario cancela

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
