# PyQt5 imports
from PyQt5.QtWidgets import QMessageBox, QWidget, QTableWidgetItem
from PyQt5.QtCore import QRegularExpression, QTimer, QUrl
from PyQt5.QtGui import QRegularExpressionValidator
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal



# Relative imports
from ..database.database import SessionLocal
from ..controllers.producto_crud import *
from ..controllers.detalle_factura_crud import *
from ..controllers.facturas_crud import *
from ..controllers.metodo_pago_crud import *
from ..controllers.facturas_crud import crear_factura
from ..controllers.detalle_factura_crud import crear_detalle_factura
from ..controllers.metodo_pago_crud import obtener_metodo_pago_por_nombre
from ..controllers.clientes_crud import *
from ..ui import Ui_VentasA
from ..utils.restructura_ticket import generate_ticket
from ..utils.autocomplementado import configurar_autocompletado

# Standard library imports
import os
import locale

class VentasA_View(QWidget, Ui_VentasA):
    cambiar_a_ventanab = pyqtSignal()
    
    def __init__(self, parent=None):
        super(VentasA_View, self).__init__(parent)
        self.setupUi(self)
        
        # Configuración inicial
        QTimer.singleShot(0, self.InputCodigo.setFocus)
        self.player = QMediaPlayer()
        self.InputCodigo.setFocus()
        self.id_categoria = None
        self.valor_domicilio = 0.0
        self.fila_seleccionada = None
        self.aplicando_descuento = False  # Inicializar la bandera
        self.timer = QTimer(self)  # Timer para evitar consultas excesivas
        
        #placeholder
        self.InputPago.setPlaceholderText("$")
        self.InputCedula.setPlaceholderText("Ej: 10004194608")
        self.InputNombreCli.setPlaceholderText("Ej: Pepito Perez")
        self.InputTelefonoCli.setPlaceholderText("Ej: 3170065430")
        self.InputDireccion.setPlaceholderText("Ej: Calle 1, 123 - Piso 1")
        self.BtnFacturaA.setStyleSheet("""
            QPushButton {
                background-color: red; 
            }
        """)
        # Inicialización y configuración
        self.limpiar_tabla()
        self.configurar_localizacion()
        self.validar_campos()
        self.MetodoPagoBox.addItems(self.metodo_pago())

        # Conexiones de señales - Entradas de texto
        self.db = SessionLocal()
        self.InputCodigo.returnPressed.connect(self.procesar_codigo)
        self.InputCodigo.textChanged.connect(self.iniciar_timer)
        self.InputDomicilio.returnPressed.connect(self.actualizar_datos)
        self.InputCantidad.returnPressed.connect(self.actualizar_datos)
        self.InputPrecioUnitario.returnPressed.connect(self.actualizar_datos)
        self.InputDomicilio.editingFinished.connect(self.actualizar_total)
        self.InputDomicilio.textChanged.connect(self.calcular_subtotal)
        self.InputCedula.textChanged.connect(self.validar_campos)
        self.InputCedula.returnPressed.connect(self.completar_campos)
        self.InputDescuento.textChanged.connect(self.aplicar_descuento)
        self.MetodoPagoBox.currentIndexChanged.connect(self.configuracion_pago)
        self.BtnFacturaB.clicked.connect(self.cambiar_a_ventanab)
        self.BtnGenerarVenta.clicked.connect(self.generar_venta)
        configurar_autocompletado(self.InputNombre, obtener_productos, "Nombre", self.db, self.procesar_codigo)

        # Conexiones de señales - Botones y tabla
        self.BtnEliminar.clicked.connect(self.eliminar_fila)
        self.tableWidget.cellClicked.connect(self.cargar_datos)
        self.tableWidget.itemChanged.connect(self.actualizar_total)
        
        self.usuario_actual_id = None
        # Timer
        self.timer.timeout.connect(self.procesar_codigo_y_agregar)
        
    def generar_venta(self):
        
        if self.tableWidget.rowCount() == 0:
            QMessageBox.warning(self, "Error", "No hay productos en la venta.")
            return
    
        try:
            # Obtener datos del cliente
            client_name = self.InputNombreCli.text().strip()
            client_id = self.InputCedula.text().strip()
            client_address = self.InputDireccion.text().strip()
            client_phone = self.InputTelefonoCli.text().strip()
            monto_pago = self.InputPago.text().strip()
            payment_method = self.MetodoPagoBox.currentText().strip()
            
            # Verificar que los datos básicos estén completos
            if not client_name or not client_id or not client_address or not client_phone:
                QMessageBox.warning(self, "Datos incompletos", "Por favor, completa los datos del cliente.")
                return
            
            self.verificar_cliente(client_id, client_name, client_address, client_phone)

            db = SessionLocal()
            
            # Obtener los artículos de la tabla
            produc_datos = []
            items = []
            for row in range(self.tableWidget.rowCount()):
                codigo = self.tableWidget.item(row, 0).text()
                quantity = int(self.tableWidget.item(row, 4).text())
                description = self.tableWidget.item(row, 1).text()
                value = float(self.tableWidget.item(row, 6).text())
                
                producto = obtener_producto_por_id(db, int(codigo))
                
                if not producto:
                    QMessageBox.warning(self, "Error", f"Producto con código {codigo} no encontrado.")
                    return
                producto = producto[0]
                
                stock_actual = producto.Stock_actual - quantity
                
                actualizar_producto(db, id_producto=int(codigo), stock_actual=stock_actual)
                items.append((quantity, description, value))
                produc_datos.append((codigo, quantity, value))

            # Calcular totales
            subtotal = sum(item[2] for item in items)
            delivery_fee = float(self.InputDomicilio.text()) if self.InputDomicilio.text() else 0.0
            total = subtotal + delivery_fee
            
            pago = float(self.InputPago.text().strip()) if payment_method == "Efectivo" else 0.0

            self.guardar_factura(db, client_id, payment_method, produc_datos, monto_pago, delivery_fee, self.usuario_actual_id)
            
            # Datos adicionales
            invoice_number = f"001"
            pan = "123456789"  # Cambiar por el PAN de tu empresa
            filename = ""  # El usuario seleccionará el nombre y ruta

            # Llamar a la función para generar el ticket
            generate_ticket(
                client_name=client_name,
                client_id=client_id,
                client_address=client_address,
                client_phone=client_phone,
                items=items,
                subtotal=subtotal,
                delivery_fee=delivery_fee,
                total=total,
                payment_method=payment_method,
                invoice_number=invoice_number,
                pan=pan,
                pago = pago,
                filename=filename,
            )
            db.close()

            QMessageBox.information(self, "Éxito", "Factura generada exitosamente.")
            self.limpiar_campos()  # Opcional: limpiar campos después de generar la venta

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al generar la factura: {str(e)}")
            
        self.limpiar_tabla()
        self.limpiar_campos()
        self.limpiar_datos_cliente()
          
    def verificar_cliente(self, cedula, nombre_completo , direccion, telefono): 

        # Crear una sesión de base de datos 
        db = SessionLocal()  # Asegúrate de que SessionLocal está correctamente configurado 
        try: 
            # Verificar si el cliente ya existe 
            cliente_existente = obtener_cliente_por_id(db, cedula) 
            if cliente_existente: 
                QMessageBox.information( 
                    self, 
                    "Cliente existente", 
                    f"El cliente con cédula {cedula} ya existe. Se utilizarán sus datos." 
                ) 
            else: 
                try:
                    nombres = nombre_completo.split(" ")
                    nombre = nombres[0]
                    apellido = nombres[1]
                except Exception as e:
                    print(f"Error al procesar el nombre del cliente: {e}")
                    return
                # Crear un nuevo cliente si no existe 
                nuevo_cliente = crear_cliente( 
                    db=db, 
                    id_cliente=cedula, 
                    nombre=nombre, 
                    apellido=apellido, 
                    direccion=direccion, 
                    telefono=telefono, 
                ) 
                if nuevo_cliente:
                    QMessageBox.information(self, "Cliente creado", "El cliente ha sido creado exitosamente") 
 
        except Exception as e: 
            QMessageBox.critical(self, "Error", f"Error al procesar el cliente: {str(e)}") 
        finally: 
            # Cerrar la sesión para liberar recursos 
            db.close()    
        
    def guardar_factura(self, db, client_id, payment_method, items, monto_pago, delivery_fee, id_usuario):
    
        """
        Registra la factura y sus detalles en la base de datos.
        """
        try:
            
            id_metodo_pago = obtener_metodo_pago_por_nombre(db, payment_method)
            if not id_metodo_pago:
                QMessageBox.warning(self, "Error", f"Método de pago {payment_method} no encontrado.")
                return False
            
            if self.valor_domicilio == 0.0:
                estado = True
            else: 
                estado = False
            
            if '/' in monto_pago:
                total = monto_pago.split("/") 
                efectivo = float(total[0])
                tranferencia = float(total[1])
            else:
                efectivo = float(monto_pago)
                tranferencia = float(monto_pago)
            
            # Crear registro en la tabla 'facturas'
            factura = crear_factura(
                db=db,
                monto_efectivo= efectivo if payment_method != "Transferencia" else 0.0,
                monto_transaccion= tranferencia if payment_method != "Efectivo" else 0.0,
                estado=estado,
                id_metodo_pago=id_metodo_pago.ID_Metodo_Pago,
                id_tipo_factura=1,
                id_cliente=client_id,
                id_usuario=id_usuario,
            )
            
            # Obtener el ID de la factura recién creada
            id_factura = factura.ID_Factura

            # Crear registros en la tabla 'detalle_factura' para cada producto
            for item in items:
                codigo, quantity, value = item
                
                total = quantity * value

                # Crear detalle de factura
                crear_detalle_factura(
                    db=db,
                    cantidad=quantity,
                    precio_unitario=value,
                    subtotal=total,
                    descuento=delivery_fee,
                    id_producto=codigo,
                    id_factura=id_factura
                )

            # Confirmar cambios en la base de datos
            db.commit()
            print("Factura guardada exitosamente.")

        except Exception as e:
            db.rollback()
            print(f"Error al guardar la factura: {e}")
            raise
        
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
        # Obtener los valores de los inputs
        codigo = self.InputCodigo.text().strip()
        nombre = self.InputNombre.text().strip()

        # Conexión a la base de datos
        db = SessionLocal()

        try:
            # Caso 1: Si se proporciona el código
            if codigo:
                if not codigo.isdigit():
                    QMessageBox.warning(self, "Error", "El código debe ser un número válido.")
                    return

                # Convertir el código a entero
                codigo = int(codigo)

                # Buscar producto por código
                productos = obtener_producto_por_id(db, codigo)

                if productos:
                    producto = productos[0]
                    # Actualizar los campos con los datos del producto
                    self.InputCodigo.setText(str(producto.ID_Producto))
                    self.InputNombre.setText(producto.Nombre)
                    self.InputMarca.setText(str(producto.marcas))
                    self.InputMarca.setEnabled(False)
                    self.InputPrecioUnitario.setText(str(producto.Precio_venta_normal))
                    self.InputPrecioUnitario.setEnabled(False)
                    self.id_categoria = producto.categorias
                    self.InputCantidad.clear()  # Limpiar cantidad
                else:
                    QMessageBox.warning(
                        self,
                        "Producto no encontrado",
                        "No existe un producto asociado a este código.",
                    )
                return  # Terminar el procesamiento si el código fue encontrado

            # Caso 2: Si no se proporciona el código pero sí el nombre
            elif nombre:
                # Buscar producto por nombre
                productos_nom = buscar_productos(db, nombre)

                if productos_nom:
                    producto = productos_nom[0]
                    # Actualizar los campos con los datos del producto
                    self.InputCodigo.setText(str(producto.ID_Producto))
                    self.InputNombre.setText(producto.Nombre)
                    self.InputMarca.setText(str(producto.marcas))
                    self.InputMarca.setEnabled(False)
                    self.InputPrecioUnitario.setText(str(producto.Precio_venta_normal))
                    self.InputPrecioUnitario.setEnabled(False)
                    self.id_categoria = producto.categorias
                    self.InputCantidad.clear()  # Limpiar cantidad
                else:
                    QMessageBox.warning(
                        self,
                        "Producto no encontrado",
                        "No existe un producto asociado a este nombre.",
                    )
                return  # Terminar el procesamiento si el nombre fue encontrado

            # Caso 3: Si no se proporciona ni código ni nombre
            else:
                QMessageBox.warning(
                    self,
                    "Error",
                    "Por favor, ingrese un código o un nombre para buscar el producto.",
                )

        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"Error al buscar el producto: {str(e)}"
            )

        finally:
            # Asegurarse de cerrar la sesión de la base de datos
            db.close()

    def limpiar_tabla(self):

        self.tableWidget.setRowCount(
            0
        )  # Solo elimina las filas, pero mantiene las columnas

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
                    self.limpiar_campos()
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
            item_total_redondeado.setFlags(
                item_total_redondeado.flags() & ~QtCore.Qt.ItemIsEditable
            )
            item_total_redondeado.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(rowPosition, 6, item_total_redondeado)
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
                "¿Estás seguro de que deseas eliminar este producto?",
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
            
    def aplicar_descuento(self):
        try:
            # Obtener el valor del descuento desde el campo de texto
            descuento_str = self.InputDescuento.text().strip()

            # Si el campo está vacío, asignar 0 al descuento (sin necesidad de actualizar visualmente a 0)
            if descuento_str == "":
                descuento = 0
            else:
                descuento = float(descuento_str)
                if descuento < 0:  # Validar que el descuento no sea negativo
                    raise ValueError("El descuento no puede ser negativo.")
        
        except ValueError:
            # Si hay un error al convertir el descuento (ej. no es un número válido)
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

        # Aplicar el descuento
        nuevo_subtotal = subtotal_antes_descuento - descuento

        # Obtener el valor del domicilio
        domicilio = self.obtener_valor_domicilio()
        print (domicilio)

        # Calcular el total final considerando el domicilio
        total = nuevo_subtotal + domicilio

        # Formatear el subtotal y total con 2 decimales si es necesario
        if nuevo_subtotal.is_integer():
            subtotal_formateado = f"{nuevo_subtotal:,.0f}"
        else:
            subtotal_formateado = f"{nuevo_subtotal:,.2f}"

        if total.is_integer():
            total_formateado = f"{total:,.0f}"
        else:
            total_formateado = f"{total:,.2f}"

        # Actualizar los labels de la interfaz en tiempo real
        self.LabelSubtotal.setText(f"Subtotal: {subtotal_formateado}")
        self.LabelTotal.setText(f"Total: {total_formateado}")
        
    def cargar_datos(self, row, column):
        try:
            if (
                row >= 0 and row < self.tableWidget.rowCount()
            ):  # Comprobar que la fila existe
                # codigo_item = self.tableWidget.item(row, 0)
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
                if row < self.tableWidget.rowCount():
                    item_codigo = self.tableWidget.item(
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
                self.tableWidget.setItem(row, 4, QTableWidgetItem(str(cantidad)))
                self.tableWidget.item(row, 4).setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableWidget.setItem(row, 5, QTableWidgetItem(str(precio_unitario)))
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
        rx_descuento = QRegularExpression(r"^\d+$")  # Permite numeros enteros
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
            self.InputPago.setPlaceholderText("$Efectivo / $Transferencia")
            
            # Expresión regular para permitir el formato 50000 / 30000 (con espacio antes y después de la barra)
            rx_inpago = QRegularExpression(r"^\d+(\.\d{1,2})?\s*/\s*\d+(\.\d{1,2})?$")  # Formato: 50000.00 / 30000.00
            validator_inpago = QRegularExpressionValidator(rx_inpago)
            self.InputPago.setValidator(validator_inpago)
        else:
            # Si no es Efectivo, Transferencia ni Mixto, mostramos solo el símbolo $
            self.InputPago.setText("$")
            
    def limpiar_datos_cliente(self):
        self.InputPago.clear()
        self.InputCedula.clear() 
        self.InputNombreCli.clear() 
        self.InputTelefonoCli.clear()
        self.InputDireccion.clear()    
        self.InputDescuento.clear()
        self.InputPago.clear()
        self.LabelTotal.setText("$")
        self.LabelSubtotal.setText("$")
         
    