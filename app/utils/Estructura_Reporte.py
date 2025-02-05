from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch


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
