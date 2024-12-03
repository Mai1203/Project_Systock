from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart

def generar_reporte(nombre_archivo, titulo, datos_tabla, datos_grafico):
    # Crear documento PDF
    doc = SimpleDocTemplate(nombre_archivo, pagesize=letter)
    elementos = []

    # Estilos
    estilos = getSampleStyleSheet()
    estilo_titulo = estilos['Title']
    estilo_normal = estilos['BodyText']

    # Título del reporte
    elementos.append(Paragraph(titulo, estilo_titulo))
    elementos.append(Spacer(1, 20))

    # Tabla
    tabla = Table(datos_tabla)
    estilo_tabla = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Fila de encabezado en gris
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold '),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])
    tabla.setStyle(estilo_tabla)
    elementos.append(tabla)
    elementos.append(Spacer(1, 20))

    # Gráfico de barras
    dibujo = Drawing(400, 200)
    grafico = VerticalBarChart()
    grafico.x = 50
    grafico.y = 50
    grafico.height = 125
    grafico.width = 300
    grafico.data = datos_grafico
    grafico.categoryAxis.categoryNames = ['Producto A', 'Producto B', 'Producto C']
    grafico.bars[0].fillColor = colors.blue
    grafico.valueAxis.valueMin = 0
    grafico.valueAxis.valueMax = max(max(datos_grafico)) + 10
    grafico.valueAxis.valueStep = 50
    dibujo.add(grafico)
    elementos.append(dibujo)

    # Guardar el PDF
    doc.build(elementos)
    print(f"Reporte generado: {nombre_archivo}")

# Datos de prueba
datos_tabla = [
    ['Producto', 'Ventas', 'Stock'],
    ['Producto A', '100', '50'],
    ['Producto B', '150', '40'],
    ['Producto C', '200', '30'],
]

datos_grafico = [[100, 150, 200]]

# Generar reporte
generar_reporte("reporte_tienda.pdf", "Reporte de Ventas y Stock", datos_tabla, datos_grafico)
