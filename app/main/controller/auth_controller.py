from flask import request
from flask_restplus import Resource

from app.main.service.auth_service import Auth
from ..util.dto import AuthDto

api = AuthDto.api
_usuario_auth = AuthDto.usuario_auth


@api.route('/login')
class UsuarioLogin(Resource):
    """
        API Login de usuario
    """
    @api.doc('login de usuario')
    @api.expect(_usuario_auth, validate=True)
    def post(self):
        """Ingresar al sistema"""
        data = request.json
        return Auth.login_usuario(data)


@api.route('/logout')
class UsuarioLogout(Resource):
    """
        API Logout de usuario
    """
    @api.doc('logout de usuario')
    def get(self):
        """Salir del sistema"""
        auth_header = request.headers.get('Authorization')
        return Auth.logout_usuario(data=auth_header)


@api.route('/logged')
class UsuarioLogged(Resource):
    """
        API para verificar si el token aun es valido
    """
    @api.doc('usuario logged')
    def post(self):
        """Verificar token valido"""
        auth_header = request.headers.get('Authorization')
        return Auth.obtener_usuario_logeado(data=auth_header)
