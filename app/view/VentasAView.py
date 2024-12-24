from PyQt5.QtWidgets import (
    QMessageBox,
    QWidget
)
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
        # Conectar evento del input para escanear el código
        self.InputCodigo.returnPressed.connect(self.procesar_codigo)

    def procesar_codigo(self):
        """
        Procesa el código ingresado en el campo InputCodigo.
        Obtiene el nombre, la marca y el precio unitario del producto asociado.
        """
        codigo = self.InputCodigo.text().strip()

        if not codigo:
            QMessageBox.warning(self, "Error", "Por favor, ingrese un código válido.")
            return

        try:
            # Conexión a la base de datos
            db = SessionLocal()

            # Llamada a la función que obtiene el producto por código usando la función definida
            producto = obtener_producto_por_id(db, int(codigo))  # Convierte el código a entero si es necesario

            if producto:
                # Mostrar el código en el campo InputCodigo para asegurarse que se lee correctamente
                self.InputCodigo.setText(codigo)  # Esto actualizará el campo con el código ingresado

                # Actualiza los campos con la información del producto
                self.InputNombre.setText(producto.Nombre)
                self.InputMarca.setText(str(producto.ID_Marca))  # Ajusta si necesitas el nombre de la marca
                self.InputPrecioUnitario.setText(str(producto.Precio_venta_normal))
                id_categoria = producto.ID_Categoria  # Ajusta según el nombre de la propiedad en tu modelo

            else:
                QMessageBox.warning(self, "Producto no encontrado", "No existe un producto asociado a este código.")

            db.close()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al buscar el producto: {str(e)}")
            
    