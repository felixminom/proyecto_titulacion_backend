from ..model.usuario import Usuario
from ..model.rol_usuario import RolUsuario
from ..util.dto import UsuarioDto
from ..service.lista_negra_service import guardar_token
from ..util.clases_auxiliares import ModuloConsultarHijos, UsuarioConsultarLogin
from flask_restplus import marshal

usuario = UsuarioConsultarLogin
usuario.modulos = []


def consultar_modulos_hijos(rol_usuario):
    rol_usuario = RolUsuario.query.filter_by(id=rol_usuario).first()
    i = 0
    usuario.modulos.clear()
    for modulo in rol_usuario.modulos:
        modulo_aux = ModuloConsultarHijos(modulo.nombre, modulo.icono, modulo.path, modulo.hijos)
        usuario.modulos.insert(i, modulo_aux)
        i += 1
    usuario.rol_usuario = rol_usuario.nombre
    return marshal(usuario, UsuarioDto.usuarioConsultarLogin)


class Auth:
    @staticmethod
    def login_usuario(data):
        try:
            usuario_aux = Usuario.query.filter_by(email=data['email'], activo=True).first()
            if usuario_aux and usuario_aux.comparar_clave(data['clave']):
                usuario.id = usuario_aux.id
                usuario.email = usuario_aux.email
                usuario.rol_usuario = usuario_aux.rol_usuario
                usuario.activo = usuario_aux.activo
                usuario.entrenamiento = usuario_aux.entrenamiento
                auth_token = Usuario.codificar_auth_token(usuario_id=usuario_aux.id)
                if auth_token:
                    response_object = {
                        'estado': True,
                        'mensaje': 'Sesion iniciada exitosamente',
                        'Authorization': auth_token.decode(),
                        'usuario': consultar_modulos_hijos(usuario.rol_usuario)
                    }
                    return response_object, 201
            else:
                response_object = {
                    'estado': 'fallido',
                    'mensaje': 'email o hash_clave no coinciden'
                }
                return response_object, 401
        except Exception as e:
            print(e)
            response_object = {
                'estado': 'fallido',
                'mensaje': '{}'.format(e)
            }
            return response_object, 500

    @staticmethod
    def logout_usuario(data):
        if data:
            auth_token = data
        else:
            auth_token = ''
        if auth_token:
            respuesta = Usuario.decodificar_auth_token(auth_token)
            if not isinstance(respuesta, str):
                return guardar_token(token=auth_token, usuario_id=respuesta)
            else:
                response_object = {
                    'estado': 'fallido',
                    'mensaje': respuesta
                }
                return response_object, 401
        else:
            response_object = {
                'estado': 'fallido',
                'mensaje': 'Provea un token de autorizacion valido'
            }
            return response_object, 403

    @staticmethod
    def obtener_usuario_logeado(data):
        auth_token = data
        if auth_token:
            respuesta = Usuario.decodificar_auth_token(auth_token)
            if not isinstance(respuesta, str):
                usuarioAux = Usuario.query.filter_by(id=respuesta).first()
                user = UsuarioConsultarLogin
                user.id = usuarioAux.id
                user.email = usuarioAux.email
                user.rol_usuario = usuarioAux.rol_usuario
                user.activo = usuarioAux.activo
                user.entrenamiento = usuarioAux.entrenamiento
                response_object = {
                    'estado': True,
                    'mensaje': 'Token valido'
                }
                return response_object, 200
            response_object = {
                'estado': 'fallido',
                'mensaje': respuesta
            }
            return response_object, 401
        else:
            response_object = {
                'estado': 'fallido',
                'mensaje': 'Provea un token valido'
            }
            return response_object, 401
