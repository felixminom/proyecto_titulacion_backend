from flask_restplus import marshal
from app.main import db
from app.main.model.usuario import Usuario
from app.main.model.rol_usuario import RolUsuario
from app.main.util.clases_auxiliares import UsuarioConsultar
from app.main.util.dto import UsuarioDto
from app.main.util.gmail.quickstart import enviar_correo
from app.main.util.respuesta import respuesta

import datetime
import string
import random


def clave_aleatoria():
    caracteres = string.ascii_uppercase + string.ascii_lowercase + string.digits
    tamano = random.randint(8, 12)
    return ''.join(random.choice(caracteres) for x in range(tamano))


def guardar_nuevo_usuario(usuario):
    user = Usuario.query.filter_by(email=usuario['email']).first()
    if not user:
        clave = clave_aleatoria()
        if enviar_correo(usuario['email'], clave, usuario['rol_usuario_id']):
            nuevo_usuario = Usuario(
                email=usuario['email'],
                hora_registro=datetime.datetime.now(),
                rol_usuario=usuario['rol_usuario_id'],
                clave=clave,
                activo=True,
                entrenamiento=usuario['entrenamiento']
            )
            guardar_cambios(nuevo_usuario)
            mensaje = respuesta(True, 'Usuario registrado exitosamente')
            return mensaje, 201
        else:
            mensaje = respuesta(False, 'Error al enviar correo. Pongase en contacto con soporte')
            return mensaje, 409
    else:
        mensaje = respuesta(False, 'El usuario ya existe, por favor inicie sesion')
        return mensaje, 409


def editar_usuario(usuario):
    usuario_editar = Usuario.query.filter_by(id=usuario['id']).first()
    if usuario_editar:
        usuario_editar.email = usuario['email']
        usuario_editar.rol_usuario = usuario['rol_usuario_id']
        usuario_editar.activo = usuario['activo']
        usuario_editar.entrenamiento = usuario['entrenamiento']

        guardar_cambios(usuario_editar)
        mensaje = respuesta(True, 'Usuario editado con exito')
        return mensaje, 201

    else:
        mensaje = respuesta(False, 'No existe el usuario')
        return mensaje, 409


def eliminar_usuario(id):
    try:
        Usuario.query.filter_by(id=id).delete()
    except:
        db.session.rollback()
        mensaje = respuesta(False, 'Error eliminando usuario')
        return mensaje, 409
    else:
        db.session.commit()
        mensaje = respuesta(True, 'Usuario eliminado con exito')
        return mensaje, 201


def obtener_usuarios():
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


def obtener_usuario(id):
    return Usuario.query.filter_by(id=id).first()


def obtener_anotadores_activos():
    anotadores_consulta = Usuario.query.filter_by(activo=True).all()
    if not anotadores_consulta:
        return [], 201
    else:
        return marshal(anotadores_consulta, UsuarioDto.usuarioConsultarAsignacion), 201


def obtener_administradores_activos():
    administradores_consultar = Usuario.query.filter_by(rol_usuario=1, activo=True).all()
    if not administradores_consultar:
        return [], 201
    else:
        return marshal(administradores_consultar, UsuarioDto.usuarioConsultarAsignacion), 201


def guardar_cambios(data):
    db.session.add(data)
    db.session.commit()
