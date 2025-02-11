from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.lib.units import inch
from datetime import datetime
import tkinter as tk
from tkinter import filedialog

def generar_pdf_creditos(self, resultado):
    # Obtener la fecha actual para el nombre del archivo
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    nombre_archivo = f"analisiscredito_{fecha_actual}.pdf"

    # Abrir el cuadro de diálogo para elegir la ubicación de guardado
    root = tk.Tk()
    root.withdraw()
    archivo_guardado = filedialog.asksaveasfilename(defaultextension=".pdf", initialfile=nombre_archivo, title="Guardar como")
    
    if archivo_guardado:
        # Crear el documento PDF
        doc = SimpleDocTemplate(archivo_guardado, pagesize=letter)
        elements = []
        
        # Estilo para los párrafos
        styles = getSampleStyleSheet()
        style_normal = styles["Normal"]
        
        # Título del reporte
        title = Paragraph("Análisis de Créditos", styles['Title'])
        elements.append(title)
        elements.append(Spacer(1, 12))  # Espacio entre el título y el contenido
        
        # Contadores para ventas viables y no viables
        viable_count = 0
        non_viable_count = 0

        # Crear una tabla por cada venta
        for item in resultado:
            venta = item['venta']
            pagos = item['pagos']
            
            # Datos de la venta
            venta_data = [
                ['ID Venta', venta['ID_Venta_Credito']],
                ['Total Deuda', venta['Total_Deuda']],
                ['Saldo Pendiente', venta['Saldo_Pendiente']],
                ['Fecha Registro', venta['Fecha_Registro']],
            ]
            
            # Crear la tabla de detalles de la venta
            venta_table = Table(venta_data, colWidths=[200, 200])
            venta_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                            ('BACKGROUND', (0, 1), (-1, -1), colors.beige)]))
            elements.append(venta_table)
            elements.append(Spacer(1, 12))  # Espacio después de la tabla

            # Escribir los detalles de los pagos en una nueva tabla
            if pagos:
                pagos_data = [['ID Pago', 'Monto', 'Fecha Pago', 'Método de Pago', 'Tipo de Pago']]
                for pago in pagos:
                    pagos_data.append([pago['ID_Pago_Credito'], pago['Monto'], pago['Fecha_Registro'], pago['Metodo_Pago'], pago['Tipo_Pago']])
                
                pagos_table = Table(pagos_data, colWidths=[100, 100, 100, 100, 100])
                pagos_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                                 ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                                 ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                                 ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                                 ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                                 ('BACKGROUND', (0, 1), (-1, -1), colors.beige)]))
                elements.append(pagos_table)
                elements.append(Spacer(1, 12))  # Espacio después de la tabla de pagos
            else:
                elements.append(Paragraph("No hay pagos asociados.", style_normal))
                elements.append(Spacer(1, 12))  # Espacio después del mensaje

            ## Verificación de viabilidad
            if venta['Saldo_Pendiente'] < (venta['Total_Deuda'] * 0.45):  # 45% del total de la deuda
                viable_count += 1
                status = "Viable"
                color = colors.green
            else:
                non_viable_count += 1
                status = "No Viable"
                color = colors.red

            # Crear gráfico de pastel para cada venta
            drawing = Drawing(2 * inch, 2 * inch)
            pie_chart = Pie()
            pie_chart.x = 10
            pie_chart.y = 10
            pie_chart.width = 150
            pie_chart.height = 150

            pie_chart.data = [1, 1]
            pie_chart.labels = [status, "Otro"]
            pie_chart.slices[0].fillColor = color
            pie_chart.slices[1].fillColor = colors.whitesmoke

            drawing.add(pie_chart)

            # Agregar gráfico de pastel al documento
            elements.append(drawing)
            elements.append(Spacer(1, 12))  # Espacio después del gráfico

            # Línea separadora
            elements.append(Spacer(1, 3))  # Espacio para la línea
            elements.append(Paragraph("_" * 90, style_normal))  # Línea separadora
            elements.append(Spacer(1, 12))  # Espacio después de la línea

        # Agregar resumen de ventas viables y no viables al final
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f"Total de Ventas Viables: {viable_count}", style_normal))
        elements.append(Paragraph(f"Total de Ventas No Viables: {non_viable_count}", style_normal))

        # Crear el PDF
        doc.build(elements)
        print(f"PDF guardado en: {archivo_guardado}")
    else:
        print("No se seleccionó ningún archivo para guardar.")
