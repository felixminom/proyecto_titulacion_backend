from flask import request
from flask_restplus import Resource

from ..util.dto import RolUsuarioDto
from ..service.rol_usuario_service import guardar_rol, obtener_roles, editar_rol, eliminar_rol,\
    obtener_rol, guardar_rol_modulo, obtener_modulo_rol

api = RolUsuarioDto.api
_rolUsuario = RolUsuarioDto.rolUsuario
_rolUsuarioConsultar = RolUsuarioDto.rolUsuarioConsultar
_rolUsuarioModulo = RolUsuarioDto.rolUsuarioModulo
_rolEditar = RolUsuarioDto.rolUsuarioEditar


@api.route('/')
class ListaRolesUsuario(Resource):
    @api.doc('lista de todos los roles de usuario')
    @api.marshal_list_with(_rolUsuarioConsultar)
    def get(self):
        return obtener_roles()

    @api.response(201, 'Rol de usuario registrado exitosamente.')
    @api.doc('Crear nuevo rol de usuario')
    @api.expect(_rolUsuario, validate=True)
    def post(self):
        rol = request.json
        return guardar_rol(rol)

    @api.response(201, 'Rol de usuario editado exitosamente')
    @api.doc('Editar Rol de usuario')
    @api.expect(_rolEditar, validate=True)
    def patch(self):
        rol = request.json
        return editar_rol(rol)


@api.route('/Modulo')
class RolUsuarioModulo(Resource):
    @api.response(201, 'Modulo agregado a Rol de usuario exitosamente')
    @api.doc('Relaciona un módulo a un rol de usuario')
    @api.expect(_rolUsuarioModulo, validate=True)
    def post(self):
        modulo = request.json
        return guardar_rol_modulo(modulo)


@api.route('/<id>')
@api.param('id', 'Identificador del rol de usuario')
@api.response(404, 'Rol de usuario no encontrado')
class RolUsuario(Resource):
    @api.doc('Obtener rol de usuario por id')
    @api.marshal_with(_rolUsuarioConsultar)
    def get(self, id):
        rol_usuario = obtener_rol(id)
        if not rol_usuario:
            api.abort(404)
        else:
            return rol_usuario

    @api.doc('Eliminar rol usuario por id')
    def delete(self, id):
        return eliminar_rol(id)
