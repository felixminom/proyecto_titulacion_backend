from flask import request
from flask_restplus import Resource

from ..util.dto import UsuarioDto
from ..service.usuario_service import guardar_nuevo_usuario, obtnener_usuarios, obtener_usuario, \
    editar_usuario, eliminar_usuario, obtener_anotadores_activos, obtener_administradores_activos

api = UsuarioDto.api
_usuario = UsuarioDto.usuario
_usuarioEditar = UsuarioDto.usuarioEditar
_usuarioConsultar = UsuarioDto.usuarioConsultar


@api.route('/', methods=['GET', 'POST', 'PATCH'])
class ListaUsuarios(Resource):
    @api.doc('lista de usuarios registrados')
    @api.marshal_list_with(_usuarioConsultar)
    def get(self):
        """Lista de todos los usuarios registrados"""
        return obtnener_usuarios()

    @api.response(201,'Usuario registrado exitosamente')
    @api.doc('Crear un nuevo usuario')
    @api.expect(_usuario, validate=True)
    def post(self):
        """Crear un nuevo usuario"""
        data = request.json
        return guardar_nuevo_usuario(data=data)

    @api.response(201, 'Usuario editado exitosamente')
    @api.doc('Editar un usuario')
    @api.expect(_usuarioEditar, validate=True)
    def patch(self):
        """Crear un nuevo usuario"""
        data = request.json
        return editar_usuario(data=data)


@api.route('/<id>', methods=['DELETE', 'GET'])
@api.param('id', 'Identificador del usuario')
@api.response(404,'Usuario no encontrado')
class Usuario(Resource):
    @api.response(201, 'Usuario eliminado exitosamente')
    @api.doc('Eliminar un usuario')
    def delete(self, id):
        """Eliminar un usuario"""
        return eliminar_usuario(id=id)

    @api.doc('Obtener Usuario por email')
    @api.marshal_with(_usuarioConsultar)
    def get(self, id):
        """obtener usuario por email"""
        usuario = obtener_usuario(id)
        if not usuario:
            api.abort(404)
        else:
            return usuario


@api.route('/AnotadoresActivos', methods=['GET'])
@api.response(404, 'Anotadores no encontrados')
class Usuario(Resource):
    @api.response(201, 'Anotadores')
    @api.doc('Obtener anotadores para asignar')
    def get(self):
        """Obtener anotadores"""
        return obtener_anotadores_activos()


@api.route('/AdministradoresActivos', methods=['GET'])
@api.response(404, 'Administradores no encontrados')
class Usuario(Resource):
    @api.response(201, 'Administradores')
    @api.doc('Obtener administradores para asignar')
    def get(self):
        """Obtener Administradores"""
        return obtener_administradores_activos()
