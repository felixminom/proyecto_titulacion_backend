from flask import request
from flask_restplus import Resource
from ..util.dto import AtributoDto
from ..service.atributo_service import guardar_atributo, obtener_todos_atributos, \
    obtener_atributos_tratamiento, editar_atributo, eliminar_atributo

api = AtributoDto.api
_atributo = AtributoDto.atributo
_atributoEditar = AtributoDto.atributoEditar
_atributoConsultar = AtributoDto.atributoConsultar


@api.route('/')
class Atributo(Resource):
    @api.doc('Lista de atributos')
    @api.marshal_list_with(_atributoConsultar)
    def get(self):
        """Lista de todos los atributos"""
        return obtener_todos_atributos()

    @api.response(201, 'Atributo creado exitosamente')
    @api.doc('Crear nuevo atributo de un tratamiento')
    @api.expect(_atributo, validate=True)
    def post(self):
        """Crear atributo de un tratamiento"""
        data = request.json
        return guardar_atributo(atributo=data)

    @api.response(201, 'Atributo editado exitosamente')
    @api.doc('Editar atributo de un tratamiento')
    @api.expect(_atributoEditar, validate=True)
    def patch(self):
        """Editar atributo de un tratamiento"""
        data = request.json
        return editar_atributo(data)


@api.route('/Tratamiento/<tratamiento_id>')
@api.param('tratamiento_id', 'id del tratamiento')
@api.response(404, 'No existen atributos para este tratamiento')
class AtributoTratamientoId(Resource):
    @api.doc('Obtener tratamiento')
    def get(self, tratamiento_id):
        """obtener atributos por tratamiento"""
        return obtener_atributos_tratamiento(tratamiento_id)


@api.route('/<id>')
@api.param('id', 'id de atributo')
@api.response(404, 'Atributo no encontrado')
class AtributoId(Resource):
    @api.doc('Eliminar atributo')
    def delete(self, id):
        """Eliminar atributo"""
        return eliminar_atributo(id)
