from plyer import notification


def enviar_notificacion(titulo, mensaje):
    """
    Envía una notificación al sistema operativo.
    """

    notification.notify(
        title=titulo,
        message=mensaje,
        app_name="Mi Aplicación",
        timeout=5,  # Duración de la notificación en segundos
    )
