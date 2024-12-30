from PyQt5.QtWidgets import QMessageBox, QWidget, QTableWidgetItem
from PyQt5.QtCore import QRegularExpression
from PyQt5.QtGui import QRegularExpressionValidator
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
from PyQt5 import QtWidgets
from ..database.database import SessionLocal
from ..controllers.producto_crud import *
from ..controllers.detalle_factura_crud import *
from ..controllers.facturas_crud import *
from ..ui import Ui_VentasA

import locale


class VentasA_View(QWidget, Ui_VentasA):
    def __init__(self, parent=None):
        super(VentasA_View, self).__init__(parent)
        self.setupUi(self)
        self.limpiar_tabla()
        self.valor_domicilio = 0.0
        self.fila_seleccionada = None
        self.configurar_localizacion()
        self.validar_campos()
        self.InputCodigo.returnPressed.connect(self.procesar_codigo)
        self.timer = QTimer(self) #Timer para evitar consultas excesivas
        self.timer.timeout.connect(self.procesar_codigo_y_agregar)
        self.InputCodigo.textChanged.connect(self.iniciar_timer)
        self.BtnEliminar.clicked.connect(self.eliminar_fila)
        self.tableWidget.cellClicked.connect(self.cargar_datos)
        self.InputCantidad.returnPressed.connect(self.actualizar_datos)
        self.InputPrecioUnitario.returnPressed.connect(self.actualizar_datos)
        self.InputDomicilio.returnPressed.connect(self.actualizar_datos)
        self.InputDomicilio.editingFinished.connect(self.actualizar_total)
        self.tableWidget.itemChanged.connect(self.actualizar_total)
        # self.InputDomicilio.textChanged.connect(self.calcular_subtotal)
        self.InputCedula.textChanged.connect(self.validar_campos)
        self.InputCedula.returnPressed.connect(self.completar_campos)
        self.InputDescuento.returnPressed.connect(self.aplicar_descuento)
        self.InputDescuento.returnPressed.connect(self.aplicar_descuento)


    def configurar_localizacion(self):
        try:
            # Configura la localización a Colombia
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
                self.InputPrecioUnitario.setText(str(producto.Precio_venta_normal))
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
        """
        Limpia todos los datos de la tabla 'tableWidget', pero mantiene las columnas.
        """

        self.tableWidget.setRowCount(
            0
        )  # Solo elimina las filas, pero mantiene las columnas
    def iniciar_timer(self):
        self.timer.stop()  # Reiniciar el timer con cada pulsación de tecla
        self.timer.start(500)  # Iniciar el timer con un retraso de 500ms
         
    def procesar_codigo_y_agregar(self):
        self.timer.stop() #Detener el timer para evitar ejecuciones duplicadas
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
        precio_unitario = self.InputPrecioUnitario.text().strip()

        try:
            cantidad = int(cantidad)  # Convertimos la cantidad a entero
            precio_unitario = float(precio_unitario)  # Convertimos el precio a flotante
        except ValueError:
            QMessageBox.warning(
                self,
                "Error",
                "Por favor, ingrese valores numéricos válidos para la cantidad y el precio.",
            )
            return
        # Verificar si el código del producto ya existe en la tabla
        for row in range(self.tableWidget.rowCount()):
            item_codigo = self.tableWidget.item(row, 0)  # Obtener el código de la fila
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
            total = cantidad * precio_unitario
            total_redondeado = round(total / 100) * 100

            # Obtener la posición de la nueva fila en la tabla
            rowPosition = (
                self.tableWidget.rowCount()
            )  # Esta es la cantidad de filas actuales en la tabla

            # Insertar una nueva fila en la tabla
            self.tableWidget.insertRow(rowPosition)

            # Agregar los datos a la nueva fila
            item_codigo = QtWidgets.QTableWidgetItem(codigo)
            item_codigo.setFlags(item_codigo.flags() & ~QtCore.Qt.ItemIsEditable)
            item_codigo.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowPosition, 0, item_codigo)

            item_nombre = QtWidgets.QTableWidgetItem(nombre)
            item_nombre.setFlags(item_nombre.flags() & ~QtCore.Qt.ItemIsEditable)
            item_nombre.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowPosition, 1, item_nombre)

            item_marca = QtWidgets.QTableWidgetItem(marca)
            item_marca.setFlags(item_marca.flags() & ~QtCore.Qt.ItemIsEditable)
            item_marca.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowPosition, 2, item_marca)

            item_categoria = QtWidgets.QTableWidgetItem(categoria)
            item_categoria.setFlags(item_categoria.flags() & ~QtCore.Qt.ItemIsEditable)
            item_categoria.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowPosition, 3, item_categoria)

            item_cantidad = QtWidgets.QTableWidgetItem(str(cantidad))
            item_cantidad.setFlags(item_cantidad.flags() & ~QtCore.Qt.ItemIsEditable)
            item_cantidad.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowPosition, 4, item_cantidad)

            item_precio = QtWidgets.QTableWidgetItem(str(precio_unitario))
            item_precio.setFlags(item_precio.flags() & ~QtCore.Qt.ItemIsEditable)
            item_precio.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowPosition, 5, item_precio)

            item_total_redondeado = QtWidgets.QTableWidgetItem(str(total_redondeado))
            item_total_redondeado.setFlags(item_total_redondeado.flags() & ~QtCore.Qt.ItemIsEditable)
            item_total_redondeado.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowPosition, 6, item_total_redondeado)
            # Limpiar los campos después de agregar
            self.limpiar_campos()

        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"Error al agregar el producto: {str(e)}"
            )

        finally:
            db.close()

    def limpiar_campos(self):
        """
        Limpia todos los campos de entrada.
        """
        self.InputCodigo.clear()
        self.InputNombre.clear()
        self.InputMarca.clear()
        self.InputCantidad.clear()
        self.InputPrecioUnitario.clear()
        self.InputDomicilio.clear()
        self.InputCodigo.setFocus()  # Establece el foco nuevamente en el campo InputCodigo

    def eliminar_fila(self):
        # Obtener la fila seleccionada
        fila_seleccionada = self.tableWidget.currentRow()

        # Verificar si se ha seleccionado una fila
        if (
            fila_seleccionada != -1
        ):  # -1 significa que no se ha seleccionado ninguna fila
            # Confirmar la eliminación con el usuario
            reply = QMessageBox.question(
                self,
                "Confirmar eliminación",
                "¿Estás seguro de que deseas eliminar esta fila?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )

            if reply == QMessageBox.Yes:
                # Eliminar la fila seleccionada
                self.tableWidget.removeRow(fila_seleccionada)
                self.limpiar_campos()

                # Actualizar el subtotal y total después de eliminar la fila
                self.actualizar_total()
        else:
            QMessageBox.warning(
                self, "Error", "Por favor, selecciona una fila para eliminar."
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
        for row in range(self.tableWidget.rowCount()):
            total_item = self.tableWidget.item(
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
                row >= 0 and row < self.tableWidget.rowCount()
            ):  # Comprobar que la fila existe
                #codigo_item = self.tableWidget.item(row, 0)
                nombre_item = self.tableWidget.item(row, 1)
                marca_item = self.tableWidget.item(row, 2)
                categoria_item = self.tableWidget.item(row, 3)
                cantidad_item = self.tableWidget.item(row, 4)
                precio_unitario_item = self.tableWidget.item(row, 5)

                if all(
                    item is not None
                    for item in [
                 #       codigo_item,
                        nombre_item,
                        marca_item,
                        categoria_item,
                        cantidad_item,
                        precio_unitario_item,
                    ]
                ):  # Comprobar que los items no son None
                 #   codigo = codigo_item.text()
                    nombre = nombre_item.text()
                    marca = marca_item.text()
                    categoria = categoria_item.text()
                    cantidad = cantidad_item.text()
                    precio_unitario = precio_unitario_item.text()

                 #   self.InputCodigo.setText(codigo)
                    self.InputNombre.setText(nombre)
                    self.InputMarca.setText(marca)
                    self.InputCantidad.setText(cantidad)
                    self.InputPrecioUnitario.setText(precio_unitario)

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

        # Almacenar la fila seleccionada para usarla más tarde en la actualización
        self.fila_seleccionada = row

    def actualizar_datos(self):  
        if self.fila_seleccionada is not None:
            try:
                cantidad_str = self.InputCantidad.text().strip()
                precio_unitario_str = self.InputPrecioUnitario.text().strip()

                if not cantidad_str or not precio_unitario_str:
                    QMessageBox.warning(
                        self,
                        "Error",
                        "Por favor, ingrese valores para cantidad y precio unitario.",
                    )
                    return

                cantidad = int(cantidad_str)
                precio_unitario = float(precio_unitario_str)

                # Obtener el código del producto desde la fila seleccionada
                row = self.fila_seleccionada
                if row < self.tableWidget.rowCount():
                    item_codigo = self.tableWidget.item(row, 0)  # Suponiendo que la columna 0 contiene el código
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
                self.tableWidget.setItem(row, 4, QTableWidgetItem(str(cantidad)))
                self.tableWidget.item(row, 4).setTextAlignment(QtCore.Qt.AlignCenter) 
                self.tableWidget.setItem(
                    row, 5, QTableWidgetItem(str(precio_unitario))
                )
                self.tableWidget.item(row, 5).setTextAlignment(QtCore.Qt.AlignCenter) 
                total = cantidad * precio_unitario
                self.tableWidget.setItem(row, 6, QTableWidgetItem(str(total)))
                self.tableWidget.item(row, 6).setTextAlignment(QtCore.Qt.AlignCenter) 

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
                    "Ingrese valores numéricos válidos para cantidad y precio unitario.",
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
        # Cédula (solo números)
        rx_codigo = QRegularExpression(r"^\d+$")  # Expresión para solo números
        validator_codigo = QRegularExpressionValidator(rx_codigo)
        self.InputCodigo.setValidator(validator_codigo)

        rx_precioU = QRegularExpression(
            r"^\d+\.\d+$"
        )  # Expresión para números y puntos
        validator_precioU = QRegularExpressionValidator(rx_precioU)
        self.InputPrecioUnitario.setValidator(validator_precioU)

        rx_domicilio = QRegularExpression(
            r"^\d+\.\d+$"
        )  # Expresión para números y puntos
        validator_domicilio = QRegularExpressionValidator(rx_domicilio)
        self.InputDomicilio.setValidator(validator_domicilio)

        rx_cantidad = QRegularExpression(r"^\d+$")  # Expresión para solo números
        validator_cantidad = QRegularExpressionValidator(rx_cantidad)
        self.InputCantidad.setValidator(validator_cantidad)

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

        rx_descuento = QRegularExpression(
            r"^\d+\.\d+$"
        )  # Expresión para números y puntos
        validator_descuento = QRegularExpressionValidator(rx_descuento)
        self.InputDescuento.setValidator(validator_descuento)
        rx_descuento = QRegularExpression(r"^\d+$") #Permite numeros enteros 
        validator_descuento = QRegularExpressionValidator(rx_descuento)
        self.InputDescuento.setValidator(validator_descuento)

    def completar_campos(self):

        if self.InputCedula.text() == "111":
            self.InputNombreCli.setText(
                "Predeterminado"
            )  # Cambia por el nombre que desees
            self.InputTelefonoCli.setText(
                "1234567890"
            )  # Cambia por el número que desees
            self.InputDireccion.setText("Predeterminado")
            
    def aplicar_descuento(self):
        try:
            # Obtener y validar el valor de descuento ingresado
            descuento_str = self.InputDescuento.text().strip()
            
            # Si el campo está vacío, asignar descuento a 0
            if not descuento_str:
                descuento = 0
                self.InputDescuento.setText("0")  # Actualizar visualmente el campo a 0
            else:
                descuento = float(descuento_str)
                if descuento < 0:  # Validar que el descuento no sea negativo
                    raise ValueError("El descuento no puede ser negativo.")

        except ValueError:
            QMessageBox.warning(self, "Error", "Valor de descuento no válido.")
            self.InputDescuento.clear()
            return

        # Calcular el subtotal antes del descuento
        subtotal_antes_descuento = self.calcular_subtotal()

        # Validar que el descuento no sea mayor al subtotal
        if descuento > subtotal_antes_descuento:
            QMessageBox.warning(self, "Error", "El descuento no puede ser mayor al subtotal.")
            self.InputDescuento.clear()
            return

        # Calcular el nuevo subtotal después del descuento
        nuevo_subtotal = subtotal_antes_descuento - descuento

        # Formatear el subtotal: Si no hay decimales, no los muestra
        if nuevo_subtotal.is_integer():
            subtotal_formateado = f"{nuevo_subtotal:,.0f}"
        else:
            subtotal_formateado = f"{nuevo_subtotal:,.2f}"

        # Actualizar el label de Subtotal con formato de moneda
        self.LabelSubtotal.setText(f"Subtotal: {subtotal_formateado}")

        # Calcular el total considerando el domicilio u otros cargos (si aplica)
        total = nuevo_subtotal + self.obtener_valor_domicilio()

        # Formatear el total: Si no hay decimales, no los muestra
        if total.is_integer():
            total_formateado = f"{total:,.0f}"
        else:
            total_formateado = f"{total:,.2f}"

        # Actualizar el label de Total con formato de moneda
        self.LabelTotal.setText(f"Total: {total_formateado}")
