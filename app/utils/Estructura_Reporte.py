from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from datetime import datetime
from tkinter import Tk, filedialog
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from reportlab.lib.units import inch
from reportlab.graphics.charts.piecharts import Pie
from reportlab.pdfgen import canvas
from datetime import datetime
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.pdfgen import canvas
from matplotlib.backends.backend_pdf import PdfPages
from reportlab.platypus import Image


def generar_pdf_caja_ingresos(caja, ingresos):
    """Genera un PDF estilizado con la información de la caja y los ingresos registrados."""
    
    try:
        # Obtener la fecha actual para el nombre del archivo
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        nombre_archivo = f"Caja_Ingresos_{fecha_actual}.pdf"

        # Abrir un diálogo para elegir dónde guardar el archivo
        ruta_archivo, _ = QFileDialog.getSaveFileName(None, "Guardar Reporte", nombre_archivo, "Archivos PDF (*.pdf)")

        # Si el usuario cancela, salir de la función
        if not ruta_archivo:
            print("El usuario canceló la selección del archivo.")
            return

        if not ruta_archivo.endswith('.pdf'):
            ruta_archivo += '.pdf'  # Asegurar la extensión .pdf

        # Crear el documento PDF
        doc = SimpleDocTemplate(ruta_archivo, pagesize=letter)
        elementos = []

        # Estilos de texto
        estilos = getSampleStyleSheet()
        estilo_titulo = estilos["Title"]
        estilo_negrita = ParagraphStyle(name="Bold", parent=estilos["Normal"], fontSize=12, textColor=colors.black, spaceAfter=10)

        # Título del reporte
        elementos.append(Paragraph("<b>📄 Reporte de Caja e Ingresos</b>", estilo_titulo))
        elementos.append(Spacer(1, 0.3 * inch))

        # Información de la Caja en tabla
        datos_caja = [
            ["Fecha Apertura:", caja.Fecha_Apertura],
            ["Fecha Cierre:", caja.Fecha_Cierre],
            ["Monto Inicial:", f"${caja.Monto_Base}"],
            ["Monto Final:", f"${caja.Monto_Final_calculado}"],
        ]

        tabla_caja = Table(datos_caja, colWidths=[150, 250])
        tabla_caja.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, -1), colors.red),  # Fondo rojo para la primera columna (izquierda)
            ("TEXTCOLOR", (0, 0), (0, -1), colors.whitesmoke),  # Texto blanco en la primera columna

            ("BACKGROUND", (1, 0), (1, -1), colors.beige),  # Fondo beige para la segunda columna (derecha)
            ("TEXTCOLOR", (1, 0), (1, -1), colors.black),  # Texto negro en la segunda columna

            ("ALIGN", (0, 0), (-1, -1), "LEFT"),  # Alinear texto a la izquierda
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 11),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),  # Bordes negros para toda la tabla
        ]))

        elementos.append(tabla_caja)
        elementos.append(Spacer(1, 0.5 * inch))

        # Tabla de Ingresos
        elementos.append(Paragraph("<b>📊 Ingresos Registrados:</b>", estilo_negrita))

        # Definir encabezados de la tabla
        datos_ingresos = [["ID", "Tipo", "M.Efectivo", "M.Transferencia", "Total"]]

        # Agregar datos de ingresos
        for ingreso in ingresos:
            monto_efectivo = ingreso.monto_efectivo if ingreso.monto_efectivo is not None else 0
            monto_transaccion = ingreso.monto_transaccion if ingreso.monto_transaccion is not None else 0
            total = monto_efectivo + monto_transaccion  # Sumar siempre valores numéricos

            datos_ingresos.append([
                ingreso.ID_Ingreso,
                ingreso.tipo_ingreso,
                f"${monto_efectivo:,.2f}",
                f"${monto_transaccion:,.2f}",
                f"${total:,.2f}"
            ])

        # Calcular totales
        total_efectivo = sum(i.monto_efectivo if i.monto_efectivo is not None else 0 for i in ingresos)
        total_transferencia = sum(i.monto_transaccion if i.monto_transaccion is not None else 0 for i in ingresos)
        total_general = total_efectivo + total_transferencia

        # Agregar fila de totales
        datos_ingresos.append(["", "TOTAL", f"${total_efectivo:,.2f}", f"${total_transferencia:,.2f}", f"${total_general:,.2f}"])

        # Crear la tabla con mejor diseño
        tabla_ingresos = Table(datos_ingresos, colWidths=[50, 100, 100, 100, 100])

        tabla_ingresos.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.red),  # Encabezado azul oscuro
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),  # Letras blancas en el encabezado
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 12),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
            
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),  # Fondo beige para las filas
            ("GRID", (0, 0), (-1, -1), 1, colors.black),

            ("BACKGROUND", (0, -1), (-1, -1), colors.lightgrey),  # Fondo gris para la fila de totales
            ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
            ("TEXTCOLOR", (0, -1), (-1, -1), colors.black),
        ]))

        elementos.append(tabla_ingresos)
        elementos.append(Spacer(1, 0.5 * inch))

                # Sumar los montos de efectivo y transferencia, asegurando que no sean None
        total_efectivo = sum(i.monto_efectivo if i.monto_efectivo is not None else 0 for i in ingresos)
        total_transferencia = sum(i.monto_transaccion if i.monto_transaccion is not None else 0 for i in ingresos)

        # Calcular el total combinado
        total_general = total_efectivo + total_transferencia

        # Calcular los porcentajes
        porcentaje_efectivo = (total_efectivo / total_general) * 100 if total_general > 0 else 0
        porcentaje_transferencia = (total_transferencia / total_general) * 100 if total_general > 0 else 0

        # Crear el dibujo para el gráfico de pastel
        dibujo = Drawing(400, 200)

        # Crear el gráfico de pastel
        grafico_pastel = Pie()
        grafico_pastel.x = 50
        grafico_pastel.y = 50
        grafico_pastel.width = 300
        grafico_pastel.height = 125

        # Datos del gráfico de pastel (Efectivo y Transferencia)
        grafico_pastel.data = [total_efectivo, total_transferencia]

        # Etiquetas con los porcentajes
        grafico_pastel.labels = [
            f'Efectivo: {porcentaje_efectivo:.2f}%',  # Efectivo con porcentaje
            f'Transferencia: {porcentaje_transferencia:.2f}%'  # Transferencia con porcentaje
        ]

        # Colores de las porciones del gráfico
        grafico_pastel.slices[0].fillColor = colors.beige # Efectivo
        grafico_pastel.slices[1].fillColor = colors.lightgrey  # Transferencia

        # Agregar el gráfico de pastel al dibujo
        dibujo.add(grafico_pastel)

        # Agregar el gráfico y el espaciado al documento
        elementos.append(dibujo)
        elementos.append(Spacer(1, 0.5 * inch))

        # Pie de página
        pie_pagina = Paragraph(f"<i>🔹 Reporte generado el {fecha_actual}.</i>", estilos["Italic"])
        elementos.append(pie_pagina)

        # Construir el PDF
        doc.build(elementos)

        # Confirmación de éxito
        QMessageBox.information(None, "Reporte Generado", f" PDF generado con éxito: {ruta_archivo}")

    except Exception as e:
        print(f"Error al generar el PDF: {e}")
        QMessageBox.critical(None, "Error", f"Error al generar el PDF: {e}")

