# PyQt5 imports
from PyQt5.QtWidgets import QMessageBox, QWidget, QTableWidgetItem
from PyQt5.QtCore import QRegularExpression, QTimer, QUrl
from PyQt5.QtGui import QRegularExpressionValidator
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from decimal import Decimal  # Importar Decimal para manejar números con precisión
from PyQt5 import QtCore, QtWidgets
from datetime import datetime, timedelta


# Relative imports
from ..database.database import SessionLocal
from ..controllers.producto_crud import *
from ..controllers.detalle_factura_crud import *
from ..controllers.clientes_crud import *
from ..controllers.facturas_crud import *
from ..controllers.metodo_pago_crud import *
from ..controllers.venta_credito_crud import *
from ..ui import Ui_VentasCredito
from ..utils.autocomplementado import configurar_autocompletado
from ..utils.restructura_ticket import *

# Standard library imports
import os
from PyQt5.QtCore import Qt
import locale


class VentasCredito_View(QWidget, Ui_VentasCredito):
    def __init__(self, parent=None):
        super(VentasCredito_View, self).__init__(parent)
        self.setupUi(self)
        # configuración inicial
        self.usuario_actual_id = None
        self.productos = []  # Lista de productos para calcular el subtotal
        self.player = QMediaPlayer()
        QTimer.singleShot(0, self.InputCodigo.setFocus)
        self.id_categoria = None
        self.valor_domicilio = 0.0
        self.invoice_number = None
        self.id_venta_credito = None
        self.fila_seleccionada = None
        self.timer = QTimer(self)  # Timer para evitar consultas excesivas

        # placeholder
        self.InputCedula.setPlaceholderText("Ej: 10004194608")
        self.InputNombreCli.setPlaceholderText("Ej: Pepito")
        self.InputApellidoCli.setPlaceholderText("Ej: Perez")
        self.InputTelefonoCli.setPlaceholderText("Ej: 3170065430")
        self.InputDireccion.setPlaceholderText("Ej: Calle 1, 123 - Piso 1")
        self.LimitePagoBox.addItems(["7 días", "15 días"])
        self.comboBoxPrecio.addItems(["PU", "PAM"])
        self.InputCodigo.setPlaceholderText("Ej: 7709991003078")
        self.InputNombre.setPlaceholderText("Ej: Esmalte")
        self.InputDomicilio.setPlaceholderText("Ej: 5000")

        # Inicialización y configuración
        self.limpiar_tabla()
        self.configurar_localizacion()
        self.validar_campos()

        # Conexiones de señales - Entradas de texto
        self.db = SessionLocal()
        self.InputCodigo.returnPressed.connect(self.procesar_codigo)
        self.InputCodigo.textChanged.connect(self.iniciar_timer)
        self.InputDomicilio.returnPressed.connect(self.actualizar_datos)
        self.InputCantidad.returnPressed.connect(self.actualizar_datos)
        self.InputPrecioUnitario.returnPressed.connect(self.actualizar_datos)
        self.InputCedula.returnPressed.connect(self.completar_campos)
        self.InputDomicilio.textChanged.connect(self.actualizar_total)
        self.InputCedula.textChanged.connect(self.validar_campos)
        self.comboBoxPrecio.currentIndexChanged.connect(self.cambiar_precio)
        configurar_autocompletado(
            self.InputNombre, obtener_productos, "Nombre", self.db, self.procesar_codigo
        )

        # Conexiones de señales - Botones y tabla
        self.BtnEliminar.clicked.connect(self.eliminar_fila)
        self.BtnGenerarVentaCredito.clicked.connect(self.generar_venta)
        self.TablaVentasCredito.cellClicked.connect(self.cargar_datos)
        self.TablaVentasCredito.itemChanged.connect(self.actualizar_total)

        self.timer.timeout.connect(self.procesar_codigo_y_agregar)

    def cargar_información(self, factura_completa, id_venta_credito=None):

        self.id_venta_credito = id_venta_credito

        factura = factura_completa["Factura"]
        cliente = factura_completa["Cliente"]
        detalles = factura_completa["Detalles"]

        # Calcular subtotal y descuento
        subtotal = sum(detalle["Subtotal"] for detalle in detalles)

        # Extraer información necesaria para el ticket
        client_name = cliente["Nombre"]
        client_apellido = cliente["Apellido"]
        client_id = cliente["ID_Cliente"]
        client_address = cliente["Direccion"]
        client_phone = cliente["Teléfono"]

        total = subtotal

        self.invoice_number = factura["ID_Factura"]

        try:
            self.TablaVentasCredito.setRowCount(len(detalles))
            # Iterar sobre las filas
            for row_idx, row in enumerate(detalles):
                # Datos de la fila
                id_producto = str(row["ID_Producto"])
                producto = str(row["Producto"])
                marca = str(row["Marca"])
                categoria = str(row["Categoria"])
                cantidad = str(row["Cantidad"])
                precio_unitario = str(row["Precio_Unitario"])
                subtotal_producto = str(row["Subtotal"])

                # Configurar items de la tabla
                items = [
                    (id_producto, 0),
                    (producto, 1),
                    (marca, 2),
                    (categoria, 3),
                    (cantidad, 4),
                    (precio_unitario, 5),
                    (subtotal_producto, 6),
                ]

                # Añadir items a la tabla
                for value, col_idx in items:
                    item = QtWidgets.QTableWidgetItem(value)
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.TablaVentasCredito.setItem(row_idx, col_idx, item)

            self.TablaVentasCredito.resizeColumnsToContents()

        except Exception as e:
            print(f"Error al cargar datos en la tablaVentasCredito: {e}")

        self.InputCedula.setText(str(client_id))
        self.InputNombreCli.setText(str(client_name))
        self.InputApellidoCli.setText(str(client_apellido))
        self.InputTelefonoCli.setText(str(client_phone))
        self.InputDireccion.setText(str(client_address))
        self.LabelSubtotal.setText(f"Subtotal: {subtotal:,.2f}")
        self.LabelTotal.setText(f"Total: {total:,.2f}")

    def actualizar_factura(
        self,
        db,
        id_factura,
        produc_datos,
        usuario_actual_id,
        deuda,
        limite_pago,
    ):
        
        venta_credito = obtener_ventaCredito_id(db, self.id_venta_credito)
        venta = venta_credito[0]
        
        pagado = venta.Total_Deuda - venta.Saldo_Pendiente 
        # Obtener los detalles actuales de la factura
        detalles_actuales = (
            db.query(DetalleFacturas)
            .filter(DetalleFacturas.ID_Factura == id_factura)
            .all()
        )

        # Convertir los detalles actuales en un diccionario para comparar
        productos_actuales = {
            detalle.ID_Producto: detalle.Cantidad for detalle in detalles_actuales
        }

        # Productos enviados desde la interfaz (nuevos o editados)
        productos_nuevos = {
            int(codigo): cantidad for codigo, cantidad, _ in produc_datos
        }

        # Productos eliminados (presentes en la factura actual, pero no en la nueva lista)
        productos_eliminados = set(productos_actuales.keys()) - set(
            productos_nuevos.keys()
        )

        # Restaurar stock de productos eliminados
        for id_producto in productos_eliminados:
            cantidad_vendida = productos_actuales[id_producto]
            producto = (
                db.query(Productos).filter(Productos.ID_Producto == id_producto).first()
            )
            producto.Stock_actual += cantidad_vendida  # Restaurar el stock
            db.delete(
                db.query(DetalleFacturas)
                .filter(
                    DetalleFacturas.ID_Factura == id_factura,
                    DetalleFacturas.ID_Producto == id_producto,
                )
                .first()
            )  # Eliminar el detalle de la factura

        # Actualizar cantidades de productos existentes y agregar nuevos
        for id_producto, nueva_cantidad in productos_nuevos.items():
            if id_producto in productos_actuales:
                # Producto ya existe, verificar cambios en la cantidad
                detalle = (
                    db.query(DetalleFacturas)
                    .filter(
                        DetalleFacturas.ID_Factura == id_factura,
                        DetalleFacturas.ID_Producto == id_producto,
                    )
                    .first()
                )

                diferencia_cantidad = nueva_cantidad - productos_actuales[id_producto]
                detalle.Cantidad = nueva_cantidad
                detalle.Subtotal = nueva_cantidad * detalle.Precio_unitario

                # Ajustar el stock del producto
                producto = (
                    db.query(Productos)
                    .filter(Productos.ID_Producto == id_producto)
                    .first()
                )
                producto.Stock_actual -= diferencia_cantidad
            else:
                # Producto nuevo, agregarlo a la factura y ajustar el stock
                precio_unitario = (
                    db.query(Productos)
                    .filter(Productos.ID_Producto == id_producto)
                    .first()
                    .Precio_venta_normal
                )
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
                producto = (
                    db.query(Productos)
                    .filter(Productos.ID_Producto == id_producto)
                    .first()
                )
                producto.Stock_actual -= nueva_cantidad
        
        saldo = deuda - pagado
        actualizar_venta_credito(
            db=db,
            id_venta_credito=self.id_venta_credito,
            total_deuda=deuda,
            saldo_pendiente=saldo,
            fecha_limite=limite_pago,
        )
        
        # Actualizar información general de la factura
        factura = db.query(Facturas).filter(Facturas.ID_Factura == id_factura).first()
        factura.ID_Usuario = usuario_actual_id

        # Confirmar los cambios
        db.commit()

        self.invoice_number = None
        self.id_venta_credito = None

    def showEvent(self, event):
        super().showEvent(event)
        self.InputCodigo.setFocus()
        self.limpiar_tabla()
        self.limpiar_campos()
        self.invoice_number = None
        configurar_autocompletado(
            self.InputNombre, obtener_productos, "Nombre", self.db, self.procesar_codigo
        )

    def calcular_fecha_futura(self, dias):
        # Obtener la fecha y hora actual
        fecha_actual = datetime.now()
        # Sumar los días a la fecha actual
        fecha_futura = fecha_actual + timedelta(days=dias)
        return fecha_futura.replace(microsecond=0)

    def generar_venta(self):

        if self.TablaVentasCredito.rowCount() == 0:
            QMessageBox.warning(self, "Error", "No hay productos en la venta.")
            self.InputCodigo.setFocus()
            return
        try:
            # Obtener datos del cliente
            client_name = self.InputNombreCli.text().strip()
            client_apellido = self.InputApellidoCli.text().strip()
            client_id = self.InputCedula.text().strip()
            client_address = self.InputDireccion.text().strip()
            client_phone = self.InputTelefonoCli.text().strip()
            limite_pago = self.LimitePagoBox.currentText().strip()

            client_name = f"{client_name} {client_apellido}"

            if limite_pago == "7 días":
                limite_pago = self.calcular_fecha_futura(7)
            elif limite_pago == "15 días":
                limite_pago = self.calcular_fecha_futura(15)

            self.verificar_cliente()

            db = SessionLocal()

            # Obtener los artículos de la tabla
            produc_datos = []
            items = []
            for row in range(self.TablaVentasCredito.rowCount()):
                codigo = self.TablaVentasCredito.item(row, 0).text()
                quantity = int(self.TablaVentasCredito.item(row, 4).text())
                description = self.TablaVentasCredito.item(row, 1).text()
                precio_unitairo = float(self.TablaVentasCredito.item(row, 5).text())
                value = float(self.TablaVentasCredito.item(row, 6).text())

                producto = obtener_producto_por_id(db, int(codigo))

                if not producto:
                    QMessageBox.warning(
                        self, "Error", f"Producto con código {codigo} no encontrado."
                    )
                    return

                producto = producto[0]

                # Validar si hay stock suficiente antes de continuar
                if producto.Stock_actual < quantity:
                    QMessageBox.warning(
                        self,
                        "Error",
                        f"Stock insuficiente para el producto: {description}",
                    )
                    return

                items.append((quantity, description, value))
                produc_datos.append((codigo, quantity, precio_unitairo))

            # Calcular totales
            subtotal = sum(item[2] for item in items)
            delivery_fee = (
                float(self.InputDomicilio.text()) if self.InputDomicilio.text() else 0.0
            )
            total = subtotal + delivery_fee

            if self.invoice_number and self.invoice_number != "":
                self.actualizar_factura(
                    db,
                    self.invoice_number,
                    produc_datos,
                    self.usuario_actual_id,
                    total,
                    limite_pago,
                )
                mensaje = "Factura actualizada exitosamente."
            else:
                for codigo, quantity, _ in produc_datos:
                    producto = obtener_producto_por_id(db, codigo)
                    producto = producto[0]
                    stock_actual = producto.Stock_actual - quantity
                    actualizar_producto(
                        db, id_producto=int(codigo), stock_actual=stock_actual
                    )

                id_factura = self.guardar_factura(
                    db,
                    client_id,
                    "Efectivo",
                    produc_datos,
                    "0.00",
                    0.0,
                    self.usuario_actual_id,
                    subtotal,
                    limite_pago,
                )
                self.invoice_number = f"0000{id_factura}"
                mensaje = "Factura generada exitosamente."

            # Datos adicionales
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
                payment_method="Credito",
                invoice_number=self.invoice_number,
                pan=pan,
                pago=0.0,
                filename=filename,
            )
            db.close()

            QMessageBox.information(self, "Éxito", mensaje)

        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"Error al generar la factura: {str(e)}"
            )
            print(e)

        self.limpiar_tabla()
        self.limpiar_campos()
        self.InputDomicilio.clear()
        self.limpiar_datos_cliente()
        self.invoice_number = None

    def guardar_factura(
        self,
        db,
        client_id,
        payment_method,
        items,
        monto_pago,
        descuento,
        id_usuario,
        deuda,
        limite_pago,
    ):
        """
        Registra la factura y sus detalles en la base de datos.
        """
        try:

            id_metodo_pago = obtener_metodo_pago_por_nombre(db, payment_method)
            print(id_metodo_pago)
            if not id_metodo_pago:
                QMessageBox.warning(
                    self, "Error", f"Método de pago {payment_method} no encontrado."
                )
                return False

            if "/" in monto_pago:
                total = monto_pago.split("/")
                efectivo = float(total[0])
                tranferencia = float(total[1])
            else:
                efectivo = float(monto_pago)
                tranferencia = float(monto_pago)

            # Crear registro en la tabla 'facturas'
            factura = crear_factura(
                db=db,
                monto_efectivo=efectivo if payment_method != "Transferencia" else 0.0,
                monto_transaccion=tranferencia if payment_method != "Efectivo" else 0.0,
                descuento=descuento,
                estado=False,
                id_metodo_pago=id_metodo_pago.ID_Metodo_Pago,
                id_tipo_factura=3,
                id_cliente=client_id,
                id_usuario=id_usuario,
            )

            # Obtener el ID de la factura recién creada
            id_factura = factura.ID_Factura

            # Crear registros en la tabla 'detalle_factura' para cada producto
            for item in items:
                codigo, quantity, precio_unitario = item

                total = quantity * precio_unitario

                # Crear detalle de factura
                crear_detalle_factura(
                    db=db,
                    cantidad=quantity,
                    precio_unitario=precio_unitario,
                    subtotal=total,
                    id_producto=codigo,
                    id_factura=id_factura,
                )

            # Crear registro en la tabla ventasCredito
            crear_venta_credito(
                db=db,
                total_deuda=deuda,
                saldo_pendiente=deuda,
                fecha_limite=limite_pago,
                id_factura=id_factura,
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
        self.InputCedula.setText("")
        self.InputNombreCli.setText("")
        self.InputApellidoCli.setText("")
        self.InputTelefonoCli.setText("")
        self.InputDireccion.setText("")
        self.LabelSubtotal.setText("$0")
        self.LabelTotal.setText("$0")

    def mostrar_mensaje_temporal(self, titulo, mensaje, duracion=2200):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(titulo)
        msg_box.setText(mensaje)
        msg_box.setIcon(QMessageBox.Warning)
        QTimer.singleShot(
            duracion, msg_box.close
        )  # Cierra el mensaje después de 'duracion' milisegundos
        msg_box.exec_()

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
            self.InputCedula.setFocus()
        elif self.focusWidget() == self.InputCedula:
            self.InputNombreCli.setFocus()
        elif self.focusWidget() == self.InputNombreCli:
            self.InputApellidoCli.setFocus()
        elif self.focusWidget() == self.InputApellidoCli:
            self.InputTelefonoCli.setFocus()
        elif self.focusWidget() == self.InputTelefonoCli:
            self.InputDireccion.setFocus()
        elif self.focusWidget() == self.InputDireccion:
            self.InputDomicilio.setFocus()  # Volver al inicio Volver al inicio
        elif self.focusWidget() == self.InputDomicilio:
            self.InputCodigo.setFocus()

    def navegar_widgets_atras(self):
        """
        Navega hacia atrás entre los widgets en el siguiente orden:
        Código <- Nombre <- Nombre Cliente <- Apellido Cliente <- Dirección <- Teléfono <- Cédula <- Nombre <- Código
        """
        if self.focusWidget() == self.InputCodigo:
            self.InputDomicilio.setFocus()  # Volver al final
        elif self.focusWidget() == self.InputDomicilio:
            self.InputDireccion.setFocus()
        elif self.focusWidget() == self.InputDireccion:
            self.InputTelefonoCli.setFocus()
        elif self.focusWidget() == self.InputTelefonoCli:
            self.InputApellidoCli.setFocus()
        elif self.focusWidget() == self.InputApellidoCli:
            self.InputNombreCli.setFocus()
        elif self.focusWidget() == self.InputNombreCli:
            self.InputCedula.setFocus()
        elif self.focusWidget() == self.InputCedula:
            self.InputNombre.setFocus()
        elif self.focusWidget() == self.InputNombre:
            self.InputCodigo.setFocus()  # Volver al inicio

    def configurar_localizacion(self):
        try:
            locale.setlocale(locale.LC_ALL, "es_CO.UTF-8")
        except locale.Error:
            print("No se pudo configurar la localización de Colombia.")

    def procesar_codigo(self):
        # Obtener los valores de los inputs
        codigo = self.InputCodigo.text().strip()
        nombre = self.InputNombre.text().strip()
        tipo_precio = self.comboBoxPrecio.currentText().strip()

        # Conexión a la base de datos
        db = SessionLocal()

        try:
            # Caso 1: Si se proporciona el código
            if codigo:
                if not codigo.isdigit():
                    QMessageBox.warning(
                        self, "Error", "El código debe ser un número válido."
                    )
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
                    self.id_categoria = producto.categorias
                    self.InputCantidad.clear()

                    if tipo_precio == "PU":
                        self.InputPrecioUnitario.setText(
                            str(producto.Precio_venta_normal)
                        )
                    else:
                        self.InputPrecioUnitario.setText(
                            str(producto.Precio_venta_mayor)
                        )

                    self.InputPrecioUnitario.setEnabled(False)
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
                    self.id_categoria = producto.categorias
                    self.InputCantidad.clear()  # Limpiar cantidad

                    if tipo_precio == "PU":
                        self.InputPrecioUnitario.setText(
                            str(producto.Precio_venta_normal)
                        )
                    else:
                        self.InputPrecioUnitario.setText(
                            str(producto.Precio_venta_mayor)
                        )

                    self.InputPrecioUnitario.setEnabled(False)
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
        precio_unitario = self.InputPrecioUnitario.text().strip()

        try:
            cantidad = int(cantidad)  # Convertimos la cantidad a entero
            precio_unitario = float(precio_unitario)  # Convertimos el precio a flotante
        except ValueError:
            if mostrar_mensaje:
                QMessageBox.warning(
                    self,
                    "Error",
                    "Por favor, ingrese valores numéricos válidos para la cantidad y el precio.",
                )
            return
        # Calcular el total del producto
        for row in range(self.TablaVentasCredito.rowCount()):
            item_codigo = self.TablaVentasCredito.item(
                row, 0
            )  # Obtener el código de la fila
            if item_codigo and item_codigo.text() == codigo:  # Si el código ya existe
                self.mostrar_mensaje_temporal(
                    "Error", "Este código de producto ya existe."
                )
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
        # traceback.print_stack()
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
            self.InputCodigo.setFocus()

    def actualizar_datos(self):
        self.InputCodigo.setFocus()

        if self.fila_seleccionada is not None:
            try:
                cantidad_str = self.InputCantidad.text().strip()
                precio_unitario_str = self.InputPrecioUnitario.text().strip()
                # domicilio_str = self.InputDomicilio.text().strip()

                if not cantidad_str or not precio_unitario_str:
                    QMessageBox.warning(
                        self,
                        "Error",
                        "Por favor, ingrese valores para cantidad.",
                    )
                    return

                cantidad = int(cantidad_str)
                precio_unitario = float(precio_unitario_str)
                # domicilio = float(domicilio_str)

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
                self.TablaVentasCredito.item(row, 4).setTextAlignment(
                    QtCore.Qt.AlignCenter
                )
                self.TablaVentasCredito.setItem(
                    row, 5, QTableWidgetItem(str(precio_unitario))
                )
                self.TablaVentasCredito.item(row, 5).setTextAlignment(
                    QtCore.Qt.AlignCenter
                )
                total = cantidad * precio_unitario
                self.TablaVentasCredito.setItem(row, 6, QTableWidgetItem(str(total)))
                self.TablaVentasCredito.item(row, 6).setTextAlignment(
                    QtCore.Qt.AlignCenter
                )

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
        )  # Expresión para números y puntos
        validator_precio_unitario = QRegularExpressionValidator(rx_precio_unitario)
        self.InputPrecioUnitario.setValidator(validator_precio_unitario)

        rx_cedula = QRegularExpression(r"^\d+$")  # Expresión para solo números
        validator_cedula = QRegularExpressionValidator(rx_cedula)
        self.InputCedula.setValidator(validator_cedula)
        # Nombre (solo letras y espacios)
        rx_nombre = QRegularExpression(r"^[a-zA-Z]+$")
        validator_nombre = QRegularExpressionValidator(rx_nombre)
        self.InputNombreCli.setValidator(validator_nombre)

        rx_apellido = QRegularExpression(r"^[a-zA-Z]+$")
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
            QMessageBox.information(
                self, "Campos obligatorios", "Todos los campos son obligatorios"
            )
            QTimer.singleShot(0, self.InputNombreCli.setFocus)

            return
        # Validación de cédula
        if len(cedula) < 6 or len(cedula) > 11 or not cedula.isdigit():
            QMessageBox.warning(
                self, "Cédula inválida", "La cédula debe tener entre 6 y 11 dígitos."
            )
            QTimer.singleShot(0, self.InputCedula.setFocus)

            return
        # Validación de teléfono
        if len(telefono) != 10 or not telefono.isdigit():
            QMessageBox.warning(
                self, "Teléfono inválido", "El teléfono debe tener 10 dígitos."
            )
            QTimer.singleShot(0, self.InputTelefonoCli.setFocus)

            return

        # Crear una sesión de base de datos
        db = (
            SessionLocal()
        )  # Asegúrate de que `SessionLocal` está correctamente configurado
        try:
            # Verificar si el cliente ya existe
            cliente_existente = obtener_cliente_por_id(db, cedula)
            if not cliente_existente:
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
                    QMessageBox.information(
                        self, "Cliente creado", "El cliente ha sido creado exitosamente"
                    )

        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"Error al procesar el cliente: {str(e)}"
            )

        finally:
            # Cerrar la sesión para liberar recursos
            db.close()

    def completar_campos(self):

        # Obtener cliente
        id_cliente = int(self.InputCedula.text().strip())
        self.db = SessionLocal()

        try:
            cliente = obtener_cliente_por_id(self.db, id_cliente)
            if cliente:
                self.InputNombreCli.setText(cliente.Nombre)
                self.InputApellidoCli.setText(cliente.Apellido)
                self.InputTelefonoCli.setText(cliente.Teléfono)
                self.InputDireccion.setText(cliente.Direccion)
            else:
                QMessageBox.warning(
                    self, "Error", f"Cliente con cédula {id_cliente} no encontrado."
                )
        except Exception as e:
            print(f"Error al obtener cliente: {e}")
        finally:
            self.db.close()

    def cambiar_precio(self):
        metodo_seleccionado = self.comboBoxPrecio.currentText().strip()

        if metodo_seleccionado == "PU":

            for row in range(self.TablaVentasCredito.rowCount()):
                codigo = self.TablaVentasCredito.item(row, 0).text()
                cantidad = int(self.TablaVentasCredito.item(row, 4).text())

                producto = obtener_producto_por_id(self.db, int(codigo))

                producto = producto[0]
                if producto:
                    precio = float(producto.Precio_venta_normal)
                    self.TablaVentasCredito.item(row, 5).setText(str(precio))
                    total = cantidad * precio
                    self.TablaVentasCredito.item(row, 6).setText(str(total))

        elif metodo_seleccionado == "PAM":

            for row in range(self.TablaVentasCredito.rowCount()):
                codigo = self.TablaVentasCredito.item(row, 0).text()
                cantidad = int(self.TablaVentasCredito.item(row, 4).text())

                producto = obtener_producto_por_id(self.db, int(codigo))

                producto = producto[0]
                if producto:
                    precio = float(producto.Precio_venta_mayor)
                    self.TablaVentasCredito.item(row, 5).setText(str(precio))
                    total = cantidad * precio
                    self.TablaVentasCredito.item(row, 6).setText(str(total))

        self.actualizar_total()
