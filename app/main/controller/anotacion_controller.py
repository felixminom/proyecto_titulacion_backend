from flask_restplus import Resource
from flask import request, abort
from ..util.dto import AnotacionDto
from werkzeug.exceptions import BadRequest
from ..service.anotacion_service import guardar_anotacion, obtener_anotaciones_parrafo, \
    obtener_anotaciones_parrafo_anotadores, obtener_anotaciones_politica_anotadores

api = AnotacionDto.api
_anotacion = AnotacionDto.anotacion
_anotacionConsultar = AnotacionDto.anotacionConsultar


@api.route('/')
class Anotacion(Resource):
    @api.response(201,'Anotacion creada con exito')
    @api.doc('Crear nueva anotacion de un parrafo')
    @api.expect(_anotacion, validate=True)
    def post(self):
        data = request.json
        return guardar_anotacion(data)


@api.route('/<id>')
@api.param('id', 'id del parrafo')
@api.response(404, 'Anotaciones no encontradas')
class AnotacionConsultar(Resource):
    @api.doc('Lista de tratamientos')
    @api.marshal_list_with(_anotacion)
    def get(self, id):
        """Lista de anotaciones por parrafo"""
        return obtener_anotaciones_parrafo(id)


@api.route('/ParrafoAnotador/<parrafo_id>')
@api.param('parrafo_id', 'id del parrafo')
@api.response(404, 'Anotaciones no encontradas')
class AnotacionConsultar(Resource):
    @api.doc('Lista de tratamientos')
    @api.marshal_list_with(_anotacionConsultar)
    def get(self, parrafo_id):
        return obtener_anotaciones_parrafo_anotadores(parrafo_id)


@api.route('/PoliticaAnotador/<politica_id>')
@api.param('politica_id', 'id de la politica')
@api.response(404, 'Anotaciones no encontradas')
class AnotacionConsultar(Resource):
    @api.doc('Lista de Anotaciones')
    def get(self, politica_id):
        return obtener_anotaciones_politica_anotadores(politica_id)


@api.route('/ParrafoConsolidador/<parrafo2_id>')
@api.param('id', 'id del parrafo')
@api.response(404, 'Anotaciones no encontradas')
class AnotacionConsultar(Resource):
    @api.doc('Lista de tratamientos')
    def get(self, parrafo_id):
        return obtener_anotaciones_politica_anotadores(parrafo_id)


@api.errorhandler
def default_error_handler(error):
    '''Default error handler'''
    return {'message': str(error)}, getattr(error, 'code', 500)