def crear_pdf(ruta_archivo, productos, tipo):
    # Verificar que los parámetros sean correctos
    print(f"Ruta del archivo: {ruta_archivo}")
    print(f"Tipo de reporte: {tipo}")
    print(f"Productos recibidos: {productos}")

    # Crear un documento PDF
    doc = SimpleDocTemplate(ruta_archivo, pagesize=letter)
    elementos = []
    
    # Estilos de texto
    estilos = getSampleStyleSheet()

    # Título del documento según el tipo
    if tipo == "Bajo Stock":
        titulo = Paragraph("📌 <b>Reporte de Productos con Bajo Stock</b>", estilos['Title'])
    elif tipo == "Inactivos":
        titulo = Paragraph("📌 <b>Reporte de Productos Inactivos y Activos</b>", estilos['Title'])
    else:
        titulo = Paragraph("📌 <b>Reporte de Productos</b>", estilos['Title'])
    
    # Agregar el título al documento
    elementos.append(titulo)
    print("Título agregado.")
    elementos.append(Spacer(1, 0.3 * inch))  # Espacio entre título y tabla

    # Definir encabezados de la tabla
    if tipo == "Bajo Stock":
        data = [["ID", "Nombre", "Stock"]]
    elif tipo == "Inactivos":
        data = [["ID", "Nombre", "Estado"]]  # Mostramos estado en lugar de stock

    # Verificar que los datos de los productos estén correctamente estructurados
    print("Agregando productos a la tabla:")
    for producto in productos:
        print(f"Producto: {producto}")
        data.append([producto[0], producto[1], producto[2]])

    # Crear tabla
    table = Table(data, colWidths=[1.7 * inch, 2.8 * inch, 1 * inch])

    # Estilos de la tabla
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.red),  # Fondo rojo para encabezados
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Texto blanco para encabezados
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),  # Fondo gris para filas
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Líneas negras en la tabla
    ])
    table.setStyle(style)

    # Agregar tabla a la lista de elementos
    elementos.append(table)
    print("Tabla agregada al documento.")

    # Construir el PDF (maneja automáticamente múltiples páginas)
    doc.build(elementos)

    print("✅ PDF generado con éxito en:", ruta_archivo)

