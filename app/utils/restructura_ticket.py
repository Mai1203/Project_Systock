import tkinter as tk
import locale
from tkinter import filedialog
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from datetime import datetime

locale.setlocale(locale.LC_ALL, "es_CO.UTF-8")


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
    """
    Genera un ticket en formato PDF con diseño mejorado y estructura definida.

    :param client_name: Nombre del cliente.
    :param client_id: Cédula del cliente.
    :param client_address: Dirección del cliente.
    :param client_phone: Teléfono del cliente.
    :param items: Lista de tuples (cantidad, descripción, valor).
    :param subtotal: Subtotal de los productos.
    :param delivery_fee: Costo del domicilio.
    :param total: Total a pagar.
    :param payment_method: Forma de pago.
    :param invoice_number: Número de la factura.
    :param pan: PAN de la empresa.
    :param filename: Ruta y nombre del archivo donde se guardará el PDF.
    """

    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    default_filename = f"{client_name.replace(' ', '_')}_{current_datetime}.pdf"

    # Ventana emergente para seleccionar la ruta donde guardar el archivo PDF
    filename = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")],
        initialfile=default_filename,
    )

    # Configuración del tamaño dinámico del PDF
    line_height = 15
    header_height = 100
    footer_height = 60
    content_height = header_height + footer_height + (line_height * (len(items) + 7))

    pdf_height = max(content_height, 400)  # Altura mínima del PDF
    pdf = canvas.Canvas(filename, pagesize=(300, pdf_height))

    # Estilos generales
    pdf.setStrokeColor(colors.black)
    pdf.setFillColor(colors.black)

    # Encabezado
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawCentredString(150, pdf_height - 30, "Lady NailShop")
    pdf.setFont("Helvetica", 10)
    pdf.drawCentredString(150, pdf_height - 45, "Pasto, Colombia")
    pdf.drawCentredString(150, pdf_height - 60, "Teléfono: +57 123 456 7890")
    pdf.drawCentredString(
        150, pdf_height - 75, f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    # Línea divisoria
    pdf.line(20, pdf_height - 85, 280, pdf_height - 85)

    # Información de la factura
    y = pdf_height - 100
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(20, y, "Factura de Venta")
    y -= line_height
    pdf.setFont("Helvetica", 10)
    pdf.drawString(20, y, f"Número de Factura: {invoice_number}")
    y -= line_height
    pdf.drawString(20, y, f"PAN: {pan}")
    y -= line_height
    pdf.drawString(20, y, f"Cliente: {client_name}")
    y -= line_height
    pdf.drawString(20, y, f"Cédula: {client_id}")
    y -= line_height
    pdf.drawString(20, y, f"Dirección: {client_address}")
    y -= line_height
    pdf.drawString(20, y, f"Teléfono: {client_phone}")

    # Línea divisoria
    y -= line_height
    pdf.line(20, y, 280, y)
    y -= line_height

    # Descripción de la factura
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(20, y, "Cantidad")
    pdf.drawString(100, y, "Descripción")
    pdf.drawString(240, y, "Valor")
    y -= line_height
    pdf.setFont("Helvetica", 10)
    for quantity, description, value in items:
        pdf.drawString(20, y, str(quantity))
        pdf.drawString(100, y, description[:20])  # Limitar a 20 caracteres
        pdf.drawString(240, y, f"${value:.2f}")
        y -= line_height

    sub = locale.currency(subtotal, grouping=True)
    descu = locale.currency(delivery_fee, grouping=True)
    totalpagar = locale.currency(total, grouping=True)
    pago = locale.currency(pago, grouping=True)

    # Subtotales y totales
    pdf.setFont("Helvetica-Bold", 10)
    y -= line_height
    pdf.drawString(160, y, "Subtotal:")
    pdf.drawString(240, y, f"{sub}")
    y -= line_height
    pdf.drawString(160, y, "Domicilio:")
    pdf.drawString(240, y, f"{descu}")
    y -= line_height
    pdf.drawString(160, y, "Total:")
    pdf.drawString(240, y, f"{totalpagar}")
    y -= line_height
    pdf.drawString(160, y, "Pago:")
    pdf.drawString(240, y, f"{pago}")

    # Forma de pago
    y -= line_height * 2
    pdf.setFont("Helvetica", 10)
    pdf.drawString(20, y, f"Forma de Pago: {payment_method}")

    # Pie de página
    y -= line_height * 2
    pdf.setFillColor(colors.lightgrey)
    pdf.rect(0, 0, 300, footer_height, fill=True, stroke=False)
    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica", 8)
    pdf.drawCentredString(150, 30, "Gracias por tu compra")

    # Guardar el PDF
    pdf.save()


# Crear la ventana principal
root = tk.Tk()
root.withdraw()  # Ocultar la ventana principal
