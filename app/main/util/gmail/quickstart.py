from __future__ import print_function
import pickle
import base64
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from app.main.model.rol_usuario import RolUsuario
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template

SCOPES = ['https://www.googleapis.com/auth/gmail.send']
DIRECCION_ORIGEN = "soporte.politicasprivacidad@gmail.com"


def leer_email():
    if os.name == 'nt':
        os.chdir(os.getcwd() + '\\app\\main\\util\\gmail')
    else:
        os.chdir(os.getcwd() + '/app/main/util/gmail')

    with open('email.html', 'r', encoding='utf-8') as email_html:
        email_html_contenido = email_html.read()
    return Template(email_html_contenido)


def crear_mensaje(usuario, clave, rol_usuario):
    rol_usuario_string = RolUsuario.query.filter_by(id=rol_usuario).first()
    rol = rol_usuario_string.nombre

    email = MIMEMultipart()
    email['From'] = DIRECCION_ORIGEN
    email['To'] = usuario
    email['Subject'] = 'Bienvenido!'

    mensaje_html = leer_email()
    mensaje = mensaje_html.safe_substitute(ROL_USUARIO=rol, EMAIL=usuario, CLAVE=clave)

    email.attach(MIMEText(mensaje, 'html'))

    raw_message = base64.urlsafe_b64encode(email.as_string().encode("utf-8"))
    return {
        'raw': raw_message.decode("utf-8")
    }


def enviar_correo(usuario, clave, rol_usuario):
    mensaje = crear_mensaje(usuario, clave, rol_usuario)
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    try:
        service.users().messages().send(userId="me", body=mensaje).execute()
        return True
    except:
        return False