def generar_pdf_productos_mas_vendidos(productos):
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    default_filename = f"Productos_Mas_Vendido_{fecha_actual}.pdf"

    file_path = filedialog.asksaveasfilename(
        defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")],
        initialfile=default_filename,
        title=f"Guardar Reporte productos mas vendidos"
    )

    if not file_path:
        print("Operación cancelada.")
        return

    doc = SimpleDocTemplate(file_path, pagesize=letter)
    styles = getSampleStyleSheet()

    # Estilos personalizados
    titulo_style = styles["h1"]
    titulo_style.alignment = 1  # Centrado
    titulo_style.textColor = colors.black
    titulo_style.fontName = 'Helvetica-Bold'  # Negrita

    fecha_style = ParagraphStyle(
        'Fecha',
        parent=styles['Normal'],
        fontSize=10,
        alignment=2,  # Alineado a la derecha
        textColor=colors.grey
    )

    encabezado_style = ParagraphStyle(
        'Encabezado',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        textColor=colors.white,
        backColor=colors.red,
        paddingLeft=6,
        paddingRight=6,
        paddingTop=4,
        paddingBottom=4,
    )

    tabla_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.red),  # Encabezado rojo
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Texto blanco en el encabezado
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),  # Centrar texto en el encabezado
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fuente en negrita para el encabezado
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Espacio inferior en el encabezado
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Filas alternas de color beige
        ('GRID', (0, 0), (-1, -1), 1, colors.black)  # Bordes de la tabla
    ])

    story = []

    # Logo
    logo_path = "assets/logo.png"  # Ajusta la ruta
    try:
        img = ImageReader(logo_path)
        story.append(Image(img, width=100, height=100))
        story.append(Spacer(1, 0.2*inch))  # Espacio después del logo
    except Exception as e:
        print(f"Error al cargar el logo: {e}")

    # Título
    titulo = Paragraph("Reporte de Productos Más Vendidos", titulo_style)
    story.append(titulo)
    story.append(Spacer(1, 0.1*inch))  # Espacio después del título

    # Fecha
    fecha = Paragraph(f"Fecha de Exportación: {fecha_actual}", fecha_style)
    story.append(fecha)
    story.append(Spacer(1, 0.2*inch))  # Espacio después de la fecha

    # Tabla
    data = [["ID", "Nombre", "Unidades Vendidas"]]  # Encabezado de la tabla
    for producto in productos:
        data.append([producto.ID_Producto, producto.Nombre, producto.Total_Unidades_Vendidas])

    table = Table(data)
    table.setStyle(tabla_style)
    story.append(table)
    story.append(Spacer(1, 0.2*inch))  # Espacio después de la tabla

    # Top 3 de productos más vendidos (si hay suficientes productos)
    if len(productos) >= 3:
        top_3 = productos[:3]
        top_3_data = [["Posición", "Nombre", "Unidades Vendidas"]]
        for i, producto in enumerate(top_3):
            top_3_data.append([i+1, producto.Nombre, producto.Total_Unidades_Vendidas])

        top_3_table = Table(top_3_data)
        top_3_table.setStyle(tabla_style)
       # The above code is creating a paragraph object titled "Top 3 Productos Más Vendidos" with the
       # style "h2" and appending it to a story.
       
        story.append(top_3_table)

    doc.build(story)
    print(f"Reporte guardado en {file_path}")
    QMessageBox.information(None, "Reporte generado", f"Reporte de productos mas vendidos guardado correctamente")

