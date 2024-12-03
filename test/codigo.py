import barcode
from barcode.writer import ImageWriter

def calcular_digito_control(codigo_base):
    """Calcula el dígito de control para un código EAN-13."""
    suma_impar = sum(int(codigo_base[i]) for i in range(0, 12, 2))
    suma_par = sum(int(codigo_base[i]) for i in range(1, 12, 2)) * 3
    total = suma_impar + suma_par
    digito_control = (10 - (total % 10)) % 10
    return digito_control

def generar_codigos(valor_inicial, valor_final):
    """Genera los códigos EAN-13 para los productos. """
    codigos = []
    for i in range(valor_inicial, valor_final + 1):
        codigo_base = f"770999{i:06d}"  # Rellena con 6 dígitos
        digito_control = calcular_digito_control(codigo_base)
        codigo_completo = codigo_base + str(digito_control)
        codigos.append(codigo_completo)
    return codigos

def generar_codigos_barras(codigos):
    """Genera archivos de imágenes de códigos de barras."""
    for codigo in codigos:
        # Generar el código de barras EAN-13 con python-barcode
        barcode_instance = barcode.get_barcode_class('ean13')
        barcode_image = barcode_instance(codigo, writer=ImageWriter())
        archivo_salida = f"codigo_barra_{codigo}.png"
        barcode_image.save(archivo_salida)
        print(f"Código de barras generado: {archivo_salida}")

# Generar códigos para los productos 100001 a 100500
codigos = generar_codigos(100001, 101000)

# Generar imágenes de códigos de barras
generar_codigos_barras(codigos)
