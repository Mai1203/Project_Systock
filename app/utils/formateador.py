def formatear_numero(total):
    """
    Formatea un número con miles y decimales según sea necesario.
    """
    if isinstance(total, str):
        # Si el valor es un string, conviértelo a float
        total = float(total)

    if total % 1 == 0:
        # Si es un número entero, formatear sin decimales
        return f"{total:,.0f}"
    else:
        # Si no es entero, mostrar con dos decimales
        return f"{total:,.2f}"


def formatear_numero_entero(total):
    """
    Formatea un número entero con miles.
    """
    return f"{total:,.0f}"


def formatear_numero_decimal(total, decimales=2):
    """
    Formatea un número decimal con miles y un número específico de decimales.
    """
    return f"{total:,.{decimales}f}"
