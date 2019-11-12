from flask import request
from flask_restplus import Resource

from ..util.dto import RolUsuarioDto
from ..service.rol_usuario_service import guardar_nuevo_rol, obtener_todos_roles, obtener_un_rol, guardar_rol_modulo, obtener_modulo_rol

api = RolUsuarioDto.api
_rolUsuario = RolUsuarioDto.rolUsuario
_rolUsuarioConsultar = RolUsuarioDto.rolUsuarioConsultar
_rolUsuarioModulo = RolUsuarioDto.rolUsuarioModulo


@api.route('/')
class ListaRolesUsuario(Resource):
    @api.doc('lista de roles de usuario')
    @api.marshal_list_with(_rolUsuarioConsultar)
    def get(self):
        """"Obtener todos los roles de usuario"""
        return obtener_todos_roles()

    @api.response(201,'Rol de usuario registrado exitosamente.')
    @api.doc('Crear nuevo rol de usuario')
    @api.expect(_rolUsuario, validate=True)
    def post(self):
        """Crear un rol de usuario"""
        data = request.json
        return guardar_nuevo_rol(data=data)


@api.route('/Modulo')
class RolUsuarioModulo(Resource):
    @api.response(201, 'Modulo agregado a Rol de usuario exitosamente')
    @api.doc('Agregar un modulo a un rol de usuario')
    @api.expect(_rolUsuarioModulo, validate= True)
    def post(self):
        """Agregar un modulo a un rol de usuario"""
        data=request.json
        return guardar_rol_modulo(data=data)
    @api.doc('Obtener modulos de los roles de usuario')
    def get(self):
        """Obtener modulos de los roles de usuario"""
        return obtener_modulo_rol(rol_id=0)



@api.route('/<id>')
@api.param('id','Identificador del rol de usuario')
@api.response(404,'Rol de usuario no encontrado')
class RolUsuario(Resource):
    @api.doc('Obtener rol de usuario por id')
    @api.marshal_with(_rolUsuarioConsultar)
    def get(self,id):
        """Buscar rol de usuario por id"""
        rol_usuario = obtener_un_rol(id)
        if not rol_usuario:
            api.abort(404)
        else:
            return rol_usuario

