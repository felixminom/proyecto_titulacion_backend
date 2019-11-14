from flask import request
from flask_restplus import Resource

from ..util.dto import AtributoDto
from ..service.atributo_services import guardar_atributo, obtener_todos_atributos, obtener_atributo, \
    obtener_atributos_tratamiento

api = AtributoDto.api
_atributo = AtributoDto.atributo
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


@api.route('/Tratamiento/<tratamiento_id>')
@api.param('tratamiento_id', 'id del tratamiento')
@api.response(404, 'No existen atributos para este tratamiento')
class AtributoTratamientoId(Resource):
    @api.doc('Obtener tratamiento')
    @api.marshal_with(_atributoConsultar)
    def get(self, tratamiento_id):
        """obtener atributos por tratamiento"""
        return obtener_atributos_tratamiento(tratamiento_id)


@api.route('/<id>')
@api.param('id','id de atributo')
@api.response(404, 'Atributo no encontrado')
class AtributoId(Resource):
    @api.doc('Obtener tratamiento')
    @api.marshal_with(_atributoConsultar)
    def get(self, id):
        """obtener atributos por id"""
        atributo = obtener_atributo(id)
        if not atributo:
            response_object = {
                'estado': 'fallido',
                'mensaje': 'No existen atributo'
            }
            return response_object, 404
        else:
            return atributo


