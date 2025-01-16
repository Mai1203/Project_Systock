import jwt
import datetime
from app.utils.enviar_notifi import enviar_notificacion
from app.controllers.usuario_crud import verificar_credenciales

SECRET_KEY = "5ha2bD9GH#"  # Cambia esto por una clave más segura

def generar_token(usuario_id):
    """
    Genera un token JWT para el usuario autenticado.
    """
    payload = {
        "id_usuario": usuario_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),  # Expira en 1 hora
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def iniciar_sesion(self):
    usuario = self.Login.InputNombreUsuario.text()
    contraseña = self.Login.InputPassword.text()

    if not usuario or not contraseña:
        enviar_notificacion("Error", "Por favor, ingresa tus credenciales")
        return

    usuario_autenticado = verificar_credenciales(self.db, usuario, contraseña)
    if not usuario_autenticado:
        enviar_notificacion("Error al ingresar", "Usuario o contraseña incorrectos")
        return

    # Generar el token JWT
    token = generar_token(usuario_autenticado.ID_Usuario)
    enviar_notificacion("Inicio de sesión exitoso", "Puedes continuar con tus operaciones")

    # Almacenar el token para usarlo después
    self.token_actual = token  # Lo guardas en el objeto MainWindow
    self.stacked_widget.setCurrentWidget(self.MainApp)
    self.db.close()

def validar_token(token):
    """
    Decodifica el token JWT y verifica su validez.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload  # Retorna los datos dentro del token
    except jwt.ExpiredSignatureError:
        enviar_notificacion("Error", "El token ha expirado. Por favor, inicia sesión nuevamente.")
        return None
    except jwt.InvalidTokenError:
        enviar_notificacion("Error", "Token inválido.")
        return None

