from PyQt5.QtWidgets import QMessageBox, QWidget
from PyQt5 import QtWidgets, QtCore
from ..database.database import SessionLocal
from ..controllers.producto_crud import *
from ..controllers.marca_crud import *
from ..controllers.categorias_crud import *
from ..ui import Ui_Productos


class ProductosView(QWidget, Ui_Productos):
    def __init__(self, parent=None):
        super(ProductosView, self).__init__(parent)
        self.setupUi(self)
        self.InputCodigo.setFocus()
        self.TablaProductos.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        # Conectar el evento de presionar Enter en los inputs
        self.InputNombre.returnPressed.connect(self.editar_producto)
        self.InputPrecioCompra.returnPressed.connect(self.editar_producto)
        self.InputCantidad.returnPressed.connect(self.editar_producto)
        self.InputCantidadMin.returnPressed.connect(self.editar_producto)
        self.InputCantidadMax.returnPressed.connect(self.editar_producto)
        self.InputMarca.returnPressed.connect(self.editar_producto)
        self.InputCategoria.returnPressed.connect(self.editar_producto)
        self.InputPrecioUnitario.returnPressed.connect(self.editar_producto)
        self.InputPrecioMayor.returnPressed.connect(self.editar_producto)

        # Enfocar automáticamente el campo de entrada al abrir
        # Conectar el evento de tecla Enter para procesar el código
        self.InputCodigo.returnPressed.connect(self.procesar_codigo)
        self.TablaProductos.cellClicked.connect(self.cargar_datos_fila)
        self.BtnIngresarProducto.clicked.connect(self.ingresar_producto)
        self.BtnEliminar.clicked.connect(self.eliminar_producto)
        self.limpiar_tabla_productos()
        self.mostrar_productos()

    def procesar_codigo(self):
        """
        Procesa el código ingresado en el campo InputCodigo.
        """
        codigo = self.InputCodigo.text().strip()
        self.limpiar_formulario()

    def obtener_id_producto(self):
        """
        Obtiene el id del producto seleccionado en la tabla.
        """
        fila_seleccionada = self.TablaProductos.currentRow()

        if fila_seleccionada == -1:
            QtWidgets.QMessageBox.warning(self, "Error", "Selecciona un producto")
            return None

        id = self.TablaProductos.item(fila_seleccionada, 0).text()
        if id:
            return id
        else:
            QtWidgets.QMessageBox.warning(
                self, "Error", "No se pudo obtener el ID del producto"
            )
            return None

    def cargar_datos_fila(self):
        """
        Muestra los productos en los campos de entredada.
        """
        fila_seleccionada = self.TablaProductos.currentRow()
        datos_fila = []
        for columna in range(self.TablaProductos.columnCount()):
            item = self.TablaProductos.item(fila_seleccionada, columna)
            datos_fila.append(item.text() if item else "")

        self.InputCodigo.setText(datos_fila[0])
        self.InputNombre.setText(datos_fila[1])
        self.InputMarca.setText(datos_fila[2])
        self.InputCategoria.setText(datos_fila[3])
        self.InputCantidad.setText(datos_fila[4])
        self.InputCantidadMin.setText(datos_fila[5])
        self.InputCantidadMax.setText(datos_fila[6])
        self.InputPrecioCompra.setText(datos_fila[7])
        self.InputPrecioUnitario.setText(datos_fila[8])
        self.InputPrecioMayor.setText(datos_fila[9])

    def eliminar_producto(self):
        """
        Elimina el producto seleccionado en la tabla.
        """
        id = self.obtener_id_producto()
        if id is None:
            return
        respuesta = QMessageBox.question(
            self,
            "Confirmar Eliminación",
            f"¿Estás seguro de que deseas eliminar el producto con ID {id}?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if respuesta == QMessageBox.No:
            return

        try:
            self.db = SessionLocal()
            eliminar_producto(self.db, id)  # Llamar a la función de base de datos
        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"No se pudo eliminar el producto: {str(e)}"
            )
            return

        QMessageBox.information(self, "Éxito", "Producto eliminado correctamente.")

        self.db.close()
        self.limpiar_formulario()
        self.limpiar_tabla_productos()
        self.mostrar_productos()

    def mostrar_productos(self):
        """
        Obtener todos los productos de la base de datos y mostrarlos en la tabla.
        """
        self.db = SessionLocal()
        rows = obtener_productos(self.db)

        if rows:
            self.TablaProductos.setRowCount(len(rows))
            self.TablaProductos.setColumnCount(12)

            for row_idx, row in enumerate(rows):
                id_producto = str(row.ID_Producto)
                nombre = str(row.Nombre)
                precio_compra = str(row.Precio_costo)
                precio_venta_mayor = str(row.Precio_venta_mayor)
                precio_venta_normal = str(row.Precio_venta_normal)
                ganancia_producto_mayor = str(row.Ganancia_Producto_mayor)
                ganancia_producto_normal = str(row.Ganancia_Producto_normal)
                cantidad = str(row.Stock_actual)
                cantidad_min = str(row.Stock_min)
                cantidad_max = str(row.Stock_max)
                marca = str(row.marcas)
                categoria = str(row.categorias)

                id_item = QtWidgets.QTableWidgetItem(id_producto)
                id_item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.TablaProductos.setItem(row_idx, 0, id_item)

                nombre_item = QtWidgets.QTableWidgetItem(nombre)
                nombre_item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.TablaProductos.setItem(row_idx, 1, nombre_item)

                marca_item = QtWidgets.QTableWidgetItem(marca)
                marca_item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.TablaProductos.setItem(row_idx, 2, marca_item)

                categoria_item = QtWidgets.QTableWidgetItem(categoria)
                categoria_item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.TablaProductos.setItem(row_idx, 3, categoria_item)

                cantidad_item = QtWidgets.QTableWidgetItem(cantidad)
                cantidad_item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.TablaProductos.setItem(row_idx, 4, cantidad_item)

                cantidad_min_item = QtWidgets.QTableWidgetItem(cantidad_min)
                cantidad_min_item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.TablaProductos.setItem(row_idx, 5, cantidad_min_item)

                cantidad_max_item = QtWidgets.QTableWidgetItem(cantidad_max)
                cantidad_max_item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.TablaProductos.setItem(row_idx, 6, cantidad_max_item)

                precio_compra_item = QtWidgets.QTableWidgetItem(precio_compra)
                precio_compra_item.setTextAlignment(QtCore.Qt.AlignRight)
                self.TablaProductos.setItem(row_idx, 7, precio_compra_item)

                precio_venta_normal_item = QtWidgets.QTableWidgetItem(
                    precio_venta_normal
                )
                precio_venta_normal_item.setTextAlignment(QtCore.Qt.AlignRight)
                self.TablaProductos.setItem(row_idx, 8, precio_venta_normal_item)

                precio_venta_mayor_item = QtWidgets.QTableWidgetItem(precio_venta_mayor)
                precio_venta_mayor_item.setTextAlignment(QtCore.Qt.AlignRight)
                self.TablaProductos.setItem(row_idx, 9, precio_venta_mayor_item)

                ganancia_producto_normal_item = QtWidgets.QTableWidgetItem(
                    ganancia_producto_normal
                )
                ganancia_producto_normal_item.setTextAlignment(QtCore.Qt.AlignRight)
                self.TablaProductos.setItem(row_idx, 10, ganancia_producto_normal_item)

                ganancia_producto_mayor_item = QtWidgets.QTableWidgetItem(
                    ganancia_producto_mayor
                )
                ganancia_producto_mayor_item.setTextAlignment(QtCore.Qt.AlignRight)
                self.TablaProductos.setItem(row_idx, 11, ganancia_producto_mayor_item)

        self.db.close()

    def limpiar_tabla_productos(self):
        """
        Limpia la tabla de productos.
        """
        self.TablaProductos.setRowCount(0)
        self.TablaProductos.setColumnCount(12)

    def ingresar_producto(self):
        """
        Captura los datos del formulario y los registra en la base de datos.
        """
        id = self.InputCodigo.text()
        nombre = self.InputNombre.text()
        precio_compra = self.InputPrecioCompra.text()
        cantidad = self.InputCantidad.text()
        cantidad_min = self.InputCantidadMin.text()
        cantidad_max = self.InputCantidadMax.text()
        marca = self.InputMarca.text()
        categoria = self.InputCategoria.text()

        if (
            not id
            or not nombre
            or not precio_compra
            or not cantidad
            or not cantidad_min
            or not cantidad_max
            or not marca
            or not categoria
        ):
            QtWidgets.QMessageBox.warning(
                self, "Error", "Por favor, rellene todos los campos"
            )
            return

        try:
            id = int(id)
            precio_compra = float(precio_compra)
            cantidad = int(cantidad)
            cantidad_min = int(cantidad_min)
            cantidad_max = int(cantidad_max)

            self.db = SessionLocal()
            id_marca = obtener_o_crear_marca(self.db, marca)
            id_categoria = obtener_o_crear_categoria(self.db, categoria)

            crear_producto(
                self.db,
                id,
                nombre,
                precio_compra,
                cantidad,
                cantidad_min,
                cantidad_max,
                id_marca,
                id_categoria,
            )
            QtWidgets.QMessageBox.information(
                self, "Éxito", "Producto registrado exitosamente"
            )
            self.limpiar_formulario()
            self.limpiar_tabla_productos()
            self.mostrar_productos()

        except ValueError:
            QtWidgets.QMessageBox.warning(
                self, "Error", "Por favor, ingrese valores numéricos"
            )

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Error: {e}")

        finally:
            if hasattr(self, "db") and self.db:
                self.db.close()

    def editar_producto(self):
        """
        Al presionar Enter en cualquier input, pregunta si desea guardar los cambios
        y luego edita el producto si es confirmado.
        """
        # Obtener los nuevos datos de los inputs
        id = self.InputCodigo.text()
        nombre = self.InputNombre.text()
        precio_compra = self.InputPrecioCompra.text()
        cantidad = self.InputCantidad.text()
        cantidad_min = self.InputCantidadMin.text()
        cantidad_max = self.InputCantidadMax.text()
        marca = self.InputMarca.text()
        categoria = self.InputCategoria.text()
        precio_mayor = self.InputPrecioMayor.text()
        precio_unitario = self.InputPrecioUnitario.text()

        # Verificar que todos los campos tengan datos
        if (
            not id
            or not nombre
            or not precio_compra
            or not cantidad
            or not cantidad_min
            or not cantidad_max
            or not marca
            or not categoria
            or not precio_mayor
            or not precio_unitario
        ):
            QMessageBox.warning(self, "Error", "Por favor, rellene todos los campos")
            return

        # Confirmar si el usuario desea realizar la edición
        reply = QMessageBox.question(
            self,
            "Confirmación",
            "¿Desea guardar los cambios?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            try:
                # Hacer la actualización en la base de datos
                self.db = SessionLocal()

                id = int(id)
                precio_compra = float(precio_compra)
                cantidad = int(cantidad)
                cantidad_min = int(cantidad_min)
                cantidad_max = int(cantidad_max)
                precio_mayor = float(precio_mayor)
                precio_unitario = float(precio_unitario)
                id_marca = obtener_o_crear_marca(self.db, marca)
                id_categoria = obtener_o_crear_categoria(self.db, categoria)

                # Actualizar el producto en la base de datos
                producto_actualizado = actualizar_producto(
                    self.db,
                    id,
                    nombre,
                    precio_compra,
                    precio_mayor,
                    precio_unitario,
                    cantidad,
                    cantidad_min,
                    cantidad_max,
                    id_marca,
                    id_categoria,
                )

                if producto_actualizado:
                    QMessageBox.information(
                        self, "Éxito", "Producto actualizado correctamente"
                    )
                    self.limpiar_formulario()
                    self.limpiar_tabla_productos()
                    self.mostrar_productos()
                else:
                    QMessageBox.warning(
                        self, "Error", "Hubo un problema al actualizar el producto"
                    )

                self.db.close()

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error: {e}")
        else:
            # Si el usuario cancela la edición
            print("Edición cancelada")

    def limpiar_formulario(self):
        """
        Limpia el formulario de todos los campos.
        """
        self.InputNombre.setText("")
        self.InputPrecioCompra.setText("")
        self.InputCantidad.setText("")
        self.InputCantidadMin.setText("")
        self.InputCantidadMax.setText("")
        self.InputMarca.setText("")
        self.InputCategoria.setText("")
        self.InputPrecioUnitario.setText("")
        self.InputPrecioMayor.setText("")
