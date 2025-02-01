# PyQt5 imports
from PyQt5.QtWidgets import QMessageBox, QWidget, QTableWidgetItem
from PyQt5.QtCore import QRegularExpression, QTimer, QUrl
from PyQt5.QtGui import QRegularExpressionValidator
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtGui
from PyQt5.QtCore import Qt




# Relative imports
from ..database.database import SessionLocal
from ..controllers.producto_crud import *
from ..controllers.detalle_factura_crud import *
from ..controllers.facturas_crud import *
from ..controllers.metodo_pago_crud import *
from ..ui import Ui_VentasB
from ..utils.restructura_ticket import generate_ticket
from ..utils.autocomplementado import configurar_autocompletado
from ..controllers.clientes_crud import *

# Standard library imports
import os
import locale
import win32print
import win32ui
import win32con
import datetime  # Asegúrate de importar el módulo 'time'



class VentasB_View(QWidget, Ui_VentasB):
    
    cambiar_a_ventanaA = pyqtSignal()
    
    def __init__(self, parent=None):
        super(VentasB_View, self).__init__(parent)
        self.setupUi(self)
        self.BtnFacturaA.clicked.connect(self.cambiar_a_ventanaA)
        self.BtnFacturaA.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        
        # Configuración inicial
        self.player = QMediaPlayer()
        QTimer.singleShot(0, self.InputCodigo.setFocus)
        
        self.valor_domicilio = 0.0
        self.id_categoria = None
        self.fila_seleccionada = None
        self.invoice_number = None
        self.timer = QTimer(self)  # Timer para evitar consultas excesivas

        # Inicialización y configuración
        self.limpiar_tabla()
        self.configurar_localizacion()
        self.validar_campos()
        self.MetodoPagoBox.addItems(self.metodo_pago())

        # Conexiones de señales - Entradas de texto
        self.db = SessionLocal()
        self.InputCodigo.returnPressed.connect(self.procesar_codigo)
        self.InputCodigo.textChanged.connect(self.iniciar_timer)
        self.InputCantidad.returnPressed.connect(self.actualizar_datos)
        self.InputPrecioMayor.returnPressed.connect(self.actualizar_datos)
        self.InputDomicilio.textChanged.connect(self.actualizar_total)
        self.InputCedula.textChanged.connect(self.validar_campos)
        self.InputCedula.returnPressed.connect(self.completar_campos)
        self.MetodoPagoBox.currentIndexChanged.connect(self.configuracion_pago)
        configurar_autocompletado(self.InputNombre, obtener_productos, "Nombre", self.db, self.procesar_codigo)
        
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
        self.InputCodigo.setPlaceholderText("Ej: 7709991003078")
        self.InputNombre.setPlaceholderText("Ej: Esmalte")
        self.InputDomicilio.setPlaceholderText("Ej: 5000")
        
        # Conexiones de señales - Botones y tabla
        self.BtnEliminar.clicked.connect(self.eliminar_fila)
        self.TablaVentaMayor.cellClicked.connect(self.cargar_datos)
        self.TablaVentaMayor.itemChanged.connect(self.actualizar_total)
        self.BtnGenerarVenta.clicked.connect(self.generar_venta)

        self.usuario_actual_id = None
        # Timer
        self.timer.timeout.connect(self.procesar_codigo_y_agregar)
    
    def showEvent(self, event):
        super().showEvent(event)
        self.InputCodigo.setFocus()
        self.limpiar_tabla()  
        self.limpiar_campos()
        self.InputDomicilio.clear()
        self.limpiar_datos_cliente()
        configurar_autocompletado(self.InputNombre, obtener_productos, "Nombre", self.db, self.procesar_codigo)

    def cargar_información(self, factura_completa):
        factura = factura_completa["Factura"]
        cliente = factura_completa["Cliente"]  # Acceder al primer elemento de la lista
        detalles = factura_completa["Detalles"]

        # Calcular subtotal y descuento
        subtotal = sum(detalle["Subtotal"] for detalle in detalles)
        delivery_fee = factura["Descuento"]

        # Extraer información necesaria para el ticket
        client_name = f"{cliente['Nombre']} {cliente['Apellido']}"
        client_id = cliente["ID_Cliente"]
        client_address = cliente["Direccion"]
        client_phone = cliente["Teléfono"]
        
        total = subtotal - delivery_fee

        # Extraer información adicional de la factura
        payment_method = factura["MetodoPago"]
        self.invoice_number = factura["ID_Factura"]
        
        if payment_method == "Efectivo":
            pago = f"{factura["Monto_efectivo"]}"
        elif payment_method == "Transferencia":
            pago = f"{factura["Monto_TRANSACCION"]}"
        else:
            pago = f"{factura['Monto_efectivo']}/{factura['Monto_TRANSACCION']}" 
            
        self.TablaVentaMayor.setRowCount(len(detalles))
        
        for row, detalles in enumerate(detalles):
            
            id_producto = detalles["ID_Producto"]
            producto = detalles["Producto"]
            marca = detalles["Marca"]
            categoria = detalles["Categoria"]
            cantidad = detalles["Cantidad"]
            precio_unitario = detalles["Precio_Unitario"]
            subtotal_producto = detalles["Subtotal"]
            
            item_id_producto = QtWidgets.QTableWidgetItem(str(id_producto))
            item_id_producto.setFlags(item_id_producto.flags() & ~QtCore.Qt.ItemIsEditable)
            item_id_producto.setTextAlignment(QtCore.Qt.AlignCenter)
            self.TablaVentaMayor.setItem(row, 0, item_id_producto)
            
            item_nombre = QtWidgets.QTableWidgetItem(producto)
            item_nombre.setFlags(item_nombre.flags() & ~QtCore.Qt.ItemIsEditable)
            item_nombre.setTextAlignment(QtCore.Qt.AlignCenter)
            self.TablaVentaMayor.setItem(row, 1, item_nombre)
            
            item_marca = QtWidgets.QTableWidgetItem(marca)
            item_marca.setFlags(item_marca.flags() & ~QtCore.Qt.ItemIsEditable)
            item_marca.setTextAlignment(QtCore.Qt.AlignCenter)
            self.TablaVentaMayor.setItem(row, 2, item_marca)
            
            item_categoria = QtWidgets.QTableWidgetItem(categoria)
            item_categoria.setFlags(item_categoria.flags() & ~QtCore.Qt.ItemIsEditable)
            item_categoria.setTextAlignment(QtCore.Qt.AlignCenter)
            self.TablaVentaMayor.setItem(row, 3, item_categoria)
            
            item_cantidad = QtWidgets.QTableWidgetItem(str(cantidad))
            item_cantidad.setFlags(item_cantidad.flags() & ~QtCore.Qt.ItemIsEditable)
            item_cantidad.setTextAlignment(QtCore.Qt.AlignCenter)
            self.TablaVentaMayor.setItem(row, 4, item_cantidad)
            
            item_precio = QtWidgets.QTableWidgetItem(str(precio_unitario))
            item_precio.setFlags(item_precio.flags() & ~QtCore.Qt.ItemIsEditable)
            item_precio.setTextAlignment(QtCore.Qt.AlignCenter)
            self.TablaVentaMayor.setItem(row, 5, item_precio)
            
            item_subtotal = QtWidgets.QTableWidgetItem(str(subtotal_producto))
            item_subtotal.setFlags(item_subtotal.flags() & ~QtCore.Qt.ItemIsEditable)
            item_subtotal.setTextAlignment(QtCore.Qt.AlignCenter)
            self.TablaVentaMayor.setItem(row, 6, item_subtotal)
            
            
        self.TablaVentaMayor.resizeColumnsToContents()
            
        self.InputCedula.setText(str(client_id))
        self.InputNombreCli.setText(str(client_name))
        self.InputTelefonoCli.setText(str(client_phone))
        self.InputDireccion.setText(str(client_address))
        self.InputPago.setText(str(pago))
        self.LabelSubtotal.setText(f"Subtotal: {subtotal:,.2f}")
        self.LabelTotal.setText(f"Total: {total:,.2f}")
        self.MetodoPagoBox.setCurrentText(payment_method)
    
    def mostrar_mensaje_temporal(self, titulo , mensaje, duracion=2200):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(titulo)
        msg_box.setText(mensaje)
        msg_box.setIcon(QMessageBox.Warning)
        QTimer.singleShot(duracion, msg_box.close)  # Cierra el mensaje después de 'duracion' milisegundos
        msg_box.exec_()
        
    def generar_venta(self):
        if self.TablaVentaMayor.rowCount() == 0:
            QMessageBox.warning(self, "Error", "No hay productos en la venta.")
            self.InputCodigo.setFocus()
            return

        try:
            # Obtener datos del cliente
            client_name = self.InputNombreCli.text().strip()
            client_id = self.InputCedula.text().strip()
            client_address = self.InputDireccion.text().strip()
            client_phone = self.InputTelefonoCli.text().strip()
            monto_pago = self.InputPago.text().strip()
            payment_method = self.MetodoPagoBox.currentText().strip()
            descuento = 0.0
            subtotal = self.LabelSubtotal.text()
            subtotal = float(subtotal.replace(",", ""))
            
            if float(monto_pago) > subtotal:
                QMessageBox.warning(self, "Error", "El monto pagado no puede ser mayor al subtotal.")
                return 

            # Validaciones
            if not client_name:
                QMessageBox.warning(self, "Datos incompletos", "El campo 'Nombre del Cliente' está vacío.")
                self.InputNombreCli.setFocus()
                return
            if not client_id:
                QMessageBox.warning(self, "Datos incompletos", "El campo 'Cédula' está vacío.")
                self.InputCedula.setFocus()
                return
            if not client_address:
                QMessageBox.warning(self, "Datos incompletos", "El campo 'Dirección' está vacío.")
                self.InputDireccion.setFocus()
                return
            if not client_phone:
                QMessageBox.warning(self, "Datos incompletos", "El campo 'Teléfono' está vacío.")
                self.InputTelefonoCli.setFocus()
                return
            if not monto_pago:
                QMessageBox.warning(self, "Datos incompletos", "El campo 'Pago' está vacío.")
                self.InputPago.setFocus()
                return

            self.verificar_cliente(client_id, client_name, client_address, client_phone)

            db = SessionLocal()

            # Obtener los artículos de la tabla
            produc_datos = []
            items = []
            for row in range(self.TablaVentaMayor.rowCount()):
                codigo = self.TablaVentaMayor.item(row, 0).text()
                quantity = int(self.TablaVentaMayor.item(row, 4).text())
                description = self.TablaVentaMayor.item(row, 1).text()
                precio_unitario = float(self.TablaVentaMayor.item(row, 5).text())
                value = float(self.TablaVentaMayor.item(row, 5).text())

                producto = obtener_producto_por_id(db, int(codigo))

                if not producto:
                    QMessageBox.warning(self, "Error", f"Producto con código {codigo} no encontrado.")
                    return

                producto = producto[0]

                # Validar si hay stock suficiente antes de continuar
                if producto.Stock_actual < quantity:
                    QMessageBox.warning(self, "Error", f"Stock insuficiente para el producto: {description}")
                    return

                items.append((quantity, description, value))
                produc_datos.append((codigo, quantity, precio_unitario))

            # Calcular totales
            subtotal = sum(item[2] for item in items)
            delivery_fee = float(self.InputDomicilio.text()) if self.InputDomicilio.text() else 0.0
            total = (subtotal + delivery_fee) - descuento

            if self.invoice_number and self.invoice_number != "":
                self.actualizar_factura(db, self.invoice_number, payment_method, produc_datos, monto_pago, delivery_fee, self.usuario_actual_id)
                mensaje = "Factura actualizada exitosamente."
            else:
                for codigo, quantity, _ in produc_datos:
                    producto = obtener_producto_por_id(db, codigo)
                    producto = producto[0]
                    stock_actual = producto.Stock_actual - quantity
                    actualizar_producto(db, id_producto=int(codigo), stock_actual=stock_actual)

                id_factura = self.guardar_factura(db, client_id, payment_method, produc_datos, monto_pago, descuento, self.usuario_actual_id)
                self.invoice_number = f"0000{id_factura}"
                mensaje = "Factura generada exitosamente."

            # Generar el contenido del ticket
            # Configuración inicial
            max_lines_per_page = 30  # Límite de líneas por página
            current_line = 0  # Contador de líneas
            empresa_nombre = "LadyNailShop"
            empresa_direccion = "Pasto, Colombia"
            empresa_telefono = "+57 316-144-44-74"

            # Obtener la fecha actual
            fecha_actual = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            # Formatear valores monetarios
            subtotal_formateado = f"${subtotal:,.2f}"
            total_formateado = f"${total:,.2f}"

            # Formatear el costo de envío
            delivery_fee = float(delivery_fee)
            if delivery_fee.is_integer():
                delivery_fee_formateado = f"${int(delivery_fee):,.0f}"
            else:
                delivery_fee_formateado = f"${delivery_fee:,.2f}"

            # Limitar la dirección del cliente a 25 caracteres por línea
            direccion = client_address
            direccion_linea1 = direccion[:25]
            direccion_linea2 = direccion[25:] if len(direccion) > 25 else ""

            # Generar el contenido del ticket
            ticket_content = f"""
            Ticket No. {self.invoice_number}
            Cliente: {client_name}
            Cédula: {client_id}
            Teléfono: {client_phone}
            Dirección: {direccion_linea1}
            {direccion_linea2}
            -----------------------------------------------------------------------------------------------------
            Productos:
            """

            # Obtener la impresora predeterminada
            impresora = win32print.GetDefaultPrinter()
            hDC = win32ui.CreateDC()
            hDC.CreatePrinterDC(impresora)

            # Crear un documento de impresión
            hDC.StartDoc("Ticket de Venta")
            hDC.StartPage()

            # Configurar la fuente
            font_size = 26
            line_height = font_size + 10
            font = win32ui.CreateFont({
                "name": "Helvetica-Bold",
                "height": font_size,
                "weight": win32con.FW_BOLD
            })
            hDC.SelectObject(font)

            # Obtener el tamaño del papel para centrar el texto
            printer_width = hDC.GetDeviceCaps(win32con.HORZRES)
            center_x = printer_width // 2  # Punto central

            # Imprimir los datos de la empresa
            hDC.TextOut(center_x - (len(empresa_nombre) * 6), 50, empresa_nombre)
            hDC.TextOut(center_x - (len(empresa_direccion) * 6), 50 + line_height, empresa_direccion)
            hDC.TextOut(center_x - (len(empresa_telefono) * 6), 50 + 2 * line_height, empresa_telefono)

            # Imprimir la fecha actual
            hDC.TextOut(center_x - (len(fecha_actual) * 6), 50 + 3 * line_height, fecha_actual)

            # Línea separadora
            hDC.TextOut(50, 50 + 4 * line_height, "----------------------------------------")
            
            # Ajuste de coordenadas iniciales para el contenido del ticket
            x, y = 2, 2 + 5 * line_height  # Espacio después de la información de la empresa, la línea y la fecha
            # Imprimir la información del cliente
            y += line_height

            hDC.TextOut(x, y, "Ticket de venta")  # Imprime el título "Productos:"
            y += line_height
            hDC.TextOut(x, y, f"Ticket No. {self.invoice_number}")# Aquí se agrega el número de factura
            y += line_height
            hDC.TextOut(x, y, f"Cliente: {client_name}")
            y += line_height
            hDC.TextOut(x, y, f"Cédula: {client_id}")
            y += line_height
            hDC.TextOut(x, y, f"Teléfono: {client_phone}")
            y += line_height
            hDC.TextOut(x, y, f"Dirección: {direccion_linea1}")
            y += line_height
            if direccion_linea2:  # Si hay una segunda línea de dirección, imprimirla
                hDC.TextOut(x, y, direccion_linea2)
                y += line_height

            # 🔹 Imprimir "Productos:" y la línea separadora
            
            hDC.TextOut(x, y, "-----------------------------------------------------------------------------------------------------------------")  # Imprime la línea separadora
            y += line_height  # Mueve la posición para empezar a imprimir los productos
            # Imprimir los productos
            hDC.TextOut(x, y, "Productos:")  # Imprime el título "Productos:"
            y += line_height  # Mueve la posición de la siguiente línea hacia abajo

            for item in items:
                producto_linea = f"{item[0]} x {item[1]} - {item[2]}"
                hDC.TextOut(x, y, producto_linea)
                y += line_height
                current_line += 1

                # Si se alcanza el límite de líneas, crear una nueva página
                if current_line >= max_lines_per_page:
                    hDC.EndPage()  # Finalizar la página actual
                    hDC.StartPage()  # Iniciar una nueva página
                    y = 2  # Reiniciar la posición Y
                    current_line = 0  # Reiniciar el contador de líneas

            # Imprimir los totales y el mensaje final
            totales = f"""
            -----------------------------------------------------------------------------------------------------
            Subtotal: {subtotal_formateado}
            Envío: {delivery_fee_formateado}
            Total: {total_formateado}
            Método de Pago: {payment_method}
            -----------------------------------------------------------------------------------------------------
            ¡Gracias por tu compra!
            """
            for line in totales.split("\n"):
                hDC.TextOut(x, y, line.strip())
                y += line_height

            # Finalizar la impresión
            hDC.EndPage()
            hDC.EndDoc()
            hDC.DeleteDC()

            # Cerrar la base de datos y mostrar mensaje de éxito
            db.close()
            QMessageBox.information(self, "Éxito", mensaje)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al generar la factura: {str(e)}")
            print(e)

        self.limpiar_tabla()
        self.limpiar_campos()
        self.InputDomicilio.clear()
        self.limpiar_datos_cliente()
        self.invoice_number = None

    def actualizar_factura(self, db, id_factura, payment_method, produc_datos, monto_pago, delivery_fee, usuario_actual_id):
        # Obtener los detalles actuales de la factura
        detalles_actuales = db.query(DetalleFacturas).filter(DetalleFacturas.ID_Factura == id_factura).all()

        # Convertir los detalles actuales en un diccionario para comparar
        productos_actuales = {detalle.ID_Producto: detalle.Cantidad for detalle in detalles_actuales}

        # Productos enviados desde la interfaz (nuevos o editados)
        productos_nuevos = {int(codigo): cantidad for codigo, cantidad, _ in produc_datos}

        # Productos eliminados (presentes en la factura actual, pero no en la nueva lista)
        productos_eliminados = set(productos_actuales.keys()) - set(productos_nuevos.keys())

        # Restaurar stock de productos eliminados
        for id_producto in productos_eliminados:
            cantidad_vendida = productos_actuales[id_producto]
            producto = db.query(Productos).filter(Productos.ID_Producto == id_producto).first()
            producto.Stock_actual += cantidad_vendida  # Restaurar el stock
            db.delete(db.query(DetalleFacturas).filter(
                DetalleFacturas.ID_Factura == id_factura,
                DetalleFacturas.ID_Producto == id_producto
            ).first())  # Eliminar el detalle de la factura

        # Actualizar cantidades de productos existentes y agregar nuevos
        for id_producto, nueva_cantidad in productos_nuevos.items():
            if id_producto in productos_actuales:
                # Producto ya existe, verificar cambios en la cantidad
                detalle = db.query(DetalleFacturas).filter(
                    DetalleFacturas.ID_Factura == id_factura,
                    DetalleFacturas.ID_Producto == id_producto
                ).first()

                diferencia_cantidad = nueva_cantidad - productos_actuales[id_producto]
                detalle.Cantidad = nueva_cantidad
                detalle.Subtotal = nueva_cantidad * detalle.Precio_unitario

                # Ajustar el stock del producto
                producto = db.query(Productos).filter(Productos.ID_Producto == id_producto).first()
                producto.Stock_actual -= diferencia_cantidad
            else:
                # Producto nuevo, agregarlo a la factura y ajustar el stock
                precio_unitario = db.query(Productos).filter(Productos.ID_Producto == id_producto).first().Precio_venta_normal
                subtotal = nueva_cantidad * precio_unitario

                nuevo_detalle = DetalleFacturas(
                    ID_Factura=id_factura,
                    ID_Producto=id_producto,
                    Cantidad=nueva_cantidad,
                    Precio_unitario=precio_unitario,
                    Subtotal=subtotal,
                )
                db.add(nuevo_detalle)

                # Ajustar el stock
                producto = db.query(Productos).filter(Productos.ID_Producto == id_producto).first()
                producto.Stock_actual -= nueva_cantidad
                
        id_metodo_pago = obtener_metodo_pago_por_nombre(db, payment_method)
                
        if '/' in monto_pago:
            total = monto_pago.split("/") 
            efectivo = float(total[0])
            tranferencia = float(total[1])
        else:
            efectivo = float(monto_pago)
            tranferencia = float(monto_pago)
    
        # Actualizar información general de la factura
        factura = db.query(Facturas).filter(Facturas.ID_Factura == id_factura).first()
        factura.Monto_TRANSACCION = tranferencia if payment_method == "Transferencia" or payment_method == "Mixto" else 0.0
        factura.Monto_efectivo = efectivo if payment_method == "Efectivo" or payment_method == "Mixto" else 0.0
        factura.ID_Metodo_Pago = id_metodo_pago.ID_Metodo_Pago
        factura.ID_Usuario = usuario_actual_id

        # Confirmar los cambios
        db.commit()
    
    def verificar_cliente(self, cedula, nombre_completo , direccion, telefono): 

        # Crear una sesión de base de datos 
        db = SessionLocal()  # Asegúrate de que SessionLocal está correctamente configurado 
        try: 
            # Verificar si el cliente ya existe 
            cliente_existente = obtener_cliente_por_id(db, cedula) 
            if not cliente_existente:  
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
        
    def guardar_factura(self, db, client_id, payment_method, items, monto_pago, descuento, id_usuario):
    
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
                descuento=descuento,
                estado=estado,
                id_metodo_pago=id_metodo_pago.ID_Metodo_Pago,
                id_tipo_factura=2,
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
                    id_producto=codigo,
                    id_factura=id_factura
                )

            # Confirmar cambios en la base de datos
            db.commit()
            print("Factura guardada exitosamente.")
            
            return id_factura

        except Exception as e:
            db.rollback()
            print(f"Error al guardar la factura: {e}")
            raise
          
    def limpiar_datos_cliente(self):
        self.InputPago.clear()
        self.InputCedula.clear() 
        self.InputNombreCli.clear() 
        self.InputTelefonoCli.clear()
        self.InputDireccion.clear()    
        self.InputPago.clear()
        self.LabelTotal.setText("$")
        self.LabelSubtotal.setText("$")
        
    def reproducir_sonido(self):
        sonido_path = "./assets/sound_scanner.wav"
        if os.path.exists(sonido_path):
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(sonido_path)))
            self.player.play()
        else:
            print("No se encontró el archivo de sonido")
    
    def keyPressEvent(self, event):
         
        if event.key() == Qt.Key_Up:
            
            self.navegar_widgets()
            
        elif event.key() == Qt.Key_Down:
            self.navegar_widgets_atras()
        # Llamar al método original para procesar otros eventos
        super().keyPressEvent(event)

    def navegar_widgets(self):
        if self.focusWidget() == self.InputCodigo:
            self.InputNombre.setFocus()
        elif self.focusWidget() == self.InputNombre:
            self.InputDomicilio.setFocus()
        elif self.focusWidget() == self.InputDomicilio:
            self.InputCedula.setFocus()
        elif self.focusWidget() == self.InputCedula:
            self.InputNombreCli.setFocus()
        elif self.focusWidget() == self.InputNombreCli:
            self.InputTelefonoCli.setFocus()
        elif self.focusWidget() == self.InputTelefonoCli:
            self.InputDireccion.setFocus()
        elif self.focusWidget() == self.InputDireccion:
            self.InputCodigo.setFocus()  # Volver al inicio

    def navegar_widgets_atras(self):
        if self.focusWidget() == self.InputCodigo:
            self.InputDireccion.setFocus()
        elif self.focusWidget() == self.InputDireccion:
            self.InputTelefonoCli.setFocus()
        elif self.focusWidget() == self.InputTelefonoCli:
            self.InputNombreCli.setFocus()
        elif self.focusWidget() == self.InputNombreCli:
            self.InputCedula.setFocus()
        elif self.focusWidget() == self.InputCedula:
            self.InputDomicilio.setFocus()
        elif self.focusWidget() == self.InputDomicilio:
            self.InputNombre.setFocus()
        elif self.focusWidget() == self.InputNombre:
            self.InputCodigo.setFocus()  # Volv
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
                    self.InputPrecioMayor.setText(str(producto.Precio_venta_mayor))
                    self.InputPrecioMayor.setEnabled(False)
                    self.id_categoria = producto.categorias
                    self.InputCantidad.clear()  # Limpiar cantidad
                else:
                    self.mostrar_mensaje_temporal(
                        "Producto no encontrado",
                        "No existe un producto asociado a este código.",
                    )
                    self.limpiar_campos()
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
                    self.InputPrecioMayor.setText(str(producto.Precio_venta_mayor))
                    self.InputPrecioMayor.setEnabled(False)
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
                self.agregar_producto(mostrar_mensaje=False)
                self.InputCodigo.clear()
                self.InputCodigo.setFocus()
                
    def agregar_producto(self, mostrar_mensaje=True):
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
            if mostrar_mensaje:
                QMessageBox.warning(self, "Error", "Por favor, ingrese valores numéricos válidos para la cantidad y el precio.")
            return
        # Verificar si el código del producto ya existe en la tabla
        for row in range(self.TablaVentaMayor.rowCount()):
            item_codigo = self.TablaVentaMayor.item(row, 0)  # Obtener el código de la fila
            if item_codigo and item_codigo.text() == codigo:  # Si el código ya existe
                self.mostrar_mensaje_temporal( "Error", "Este código de producto ya existe.")
                self.limpiar_campos()
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
                self.mostrar_mensaje_temporal(
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

        self.LabelSubtotal.setText(f"{subtotal_formateado}")

        domicilio = self.obtener_valor_domicilio()  # Obtener el valor del domicilio

        total = subtotal + domicilio

        if total.is_integer():
            total_formateado = f"{total:,.0f}"
        else:
            total_formateado = f"{total:,.2f}"

        self.LabelTotal.setText(f"{total_formateado}")
        
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
                    self.InputCantidad.setFocus()
                    

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

        # Obtener cliente
        id_cliente = int(self.InputCedula.text().strip())
        self.db = SessionLocal()
        
        try:
            cliente = obtener_cliente_por_id(self.db, id_cliente)
            if cliente:
                self.InputNombreCli.setText(f"{cliente.Nombre} {cliente.Apellido}")
                self.InputTelefonoCli.setText(cliente.Teléfono)
                self.InputDireccion.setText(cliente.Direccion)
            else:
                QMessageBox.warning(self, "Error", f"Cliente con cédula {id_cliente} no encontrado.")
        except Exception as e:
            print(f"Error al obtener cliente: {e}")
        finally:
            self.db.close()
            
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
         