def generar_analisis_financiero(analisis, ingresos, egresos_lista):
    # Obtener la fecha actual para el nombre del archivo
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    nombre_pdf = f"Analisis_financiero_{fecha_actual}.pdf"
    
    # Calcular los totales
    total_ingresos = sum([ingreso[4] for ingreso in ingresos])
    total_egresos = sum([egreso[2] for egreso in egresos_lista])
    ganancias = sum([item[5] for item in analisis])  # Ganancias Totales (Ingresos Brutos)

    # Calcular las operaciones adicionales
    ingresos_menos_egresos = total_ingresos - total_egresos
    ganancias_menos_egresos = ganancias - total_egresos

    # Crear el documento PDF
    doc = SimpleDocTemplate(nombre_pdf, pagesize=letter)
    elements = []

    # Título del análisis
    title = Paragraph(f"<font size=18><b>Análisis Financiero</b></font>", style=ParagraphStyle(name='Title', fontName='Helvetica-Bold'))
    elements.append(title)
    elements.append(Spacer(1, 12))

    # Fecha de generación
    date_info = Paragraph(f"Fecha de Generación: {fecha_actual}", style=ParagraphStyle(name='Date', fontName='Helvetica'))
    elements.append(date_info)
    elements.append(Spacer(1, 12))
    # Título para la tabla de ingresos
    # Título para la tabla de ingresos centrado
    titulo_ingresos = Paragraph("<font size=12><b>Tabla de Ingresos</b></font>", 
                                style=ParagraphStyle(name='TitleTabla', fontName='Helvetica-Bold', alignment=1))
    elements.append(titulo_ingresos)
    elements.append(Spacer(1, 6))  # Espacio debajo del título
    # Tabla de Ingresos
    data_ingresos = [["ID", "Tipo", "Monto"]]
    for ingreso in ingresos:
        data_ingresos.append([ingreso[0], ingreso[2], f"${ingreso[4]:,.2f}"])
    t_ingresos = Table(data_ingresos)
    t_ingresos.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                    ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
    elements.append(t_ingresos)
    elements.append(Spacer(1, 12))
    
    # Título para la tabla de ingresos
    # Título para la tabla de ingresos centrado
    titulo_ingresos = Paragraph("<font size=12><b>Tabla de Egresos</b></font>", 
                                style=ParagraphStyle(name='TitleTabla', fontName='Helvetica-Bold', alignment=1))
    elements.append(titulo_ingresos)
    elements.append(Spacer(1, 6))  # Espacio debajo del título
    # Tabla de Egresos
    data_egresos = [["ID", "Tipo", "Monto"]]
    for egreso in egresos_lista:
        data_egresos.append([egreso[0], egreso[1], f"${egreso[2]:,.2f}"])
    t_egresos = Table(data_egresos)
    t_egresos.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                    ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
    elements.append(t_egresos)
    elements.append(Spacer(1, 12))

    # Resumen de Ingresos y Ganancias
    resumen = Paragraph(f"<font size=12><b>Ingres Neto:</b></font>", style=ParagraphStyle(name='Resumen', fontName='Helvetica-Bold'))
    elements.append(resumen)
    elements.append(Spacer(1, 6))

    for item in analisis:
        elements.append(Paragraph(f"Factura ID: {item[0]}, Ganancia: ${item[5]:,.2f}", style=ParagraphStyle(name='ResumenDetalle', fontName='Helvetica')))
        elements.append(Spacer(1, 6))

    # Resultados finales
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"<font size=12><b>Ganancias Totales: ${ganancias:,.2f}</b></font>", style=ParagraphStyle(name='Resultado', fontName='Helvetica-Bold')))
    elements.append(Spacer(1, 6))

    # Operaciones finales
    elements.append(Paragraph(f"<font size=12><b>Ingresos - Egresos: ${ingresos_menos_egresos:,.2f}</b></font>", style=ParagraphStyle(name='Resultado', fontName='Helvetica-Bold')))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph(f"<font size=12><b>Ganancias Totales - Egresos: ${ganancias_menos_egresos:,.2f}</b></font>", style=ParagraphStyle(name='Resultado', fontName='Helvetica-Bold')))
    elements.append(Spacer(1, 12))

    # Generar gráfico de pastel
    fig, ax = plt.subplots()
    labels = ['Ganancias', 'Egresos']
    sizes = [ganancias, total_egresos]
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#66ff66', '#ff6666'])
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Guardar gráfico como imagen
    chart_filename = "grafico_pastel2.png"
    plt.savefig(chart_filename, format='png')
    plt.close(fig)  # Cerrar el gráfico

    titulo_distribucion = Paragraph("<font size=12><b>Distribución de Ganancias y Egresos:</b></font>", 
                                    style=ParagraphStyle(name='GraphTitle', fontName='Helvetica-Bold', alignment=1))
    elements.append(Spacer(1, 12))  # Espacio antes del título
    elements.append(titulo_distribucion)  # Agregar título centrado
    elements.append(Spacer(1, 6))  # Espacio debajo del título
      # Insertar imagen del gráfico usando Image de reportlab.platypus
    img = Image(chart_filename, width=400, height=250)
    elements.append(img)
    
    # Generar gráfico de pastel
    fig, ax = plt.subplots()
    labels = ['Ingresos', 'Egresos']
    sizes = [total_ingresos, total_egresos]
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#66b3ff', '#ff6666'])
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Guardar gráfico como imagen
    chart_filename = "grafico_pastel.png"
    plt.savefig(chart_filename, format='png')
    plt.close(fig)  # Cerrar el gráfico

    # Centrar el título "Distribución de Ingresos y Egresos"
    titulo_distribucion = Paragraph("<font size=12><b>Distribución de ingresos y Egresos:</b></font>", 
                                    style=ParagraphStyle(name='GraphTitle', fontName='Helvetica-Bold', alignment=1))
    elements.append(Spacer(1, 12))  # Espacio antes del título
    elements.append(titulo_distribucion)  # Agregar título centrado
    elements.append(Spacer(1, 6))  # Espacio debajo del título

     # Insertar imagen del gráfico usando Image de reportlab.platypus
    img = Image(chart_filename, width=400, height=250)
    elements.append(img)
    
    # Crear PDF
    doc.build(elements)

    print(f"PDF generado exitosamente: {nombre_pdf}")
