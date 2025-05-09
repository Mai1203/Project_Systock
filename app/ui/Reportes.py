# Form implementation generated from reading ui file 'd:\SYSTOCK\SYSTOCK\DESARROLLO\python\SYS-Systock\app\ui\Reportes.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Reportes(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1379, 1083)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setStyleSheet("background-color: rgb(255, 255, 255);\n" "")
        self.gridLayout_2 = QtWidgets.QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.Contenedor = QtWidgets.QWidget(parent=Form)
        self.Contenedor.setStyleSheet(
            "\n"
            "QPushButton {\n"
            "    background-color: black; /* Fondo blanco */\n"
            "    border: none; /* Sin borde ni decoración inicial */\n"
            "    color:  white; /* Color del texto */\n"
            "    border-radius: 15px; /* Bordes circulares */\n"
            "    padding: 5px 10px; /* Espaciado interno para mejor apariencia */\n"
            "    height: 40px; /* Altura del botón */\n"
            "    text-align: center; /* Alinea el texto del botón a la izquierda */\n"
            "    font-size: 18px; /* Tamaño de fuente */\n"
            "    margin-top:20px;\n"
            "}\n"
            "\n"
            "QPushButton:hover {\n"
            "    background-color: rgb(106, 106, 106); /* Gris claro al pasar el mouse */\n"
            "    cursor: pointer; /* Cursor de mano al pasar sobre el botón */\n"
            "}\n"
            "\n"
            "QToolButton {\n"
            "    background-color: white; /* Fondo blanco */\n"
            "    border: none; /* Sin borde ni decoración inicial */\n"
            "    color:  rgb(50, 50, 50); /* Color del texto */\n"
            "    border-radius: 15px; /* Bordes circulares */\n"
            "    padding: 5px 10px; /* Espaciado interno para mejor apariencia */\n"
            "    height: 40px; /* Altura del botón */\n"
            "    text-align: left; /* Alinea el texto del botón a la izquierda */\n"
            "    font-size: 18px; /* Tamaño de fuente */\n"
            "    cursor: pointer;\n"
            "}\n"
            "\n"
            "QToolButton:hover {\n"
            "    background-color: #f2f2f2; /* Gris claro al pasar el mouse */\n"
            "    cursor: pointer;\n"
            "}\n"
            "QLineEdit {\n"
            "    background-color: rgb(255, 255, 255); /* Fondo blanco */\n"
            "    border: none; /* Sin bordes visibles */\n"
            "    padding: 4px; /* Espaciado interno entre el texto y los bordes */\n"
            "    margin-right: 5px; /* Espaciado externo solo a la derecha */\n"
            "    border-radius: 10px; /* Bordes redondeados */\n"
            "    color: black; /* Texto negro */\n"
            "    text-align: left; /* Texto alineado a la izquierda */\n"
            "    font-size: 18px; /* Tamaño del texto */\n"
            "}\n"
            "\n"
            "/* Cuando el QLineEdit está enfocado (se está escribiendo) */\n"
            "QLineEdit:focus {\n"
            "    background-color: rgb(230, 230, 250); /* Color de fondo cuando el campo está activo */\n"
            "    border: 1px solid rgb(0, 0, 0); /* Borde negro al estar activo */\n"
            "}\n"
            "\n"
            "QLabel {\n"
            "    font-size: 20px; /* Tamaño de fuente */\n"
            "    color:  black; /* Color del texto */\n"
            "    margin-right: 10px; /* Espaciado a la derecha */\n"
            "    padding: 5px; /* Espaciado interno */\n"
            "    text-align: left; /* Alineación del texto a la izquierda */\n"
            "}\n"
            "QTableWidget {\n"
            "    border: none;\n"
            "    background-color: #ffffff; /* Fondo blanco para la tabla */\n"
            "    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Sombra suave alrededor de la tabla */\n"
            "}\n"
            "\n"
            "QTableWidget::item {\n"
            "    background-color: #f2f2f2; \n"
            "    border: none; \n"
            "    transition: background-color 0.3s ease; /* Suavizado de transición de color de fondo */\n"
            "    pointer-events: none; /* Desactiva la interacción con las celdas (como editar) */\n"
            "}\n"
            "\n"
            "QTableWidget::item:selected {\n"
            "    background-color: #aad4ff; /* Color azul claro para celdas seleccionadas */\n"
            "    color: black; /* Texto negro para celdas seleccionadas */\n"
            "}\n"
            "\n"
            "QTableWidget::item:hover {\n"
            "    background-color: #e6e6e6; /* Color de fondo al pasar el cursor sobre las celdas */\n"
            "}\n"
            "\n"
            "QHeaderView::section {\n"
            "    border: none; \n"
            "    background-color: #f2f2f2; \n"
            "    font-weight: normal; /* No negritas */\n"
            "    text-align: center; /* Centrado del texto en los encabezados */\n"
            "    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Sombra suave para los encabezados */\n"
            "}\n"
            "\n"
            "QHeaderView::section:focus {\n"
            "    background-color: #f2f2f2; /* Sin color de fondo cuando está en foco */\n"
            "    border: none; /* Sin borde cuando está en foco */\n"
            "}\n"
            "\n"
            "QTableWidget::item:focus {\n"
            "    border: none; /* Sin borde cuando las celdas tienen el foco */\n"
            "    background-color: #f2f2f2; /* Mantener el fondo sin color azul */\n"
            "}\n"
            "\n"
            "QTableCornerButton::section {\n"
            "    background-color: #f2f2f2; \n"
            "    border: none; \n"
            "}\n"
            "\n"
            "QTableWidget::verticalHeader {\n"
            "    background-color: #f2f2f2;\n"
            "    border: none;\n"
            "    font-weight: normal; /* No negritas */\n"
            "}\n"
            "\n"
            "QTableWidget::item:hover {\n"
            "    background-color: #e6e6e6; /* Color de fondo al pasar el cursor sobre las celdas */\n"
            "}\n"
            "\n"
            "/* Personalización de la barra de desplazamiento */\n"
            "QScrollBar:vertical {\n"
            "    border: none;\n"
            "    background: #f7f7f7; /* Fondo de la barra */\n"
            "    width: 8px; /* Barra más delgada */\n"
            "    border-radius: 4px; /* Bordes más redondeados */\n"
            "}\n"
            "\n"
            "QScrollBar::handle:vertical {\n"
            "    background: #bbb; /* Fondo del control deslizante */\n"
            "    min-height: 20px; /* Control deslizante más delgado */\n"
            "    border-radius: 4px; /* Bordes redondeados */\n"
            "    transition: background-color 0.3s ease; /* Transición suave para el cambio de color */\n"
            "}\n"
            "\n"
            "QScrollBar::handle:vertical:hover {\n"
            "    background: #888; /* Color más oscuro cuando el control deslizante está siendo desplazado */\n"
            "}\n"
            "\n"
            "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {\n"
            "    border: none;\n"
            "    background: #f2f2f2; /* Fondo para los botones de la barra */\n"
            "    height: 0px; /* Sin altura para los botones */\n"
            "}\n"
            "\n"
            "QScrollBar:horizontal {\n"
            "    border: none;\n"
            "    background: #f7f7f7; /* Fondo de la barra */\n"
            "    height: 8px; /* Barra más delgada */\n"
            "    border-radius: 4px; /* Bordes más redondeados */\n"
            "}\n"
            "\n"
            "QScrollBar::handle:horizontal {\n"
            "    background: #bbb; /* Fondo del control deslizante */\n"
            "    min-width: 20px; /* Control deslizante más delgado */\n"
            "    border-radius: 4px; /* Bordes redondeados */\n"
            "    transition: background-color 0.3s ease; /* Transición suave para el cambio de color */\n"
            "}\n"
            "\n"
            "QScrollBar::handle:horizontal:hover {\n"
            "    background: #888; /* Color más oscuro cuando el control deslizante está siendo desplazado */\n"
            "}\n"
            "\n"
            "QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {\n"
            "    border: none;\n"
            "    background: #f2f2f2; /* Fondo para los botones de la barra */\n"
            "    width: 0px; /* Sin ancho para los botones */\n"
            "}\n"
            "\n"
            "\n"
            ""
        )
        self.Contenedor.setObjectName("Contenedor")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.Contenedor)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.Contenido = QtWidgets.QStackedWidget(parent=self.Contenedor)
        self.Contenido.setStyleSheet(
            "margin-left:10px;\n"
            "border-radius:15px;\n"
            "\n"
            "background-color: #f2f2f2; \n"
            "\n"
            ""
        )
        self.Contenido.setObjectName("Contenido")
        self.ContenidoPage1 = QtWidgets.QWidget()
        self.ContenidoPage1.setObjectName("ContenidoPage1")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.ContenidoPage1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget = QtWidgets.QWidget(parent=self.ContenidoPage1)
        self.widget.setStyleSheet("")
        self.widget.setObjectName("widget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.widget_2 = QtWidgets.QWidget(parent=self.widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy)
        self.widget_2.setMinimumSize(QtCore.QSize(0, 80))
        self.widget_2.setStyleSheet("")
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.LabelReportes = QtWidgets.QLabel(parent=self.widget_2)
        self.LabelReportes.setStyleSheet(
            "#LabelReportes\n"
            " {\n"
            "    font-weight: bold; /* Negrita */\n"
            "    font-size: 34px; /* Tamaño de fuente */\n"
            "}\n"
            ""
        )
        self.LabelReportes.setObjectName("LabelReportes")
        self.horizontalLayout_3.addWidget(self.LabelReportes)
        self.verticalLayout_3.addWidget(self.widget_2)
        self.widget_3 = QtWidgets.QWidget(parent=self.widget)
        self.widget_3.setStyleSheet("")
        self.widget_3.setObjectName("widget_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget_4 = QtWidgets.QWidget(parent=self.widget_3)
        self.widget_4.setStyleSheet("")
        self.widget_4.setObjectName("widget_4")
        self.gridLayout = QtWidgets.QGridLayout(self.widget_4)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(parent=self.widget_4)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setStyleSheet(
            "\n" "    font-size: 28px; /* Tamaño de fuente */\n" ""
        )
        self.label.setObjectName("label")
        self.gridLayout.addWidget(
            self.label,
            0,
            0,
            1,
            1,
            QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop,
        )
        self.label_2 = QtWidgets.QLabel(parent=self.widget_4)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QtCore.QSize(250, 50))
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(
            self.label_2, 1, 0, 1, 1, QtCore.Qt.AlignmentFlag.AlignLeft
        )
        self.CalendarioCaja = QtWidgets.QCalendarWidget(parent=self.widget_4)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.CalendarioCaja.sizePolicy().hasHeightForWidth()
        )
        self.CalendarioCaja.setSizePolicy(sizePolicy)
        self.CalendarioCaja.setObjectName("CalendarioCaja")
        self.gridLayout.addWidget(
            self.CalendarioCaja,
            7,
            0,
            1,
            1,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignTop,
        )
        self.BtnTicketCaja = QtWidgets.QPushButton(parent=self.widget_4)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.BtnTicketCaja.sizePolicy().hasHeightForWidth()
        )
        self.BtnTicketCaja.setSizePolicy(sizePolicy)
        self.BtnTicketCaja.setMinimumSize(QtCore.QSize(350, 70))
        self.BtnTicketCaja.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        )
        self.BtnTicketCaja.setStyleSheet(
            "\n"
            "QPushButton {\n"
            "    background-color: red; /* Fondo blanco */\n"
            "    border: none; /* Sin borde ni decoración inicial */\n"
            "    color:  white; /* Color del texto */\n"
            "    border-radius: 15px; /* Bordes circulares */\n"
            "    padding: 5px 10px; /* Espaciado interno para mejor apariencia */\n"
            "    height: 40px; /* Altura del botón */\n"
            "    text-align: center; /* Alinea el texto del botón a la izquierda */\n"
            "    font-size: 18px; /* Tamaño de fuente */\n"
            "    margin-top:20px;\n"
            "    cursor: pointer; /* Cursor de mano al pasar sobre el botón */\n"
            "}\n"
            "\n"
            "QPushButton:hover {\n"
            "    background-color: rgb(106, 106, 106); /* Gris claro al pasar el mouse */\n"
            "    cursor: pointer; /* Cursor de mano al pasar sobre el botón */\n"
            "}"
        )
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap("assets/iconos/pdf.png"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        self.BtnTicketCaja.setIcon(icon)
        self.BtnTicketCaja.setIconSize(QtCore.QSize(30, 30))
        self.BtnTicketCaja.setObjectName("BtnTicketCaja")
        self.gridLayout.addWidget(
            self.BtnTicketCaja, 8, 0, 1, 1, QtCore.Qt.AlignmentFlag.AlignHCenter
        )
        self.label_3 = QtWidgets.QLabel(parent=self.widget_4)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setMinimumSize(QtCore.QSize(250, 50))
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 5, 0, 1, 1)
        self.TipoCajaComboBox = QtWidgets.QComboBox(parent=self.widget_4)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.TipoCajaComboBox.sizePolicy().hasHeightForWidth()
        )
        self.TipoCajaComboBox.setSizePolicy(sizePolicy)
        self.TipoCajaComboBox.setMinimumSize(QtCore.QSize(250, 50))
        self.TipoCajaComboBox.setStyleSheet(
            "QComboBox {\n"
            "    background-color: white; /* Fondo blanco */\n"
            "    border: none; /* Sin borde */\n"
            "    color: black; /* Color del texto */\n"
            "    border-radius: 15px; /* Bordes redondeados */\n"
            "    padding: 5px 10px; /* Espaciado interno */\n"
            "    font-size: 18px; /* Tamaño de fuente */\n"
            "    height: 40px; /* Altura del combo box */\n"
            "    \n"
            "}\n"
            "\n"
            "QComboBox::drop-down {\n"
            "    background-color: transparent; /* Fondo transparente */\n"
            "    border: none; /* Sin borde */\n"
            "    width: 20px; /* Tamaño del botón */\n"
            "    /* No se define la flecha, por lo que se elimina */\n"
            "}\n"
            "\n"
            "QComboBox:hover {\n"
            "    cursor: pointer; /* Cursor de mano */\n"
            "}\n"
            "\n"
            "QComboBox QAbstractItemView {\n"
            "    background-color: white; /* Fondo del menú desplegable */\n"
            "    border: none; /* Sin borde */\n"
            "    color: black; /* Color del texto en las opciones */\n"
            "    selection-background-color: rgb(106, 106, 106); /* Fondo gris claro al seleccionar */\n"
            "    selection-color: white; /* Texto blanco al seleccionar */\n"
            "    border-radius: 10px; /* Bordes redondeados */\n"
            "}\n"
            ""
        )
        self.TipoCajaComboBox.setObjectName("TipoCajaComboBox")
        self.gridLayout.addWidget(self.TipoCajaComboBox, 2, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.gridLayout.addItem(spacerItem, 9, 0, 1, 1)
        self.TiempoCajaComboBox = QtWidgets.QComboBox(parent=self.widget_4)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.TiempoCajaComboBox.sizePolicy().hasHeightForWidth()
        )
        self.TiempoCajaComboBox.setSizePolicy(sizePolicy)
        self.TiempoCajaComboBox.setMinimumSize(QtCore.QSize(250, 50))
        self.TiempoCajaComboBox.setStyleSheet(
            "QComboBox {\n"
            "    background-color: white; /* Fondo blanco */\n"
            "    border: none; /* Sin borde */\n"
            "    color: black; /* Color del texto */\n"
            "    border-radius: 15px; /* Bordes redondeados */\n"
            "    padding: 5px 10px; /* Espaciado interno */\n"
            "    font-size: 18px; /* Tamaño de fuente */\n"
            "    height: 40px; /* Altura del combo box */\n"
            "    \n"
            "}\n"
            "\n"
            "QComboBox::drop-down {\n"
            "    background-color: transparent; /* Fondo transparente */\n"
            "    border: none; /* Sin borde */\n"
            "    width: 20px; /* Tamaño del botón */\n"
            "    /* No se define la flecha, por lo que se elimina */\n"
            "}\n"
            "\n"
            "QComboBox:hover {\n"
            "    cursor: pointer; /* Cursor de mano */\n"
            "}\n"
            "\n"
            "QComboBox QAbstractItemView {\n"
            "    background-color: white; /* Fondo del menú desplegable */\n"
            "    border: none; /* Sin borde */\n"
            "    color: black; /* Color del texto en las opciones */\n"
            "    selection-background-color: rgb(106, 106, 106); /* Fondo gris claro al seleccionar */\n"
            "    selection-color: white; /* Texto blanco al seleccionar */\n"
            "    border-radius: 10px; /* Bordes redondeados */\n"
            "}\n"
            ""
        )
        self.TiempoCajaComboBox.setObjectName("TiempoCajaComboBox")
        self.gridLayout.addWidget(self.TiempoCajaComboBox, 6, 0, 1, 1)
        self.horizontalLayout.addWidget(self.widget_4)
        self.widget_5 = QtWidgets.QWidget(parent=self.widget_3)
        self.widget_5.setStyleSheet("")
        self.widget_5.setObjectName("widget_5")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.widget_5)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_5 = QtWidgets.QLabel(parent=self.widget_5)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setStyleSheet(
            "\n" "    font-size: 28px; /* Tamaño de fuente */\n" ""
        )
        self.label_5.setObjectName("label_5")
        self.gridLayout_3.addWidget(
            self.label_5, 0, 0, 1, 1, QtCore.Qt.AlignmentFlag.AlignHCenter
        )
        self.BtnTicketProducto = QtWidgets.QPushButton(parent=self.widget_5)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.BtnTicketProducto.sizePolicy().hasHeightForWidth()
        )
        self.BtnTicketProducto.setSizePolicy(sizePolicy)
        self.BtnTicketProducto.setMinimumSize(QtCore.QSize(350, 70))
        self.BtnTicketProducto.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        )
        self.BtnTicketProducto.setStyleSheet(
            "\n"
            "QPushButton {\n"
            "    background-color: red; /* Fondo blanco */\n"
            "    border: none; /* Sin borde ni decoración inicial */\n"
            "    color:  white; /* Color del texto */\n"
            "    border-radius: 15px; /* Bordes circulares */\n"
            "    padding: 5px 10px; /* Espaciado interno para mejor apariencia */\n"
            "    height: 40px; /* Altura del botón */\n"
            "    text-align: center; /* Alinea el texto del botón a la izquierda */\n"
            "    font-size: 18px; /* Tamaño de fuente */\n"
            "    margin-top:20px;\n"
            "    cursor: pointer; /* Cursor de mano al pasar sobre el botón */\n"
            "}\n"
            "\n"
            "QPushButton:hover {\n"
            "    background-color: rgb(106, 106, 106); /* Gris claro al pasar el mouse */\n"
            "    cursor: pointer; /* Cursor de mano al pasar sobre el botón */\n"
            "}"
        )
        self.BtnTicketProducto.setIcon(icon)
        self.BtnTicketProducto.setIconSize(QtCore.QSize(30, 30))
        self.BtnTicketProducto.setObjectName("BtnTicketProducto")
        self.gridLayout_3.addWidget(self.BtnTicketProducto, 2, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.gridLayout_3.addItem(spacerItem1, 3, 0, 1, 1)
        self.TipoProductosComboBox = QtWidgets.QComboBox(parent=self.widget_5)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.TipoProductosComboBox.sizePolicy().hasHeightForWidth()
        )
        self.TipoProductosComboBox.setSizePolicy(sizePolicy)
        self.TipoProductosComboBox.setMinimumSize(QtCore.QSize(250, 50))
        self.TipoProductosComboBox.setStyleSheet(
            "QComboBox {\n"
            "    background-color: white; /* Fondo blanco */\n"
            "    border: none; /* Sin borde */\n"
            "    color: black; /* Color del texto */\n"
            "    border-radius: 15px; /* Bordes redondeados */\n"
            "    padding: 5px 10px; /* Espaciado interno */\n"
            "    font-size: 18px; /* Tamaño de fuente */\n"
            "    height: 40px; /* Altura del combo box */\n"
            "    \n"
            "}\n"
            "\n"
            "QComboBox::drop-down {\n"
            "    background-color: transparent; /* Fondo transparente */\n"
            "    border: none; /* Sin borde */\n"
            "    width: 20px; /* Tamaño del botón */\n"
            "    /* No se define la flecha, por lo que se elimina */\n"
            "}\n"
            "\n"
            "QComboBox:hover {\n"
            "    cursor: pointer; /* Cursor de mano */\n"
            "}\n"
            "\n"
            "QComboBox QAbstractItemView {\n"
            "    background-color: white; /* Fondo del menú desplegable */\n"
            "    border: none; /* Sin borde */\n"
            "    color: black; /* Color del texto en las opciones */\n"
            "    selection-background-color: rgb(106, 106, 106); /* Fondo gris claro al seleccionar */\n"
            "    selection-color: white; /* Texto blanco al seleccionar */\n"
            "    border-radius: 10px; /* Bordes redondeados */\n"
            "}\n"
            ""
        )
        self.TipoProductosComboBox.setObjectName("TipoProductosComboBox")
        self.gridLayout_3.addWidget(
            self.TipoProductosComboBox, 1, 0, 1, 1, QtCore.Qt.AlignmentFlag.AlignHCenter
        )
        self.horizontalLayout.addWidget(self.widget_5)
        self.widget_6 = QtWidgets.QWidget(parent=self.widget_3)
        self.widget_6.setStyleSheet("")
        self.widget_6.setObjectName("widget_6")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.widget_6)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.BtnTicketAnalisis = QtWidgets.QPushButton(parent=self.widget_6)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.BtnTicketAnalisis.sizePolicy().hasHeightForWidth()
        )
        self.BtnTicketAnalisis.setSizePolicy(sizePolicy)
        self.BtnTicketAnalisis.setMinimumSize(QtCore.QSize(350, 70))
        self.BtnTicketAnalisis.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        )
        self.BtnTicketAnalisis.setStyleSheet(
            "\n"
            "QPushButton {\n"
            "    background-color: red; /* Fondo blanco */\n"
            "    border: none; /* Sin borde ni decoración inicial */\n"
            "    color:  white; /* Color del texto */\n"
            "    border-radius: 15px; /* Bordes circulares */\n"
            "    padding: 5px 10px; /* Espaciado interno para mejor apariencia */\n"
            "    height: 40px; /* Altura del botón */\n"
            "    text-align: center; /* Alinea el texto del botón a la izquierda */\n"
            "    font-size: 18px; /* Tamaño de fuente */\n"
            "    margin-top:20px;\n"
            "    cursor: pointer; /* Cursor de mano al pasar sobre el botón */\n"
            "}\n"
            "\n"
            "QPushButton:hover {\n"
            "    background-color: rgb(106, 106, 106); /* Gris claro al pasar el mouse */\n"
            "    cursor: pointer; /* Cursor de mano al pasar sobre el botón */\n"
            "}"
        )
        self.BtnTicketAnalisis.setIcon(icon)
        self.BtnTicketAnalisis.setIconSize(QtCore.QSize(30, 30))
        self.BtnTicketAnalisis.setObjectName("BtnTicketAnalisis")
        self.gridLayout_4.addWidget(
            self.BtnTicketAnalisis, 6, 0, 1, 1, QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.label_6 = QtWidgets.QLabel(parent=self.widget_6)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setStyleSheet(
            "\n" "    font-size: 28px; /* Tamaño de fuente */\n" ""
        )
        self.label_6.setObjectName("label_6")
        self.gridLayout_4.addWidget(
            self.label_6, 0, 0, 1, 1, QtCore.Qt.AlignmentFlag.AlignLeft
        )
        self.label_8 = QtWidgets.QLabel(parent=self.widget_6)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setMinimumSize(QtCore.QSize(250, 50))
        self.label_8.setObjectName("label_8")
        self.gridLayout_4.addWidget(self.label_8, 3, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(parent=self.widget_6)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setMinimumSize(QtCore.QSize(250, 50))
        self.label_7.setObjectName("label_7")
        self.gridLayout_4.addWidget(self.label_7, 1, 0, 1, 1)
        self.ReporteAnalisisComboBox = QtWidgets.QComboBox(parent=self.widget_6)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.ReporteAnalisisComboBox.sizePolicy().hasHeightForWidth()
        )
        self.ReporteAnalisisComboBox.setSizePolicy(sizePolicy)
        self.ReporteAnalisisComboBox.setMinimumSize(QtCore.QSize(250, 50))
        self.ReporteAnalisisComboBox.setStyleSheet(
            "QComboBox {\n"
            "    background-color: white; /* Fondo blanco */\n"
            "    border: none; /* Sin borde */\n"
            "    color: black; /* Color del texto */\n"
            "    border-radius: 15px; /* Bordes redondeados */\n"
            "    padding: 5px 10px; /* Espaciado interno */\n"
            "    font-size: 18px; /* Tamaño de fuente */\n"
            "    height: 40px; /* Altura del combo box */\n"
            "    \n"
            "}\n"
            "\n"
            "QComboBox::drop-down {\n"
            "    background-color: transparent; /* Fondo transparente */\n"
            "    border: none; /* Sin borde */\n"
            "    width: 20px; /* Tamaño del botón */\n"
            "    /* No se define la flecha, por lo que se elimina */\n"
            "}\n"
            "\n"
            "QComboBox:hover {\n"
            "    cursor: pointer; /* Cursor de mano */\n"
            "}\n"
            "\n"
            "QComboBox QAbstractItemView {\n"
            "    background-color: white; /* Fondo del menú desplegable */\n"
            "    border: none; /* Sin borde */\n"
            "    color: black; /* Color del texto en las opciones */\n"
            "    selection-background-color: rgb(106, 106, 106); /* Fondo gris claro al seleccionar */\n"
            "    selection-color: white; /* Texto blanco al seleccionar */\n"
            "    border-radius: 10px; /* Bordes redondeados */\n"
            "}\n"
            ""
        )
        self.ReporteAnalisisComboBox.setObjectName("ReporteAnalisisComboBox")
        self.gridLayout_4.addWidget(self.ReporteAnalisisComboBox, 2, 0, 1, 1)
        self.CalendarioAnalisis = QtWidgets.QCalendarWidget(parent=self.widget_6)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.CalendarioAnalisis.sizePolicy().hasHeightForWidth()
        )
        self.CalendarioAnalisis.setSizePolicy(sizePolicy)
        self.CalendarioAnalisis.setObjectName("CalendarioAnalisis")
        self.gridLayout_4.addWidget(
            self.CalendarioAnalisis,
            5,
            0,
            1,
            1,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )
        spacerItem2 = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.gridLayout_4.addItem(spacerItem2, 7, 0, 1, 1)
        self.TiempoAnalisisComboBox = QtWidgets.QComboBox(parent=self.widget_6)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.TiempoAnalisisComboBox.sizePolicy().hasHeightForWidth()
        )
        self.TiempoAnalisisComboBox.setSizePolicy(sizePolicy)
        self.TiempoAnalisisComboBox.setMinimumSize(QtCore.QSize(250, 50))
        self.TiempoAnalisisComboBox.setStyleSheet(
            "QComboBox {\n"
            "    background-color: white; /* Fondo blanco */\n"
            "    border: none; /* Sin borde */\n"
            "    color: black; /* Color del texto */\n"
            "    border-radius: 15px; /* Bordes redondeados */\n"
            "    padding: 5px 10px; /* Espaciado interno */\n"
            "    font-size: 18px; /* Tamaño de fuente */\n"
            "    height: 40px; /* Altura del combo box */\n"
            "    \n"
            "}\n"
            "\n"
            "QComboBox::drop-down {\n"
            "    background-color: transparent; /* Fondo transparente */\n"
            "    border: none; /* Sin borde */\n"
            "    width: 20px; /* Tamaño del botón */\n"
            "    /* No se define la flecha, por lo que se elimina */\n"
            "}\n"
            "\n"
            "QComboBox:hover {\n"
            "    cursor: pointer; /* Cursor de mano */\n"
            "}\n"
            "\n"
            "QComboBox QAbstractItemView {\n"
            "    background-color: white; /* Fondo del menú desplegable */\n"
            "    border: none; /* Sin borde */\n"
            "    color: black; /* Color del texto en las opciones */\n"
            "    selection-background-color: rgb(106, 106, 106); /* Fondo gris claro al seleccionar */\n"
            "    selection-color: white; /* Texto blanco al seleccionar */\n"
            "    border-radius: 10px; /* Bordes redondeados */\n"
            "}\n"
            ""
        )
        self.TiempoAnalisisComboBox.setObjectName("TiempoAnalisisComboBox")
        self.gridLayout_4.addWidget(self.TiempoAnalisisComboBox, 4, 0, 1, 1)
        self.horizontalLayout.addWidget(self.widget_6)
        self.verticalLayout_3.addWidget(self.widget_3)
        self.verticalLayout_2.addWidget(self.widget)
        self.Contenido.addWidget(self.ContenidoPage1)
        self.horizontalLayout_2.addWidget(self.Contenido)
        self.gridLayout_2.addWidget(self.Contenedor, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.LabelReportes.setText(_translate("Form", "Reportes"))
        self.label.setText(_translate("Form", "Reporte de Caja"))
        self.label_2.setText(_translate("Form", "Caja"))
        self.BtnTicketCaja.setText(_translate("Form", "   Generar PDF"))
        self.label_3.setText(_translate("Form", "Tiempo"))
        self.label_5.setText(_translate("Form", "Reporte de Productos"))
        self.BtnTicketProducto.setText(_translate("Form", "   Generar PDF"))
        self.BtnTicketAnalisis.setText(_translate("Form", "Exportar PDF"))
        self.label_6.setText(_translate("Form", "Analisis de Venta"))
        self.label_8.setText(_translate("Form", "Tiempo"))
        self.label_7.setText(_translate("Form", "Ventas"))
