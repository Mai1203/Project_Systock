from PyQt5.QtWidgets import (
    QMessageBox,
    QWidget,
)
from PyQt5 import QtWidgets, QtCore, QtGui
from ..utils import *
from ..utils.autocomplementado import configurar_autocompletado
from ..database.database import SessionLocal
from ..controllers.producto_crud import *
from ..controllers.marca_crud import *
from ..controllers.categorias_crud import *
from ..ui import Ui_Productos
from PyQt5.QtCore import Qt



class Productos_View(QWidget, Ui_Productos):
    def __init__(self, parent=None):
        super(Productos_View, self).__init__(parent)
        self.setupUi(self)
        
        # Cambiar el orden de navegación con Tab
        self.setTabOrder(self.InputCodigo, self.InputNombre) 
        self.setTabOrder(self.InputNombre, self.InputMarca) 
        self.setTabOrder(self.InputMarca, self.InputCategoria) 
        self.setTabOrder(self.InputCategoria, self.InputCantidad) 
        self.setTabOrder(self.InputCantidad, self.InputCantidadMin) 
        self.setTabOrder(self.InputCantidadMin, self.InputCantidadMax) 
        self.setTabOrder(self.InputCantidadMax, self.InputPrecioCompra) 
        self.setTabOrder(self.InputPrecioCompra, self.InputPrecioUnitario) 
        self.setTabOrder(self.InputPrecioUnitario, self.InputPrecioMayor) 
       
        
        self.InputBuscador.setPlaceholderText(
            "Buscar por código, Nombre, Marca o Categoria"
        )
        self.InputBuscador.textChanged.connect(self.buscar_productos)

        self.db = SessionLocal()

        configurar_validador_numerico(self.InputCodigo)
        configurar_validador_numerico(self.InputCantidad)
        configurar_validador_numerico(self.InputPrecioUnitario)
        configurar_validador_numerico(self.InputCantidadMax)
        configurar_validador_numerico(self.InputCantidadMin)
        configurar_validador_numerico(self.InputPrecioMayor)
        configurar_validador_numerico(self.InputPrecioCompra)

        configurar_validador_texto(self.InputNombre)
        configurar_validador_texto(self.InputMarca)
        configurar_validador_texto(self.InputCategoria)
        
        # placeholder
        self.InputCantidadMin.setText("3")
        self.InputCantidadMax.setText("99")
        
        
        
        self.InputPrecioCompra.textChanged.connect(self.agregar_placeholder)
        
         
        configurar_autocompletado(self.InputMarca, obtener_marcas, "Nombre", self.db)

        configurar_autocompletado(
            self.InputCategoria, obtener_categorias, "Nombre", self.db
        )

        self.TablaProductos.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.TablaProductos.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
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
        

        # Conectar el evento de tecla Enter para procesar el código
        self.InputCodigo.returnPressed.connect(self.procesar_codigo)
        self.TablaProductos.cellClicked.connect(self.cargar_datos_fila)
        self.BtnIngresarProducto.clicked.connect(self.ingresar_producto)
        self.BtnEliminar.clicked.connect(self.eliminar_productos)
        
        
    def keyPressEvent(self, event):
        # Si presionas Enter en InputDomicilio, realiza una acción especial
        if event.key() == Qt.Key_Up:
            
            self.navegar_widgets()
            
        elif event.key() == Qt.Key_Down:
            self.navegar_widgets_atras()
        # Llamar al método original para procesar otros eventos
        super().keyPressEvent(event)

    def navegar_widgets(self):
        """
        Navega entre los widgets hacia adelante según el orden definido.
        """
        if self.focusWidget() == self.InputCodigo:
            self.InputNombre.setFocus()
        elif self.focusWidget() == self.InputNombre:
            self.InputMarca.setFocus()
        elif self.focusWidget() == self.InputMarca:
            self.InputCategoria.setFocus()
        elif self.focusWidget() == self.InputCategoria:
            self.InputCantidad.setFocus()
        elif self.focusWidget() == self.InputCantidad:
            self.InputCantidadMin.setFocus()
        elif self.focusWidget() == self.InputCantidadMin:
            self.InputCantidadMax.setFocus()
        elif self.focusWidget() == self.InputCantidadMax:
            self.InputPrecioCompra.setFocus()
        elif self.focusWidget() == self.InputPrecioCompra:
            self.InputPrecioUnitario.setFocus()
        elif self.focusWidget() == self.InputPrecioUnitario:
            self.InputPrecioMayor.setFocus()
        elif self.focusWidget() == self.InputPrecioMayor:
            self.InputCodigo.setFocus()  # Volver al inicio

    def navegar_widgets_atras(self):
        """
        Navega entre los widgets hacia atrás según el orden definido.
        """
        if self.focusWidget() == self.InputCodigo:
            self.InputPrecioMayor.setFocus()
        elif self.focusWidget() == self.InputPrecioMayor:
            self.InputPrecioUnitario.setFocus()
        elif self.focusWidget() == self.InputPrecioUnitario:
            self.InputPrecioCompra.setFocus()
        elif self.focusWidget() == self.InputPrecioCompra:
            self.InputCantidadMax.setFocus()
        elif self.focusWidget() == self.InputCantidadMax:
            self.InputCantidadMin.setFocus()
        elif self.focusWidget() == self.InputCantidadMin:
            self.InputCantidad.setFocus()
        elif self.focusWidget() == self.InputCantidad:
            self.InputCategoria.setFocus()
        elif self.focusWidget() == self.InputCategoria:
            self.InputMarca.setFocus()
        elif self.focusWidget() == self.InputMarca:
            self.InputNombre.setFocus()
        elif self.focusWidget() == self.InputNombre:
            self.InputCodigo.setFocus()  # Volver al inicio
        
    def showEvent(self, event):
        super().showEvent(event)
        self.InputCodigo.setFocus()
        self.limpiar_tabla_productos()
        self.mostrar_productos()
        
    def agregar_placeholder(self):
        """
        Agrega un placeholder con el precio de venta
        """
        precio_compra = self.InputPrecioCompra.text().strip()
        
        if not precio_compra:
            self.InputPrecioUnitario.setPlaceholderText("")
            self.InputPrecioMayor.setPlaceholderText("")
            return
        
        precio_compra = float(precio_compra)
        
        precio_unitario = precio_compra + (precio_compra * 0.5)
        precio_mayor = precio_compra + (precio_compra * 0.35)
        
        precio_unitario = redondear_a_cientos(precio_unitario)
        precio_mayor = redondear_a_cientos(precio_mayor)
        
        self.InputPrecioUnitario.setPlaceholderText(f"{precio_unitario}")
        self.InputPrecioMayor.setPlaceholderText(f"{precio_mayor}")
        
    def redondear_a_cientos(numero):
        """
        Redondea el número hacia el siguiente múltiplo de 100.
        Siempre redondea hacia arriba.
        """
        if numero is None:  # Comprobar si el número es None
            raise ValueError("El valor de 'numero' no puede ser None")

        if not isinstance(numero, (int, float)):  # Verifica que el número sea int o float
            raise TypeError("El valor debe ser un número entero o flotante")

        if numero % 100 == 0:
            return numero  # Ya es múltiplo de 100
        
        return ((numero // 100) + 1) * 100
        
    def obtener_ids_seleccionados(self):
        """
        Obtiene los IDs de los productos seleccionados en la tabla.
        """
        filas_seleccionadas = self.TablaProductos.selectionModel().selectedRows()
        ids = []

        for fila in filas_seleccionadas:
            id_producto = self.TablaProductos.item(
                fila.row(), 0
            ).text()  # Columna 0: ID del producto
            ids.append(int(id_producto))

        return ids

    def buscar_productos(self):
        """
        Busca productos por código, nombre, marca o categoría.
        """
        busqueda = self.InputBuscador.text().strip()
        if not busqueda:
            self.mostrar_productos()
            return

        self.db = SessionLocal()

        productos = buscar_productos(self.db, busqueda)
        self.actualizar_tabla_productos(productos)

        self.db.close()

    def actualizar_tabla_productos(self, productos):
        """
        Actualiza la tabla de productos con los productos buscados.
        """

        if productos:
            self.TablaProductos.setRowCount(len(productos))
            self.TablaProductos.setColumnCount(13)

            for row_idx, row in enumerate(productos):
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
                if row.Estado:
                    estado = "Activo"
                else:
                    estado = "Inactivo"

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

                estado_item = QtWidgets.QTableWidgetItem(estado)
                estado_item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.TablaProductos.setItem(row_idx, 12, estado_item)
                
                if row.Stock_actual <= row.Stock_min:
                    for col in range(self.TablaProductos.columnCount()):
                        item = self.TablaProductos.item(row_idx, col)
                        if item:  # Verifica que el elemento no sea None
                            item.setForeground(QtGui.QColor(255, 0, 0))  # Texto blanco
                        else:
                            print(f"No se encontró un elemento en la fila {row_idx}, columna {col}")
                    self.TablaProductos.viewport().update() 
                           
    def procesar_codigo(self):
        """
        Procesa el código ingresado en el campo InputCodigo.
        """
        self.limpiar_formulario_codigo()
        codigo = self.InputCodigo.text().strip()

    def obtener_id_producto(self):
        """
        Obtiene el id del producto seleccionado en la tabla.
        """
        fila_seleccionada = self.TablaProductos.currentRow()

        if fila_seleccionada == -1:
            enviar_notificacion("Error", "Seleccione un Producto!")
            return None

        id = self.TablaProductos.item(fila_seleccionada, 0).text()
        if id:
            return id
        else:
            enviar_notificacion("Error", "No se pudo obtener el ID del Producto")
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

    def mostrar_productos(self):
        """
        Obtener todos los productos de la base de datos y mostrarlos en la tabla.
        """
        self.db = SessionLocal()
        rows = obtener_productos(self.db)

        self.actualizar_tabla_productos(rows)

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
        precio_unitario = self.InputPrecioUnitario.text()
        precio_mayor = self.InputPrecioMayor.text()
        
        if not precio_unitario:
            precio_unitario = self.InputPrecioUnitario.placeholderText()
            
        if not precio_mayor:
            precio_mayor = self.InputPrecioMayor.placeholderText()

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
            enviar_notificacion("Error", "Por favor, rellene todos los campos")
            return

        try:
            id = int(id)

            precio_compra = float(precio_compra)
            precio_unitario = float(precio_unitario)
            precio_mayor = float(precio_mayor)
            cantidad = int(cantidad)
            cantidad_min = int(cantidad_min)
            cantidad_max = int(cantidad_max)

            self.db = SessionLocal()
            id_marca = obtener_o_crear_marca(self.db, marca)
            id_categoria = obtener_o_crear_categoria(self.db, categoria)
            
            configurar_autocompletado(self.InputMarca, obtener_marcas, "Nombre", self.db)
            configurar_autocompletado(self.InputCategoria, obtener_categorias, "Nombre", self.db)

            producto_existente = obtener_producto_por_id(self.db, id)
            if producto_existente:
                enviar_notificacion(
                    "Error", "El producto ya existe en la base de datos"
                )
                return

            crear_producto(
                self.db,
                id,
                nombre,
                precio_compra,
                cantidad,
                cantidad_min,
                cantidad_max,
                precio_unitario,
                precio_mayor,
                id_marca,
                id_categoria,
            )
            enviar_notificacion("Éxito", "Producto registrado exitosamente")
            self.limpiar_formulario()
            self.limpiar_tabla_productos()
            self.mostrar_productos()
            self.InputCodigo.setFocus()
            self.InputCantidadMin.setText("3")
            self.InputCantidadMax.setText("99")
            configurar_autocompletado(self.InputMarca, obtener_marcas, "Nombre", self.db)
            configurar_autocompletado(
                self.InputCategoria, obtener_categorias, "Nombre", self.db
            )

        except ValueError:
            enviar_notificacion("Error", "Por favor, ingrese valores numéricos")

        except Exception as e:
            print(f"Error: {e}")
            enviar_notificacion("Error", f"Error: {e}")

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
            enviar_notificacion("Error", "Por favor, rellene todos los campos")
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

                productos = obtener_producto_por_id(self.db, id)
                if not productos:
                    enviar_notificacion("Error", "Producto no encontrado")
                    return

                producto = productos[0]

                # Crear un diccionario dinámico para los valores a actualizar
                valores_a_actualizar = {}

                if producto.Precio_venta_mayor != precio_mayor:
                    valores_a_actualizar["precio_venta_mayor"] = precio_mayor

                if producto.Precio_venta_normal != precio_unitario:
                    valores_a_actualizar["precio_venta_normal"] = precio_unitario

                # Siempre actualizar estos campos
                valores_a_actualizar.update(
                    {
                        "nombre": nombre,
                        "precio_costo": precio_compra,
                        "stock_actual": cantidad,
                        "stock_min": cantidad_min,
                        "stock_max": cantidad_max,
                        "id_marca": id_marca,
                        "id_categoria": id_categoria,
                    }
                )

                # Verificar si hay algo que actualizar
                if valores_a_actualizar:
                    producto_actualizado = actualizar_producto(
                        self.db, id, **valores_a_actualizar
                    )
                    enviar_notificacion("Éxito", "Producto actualizado correctamente")
                else:
                    enviar_notificacion("Info", "No hay cambios para actualizar")

                if producto_actualizado:
                    enviar_notificacion("Éxito", "Producto actualizado correctamente")
                    self.limpiar_formulario()
                    self.limpiar_tabla_productos()
                    self.mostrar_productos()
                    self.InputCantidadMin.setText("3")
                    self.InputCantidadMax.setText("99")
                    self.InputCodigo.setFocus()
                else:
                    enviar_notificacion(
                        "Error", "Hubo un problema al actualizar el producto"
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
        self.InputCodigo.setText("")
        self.InputNombre.setText("")
        self.InputPrecioCompra.setText("")
        self.InputCantidad.setText("")
        self.InputCantidadMin.setText("")
        self.InputCantidadMax.setText("")
        self.InputMarca.setText("")
        self.InputCategoria.setText("")
        self.InputPrecioUnitario.setText("")
        self.InputPrecioMayor.setText("")

    def limpiar_formulario_codigo(self):
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

    def eliminar_productos(self):
        """
        Elimina los productos seleccionados de la base de datos y actualiza la tabla.
        """
        ids = self.obtener_ids_seleccionados()

        if not ids:
            enviar_notificacion(
                "Advertencia", "No se seleccionaron productos para eliminar."
            )
            return

        respuesta = QtWidgets.QMessageBox.question(
            self,
            "Confirmar Eliminación",
            f"¿Está seguro de que desea eliminar {len(ids)} producto(s)?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
        )

        if respuesta == QtWidgets.QMessageBox.Yes:
            try:
                self.db = SessionLocal()

                # Eliminar los productos de la base de datos
                for id_producto in ids:
                    eliminar_producto(self.db, id_producto)

                self.db.commit()
                enviar_notificacion("Éxito", "Producto(s) eliminado(s) correctamente.")

                # Actualizar la tabla
                self.limpiar_tabla_productos()
                self.mostrar_productos()
                self.limpiar_formulario()
            except Exception as e:
                enviar_notificacion("Error", f"Error al eliminar productos: {e}")
            finally:
                self.db.close()
