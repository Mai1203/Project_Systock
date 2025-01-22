from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from datetime import datetime
import textwrap
import locale
from tkinter import filedialog

# Configurar la localización
locale.setlocale(locale.LC_ALL, 'es_CO.UTF-8')  # Ajustar la localización a Colombia

def generate_ticket(
    client_name,
    client_id,
    client_address,
    client_phone,
    items,
    subtotal,
    delivery_fee,
    total,
    payment_method,
    invoice_number,
    pan,
    pago,
    filename,
):
    # Configuración inicial y ventana de diálogo para guardar archivo
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    default_filename = f"{client_name.replace(' ', '')}{current_datetime}.pdf"
    filename = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")],
        initialfile=default_filename,
    )

    # Ajustar la dirección con salto de línea
    max_length = 22
    wrapped_address = textwrap.fill(client_address, width=max_length)

    # Definición de las medidas de la página y espacio entre líneas
    pdf_width = 68 * 5
    line_height = 20
    header_height = 10
    footer_height = 80
    max_lines = len(items) + 10  # Añadir algunas líneas de margen para asegurar que el contenido no se corte

    # Cálculo dinámico de la altura de la página en base al número de productos
    content_height = header_height + footer_height + (line_height * max_lines)
    min_height = 1000  # Altura mínima de la página
    pdf_height = max(content_height, min_height)

    # Crear el objeto PDF
    pdf = canvas.Canvas(filename, pagesize=(pdf_width, pdf_height))

    # Establecer el color de fuente y el tamaño
    pdf.setStrokeColor(colors.black)
    pdf.setFillColor(colors.black)
    font_size = 18
    pdf.setFont("Helvetica-Bold", font_size)

    # Encabezado del ticket (solo se dibuja en la primera página)
    pdf.drawCentredString(pdf_width / 2, pdf_height - 30, "Lady NailShop")
    pdf.setFont("Helvetica-Bold", font_size - 2)
    pdf.drawCentredString(pdf_width / 2, pdf_height - 60, "Pasto, Colombia")
    pdf.drawCentredString(pdf_width / 2, pdf_height - 90, "Teléfono: +57 316 144 4474")
    pdf.drawCentredString(pdf_width / 2, pdf_height - 120, f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    pdf.line(20, pdf_height - 130, pdf_width - 20, pdf_height - 130)  # Línea divisoria

    # Información de la factura
    y = pdf_height - 150
    pdf.setFont("Helvetica-Bold", font_size)
    pdf.drawString(20, y, "Factura de Venta")
    y -= line_height
    pdf.setFont("Helvetica-Bold", font_size)
    pdf.drawString(20, y, f"Número de Factura: {invoice_number}")
    y -= line_height
    pdf.drawString(20, y, f"PAN: {pan}")
    y -= line_height
    pdf.drawString(20, y, f"Cliente: {client_name}")
    y -= line_height
    pdf.drawString(20, y, f"Cédula: {client_id}")
    y -= line_height
    for line in wrapped_address.split('\n'):
        pdf.drawString(20, y, f"Dirección: {line}")
        y -= line_height
    pdf.drawString(20, y, f"Teléfono: {client_phone}")

    # Línea divisoria
    y -= line_height
    pdf.line(20, y, pdf_width - 20, y)
    y -= line_height

    # Descripción de los productos
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(20, y, "Cantidad")
    pdf.drawString(105, y, "Descripción")
    pdf.drawString(240, y, "Valor")
    y -= line_height

    # Imprimir los productos
    for quantity, description, value in items:
        pdf.drawString(20, y, str(quantity))
        pdf.drawString(90, y, description[:15])  # Limitar descripción a 15 caracteres
        pdf.drawString(240, y, f"${value:.2f}")
        y -= line_height

        # Verificar si se necesita nueva página
        if y < 100:  # Si la página está a punto de llenarse
            pdf.showPage()  # Añadir una nueva página
            pdf.setFont("Helvetica-Bold", 16)  # Establecer fuente en negrita y tamaño 16
            # Continuar con los productos en la nueva página
            y = pdf_height - 50  # Reiniciar la posición Y en la nueva página
            # Solo mostrar lo que falta (sin repetir encabezado)

    # Subtotales y totales
    sub = locale.currency(subtotal, grouping=True)
    descu = locale.currency(delivery_fee, grouping=True)
    totalpagar = locale.currency(total, grouping=True)
    
    if payment_method == "Efectivo" or payment_method == "Transferencia":
        pago = locale.currency(float(pago), grouping=True)
    else:
        total = pago.split("/") 
        efectivo = float(total[0])
        tranferencia = float(total[1])
        efectivo = locale.currency(efectivo, grouping=True)
        tranferencia = locale.currency(tranferencia, grouping=True)

    # Detallar subtotales (se sigue escribiendo después de la continuación de la página)
    pdf.setFont("Helvetica-Bold", font_size)
    y -= line_height
    pdf.drawString(140, y, "Subtotal:")
    pdf.drawString(225, y, f"{sub}")
    y -= line_height
    pdf.drawString(140, y, "Domicilio:")
    pdf.drawString(230, y, f"{descu}")
    y -= line_height
    pdf.drawString(140, y, "Total:")
    pdf.drawString(220, y, f"{totalpagar}")
    y -= line_height
    if payment_method == "Efectivo" or payment_method == "Transferencia":
        pdf.drawString(140, y, "Pago:")
        pdf.drawString(220, y, pago)
    else:
        pdf.drawString(140, y, "Efectivo:")
        pdf.drawString(220, y, f"{efectivo}")
        y -= line_height
        pdf.drawString(140, y, "Transfer:")
        pdf.drawString(220, y, f"{tranferencia}")
        y -= line_height
        

    # Forma de pago
    y -= line_height * 2
    pdf.setFont("Helvetica-Bold", font_size)
    pdf.drawString(20, y, f"Forma de Pago: {payment_method}")

    # Pie de página (solo en la primera página)
    y -= line_height * 2
    pdf.setFillColor(colors.lightgrey)
    pdf.rect(0, 0, pdf_width, footer_height, fill=True, stroke=False)
    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica-Bold", font_size - 1)
    pdf.drawCentredString(pdf_width / 2, 30, "¡Gracias por tu compra!")

    # Guardar el PDF
    pdf.save()
