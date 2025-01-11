# PyQt5 imports
from PyQt5.QtWidgets import QMessageBox, QWidget, QTableWidgetItem
from PyQt5.QtCore import QRegularExpression, QTimer, QUrl
from PyQt5.QtGui import QRegularExpressionValidator
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPalette, QColor


# Relative imports
from ..database.database import SessionLocal
from ..controllers.producto_crud import *
from ..controllers.detalle_factura_crud import *
from ..controllers.facturas_crud import *
from ..controllers.metodo_pago_crud import *
from ..ui import Ui_VentasB

# Standard library imports
import os
import locale

class VentasB_View(QWidget, Ui_VentasB):
    
    cambiar_a_ventanaA = pyqtSignal()
    
    def __init__(self, parent=None):
        super(VentasB_View, self).__init__(parent)
        self.setupUi(self)
        self.BtnFacturaA.clicked.connect(self.cambiar_a_ventanaA)
        
        # Configuración inicial
        self.player = QMediaPlayer() 
        self.InputCodigo.setFocus()
        self.id_categoria = None
        self.valor_domicilio = 0.0
        self.fila_seleccionada = None
        self.aplicando_descuento = False  # Inicializar la bandera
        self.timer = QTimer(self)  # Timer para evitar consultas excesivas

        # Inicialización y configuración
        self.limpiar_tabla()
        self.configurar_localizacion()
        self.validar_campos()
        self.MetodoPagoBox.addItems(self.metodo_pago())

        # Conexiones de señales - Entradas de texto
        self.InputCodigo.returnPressed.connect(self.procesar_codigo)
        self.InputCodigo.textChanged.connect(self.iniciar_timer)
        self.InputDomicilio.returnPressed.connect(self.actualizar_datos)
        self.InputCantidad.returnPressed.connect(self.actualizar_datos)
        self.InputPrecioMayor.returnPressed.connect(self.actualizar_datos)
        self.InputDomicilio.editingFinished.connect(self.actualizar_total)
        self.InputDomicilio.textChanged.connect(self.calcular_subtotal)
        self.InputCedula.textChanged.connect(self.validar_campos)
        self.InputCedula.returnPressed.connect(self.completar_campos)
        self.MetodoPagoBox.currentIndexChanged.connect(self.configuracion_pago)
        
        #placeholder
        self.InputPago.setPlaceholderText("$")
        self.InputCedula.setPlaceholderText("Ej: 10004194608")
        self.InputNombreCli.setPlaceholderText("Ej: Pepito Perez")
        self.InputTelefonoCli.setPlaceholderText("Ej: 3170065430")
        self.InputDireccion.setPlaceholderText("Ej: Calle 1, 123 - Piso 1")
        self.BtnFacturaB.setStyleSheet("""
            QPushButton {
                background-color: red; 
            }
        """)
      
        
        # Conexiones de señales - Botones y tabla
        self.BtnEliminar.clicked.connect(self.eliminar_fila)
        self.TablaVentaMayor.cellClicked.connect(self.cargar_datos)
        self.TablaVentaMayor.itemChanged.connect(self.actualizar_total)


        # Timer
        self.timer.timeout.connect(self.procesar_codigo_y_agregar)
        
    def reproducir_sonido(self):
        sonido_path = "./assets/sound_scanner.wav"
        if os.path.exists(sonido_path):
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(sonido_path)))
            self.player.play()
        else:
            print("No se encontró el archivo de sonido")
    
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return and self.InputDomicilio.hasFocus():
            self.actualizar_datos()
        # Llamar al método original para procesar otros eventos
        super().keyPressEvent(event)
        
    def configurar_localizacion(self):
        try:
            locale.setlocale(locale.LC_ALL, "es_CO.UTF-8")
        except locale.Error:
            print("No se pudo configurar la localización de Colombia.")
    
    def procesar_codigo(self):
        codigo = self.InputCodigo.text().strip()
        if not codigo:
            QMessageBox.warning(self, "Error", "Por favor, ingrese un código válido.")
            return
        try:
            # Conexión a la base de datos
            db = SessionLocal()
            productos = obtener_producto_por_id(db, int(codigo))

            if productos:
                producto = productos[0]

                self.InputCodigo.setText(codigo)
                self.InputNombre.setText(producto.Nombre)
                self.InputNombre.setEnabled(False)  # Deshabilitar el input
                self.InputMarca.setText(str(producto.marcas))
                self.InputMarca.setEnabled(False)  # Deshabilitar el input
                self.InputPrecioMayor.setText(str(producto.Precio_venta_mayor))
                self.InputPrecioMayor.setEnabled(False)  # Deshabilitar el input
                self.id_categoria = producto.categorias
                # *** LIMPIAR InputCantidad e InputDomicilio ***
                self.InputCantidad.clear()
                self.InputDomicilio.clear()
            else:
                QMessageBox.warning(
                    self,
                    "Producto no encontrado",
                    "No existe un producto asociado a este código.",
                )

            db.close()

        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"Error al buscar el producto: {str(e)}"
            )
            
    def limpiar_tabla(self):
        self.TablaVentaMayor.setRowCount(0)
        
    def iniciar_timer(self):
        self.timer.stop()  # Reiniciar el timer con cada pulsación de tecla
        self.timer.start(500)  # Iniciar el timer con un retraso de 500ms
        
    def procesar_codigo_y_agregar(self):
        self.timer.stop()  # Detener el timer para evitar ejecuciones duplicadas
        codigo = self.InputCodigo.text().strip()
        if codigo:
            self.procesar_codigo()
            if self.id_categoria is not None:
                self.InputCantidad.setText("1")
                self.agregar_producto()
                self.InputCodigo.clear()
                self.InputCodigo.setFocus()
                
    def agregar_producto(self):
        # Leer los datos de los campos de entrada
        codigo = self.InputCodigo.text().strip()
        nombre = self.InputNombre.text().strip()
        marca = self.InputMarca.text().strip()
        categoria = str(self.id_categoria)  # Usamos el valor guardado de id_categoria
        cantidad = self.InputCantidad.text().strip()
        precio_mayor = self.InputPrecioMayor.text().strip()

        try:
            cantidad = int(cantidad)  # Convertimos la cantidad a entero
            precio_mayor = float(precio_mayor)  # Convertimos el precio a flotante
        except ValueError:
            QMessageBox.warning(
                self,
                "Error",
                "Por favor, ingrese valores numéricos válidos para la cantidad y el precio.",
            )
            return
        # Verificar si el código del producto ya existe en la tabla
        for row in range(self.TablaVentaMayor.rowCount()):
            item_codigo = self.TablaVentaMayor.item(row, 0)  # Obtener el código de la fila
            if item_codigo and item_codigo.text() == codigo:  # Si el código ya existe
                QMessageBox.warning(self, "Error", "Este código de producto ya existe.")
                return  # No agregar el producto si ya existe el código

        # Conexión a la base de datos
        db = SessionLocal()

        try:
            # Obtener el producto desde la base de datos usando la función obtener_producto_por_id
            productos = obtener_producto_por_id(db, int(codigo))

            if productos:
                producto = productos[0]
                # Obtener el stock disponible
                stock_disponible = producto.Stock_actual

                # Verificar si la cantidad ingresada es mayor al stock disponible
                if cantidad > stock_disponible:
                    QMessageBox.warning(
                        self,
                        "Stock insuficiente",
                        f"No hay suficiente stock para esta venta. Solo quedan {stock_disponible} unidades.",
                    )
                    return  # No proceder con la venta si no hay suficiente stock

            else:
                QMessageBox.warning(
                    self,
                    "Producto no encontrado",
                    "No existe un producto asociado a este código.",
                )
                return

            # Calcular el total
            total = cantidad * precio_mayor
            total_redondeado = round(total / 100) * 100

            # Obtener la posición de la nueva fila en la tabla
            rowPosition = (
                self.TablaVentaMayor.rowCount()
            )  # Esta es la cantidad de filas actuales en la tabla

            # Insertar una nueva fila en la tabla
            self.TablaVentaMayor.insertRow(rowPosition)

            # Agregar los datos a la nueva fila
            item_codigo = QtWidgets.QTableWidgetItem(codigo)
            item_codigo.setFlags(item_codigo.flags() & ~QtCore.Qt.ItemIsEditable)
            item_codigo.setTextAlignment(QtCore.Qt.AlignCenter)
            self.TablaVentaMayor.setItem(rowPosition, 0, item_codigo)

            item_nombre = QtWidgets.QTableWidgetItem(nombre)
            item_nombre.setFlags(item_nombre.flags() & ~QtCore.Qt.ItemIsEditable)
            item_nombre.setTextAlignment(QtCore.Qt.AlignCenter)
            self.TablaVentaMayor.setItem(rowPosition, 1, item_nombre)

            item_marca = QtWidgets.QTableWidgetItem(marca)
            item_marca.setFlags(item_marca.flags() & ~QtCore.Qt.ItemIsEditable)
            item_marca.setTextAlignment(QtCore.Qt.AlignCenter)
            self.TablaVentaMayor.setItem(rowPosition, 2, item_marca)

            item_categoria = QtWidgets.QTableWidgetItem(categoria)
            item_categoria.setFlags(item_categoria.flags() & ~QtCore.Qt.ItemIsEditable)
            item_categoria.setTextAlignment(QtCore.Qt.AlignCenter)
            self.TablaVentaMayor.setItem(rowPosition, 3, item_categoria)

            item_cantidad = QtWidgets.QTableWidgetItem(str(cantidad))
            item_cantidad.setFlags(item_cantidad.flags() & ~QtCore.Qt.ItemIsEditable)
            item_cantidad.setTextAlignment(QtCore.Qt.AlignCenter)
            self.TablaVentaMayor.setItem(rowPosition, 4, item_cantidad)

            item_precio = QtWidgets.QTableWidgetItem(str(precio_mayor))
            item_precio.setFlags(item_precio.flags() & ~QtCore.Qt.ItemIsEditable)
            item_precio.setTextAlignment(QtCore.Qt.AlignCenter)
            self.TablaVentaMayor.setItem(rowPosition, 5, item_precio)

            item_total_redondeado = QtWidgets.QTableWidgetItem(str(total_redondeado))
            item_total_redondeado.setFlags(
                item_total_redondeado.flags() & ~QtCore.Qt.ItemIsEditable
            )
            item_total_redondeado.setTextAlignment(QtCore.Qt.AlignCenter)
            self.TablaVentaMayor.setItem(rowPosition, 6, item_total_redondeado)
            # Limpiar los campos después de agregar
            # Dentro de la función donde agregas el producto
            self.reproducir_sonido()
            self.limpiar_campos()

        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"Error al agregar el producto: {str(e)}"
            )

        finally:
            db.close()
            
    def limpiar_campos(self):
        self.InputCodigo.clear()
        self.InputNombre.clear()
        self.InputMarca.clear()
        self.InputCantidad.clear()
        self.InputPrecioMayor.clear()
        self.InputDomicilio.clear()
        self.InputCodigo.setFocus()  # Establece el foco nuevamente en el campo InputCodigo
    def eliminar_fila(self):
        # Obtener la fila seleccionada
        fila_seleccionada = self.TablaVentaMayor.currentRow()

        # Verificar si se ha seleccionado una fila
        if (
            fila_seleccionada != -1
        ):  # -1 significa que no se ha seleccionado ninguna fila
            # Confirmar la eliminación con el usuario
            reply = QMessageBox.question(
                self,
                "Confirmar eliminación",
                "¿Estás seguro de que deseas eliminar este producto?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )

            if reply == QMessageBox.Yes:
                # Eliminar la fila seleccionada
                self.TablaVentaMayor.removeRow(fila_seleccionada)
                self.limpiar_campos()

                # Actualizar el subtotal y total después de eliminar la fila
                self.actualizar_total()
        else:
            QMessageBox.warning(
                self, "Error", "Por favor, selecciona un producto para eliminar."
            )
            
    def obtener_valor_domicilio(self):
        if self.InputDomicilio.isEnabled():
            VarDomicilio = self.InputDomicilio.text().strip()
            try:
                self.valor_domicilio = float(VarDomicilio) if VarDomicilio else 0.0
            except ValueError:
                QMessageBox.warning(self, "Error", "Ingrese un número válido.")
                self.valor_domicilio = 0.0  # Resetear el valor
                self.InputDomicilio.clear()  # Limpiar el input
                return 0.0
            return self.valor_domicilio
        else:
            return self.valor_domicilio  # Retornar el valor actual
        
    def calcular_subtotal(self):
        # Calcular el subtotal sumando los valores de la columna "Total" (columna 6)
        subtotal = 0.0
        for row in range(self.TablaVentaMayor.rowCount()):
            total_item = self.TablaVentaMayor.item(
                row, 6
            )  # Columna 6 contiene el total por producto
            if total_item is not None:
                try:
                    subtotal += float(total_item.text())
                except ValueError:
                    continue  # Ignorar valores inválidos
        return subtotal
    def actualizar_total(self):
        subtotal = self.calcular_subtotal()

        if subtotal.is_integer():
            subtotal_formateado = f"{subtotal:,.0f}"
        else:
            subtotal_formateado = f"{subtotal:,.2f}"

        self.LabelSubtotal.setText(f"Subtotal: {subtotal_formateado}")

        domicilio = self.obtener_valor_domicilio()  # Obtener el valor del domicilio

        total = subtotal + domicilio

        if total.is_integer():
            total_formateado = f"{total:,.0f}"
        else:
            total_formateado = f"{total:,.2f}"

        self.LabelTotal.setText(f"Total: {total_formateado}")
        
    def cargar_datos(self, row, column):
        try:
            if (
                row >= 0 and row < self.TablaVentaMayor.rowCount()
            ):  # Comprobar que la fila existe
                nombre_item = self.TablaVentaMayor.item(row, 1)
                marca_item = self.TablaVentaMayor.item(row, 2)
                categoria_item = self.TablaVentaMayor.item(row, 3)
                cantidad_item = self.TablaVentaMayor.item(row, 4)
                precio_mayor_item = self.TablaVentaMayor.item(row, 5)

                if all(
                    item is not None
                    for item in [
                        #       codigo_item,
                        nombre_item,
                        marca_item,
                        categoria_item,
                        cantidad_item,
                        precio_mayor_item,
                    ]
                ):
                    Nnombre = nombre_item.text()
                    Mmarca = marca_item.text()
                    Mcategoria = categoria_item.text()
                    Mcantidad = cantidad_item.text()
                    Mprecio_mayor = precio_mayor_item.text()

                    self.InputNombre.setText(Nnombre)
                    self.InputMarca.setText(Mmarca)
                    self.InputCantidad.setText(Mcantidad)
                    self.InputPrecioMayor.setText(Mprecio_mayor)

                    self.fila_seleccionada = row
                    self.InputDomicilio.setEnabled(True)

                    # *** MOSTRAR el valor de self.valor_domicilio en InputDomicilio ***
                    self.InputDomicilio.setText(str(self.valor_domicilio))

                else:
                    QMessageBox.warning(
                        self,
                        "Error",
                        "Algunas celdas de la fila seleccionada están vacías.",
                    )
            else:
                QMessageBox.warning(self, "Error", "Fila seleccionada fuera de rango.")
                self.fila_seleccionada = None
                self.InputDomicilio.clear()
        except (
            AttributeError
        ):  # Capturar la excepcion en caso de que algun item sea None
            QMessageBox.warning(
                self, "Error", "Algunas celdas de la fila seleccionada están vacías."
            )
        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"Ocurrió un error al cargar los datos: {e}"
            )
            
    def actualizar_datos(self):
        if self.fila_seleccionada is not None:
            try:
                cantidad_str = self.InputCantidad.text().strip()
                precio_mayor_str = self.InputPrecioMayor.text().strip()
                #domicilio_str = self.InputDomicilio.text().strip()

                if not cantidad_str or not precio_mayor_str:
                    QMessageBox.warning(
                        self,
                        "Error",
                        "Por favor, ingrese valores para cantidad.",
                    )
                    return

                cantidad = int(cantidad_str)                
                precio_mayor = float(precio_mayor_str)
                #domicilio = float(domicilio_str)

                # Obtener el código del producto desde la fila seleccionada
                row = self.fila_seleccionada
                if row < self.TablaVentaMayor.rowCount():
                    item_codigo = self.TablaVentaMayor.item(
                        row, 0
                    )  # Suponiendo que la columna 0 contiene el código
                    if item_codigo:
                        codigo = item_codigo.text().strip()
                    else:
                        QMessageBox.warning(
                            self,
                            "Error",
                            "No se pudo obtener el código del producto desde la fila seleccionada.",
                        )
                        return
                else:
                    QMessageBox.warning(
                        self,
                        "Error",
                        "La fila seleccionada ya no existe en la tabla.",
                    )
                    return

                # Conexión a la base de datos
                db = SessionLocal()

                try:
                    # Obtener el producto desde la base de datos usando la función obtener_producto_por_id
                    productos = obtener_producto_por_id(db, int(codigo))

                    if productos:
                        producto = productos[0]
                        # Obtener el stock disponible
                        stock_disponible = producto.Stock_actual

                        # Verificar si la cantidad ingresada es mayor al stock disponible
                        if cantidad > stock_disponible:
                            QMessageBox.warning(
                                self,
                                "Stock insuficiente",
                                f"No hay suficiente stock para esta venta. Solo quedan {stock_disponible} unidades.",
                            )
                            return  # No proceder con la venta si no hay suficiente stock
                    else:
                        QMessageBox.warning(
                            self,
                            "Producto no encontrado",
                            "No existe un producto asociado a este código.",
                        )
                        return
                finally:
                    db.close()

                # Actualizar los datos en la tabla
                self.TablaVentaMayor.setItem(row, 4, QTableWidgetItem(str(cantidad)))
                self.TablaVentaMayor.item(row, 4).setTextAlignment(QtCore.Qt.AlignCenter)
                self.TablaVentaMayor.setItem(row, 5, QTableWidgetItem(str(precio_mayor)))
                self.TablaVentaMayor.item(row, 5).setTextAlignment(QtCore.Qt.AlignCenter)
                total = cantidad * precio_mayor
                self.TablaVentaMayor.setItem(row, 6, QTableWidgetItem(str(total)))
                self.TablaVentaMayor.item(row, 6).setTextAlignment(QtCore.Qt.AlignCenter)

                self.actualizar_total()  # Recalcular el total

                self.limpiar_campos()
                QMessageBox.information(
                    self, "Actualización", "Datos actualizados satisfactoriamente."
                )
                self.fila_seleccionada = None

            except ValueError:
                QMessageBox.warning(
                    self,
                    "Error",
                    "Ingrese valores numéricos válidos para cantidad y precio mayor.",
                )
            except Exception as e:
                QMessageBox.critical(
                    self, "Error", f"Ocurrió un error al actualizar los datos: {e}"
                )
        else:
            QMessageBox.warning(
                self, "Error", "No se ha seleccionado ninguna fila para actualizar."
            )
            
    def validar_campos(self):
        rx_codigo = QRegularExpression(r"^\d+$")  # Expresión para solo números
        validator_codigo = QRegularExpressionValidator(rx_codigo)
        self.InputCodigo.setValidator(validator_codigo)

        rx_domicilio = QRegularExpression(
            r"^\d+\.\d+$"
        )  # Expresión para números y puntos
        validator_domicilio = QRegularExpressionValidator(rx_domicilio)
        self.InputDomicilio.setValidator(validator_domicilio)

        rx_cantidad = QRegularExpression(r"^\d+$")  # Expresión para solo números
        validator_cantidad = QRegularExpressionValidator(rx_cantidad)
        self.InputCantidad.setValidator(validator_cantidad)

        rx_precio_mayor = QRegularExpression(
            r"^\d+\.\d+$"
        )   # Expresión para números y puntos
        validator_precio_mayor = QRegularExpressionValidator(rx_precio_mayor)
        self.InputPrecioMayor.setValidator(validator_precio_mayor)

        rx_cedula = QRegularExpression(r"^\d+$")  # Expresión para solo números
        validator_cedula = QRegularExpressionValidator(rx_cedula)
        self.InputCedula.setValidator(validator_cedula)

        # Nombre (solo letras y espacios)
        rx_nombre = QRegularExpression(
            r"^[a-zA-Z ]+$"
        )  # Expresión para letras y espacios
        validator_nombre = QRegularExpressionValidator(rx_nombre)
        self.InputNombreCli.setValidator(validator_nombre)

        # Teléfono (solo números y guiones)
        rx_telefono = QRegularExpression(
            r"^[0-9]{10}$"
        )  # Expresión para números y guiones
        validator_telefono = QRegularExpressionValidator(rx_telefono)
        self.InputTelefonoCli.setValidator(validator_telefono)

    def completar_campos(self):

          
        if self.InputCedula.text() == "111":
            self.InputNombreCli.setText("Predeterminado")  # Cambia por el nombre que desees
            self.InputTelefonoCli.setText("1234567890")  # Cambia por el número que desees
            self.InputDireccion.setText("Predeterminado")
            
            
    def metodo_pago(self):
        try:
            # Iniciar conexión con la base de datos
            db = SessionLocal()

            # Verificar si la conexión fue exitosa
            if db:
                metodos = obtener_metodos_pago(db)
                
                # Obtener nombres de los métodos de pago si existen
                if metodos:
                    nombres_metodos = [metodo.Nombre for metodo in metodos]
                else:
                    nombres_metodos = []
            else:
                nombres_metodos = []

            return nombres_metodos  # Retorna los nombres de los métodos de pago

        except Exception as e:
            # Manejo de errores (opcionalmente, puedes registrar errores en logs)
            return []

        finally:
            # Cerrar la conexión con la base de datos
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
            self.InputPago.setPlaceholderText("$ / $")
            
            # Expresión regular para permitir el formato 50000 / 30000 (con espacio antes y después de la barra)
            rx_inpago = QRegularExpression(r"^\d+(\.\d{1,2})?\s*/\s*\d+(\.\d{1,2})?$")  # Formato: 50000.00 / 30000.00
            validator_inpago = QRegularExpressionValidator(rx_inpago)
            self.InputPago.setValidator(validator_inpago)
        else:
            # Si no es Efectivo, Transferencia ni Mixto, mostramos solo el símbolo $
            self.InputPago.setText("$")
         
