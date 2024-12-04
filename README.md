# Sistema de Gestión de Inventarios y Ventas

## Descripción

Este es un **sistema completo de gestión de inventarios y ventas**, diseñado para automatizar tareas clave como el seguimiento de inventarios, la generación de facturas y reportes, la gestión de ventas a crédito y la seguridad del acceso al sistema.

El proyecto está desarrollado en **Python** y utiliza diversas librerías para manejar funciones avanzadas como escaneo de códigos de barras, generación de reportes en PDF y gráficos interactivos.

---

## Características Principales

- **Gestión de Inventarios**:
  - Escaneo y generación de códigos de barras.
  - Alertas y notificaciones en tiempo real.
  - Exportación de datos a Excel y generación de reportes en PDF.

- **Facturación y Generación de Tickets**:
  - Generación de facturas electrónicas y tickets.
  - Cálculo de descuentos y totales con alta precisión.
  - Impresión directa a través de impresoras locales.

- **Gestión de Ventas a Crédito**:
  - Seguimiento de pagos y deudas.
  - Notificaciones automáticas de recordatorios de pagos.
  - Visualización de transacciones en tiempo real.

- **Reportes y Análisis**:
  - Gráficos financieros interactivos.
  - Análisis detallado de inventarios y ventas.
  - Exportación de reportes en Excel y PDF.

- **Seguridad y Control de Acceso**:
  - Autenticación con **JWT**.
  - Manejo seguro de contraseñas con **bcrypt**.
  - Registro de auditorías y roles personalizados.

---

## Estructura del Proyecto

```plaintext
inventario_proyecto/
├── docs/                             # Documentación del proyecto
├── app/                              # Código fuente
│   ├── models/                      # Definición de los modelos de datos
│   ├── inventory/                   # Gestión de inventarios
|   ├── controllers/                 # Lógica de negocio y manejo de datos
│   ├── routes/                      # Definición de rutas para cada funcionalidad
│   ├── sales/                       # Facturación y ventas
│   ├── credit/                      # Ventas a crédito
│   ├── reports/                     # Reportes y análisis
│   ├── utils/                       # Funciones auxiliares y herramientas
│   └── security/                    # Seguridad y autenticación
├── tests/                            # Pruebas unitarias
├── requirements.txt                  # Dependencias del proyecto
├── README.md                         # Este archivo
└── setup.py                          # Configuración del paquete
