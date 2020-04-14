from flask_restplus import marshal
from app.main import db
from app.main.model.usuario import Usuario
from app.main.model.rol_usuario import RolUsuario
from app.main.util.clases_auxiliares import UsuarioConsultar
from app.main.util.dto import UsuarioDto

import datetime
import string
import random
import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

MY_ADDRESS = 'soporte.politicasprivacidad@gmail.com'
PASSWORD = 'Politicas_2020'


def leer_email(filename):
    with open(filename, 'r', encoding='utf-8') as email_html:
        email_html_contenido = email_html.read()
    return Template(email_html_contenido)


def clave_aleatoria():
    caracteres = string.ascii_uppercase + string.ascii_lowercase + string.digits
    tamano = random.randint(8, 12)
    return ''.join(random.choice(caracteres) for x in range(tamano))


def enviar_correo(usuario, clave, rol_usuario):
    rol_usuario_string = RolUsuario.query.filter_by(id=rol_usuario).first()
    rol = rol_usuario_string.nombre

    servidor = smtplib.SMTP(host='smtp.gmail.com', port=587)
    servidor.starttls()
    servidor.login(MY_ADDRESS, PASSWORD)

    email = MIMEMultipart()
    email['From'] = MY_ADDRESS
    email['To'] = usuario
    email['Subject'] = 'Bienvenido!'

    mensaje_html = leer_email('email.html')
    mensaje = mensaje_html.safe_substitute(ROL_USUARIO=rol, EMAIL=usuario, CLAVE=clave)

    email.attach(MIMEText(mensaje, 'html'))

    servidor.send_message(email)

    servidor.quit()


def guardar_nuevo_usuario(data):
    user = Usuario.query.filter_by(email=data['email']).first()
    if not user:
        clave = clave_aleatoria()
        enviar_correo(data['email'], clave, data['rol_usuario'])
        nuevo_usuario = Usuario(
            email=data['email'],
            hora_registro=datetime.datetime.now(),
            rol_usuario=data['rol_usuario'],
            clave=clave,
            activo=True,
            entrenamiento= data['entrenamiento']
        )
        guardar_cambios(nuevo_usuario)
        respuesta = {
            'estado': 'exito',
            'mensaje': 'Usuario registrado exitosamente'
        }
        return respuesta, 201
    else:
        respuesta = {
            'estado': 'fallido',
            'mensaje': 'El usuario ya existe, por favor inicie sesion'
        }
        return respuesta, 409


def editar_usuario(data):
    usuario = Usuario.query.filter_by(id=data['id']).first()
    if usuario:
        usuario.email = data['email']
        usuario.rol_usuario = data['rol_usuario']
        usuario.activo = data['activo']
        usuario.entrenamiento = data['entrenamiento']

        guardar_cambios(usuario)

        respuesta = {
            'estado': 'exito',
            'mensaje': 'Usuario editado con exito'
        }
        return respuesta, 201

    else:
        respuesta = {
            'estado': 'fallido',
            'mensaje': 'No existe el usuario'
        }
        return respuesta, 409


def eliminar_usuario(id):
    try:
        Usuario.query.filter_by(id=id).delete()
    except:
        db.session.rollback()
        respuesta = {
            'estado': 'fallido',
            'mensaje': 'Error eliminando usuario'
        }
        return respuesta, 409
    else:
        db.session.commit()
        respuesta = {
            'estado': 'exito',
            'mensaje': 'Usuario eliminado con exito'
        }
        return respuesta, 201


def obtnener_todos_usuarios():
    db.session.configure(autoflush=False)
    resultado = db.session.query(Usuario.id, Usuario.email, Usuario.activo, Usuario.entrenamiento,
                                 RolUsuario.id, RolUsuario.nombre).\
                            outerjoin(RolUsuario, RolUsuario.id == Usuario.rol_usuario).all()
    usuarios = [UsuarioConsultar]
    i = 0
    usuarios.clear()
    for item in resultado:
        user_aux = UsuarioConsultar(item[0], item[1], item[4], item[5], item[2], item[3])
        usuarios.insert(i, user_aux)
        i += 1
    return usuarios


def obtener_un_usuario(id):
    return Usuario.query.filter_by(id=id).first()


def obtener_anotadores_activos():
    anotadores_consulta = Usuario.query.filter_by(activo=True).all()
    if not anotadores_consulta:
        respuesta = {
            'estado': 'fallido',
            'mensaje': 'Ocurrio un error, por favor intente de nuevo'
        }
        return respuesta, 404

    else:
        return marshal(anotadores_consulta, UsuarioDto.usuarioConsultarAsignacion), 201


def obtener_administradores_activos():
    administradores_consultar = Usuario.query.filter_by(rol_usuario=1, activo=True).all()
    if not administradores_consultar:
        respuesta = {
            'estado': 'fallido',
            'mensaje': 'No existen administradores'
        }
        return respuesta, 404

    else:
        return marshal(administradores_consultar, UsuarioDto.usuarioConsultarAsignacion), 201


def generar_token(usuario):
    try:
        auth_token = usuario.codificar_auth_token(usuario_id=usuario.id)
        respuesta = {
            'estado': 'exito',
            'mensaje': 'Usuario registrado exitosamente',
            'Authorization': auth_token.decode()
        }
        return  respuesta, 201
    except Exception as e:
        respuesta = {
            'estado': 'fallido',
            'mensaje': 'Ocurrio un error, por favor intente de nuevo'
        }
        return respuesta, 401


def guardar_cambios(data):
    db.session.add(data)
    db.session.commit()

