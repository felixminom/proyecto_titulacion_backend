from flask import request
from flask_restplus import Resource

from ..util.dto import ModuloDto
from ..service.modulo_service import guardar_modulo, obtener_modulos, obtener_modulo, editar_modulo, eliminar_modulo

api = ModuloDto.api
_modulo = ModuloDto.modulo
_moduloConsultar = ModuloDto.moduloConsultar
_moduloEditar = ModuloDto.moduloEditar


@api.route('/')
class ListaModulos(Resource):
    @api.doc('lista de modulos regitrados')
    @api.marshal_list_with(_moduloConsultar)
    def get(self):
        return obtener_modulos()

    @api.response(201, 'Modulo creado exitosamente')
    @api.doc('Crear un nuevo modulo')
    @api.expect(_modulo, validate=True)
    def post(self):
        data = request.json
        return guardar_modulo(data)

    @api.response(201, 'Módulo editado exitosamente')
    @api.doc('Editar un módulo')
    @api.expect(_moduloEditar, validate=True)
    def patch(self):
        data = request.json
        return editar_modulo(data)


@api.route('/<id>')
@api.param('id', 'id del modulo')
@api.response(404, 'Modulo no encontrado')
class Modulo(Resource):
    @api.doc('Obtener modulo por id')
    @api.marshal_with(_moduloConsultar)
    def get(self, id):
        modulo = obtener_modulo(id)
        if not modulo:
            api.abort(404)
        else:
            return modulo

    @api.doc('Eliminar color')
    def delete(self, id):
        return eliminar_modulo(id)
