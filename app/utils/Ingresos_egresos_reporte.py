import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from tkinter import Tk, filedialog
from PyQt5.QtWidgets import QMessageBox

def generar_pdf_transacciones(transacciones, tipo, fecha_inicio=None, fecha_fin=None):
    """
    Genera un PDF con la lista de ingresos o egresos y permite elegir dónde guardarlo.
    :param transacciones: Lista de transacciones (ingresos o egresos).
    :param tipo: "ingresos" o "egresos" para personalizar el reporte.
    """
    # Ocultar la ventana de Tkinter
    root = Tk()
    root.withdraw()
    
    # Elegir dónde guardar el archivo
    file_path = filedialog.asksaveasfilename(
        defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")],
        title=f"Guardar Reporte de {tipo.capitalize()}"
    )
    
    if not file_path:
        print("Operación cancelada.")
        return
    
    # Crear el PDF
    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter
    
    # Agregar logo y título
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    logo_path = os.path.join(root_dir, 'assets', 'logo.png')
    print(logo_path)
    
    c.drawImage(logo_path, 50, 680, width=100, height=100, mask='auto')

    # Título del reporte
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(colors.black)
    c.drawString(200, 730, f"Reporte Detallado de {tipo}")

    # Detalles del reporte
    c.setFont("Helvetica", 11)
    c.setFillColor(colors.black)
    if fecha_fin:
        c.drawString(50, 650, f"Rango de fechas: {fecha_inicio} - {fecha_fin}")
    else:
        c.drawString(50, 650, f"Fecha de reporte: {fecha_inicio}")
    c.drawString(50, 635, "Generado por: Sistema LADYNAILS POS")
    
    # Encabezados
    y_position = height - 200
    if tipo == "ingresos":
        c.drawString(50, y_position, "ID")
        c.drawString(100, y_position, "Tipo")
        c.drawString(200, y_position, "Monto Efectivo")
        c.drawString(320, y_position, "Monto Transacción")
        c.drawString(450, y_position, "Fecha Venta")
    elif tipo == "egresos":
        c.drawString(50, y_position, "ID")
        c.drawString(100, y_position, "Nombre")
        c.drawString(250, y_position, "Monto")
        c.drawString(400, y_position, "Fecha")
    
    y_position -= 20
    c.line(50, y_position, 550, y_position)
    y_position -= 20
    
    # Variables para las sumas
    total_efectivo = 0
    total_transferencia = 0
    total_egresos = 0
    
    # Agregar los datos
    for trans in transacciones:
        if tipo == "ingresos":
            c.drawString(50, y_position, str(trans[0]))  # ID
            c.drawString(100, y_position, str(trans[1]))  # Tipo
            c.drawString(200, y_position, str(trans[2] or 0.0))  # Monto efectivo
            c.drawString(320, y_position, str(trans[3] or 0.0))  # Monto transacción
            c.drawString(450, y_position, str(trans[4]))  # Fecha venta
            
            # Actualizar los totales
            total_efectivo += float(trans[2])
            total_transferencia += float(trans[3])
            
        elif tipo == "egresos":
            c.drawString(50, y_position, str(trans[0]))  # ID
            c.drawString(100, y_position, str(trans[1]))  # Nombre
            c.drawString(250, y_position, str(trans[2]))  # Monto
            c.drawString(400, y_position, str(trans[3]))  # Fecha
            
            total_egresos += float(trans[2])
        
        y_position -= 20
        if y_position < 50:
            c.showPage()
            c.setFont("Helvetica", 12)
            y_position = height - 50
        
        # Agregar la sumatoria al final
        c.line(50, y_position, 550, y_position)
        y_position -= 20
        
    total = total_efectivo + total_transferencia
    if tipo == "ingresos":
        c.drawString(50, y_position, "Total Ingresos:")
        c.drawString(200, y_position, f"{total_efectivo:,.2f}")
        c.drawString(320, y_position, f"{total_transferencia:,.2f}")
        y_position -= 20
        c.drawString(50, y_position, f"Total: {total:,.2f}")
    elif tipo == "egresos":
        c.drawString(50, y_position, "Total Egresos:")
        c.drawString(250, y_position, f"{total_egresos:,.2f}")
    
    c.save()
    QMessageBox.information(None, "Reporte generado", f"Reporte de {tipo} guardado correctamente")
