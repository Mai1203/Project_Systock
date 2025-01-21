# PyQt5 imports
from PyQt5.QtWidgets import QMessageBox, QWidget, QTableWidgetItem
from PyQt5.QtCore import QRegularExpression, QTimer, QUrl
from PyQt5.QtGui import QRegularExpressionValidator
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from decimal import Decimal  # Importar Decimal para manejar números con precisión
from PyQt5 import QtCore, QtWidgets


# Relative imports
from ..database.database import SessionLocal
from ..controllers.producto_crud import *
from ..controllers.detalle_factura_crud import *
from ..controllers.clientes_crud import *
from ..controllers.facturas_crud import *
from ..ui import Ui_VentasCredito

# Standard library imports
import os
from PyQt5.QtCore import Qt
import locale

class VentasCredito_View(QWidget, Ui_VentasCredito):
    def __init__(self, parent=None):
        super(VentasCredito_View, self).__init__(parent)
        self.setupUi(self)
        # configuración inicial
        self.productos = []  # Lista de productos para calcular el subtotal
        self.player = QMediaPlayer() 
        QTimer.singleShot(0, self.InputCodigo.setFocus)
        self.id_categoria = None
        self.valor_domicilio = 0.0
        self.fila_seleccionada = None
        self.timer = QTimer(self)  # Timer para evitar consultas excesivas     
    
        
        # Inicialización y configuración
        self.limpiar_tabla()
        self.configurar_localizacion()
        self.validar_campos()
        
        # Conexiones de señales - Entradas de texto
        self.InputCodigo.returnPressed.connect(self.procesar_codigo)
        self.InputCodigo.textChanged.connect(self.iniciar_timer)
        self.InputDomicilio.returnPressed.connect(self.actualizar_datos)
        self.InputCantidad.returnPressed.connect(self.actualizar_datos)
        self.InputPrecioUnitario.returnPressed.connect(self.actualizar_datos)
        self.InputDomicilio.editingFinished.connect(self.actualizar_total)
        self.InputDomicilio.textChanged.connect(self.calcular_subtotal)
        self.InputCedula.textChanged.connect(self.validar_campos)    
        

        
        #placeholder
        self.InputCedula.setPlaceholderText("Ej: 10004194608")
        self.InputNombreCli.setPlaceholderText("Ej: Pepito")
        self.InputApellidoCli.setPlaceholderText("Ej: Perez")
        self.InputTelefonoCli.setPlaceholderText("Ej: 3170065430")
        self.InputDireccion.setPlaceholderText("Ej: Calle 1, 123 - Piso 1")
        self.LimitePagoBox.addItems(["7 días","15 dias"])
        
        # Conexiones de señales - Botones y tabla
        self.BtnEliminar.clicked.connect(self.eliminar_fila)
        self.BtnGenerarVentaCredito.clicked.connect(self.verificar_cliente)
        self.TablaVentasCredito.cellClicked.connect(self.cargar_datos)
        self.TablaVentasCredito.itemChanged.connect(self.actualizar_total)
        
        self.timer.timeout.connect(self.procesar_codigo_y_agregar)
        
    def reproducir_sonido(self):
        sonido_path = "./assets/sound_scanner.wav"
        if os.path.exists(sonido_path):
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(sonido_path)))
            self.player.play()
        else:
            print("No se encontró el archivo de sonido")
            
    def keyPressEvent(self, event):
        # Si presionas Enter en InputDomicilio, realiza una acción especial
        if self.InputDomicilio.hasFocus() and event.key() == Qt.Key_Return:
            self.actualizar_datos()  # Acción personalizada para InputDomicilio
        elif event.key() == Qt.Key_Up:
            
            self.navegar_widgets()
            
        elif event.key() == Qt.Key_Down:
            self.navegar_widgets_atras()
        # Llamar al método original para procesar otros eventos
        super().keyPressEvent(event)
    def navegar_widgets(self):
        if self.focusWidget() == self.InputCodigo:
            self.InputNombre.setFocus()
        elif self.focusWidget() == self.InputNombre:
            self.InputNombreCli.setFocus()
        elif self.focusWidget() == self.InputNombreCli:
            self.InputApellidoCli.setFocus()
        elif self.focusWidget() == self.InputApellidoCli:
            self.InputDireccion.setFocus()
        elif self.focusWidget() == self.InputDireccion:
            self.InputTelefonoCli.setFocus()
        elif self.focusWidget() == self.InputTelefonoCli:
            self.InputCedula.setFocus()
        elif self.focusWidget() == self.InputCedula:
            self.InputCodigo.setFocus()  # Volver al inicio

    def navegar_widgets_atras(self):
        """
        Navega hacia atrás entre los widgets en el siguiente orden:
        Código <- Nombre <- Nombre Cliente <- Apellido Cliente <- Dirección <- Teléfono <- Cédula <- Nombre <- Código
        """
        if self.focusWidget() == self.InputCodigo:
            self.InputCedula.setFocus()
        elif self.focusWidget() == self.InputCedula:
            self.InputTelefonoCli.setFocus()
        elif self.focusWidget() == self.InputTelefonoCli:
            self.InputDireccion.setFocus()
        elif self.focusWidget() == self.InputDireccion:
            self.InputApellidoCli.setFocus()
        elif self.focusWidget() == self.InputApellidoCli:
            self.InputNombreCli.setFocus()
        elif self.focusWidget() == self.InputNombreCli:
            self.InputNombre.setFocus()
        elif self.focusWidget() == self.InputNombre:
            self.InputCodigo.setFocus()  # Volver al inicio

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
                self.InputPrecioUnitario.setText(str(producto.Precio_venta_normal))
                self.InputPrecioUnitario.setEnabled(False)  # Deshabilitar el input
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
        self.TablaVentasCredito.setRowCount(0)
        
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
                
        # Calcular el total del producto
       
        for row in range(self.TablaVentasCredito.rowCount()):
            item_codigo = self.TablaVentasCredito.item(row, 0)  # Obtener el código de la fila
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
                self.TablaVentasCredito.rowCount()
            )  # Esta es la cantidad de filas actuales en la tabla

            # Insertar una nueva fila en la tabla
            self.TablaVentasCredito.insertRow(rowPosition)

            # Agregar los datos a la nueva fila
            item_codigo = QtWidgets.QTableWidgetItem(codigo)
            item_codigo.setFlags(item_codigo.flags() & ~QtCore.Qt.ItemIsEditable)
            item_codigo.setTextAlignment(QtCore.Qt.AlignCenter)
            self.TablaVentasCredito.setItem(rowPosition, 0, item_codigo)

            item_nombre = QtWidgets.QTableWidgetItem(nombre)
            item_nombre.setFlags(item_nombre.flags() & ~QtCore.Qt.ItemIsEditable)
            item_nombre.setTextAlignment(QtCore.Qt.AlignCenter) 
            self.TablaVentasCredito.setItem(rowPosition, 1, item_nombre)

            item_marca = QtWidgets.QTableWidgetItem(marca)
            item_marca.setFlags(item_marca.flags() & ~QtCore.Qt.ItemIsEditable)
            item_marca.setTextAlignment(QtCore.Qt.AlignCenter)
            self.TablaVentasCredito.setItem(rowPosition, 2, item_marca)

            item_categoria = QtWidgets.QTableWidgetItem(categoria)
            item_categoria.setFlags(item_categoria.flags() & ~QtCore.Qt.ItemIsEditable)
            item_categoria.setTextAlignment(QtCore.Qt.AlignCenter)
            self.TablaVentasCredito.setItem(rowPosition, 3, item_categoria)

            item_cantidad = QtWidgets.QTableWidgetItem(str(cantidad))
            item_cantidad.setFlags(item_cantidad.flags() & ~QtCore.Qt.ItemIsEditable)
            item_cantidad.setTextAlignment(QtCore.Qt.AlignCenter)
            self.TablaVentasCredito.setItem(rowPosition, 4, item_cantidad)

            item_precio = QtWidgets.QTableWidgetItem(str(precio_unitario))
            item_precio.setFlags(item_precio.flags() & ~QtCore.Qt.ItemIsEditable)
            item_precio.setTextAlignment(QtCore.Qt.AlignCenter)
            self.TablaVentasCredito.setItem(rowPosition, 5, item_precio)

            item_total_redondeado = QtWidgets.QTableWidgetItem(str(total_redondeado))
            item_total_redondeado.setFlags(
                item_total_redondeado.flags() & ~QtCore.Qt.ItemIsEditable
            )
            item_total_redondeado.setTextAlignment(QtCore.Qt.AlignCenter)
            self.TablaVentasCredito.setItem(rowPosition, 6, item_total_redondeado)
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
        self.InputPrecioUnitario.clear()
        self.InputDomicilio.clear()
        
    def eliminar_fila(self):
        # Obtener la fila seleccionada
        fila_seleccionada = self.TablaVentasCredito.currentRow()

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
                self.TablaVentasCredito.removeRow(fila_seleccionada)
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
        for row in range(self.TablaVentasCredito.rowCount()):
            total_item = self.TablaVentasCredito.item(
                row, 6
            )  # Columna 6 contiene el total por producto
            if total_item is not None:
                try:
                    subtotal += float(total_item.text())
                except ValueError:
                    continue  # Ignorar valores inválidos
        return subtotal
    def actualizar_total(self):
        #traceback.print_stack()
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
        
        return subtotal
    
    
        
    def cargar_datos(self, row, column):
        try:
            if (
                row >= 0 and row < self.TablaVentasCredito.rowCount()
            ):  # Comprobar que la fila existe
                nombre_item = self.TablaVentasCredito.item(row, 1)
                marca_item = self.TablaVentasCredito.item(row, 2)
                categoria_item = self.TablaVentasCredito.item(row, 3)
                cantidad_item = self.TablaVentasCredito.item(row, 4)
                precio_unitario_item = self.TablaVentasCredito.item(row, 5)

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
            
    def actualizar_datos(self):
        if self.fila_seleccionada is not None:
            try:
                cantidad_str = self.InputCantidad.text().strip()
                precio_unitario_str = self.InputPrecioUnitario.text().strip()
                #domicilio_str = self.InputDomicilio.text().strip()

                if not cantidad_str or not precio_unitario_str:
                    QMessageBox.warning(
                        self,
                        "Error",
                        "Por favor, ingrese valores para cantidad.",
                    )
                    return

                cantidad = int(cantidad_str)
                precio_unitario = float(precio_unitario_str)
                #domicilio = float(domicilio_str)

                # Obtener el código del producto desde la fila seleccionada
                row = self.fila_seleccionada
                if row < self.TablaVentasCredito.rowCount():
                    item_codigo = self.TablaVentasCredito.item(
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

                # Actualizar los datos 
                self.TablaVentasCredito.setItem(row, 4, QTableWidgetItem(str(cantidad)))
                self.TablaVentasCredito.item(row, 4).setTextAlignment(QtCore.Qt.AlignCenter)
                self.TablaVentasCredito.setItem(row, 5, QTableWidgetItem(str(precio_unitario)))
                self.TablaVentasCredito.item(row, 5).setTextAlignment(QtCore.Qt.AlignCenter)
                total = cantidad * precio_unitario
                self.TablaVentasCredito.setItem(row, 6, QTableWidgetItem(str(total)))
                self.TablaVentasCredito.item(row, 6).setTextAlignment(QtCore.Qt.AlignCenter)

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

        rx_precio_unitario = QRegularExpression(
            r"^\d+\.\d+$"
        )   # Expresión para números y puntos
        validator_precio_unitario = QRegularExpressionValidator(rx_precio_unitario)
        self.InputPrecioUnitario.setValidator(validator_precio_unitario)

        rx_cedula = QRegularExpression(r"^\d+$")  # Expresión para solo números
        validator_cedula = QRegularExpressionValidator(rx_cedula)
        self.InputCedula.setValidator(validator_cedula)
        # Nombre (solo letras y espacios)
        rx_nombre = QRegularExpression(
            r"^[a-zA-Z]+$"
        )       
        validator_nombre = QRegularExpressionValidator(rx_nombre)
        self.InputNombreCli.setValidator(validator_nombre)
        
        
        rx_apellido = QRegularExpression(
            r"^[a-zA-Z]+$"
        )
        validator_apellido = QRegularExpressionValidator(rx_apellido)
        self.InputApellidoCli.setValidator(validator_apellido)

        # Teléfono (solo números y guiones)
        rx_telefono = QRegularExpression(
            r"^[0-9]{10}$"
        )  # Expresión para números y guiones
        validator_telefono = QRegularExpressionValidator(rx_telefono)
        self.InputTelefonoCli.setValidator(validator_telefono)
        
        
        
    def verificar_cliente(self):
        cedula = self.InputCedula.text().strip()
        nombre = self.InputNombreCli.text().strip()
        apellido = self.InputApellidoCli.text().strip()
        direccion = self.InputDireccion.text().strip()
        telefono = self.InputTelefonoCli.text().strip()

        # Validación de campos obligatorios
        if not nombre or not apellido or not direccion or not telefono or not cedula:
            QMessageBox.information(self, "Campos obligatorios", "Todos los campos son obligatorios")
            QTimer.singleShot(0, self.InputNombreCli.setFocus)
            
            return
        # Validación de cédula
        if len(cedula) < 6 or len(cedula) > 11 or not cedula.isdigit():
            QMessageBox.warning(self, "Cédula inválida", "La cédula debe tener entre 6 y 11 dígitos.")
            QTimer.singleShot(0, self.InputCedula.setFocus)
            
            return
        # Validación de teléfono
        if len(telefono) != 10 or not telefono.isdigit():
            QMessageBox.warning(self, "Teléfono inválido", "El teléfono debe tener 10 dígitos.")
            QTimer.singleShot(0, self.InputTelefonoCli.setFocus)
            
            return

        # Crear una sesión de base de datos
        db = SessionLocal()  # Asegúrate de que `SessionLocal` está correctamente configurado
        try:
            # Verificar si el cliente ya existe
            cliente_existente = obtener_cliente_por_id(db, cedula)
            if cliente_existente:
                QMessageBox.information(
                    self,
                    "Cliente existente",
                    f"El cliente con cédula {cedula} ya existe. Se utilizarán sus datos."
                )
                print(f"Cliente encontrado: {cliente_existente.Nombre} {cliente_existente.Apellido}")
                clientes_db = db.query(Clientes).all()
                print("Clientes en la base de datos:")
                for cliente in clientes_db:
                    print(f"ID: {cliente.ID_Cliente}, Nombre: {cliente.Nombre}, Apellido: {cliente.Apellido}, Dirección: {cliente.Direccion}, Teléfono: {cliente.Teléfono}")

            else:
                # Crear un nuevo cliente si no existe
                nuevo_cliente = crear_cliente(
                    db=db,
                    id_cliente=cedula,
                    nombre=nombre,
                    apellido=apellido,
                    direccion=direccion,
                    telefono=telefono,
                )
                QMessageBox.information(self, "Cliente creado", "El cliente ha sido creado exitosamente")

                # Opcional: Mostrar todos los clientes en la base de datos
                clientes_db = db.query(Clientes).all()
                print("Clientes en la base de datos:")
                for cliente in clientes_db:
                    print(f"ID: {cliente.ID_Cliente}, Nombre: {cliente.Nombre}, Apellido: {cliente.Apellido}, Dirección: {cliente.Direccion}, Teléfono: {cliente.Teléfono}")

            # Limpiar los campos del formulario
            self.InputCedula.clear()
            self.InputNombreCli.clear()
            self.InputApellidoCli.clear()
            self.InputDireccion.clear()
            self.InputTelefonoCli.clear()
            self.limpiar_campos()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al procesar el cliente: {str(e)}")
            
        finally:
            # Cerrar la sesión para liberar recursos
            db.close()
            
            
            