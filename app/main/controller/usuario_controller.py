from flask import request
from flask_restplus import Resource

from ..util.dto import UsuarioDto
from ..service.usuario_service import guardar_nuevo_usuario, obtnener_todos_usuarios, obtener_un_usuario

api = UsuarioDto.api
_usuario = UsuarioDto.usuario
_usuarioConsultar = UsuarioDto.usuarioConsultar


@api.route('/')
class ListaUsuarios(Resource):
    @api.doc('lista de usuarios registrados')
    @api.marshal_list_with(_usuarioConsultar)
    def get(self):
        """Lista de todos los usuarios registrados"""
        return obtnener_todos_usuarios()

    @api.response(201,'Usuario registrado exitosamente')
    @api.doc('Crear un nuevo usuario')
    @api.expect(_usuario, validate=True)
    def post(self):
        """Crear un nuevo usuario"""
        data = request.json
        return guardar_nuevo_usuario(data=data)


@api.route('/<email>')
@api.param('email','Identificador del usuario')
@api.response(404,'Usuario no encontrado')
class Usuario(Resource):
    @api.doc('Obtener Usuario por email')
    @api.marshal_with(_usuarioConsultar)
    def get(self,email):
        """obtener usuario por email"""
        usuario = obtener_un_usuario(email)
        if not usuario:
            api.abort(404)
        else:
            return usuario




