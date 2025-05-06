from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.graphics.shapes import Drawing
from reportlab.lib.units import inch
from reportlab.graphics.charts.piecharts import Pie
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.platypus import Image
from reportlab.platypus import PageBreak, KeepTogether
from datetime import datetime
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from tkinter import  filedialog
from tkinter import messagebox
from datetime import datetime
import matplotlib.pyplot as plt
import tkinter as tk
import numpy as np
import os
import tempfile


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
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    
    default_filename = f"Analisis_financiero_{fecha_actual}.pdf"
    
    file_path = filedialog.asksaveasfilename(
        defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")],
        initialfile=default_filename,
        title="Guardar Reporte productos más vendidos"
    )

    if not file_path:
        print("Operación cancelada.")
        return

    save_dir = os.path.dirname(file_path) 
    
    try:
        total_ingresos_efectivo = sum([ingreso[3] for ingreso in ingresos if ingreso[2] == "Venta"])
        print("Total Efectivo:",total_ingresos_efectivo) 
        total_ingresos_transferencia = sum([ingreso[4] for ingreso in ingresos if ingreso[2] == "Venta"])
        print("Total Transferencia:",total_ingresos_transferencia) 
        total_ingresos = total_ingresos_efectivo + total_ingresos_transferencia
    except Exception as e:
        print(f"Error al extraer datos: {e}")
    
    total_egresos = sum([egreso[2] for egreso in egresos_lista])
    total_ganancias = sum([dato[5] for dato in analisis])
    
    doc = SimpleDocTemplate(file_path, pagesize=letter,
                          leftMargin=0.5*inch,
                          rightMargin=0.5*inch,
                          topMargin=0.5*inch,
                          bottomMargin=0.5*inch)
    elements = []
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(name='Title', fontSize=16, alignment=1, spaceAfter=10, fontName='Helvetica-Bold')
    section_title_style = ParagraphStyle(name='SectionTitle', fontSize=12, spaceAfter=6, fontName='Helvetica-Bold')
    
    elements.append(Paragraph("Informe de Análisis Financiero", title_style))
    elements.append(Paragraph(f"Generado: {fecha_actual}", styles['Normal']))
    elements.append(Spacer(1, 12))
        
    # 1. Configuración de estilos y parámetros
    styles = getSampleStyleSheet()
    section_title_style = styles['Heading2']
    ancho_columna = (doc.width - 1*inch) / 2  # Dividir espacio disponible entre 2 tablas
    
    # 2. Función para crear tablas optimizadas
    def crear_tabla_compacta(datos, encabezados, columna_derecha_index):
        tabla = Table([encabezados] + datos, colWidths=[ancho_columna*0.3, ancho_columna*0.4, ancho_columna*0.3])
        estilo = TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#3d5c95')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('LEADING', (0,0), (-1,-1), 8),
            ('GRID', (0,0), (-1,-1), 0.5, colors.black),
            ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#f8f8f8')),
            
            # Alineación específica para la columna de montos (columna_derecha_index)
            ('ALIGN', (columna_derecha_index, 1), (columna_derecha_index, -1), 'RIGHT'),
            ('PADDING', (columna_derecha_index, 0), (columna_derecha_index, -1), (0, 0, 10, 0))  # Padding derecho
        ])
        tabla.setStyle(estilo)
        return tabla

    # 3. Preparar datos formateados
    datos_ingresos = [[str(ing[0])[:8], ing[2][:15], f"${ing[3]+ing[4]:,.0f}"] for ing in ingresos if ing[2] == "Venta"]
    datos_ganancias = [[str(dato[0])[:8], dato[1][:15], f"${dato[5]:,.0f}"] for dato in analisis]

    # 4. Función para dividir datos en chunks que caben en una página
    def dividir_en_chunks(datos, max_filas_por_pagina):
        return [datos[i:i + max_filas_por_pagina] for i in range(0, len(datos), max_filas_por_pagina)]

    # Calcular filas que caben por página (aproximadamente 1.5 pulgadas por fila)
    espacio_disponible = doc.height - 2*inch  # Espacio para títulos y márgenes
    max_filas_por_pagina = min(
        int(espacio_disponible / 12),  # ~12 puntos por fila
        40  # Límite máximo para mantener legibilidad
    )

    chunks_ingresos = dividir_en_chunks(datos_ingresos, max_filas_por_pagina)
    chunks_ganancias = dividir_en_chunks(datos_ganancias, max_filas_por_pagina)

    # 5. Generar páginas con tablas paralelas
    for i in range(max(len(chunks_ingresos), len(chunks_ganancias))):
        # Agregar título solo en la primera página
        if i == 0:
            elements.append(Paragraph("Análisis Financiero Detallado", title_style))
            elements.append(Spacer(1, 12))
        
        # Obtener chunks actuales (o listas vacías si no hay más datos)
        chunk_ing = chunks_ingresos[i] if i < len(chunks_ingresos) else []
        chunk_gan = chunks_ganancias[i] if i < len(chunks_ganancias) else []

        # Crear tablas para los chunks actuales
        tabla_ing = crear_tabla_compacta(chunk_ing, ["ID", "INGRESOS", "MONTO"], 2)
        tabla_gan = crear_tabla_compacta(chunk_gan, ["ID", "GANANCIAS", "MONTO"], 2)

        # Contenedor para tablas lado a lado
        container = Table([
            [Paragraph("INGRESOS" + (" (cont.)" if i > 0 else ""), section_title_style),
             Paragraph("GANANCIAS" + (" (cont.)" if i > 0 else ""), section_title_style)],
            [tabla_ing, tabla_gan]
        ], colWidths=[ancho_columna]*2)
        
        container.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('BOTTOMPADDING', (0,0), (-1,0), 8),
        ]))

        elements.append(container)
        
        # Agregar salto de página si hay más datos
        if i < max(len(chunks_ingresos), len(chunks_ganancias)) - 1:
            elements.append(PageBreak())
    
    # Totales de ingresos, egresos y ganancias
    elements.append(Paragraph("Ingresos", section_title_style))
    elements.append(Paragraph(f"• Total de Ingresos: ${total_ingresos:,.2f}", styles['Normal']))
    elements.append(Spacer(1, 6))
    
    elements.append(Paragraph("Egresos", section_title_style))
    elements.append(Paragraph(f"• Total de Egresos: ${total_egresos:,.2f}", styles['Normal']))
    elements.append(Spacer(1, 6))
    
    elements.append(Paragraph("Ganancias", section_title_style))
    elements.append(Paragraph(f"• Total de Ganancias: ${total_ganancias:,.2f}", styles['Normal']))
    elements.append(Spacer(1, 12))
    
    #graficos
    save_dir = tempfile.gettempdir()
    
    # Gráfico 1: Ingresos vs Egresos
    fig1, ax1 = plt.subplots(figsize=(5, 3))
    labels = ['Ingresos', 'Egresos']
    sizes = [total_ingresos, total_egresos]
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#66b3ff', '#ff6666'])
    ax1.set_title('Distribución Ingresos/Egresos')
    ax1.axis('equal')
    chart1_filename = os.path.join(save_dir, "grafico_ingresos_egresos.png")
    plt.savefig(chart1_filename, format='png', bbox_inches='tight')
    plt.close(fig1)
    
    # Gráfico 2: Evolución de Ganancias Diarias (agrupadas por día)
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    
    # Procesar datos - agrupar por fecha
    from collections import defaultdict
    ganancias_por_dia = defaultdict(float)
    
    for dato in analisis:
        fecha = dato[4].date()  # Extraemos solo la fecha (sin hora)
        ganancias_por_dia[fecha] += dato[5]  # Sumamos las ganancias
    
    # Convertir a listas ordenadas
    fechas = sorted(ganancias_por_dia.keys())
    ganancias = [ganancias_por_dia[f] for f in fechas]
    fechas_str = [f.strftime('%d/%m') for f in fechas]  # Formato día/mes
    
    # Determinar el mejor tipo de visualización
    num_dias = len(ganancias)
    
    if num_dias == 1:
        # Gráfico de barras para un solo día con todas las ventas
        fig2, (ax2, ax3) = plt.subplots(1, 2, figsize=(12, 4))
        
        # Gráfico 1: Total del día
        ax2.bar(fechas_str, ganancias, color='#2ecc71', width=0.6)
        ax2.set_title(f'Ganancias Totales del {fechas_str[0]}')
        ax2.set_ylabel('Monto ($)')
        ax2.text(0, ganancias[0], f'${ganancias[0]:,.2f}', 
                ha='center', va='bottom', fontweight='bold')
        
        # Gráfico 2: Desglose por ventas individuales
        ventas_del_dia = [(dato[4].strftime('%H:%M'), dato[5]) for dato in analisis]
        horas = [v[0] for v in ventas_del_dia]
        montos = [v[1] for v in ventas_del_dia]
        
        ax3.bar(horas, montos, color='#3498db')
        ax3.set_title('Desglose por ventas')
        ax3.set_ylabel('Monto ($)')
        plt.sca(ax3)
        plt.xticks(rotation=45, ha='right')
        
        # Agregar valores a las barras
        for i, val in enumerate(montos):
            ax3.text(i, val, f'${val:,.2f}', ha='center', va='bottom', fontsize=8)
        
        plt.tight_layout()
        
    elif num_dias <= 15:
        # Gráfico de barras para pocos días
        bars = ax2.bar(fechas_str, ganancias, color='#2ecc71')
        ax2.set_title('Ganancias Diarias (Totales)')
        ax2.set_ylabel('Monto ($)')
        
        # Rotar etiquetas y agregar valores
        plt.xticks(rotation=45, ha='right')
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'${height:,.2f}', ha='center', va='bottom', fontsize=8)
        
    else:
        # Gráfico de línea para muchos días
        ax2.plot(fechas_str, ganancias, marker='o', color='#2ecc71', linestyle='-', linewidth=2)
        ax2.set_title('Evolución de Ganancias Diarias')
        ax2.set_ylabel('Monto ($)')
        plt.xticks(rotation=45, ha='right')
        
        # Destacar punto máximo
        max_idx = np.argmax(ganancias)
        ax2.plot(fechas_str[max_idx], ganancias[max_idx], 'ro')
        ax2.annotate(f'Máximo: ${ganancias[max_idx]:,.2f}',
                    xy=(fechas_str[max_idx], ganancias[max_idx]),
                    xytext=(10, 10), textcoords='offset points',
                    bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                    arrowprops=dict(arrowstyle='->'))
    
    # Ajustar márgenes
    plt.tight_layout()
    
    chart2_filename = os.path.join(save_dir, "grafico_ganancias.png")
    plt.savefig(chart2_filename, format='png', bbox_inches='tight', dpi=100)
    plt.close(fig2)

    # Contenedor para gráficos
    elements.append(Paragraph("Análisis Gráfico", section_title_style))
    
    # Crear tabla contenedora para los gráficos
    # container_graficos = Table([
    #     [Image(chart1_filename, width=280, height=200), 
    #      Image(chart2_filename, width=280, height=200)]
    # ], colWidths=[doc.width/2]*2)
    
    # container_graficos.setStyle(TableStyle([
    #     ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    #     ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    # ]))
    
    elements.append(Image(chart1_filename, width=280, height=200))
    elements.append(Image(chart2_filename, width=400, height=250))
    elements.append(Spacer(1, 12))
    
    # Conclusión
    elements.append(Paragraph("Conclusión", section_title_style))
    if total_ganancias > total_egresos:
        conclusion_text = "El análisis muestra que las ganancias fueron óptimas, indicando una buena salud financiera."
    else:
        conclusion_text = "El análisis indica que las ganancias no fueron óptimas, lo que podría requerir ajustes financieros."
    elements.append(Paragraph(conclusion_text, styles['Normal']))
    
    # Generar PDF
    doc.build(elements)
    
    try:
        os.remove(chart1_filename)
        os.remove(chart2_filename)
    except:
        pass
    
    root = tk.Tk()
    root.withdraw()  
    messagebox.showinfo("Éxito", f"PDF generado exitosamente: {file_path}")
    root.quit()