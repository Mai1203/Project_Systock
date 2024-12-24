from PyQt5.QtWidgets import QMessageBox, QWidget
from PyQt5 import QtWidgets
from ..database.database import SessionLocal
from ..controllers.producto_crud import *
from ..controllers.detalle_factura_crud import *
from ..controllers.facturas_crud import *
from ..ui import Ui_VentasA


class VentasAView(QWidget, Ui_VentasA):
    def __init__(self, parent=None):
        super(VentasAView, self).__init__(parent)
        self.setupUi(self)
        self.limpiar_tabla()
        # Conectar evento del input para escanear el código
        self.InputCodigo.returnPressed.connect(self.procesar_codigo)
        self.BtnAgregarProducto.clicked.connect(self.agregar_producto)
        self.BtnEliminar.clicked.connect(self.eliminar_fila)

    def procesar_codigo(self):
        codigo = self.InputCodigo.text().strip()

        if not codigo:
            QMessageBox.warning(self, "Error", "Por favor, ingrese un código válido.")
            return

        try:
            # Conexión a la base de datos
            db = SessionLocal()

            # Llamada a la función que obtiene el producto por código usando la función definida
            productos = obtener_producto_por_id(
                db, int(codigo)
            )  # Obtiene la lista de productos

            if productos:
                # Solo tomamos el primer producto de la lista, ya que asumimos que el ID es único
                producto = productos[0]

                # Mostrar el código en el campo InputCodigo para asegurarse que se lee correctamente
                self.InputCodigo.setText(
                    codigo
                )  # Esto actualizará el campo con el código ingresado

                # Actualiza los campos con la información del producto
                self.InputNombre.setText(producto.Nombre)
                self.InputMarca.setText(
                    str(producto.marcas)
                )  # Accede usando el alias 'marcas'
                self.InputPrecioUnitario.setText(str(producto.Precio_venta_normal))
                self.id_categoria = (
                    producto.categorias
                )  # Guardar el valor para su uso posterior

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

        # Conexión a la base de datos
        db = SessionLocal()

        try:
            # Obtener el producto desde la base de datos usando la función obtener_producto_por_id
            productos = obtener_producto_por_id(db, int(codigo))

            if productos:
                producto = productos[
                    0
                ]  # Suponiendo que el código del producto es único

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

            # Obtener la posición de la nueva fila en la tabla
            rowPosition = (
                self.tableWidget.rowCount()
            )  # Esta es la cantidad de filas actuales en la tabla

            # Insertar una nueva fila en la tabla
            self.tableWidget.insertRow(rowPosition)

            # Agregar los datos a la nueva fila
            self.tableWidget.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(codigo))
            self.tableWidget.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(nombre))
            self.tableWidget.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(marca))
            self.tableWidget.setItem(
                rowPosition, 3, QtWidgets.QTableWidgetItem(categoria)
            )  # Agregar categoría
            self.tableWidget.setItem(
                rowPosition, 4, QtWidgets.QTableWidgetItem(str(cantidad))
            )
            self.tableWidget.setItem(
                rowPosition, 5, QtWidgets.QTableWidgetItem(str(precio_unitario))
            )
            self.tableWidget.setItem(
                rowPosition, 6, QtWidgets.QTableWidgetItem(str(total))
            )  # Mostrar el total

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
        else:
            QMessageBox.warning(
                self, "Error", "Por favor, selecciona una fila para eliminar."
            )
