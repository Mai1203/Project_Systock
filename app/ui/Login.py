# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Login.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Login(object):
    def setupUi(self, CONTENEDEDOR1):
        CONTENEDEDOR1.setObjectName("CONTENEDEDOR1")
        CONTENEDEDOR1.resize(815, 866)
        CONTENEDEDOR1.setMinimumSize(QtCore.QSize(0, 0))
        CONTENEDEDOR1.setStyleSheet("")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(CONTENEDEDOR1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.CONTENEDOR2 = QtWidgets.QWidget(CONTENEDEDOR1)
        self.CONTENEDOR2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.CONTENEDOR2.setObjectName("CONTENEDOR2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.CONTENEDOR2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.CONTENEDOR3 = QtWidgets.QWidget(self.CONTENEDOR2)
        self.CONTENEDOR3.setMinimumSize(QtCore.QSize(200, 0))
        self.CONTENEDOR3.setMaximumSize(QtCore.QSize(540, 1000))
        self.CONTENEDOR3.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.CONTENEDOR3.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.CONTENEDOR3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.CONTENEDOR3.setStyleSheet("")
        self.CONTENEDOR3.setObjectName("CONTENEDOR3")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.CONTENEDOR3)
        self.gridLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.widget_4 = QtWidgets.QWidget(self.CONTENEDOR3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_4.sizePolicy().hasHeightForWidth())
        self.widget_4.setSizePolicy(sizePolicy)
        self.widget_4.setMaximumSize(QtCore.QSize(16777215, 60))
        self.widget_4.setObjectName("widget_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget_4)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.BtnLogin = QtWidgets.QPushButton(self.widget_4)
        self.BtnLogin.setMinimumSize(QtCore.QSize(200, 0))
        self.BtnLogin.setMaximumSize(QtCore.QSize(500, 50))
        self.BtnLogin.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.BtnLogin.setStyleSheet("QPushButton {\n"
"    background-color: #000000; /* Fondo negro */\n"
"    color: #FFFFFF; /* Letra blanca */\n"
"    border: 2px solid #FFFFFF; /* Borde blanco */\n"
"    border-radius: 8px; /* Bordes redondeados */\n"
"    padding: 8px 16px; /* Espaciado interno */\n"
"    font-size: 20px; /* Tamaño de la letra */\n"
"    font-weight: bold; /* Letra en negrita */\n"
"    transition: all 0.3s ease; /* Transición suave para hover y pressed */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #444444; /* Fondo gris oscuro al pasar el mouse */\n"
"    transform: scale(1.05); /* Efecto de aumentar tamaño */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #555555; /* Fondo gris más claro al hacer clic */\n"
"    color: #FFFFFF; /* Letra blanca */\n"
"    border-color: #FFFFFF; /* Borde blanco */\n"
"    transform: scale(0.98); /* Efecto de reducir tamaño */\n"
"}\n"
"")
        self.BtnLogin.setObjectName("BtnLogin")
        self.verticalLayout_3.addWidget(self.BtnLogin)
        self.gridLayout_2.addWidget(self.widget_4, 8, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 11, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 220, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_2.addItem(spacerItem1, 11, 1, 1, 1)
        self.IMAGEN = QtWidgets.QLabel(self.CONTENEDOR3)
        self.IMAGEN.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(200)
        sizePolicy.setVerticalStretch(200)
        sizePolicy.setHeightForWidth(self.IMAGEN.sizePolicy().hasHeightForWidth())
        self.IMAGEN.setSizePolicy(sizePolicy)
        self.IMAGEN.setMaximumSize(QtCore.QSize(900, 300))
        self.IMAGEN.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.IMAGEN.setAutoFillBackground(False)
        self.IMAGEN.setStyleSheet("")
        self.IMAGEN.setText("")
        self.IMAGEN.setPixmap(QtGui.QPixmap("assets/logoladynail.jpg"))
        self.IMAGEN.setScaledContents(True)
        self.IMAGEN.setObjectName("IMAGEN")
        self.gridLayout_2.addWidget(self.IMAGEN, 1, 1, 1, 1)
        self.widget_3 = QtWidgets.QWidget(self.CONTENEDOR3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy)
        self.widget_3.setMaximumSize(QtCore.QSize(16777215, 60))
        self.widget_3.setObjectName("widget_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget_3)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.BtnRol = QtWidgets.QPushButton(self.widget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(50)
        sizePolicy.setHeightForWidth(self.BtnRol.sizePolicy().hasHeightForWidth())
        self.BtnRol.setSizePolicy(sizePolicy)
        self.BtnRol.setMinimumSize(QtCore.QSize(0, 0))
        self.BtnRol.setMaximumSize(QtCore.QSize(500, 50))
        self.BtnRol.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.BtnRol.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.BtnRol.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.BtnRol.setStyleSheet("QPushButton {\n"
"    background-color: #000000; /* Fondo negro */\n"
"    color: #FFFFFF; /* Letra blanca */\n"
"    border: 2px solid #FFFFFF; /* Borde blanco */\n"
"    border-radius: 8px; /* Bordes redondeados */\n"
"    padding: 8px 16px; /* Espaciado interno */\n"
"    font-size: 18px; /* Tamaño de la letra */\n"
"    font-weight: bold; /* Letra en negrita */\n"
"    transition: all 0.3s ease; /* Transición suave para hover y pressed */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #444444; /* Fondo gris oscuro al pasar el mouse */\n"
"    transform: scale(1.05); /* Efecto de aumentar tamaño */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #555555; /* Fondo gris más claro al hacer clic */\n"
"    color: #FFFFFF; /* Letra blanca */\n"
"    border-color: #FFFFFF; /* Borde blanco */\n"
"    transform: scale(0.98); /* Efecto de reducir tamaño */\n"
"}\n"
"")
        self.BtnRol.setObjectName("BtnRol")
        self.horizontalLayout_3.addWidget(self.BtnRol)
        self.gridLayout_2.addWidget(self.widget_3, 4, 1, 1, 1)
        self.widget_2 = QtWidgets.QWidget(self.CONTENEDOR3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy)
        self.widget_2.setMinimumSize(QtCore.QSize(510, 0))
        self.widget_2.setMaximumSize(QtCore.QSize(550, 70))
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.InputNombreUsuario = QtWidgets.QLineEdit(self.widget_2)
        self.InputNombreUsuario.setMaximumSize(QtCore.QSize(500, 70))
        self.InputNombreUsuario.setStyleSheet("QLineEdit {\n"
"    background-color: #FFFFFF;  /* Fondo blanco */\n"
"    border: 2px solid #D3D3D3;  /* Borde gris suave */\n"
"    border-radius: 10px;        /* Bordes redondeados */\n"
"    padding: 10px;              /* Espaciado interno */\n"
"    font-size: 18px;            /* Tamaño de la letra */\n"
"    font-family: \"Arial\", sans-serif; /* Fuente por defecto */\n"
"    color: #A9A9A9;             /* Letra gris suave */\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border-color: #000000;      /* Borde verde al hacer foco */\n"
"    background-color: #ffffff;  /* Fondo blanco al hacer foco */\n"
"    color: #000000;             /* Letra negra al escribir */\n"
"}")
        self.InputNombreUsuario.setText("")
        self.InputNombreUsuario.setObjectName("InputNombreUsuario")
        self.verticalLayout.addWidget(self.InputNombreUsuario)
        self.gridLayout_2.addWidget(self.widget_2, 5, 1, 1, 1)
        self.widget = QtWidgets.QWidget(self.CONTENEDOR3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QtCore.QSize(0, 0))
        self.widget.setMaximumSize(QtCore.QSize(16777215, 70))
        self.widget.setObjectName("widget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.InputPassword = QtWidgets.QLineEdit(self.widget)
        self.InputPassword.setMinimumSize(QtCore.QSize(450, 0))
        self.InputPassword.setMaximumSize(QtCore.QSize(370, 70))
        self.InputPassword.setStyleSheet("QLineEdit {\n"
"    background-color: #FFFFFF;  /* Fondo blanco */\n"
"    border: 2px solid #D3D3D3;  /* Borde gris suave */\n"
"    border-radius: 10px;        /* Bordes redondeados */\n"
"    padding: 10px;              /* Espaciado interno */\n"
"    font-size: 18px;            /* Tamaño de la letra */\n"
"    font-family: \"Arial\", sans-serif; /* Fuente por defecto */\n"
"    color: #A9A9A9;             /* Letra gris suave */\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border-color: #000000;      /* Borde verde al hacer foco */\n"
"    background-color: #ffffff;  /* Fondo blanco al hacer foco */\n"
"    color: #000000;             /* Letra negra al escribir */\n"
"}\n"
"")
        self.InputPassword.setText("")
        self.InputPassword.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.InputPassword.setObjectName("InputPassword")
        self.horizontalLayout_2.addWidget(self.InputPassword, 0, QtCore.Qt.AlignLeft)
        self.toolButton = QtWidgets.QToolButton(self.widget)
        self.toolButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.toolButton.setStyleSheet("QToolButton {\n"
"     background-color: #FFFFFF;  /* Fondo blanco */\n"
"        border: 2px solid #D3D3D3;  /* Borde gris suave */\n"
"     border-radius: 17px; \n"
"}\n"
"")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("assets/iconos/ojo_cerrado.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton.setIcon(icon)
        self.toolButton.setIconSize(QtCore.QSize(30, 30))
        self.toolButton.setObjectName("toolButton")
        self.horizontalLayout_2.addWidget(self.toolButton)
        self.gridLayout_2.addWidget(self.widget, 7, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 50, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.gridLayout_2.addItem(spacerItem2, 0, 1, 1, 1)
        self.horizontalLayout.addWidget(self.CONTENEDOR3)
        self.verticalLayout_2.addWidget(self.CONTENEDOR2)

        self.retranslateUi(CONTENEDEDOR1)
        QtCore.QMetaObject.connectSlotsByName(CONTENEDEDOR1)

    def retranslateUi(self, CONTENEDEDOR1):
        _translate = QtCore.QCoreApplication.translate
        CONTENEDEDOR1.setWindowTitle(_translate("CONTENEDEDOR1", "Form"))
        self.BtnLogin.setText(_translate("CONTENEDEDOR1", "Iniciar Sesion"))
        self.BtnRol.setText(_translate("CONTENEDEDOR1", "ADMINISTRADOR"))
        self.InputNombreUsuario.setPlaceholderText(_translate("CONTENEDEDOR1", "Usuario"))
        self.InputPassword.setPlaceholderText(_translate("CONTENEDEDOR1", "Contraseña"))
        self.toolButton.setText(_translate("CONTENEDEDOR1", "..."))
