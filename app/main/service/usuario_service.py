from app.main import db
from app.main.model.usuario import Usuario
from app.main.model.rol_usuario import RolUsuario
from app.main.util.clases_auxiliares import UsuarioConsultar
import datetime


def guardar_nuevo_usuario(data):
    user = Usuario.query.filter_by(email=data['email']).first()
    if not user:
        nuevo_usuario = Usuario(
            email=data['email'],
            hora_registro=datetime.datetime.now(),
            rol_usuario=data['rol_usuario'],
            clave=data['clave'],
            activo=True,
            entrenamiento= data['entrenamiento']
        )
        guardar_cambios(nuevo_usuario)
        response_object = {
            'estado': 'exito',
            'mensaje': 'Usuario registrado exitosamente'
        }
        return response_object, 201
    else:
        response_object = {
            'estado': 'fallido',
            'mensaje': 'El usuario ya existe, por favor inicie sesion'
        }
        return response_object, 409


def obtnener_todos_usuarios():
    db.session.configure(autoflush=False)
    resultado = db.session.query(Usuario.id, Usuario.email, Usuario.activo, Usuario.entrenamiento, RolUsuario.nombre).\
        outerjoin(RolUsuario, RolUsuario.id == Usuario.rol_usuario).all()
    usuarios = [UsuarioConsultar]
    i = 0
    usuarios.clear()
    for item in resultado:
        user_aux = UsuarioConsultar(item[0], item[1], item[4], item[2], item[3])
        usuarios.insert(i, user_aux)
        i += 1
    return usuarios


def obtener_un_usuario(email):
    return Usuario.query.filter_by(email=email).first()


def generar_token(usuario):
    try:
        auth_token = usuario.codificar_auth_token(usuario_id=usuario.id)
        response_object = {
            'estado': 'exito',
            'mensaje': 'Usuario registrado exitosamente',
            'Authorization': auth_token.decode()
        }
        return  response_object, 201
    except Exception as e:
        response_object = {
            'estado': 'fallido',
            'mensaje': 'Ocurrio un error, por favor intente de nuevo'
        }
        return response_object, 401


def guardar_cambios(data):
    db.session.add(data)
    db.session.commit()

