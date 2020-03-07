from flask_restplus import Resource
from flask import request
from ..util.dto import AnotacionDto
from ..service.anotacion_service import guardar_anotacion, obtener_anotaciones_parrafo, \
    obtener_anotaciones_parrafo_anotadores, obtener_anotaciones_politica_anotadores, \
    consultar_anotaciones_usuarios_anotadores, consultar_inconsistencia_consolidacion, \
    obtener_total_anotaciones_parrafo_anotador, obtener_anotaciones_parrafo_anotador, \
    eliminar_anotacion, editar_anotacion

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

    @api.response(201, 'Anotacion editada con exito')
    @api.doc('Editar anotacion de un parrafo')
    def patch(self):
        data = request.json
        return editar_anotacion(data)


@api.route('/<id>')
@api.param('id', 'id del parrafo')
@api.response(404, 'Anotaciones no encontradas')
class AnotacionConsultar(Resource):
    @api.doc('Anotacion por id de parrafo')
    @api.marshal_list_with(_anotacion)
    def get(self, id):
        """Lista de anotaciones por parrafo"""
        return obtener_anotaciones_parrafo(id)

    @api.doc('Eliminar anotacion por Id')
    def delete(self, id):
        """Eliminar anotacion"""
        return eliminar_anotacion(id)


@api.route('/Notificacion/Inconsistencia')
class Anotacion(Resource):
    @api.response(201,'Inconsitencia = true')
    @api.doc('Consultar inconsistencia del parrafo')
    def post(self):
        data = request.json
        return consultar_inconsistencia_consolidacion(data)


@api.route('/Usuario')
class Anotacion(Resource):
    @api.response(201, 'Existen anotaciones')
    @api.doc('Consultar anotaciones de usuarios sobre un parrafo')
    def post(self):
        data = request.json
        return consultar_anotaciones_usuarios_anotadores(data['politica_id'], data['secuencia'])


@api.route('/Total/Anotador')
class AnotacionTotal(Resource):
    @api.response(201, 'Existen anotaciones')
    @api.doc('Consultar total anotaciones de usuarios sobre un parrafo')
    @api.expect(AnotacionDto.consultarTotalAnotaciones, validate=True)
    def post(self):
        data = request.json
        return obtener_total_anotaciones_parrafo_anotador(data)


@api.route('/Anotador/Parrafo')
class Anotacion(Resource):
    @api.response(201, 'Existen anotaciones')
    @api.doc('Consultar anotaciones de usuarios sobre un parrafo')
    @api.expect(AnotacionDto.consultarTotalAnotaciones, validate=True)
    def post(self):
        data = request.json
        return obtener_anotaciones_parrafo_anotador(data)


@api.route('/ParrafoAnotador/<parrafo_id>')
@api.param('parrafo_id', 'id del parrafo')
@api.response(404, 'Anotaciones no encontradas')
class AnotacionConsultar(Resource):
    @api.doc('Lista de tratamientos')
    def get(self, parrafo_id):
        return obtener_anotaciones_parrafo_anotadores(parrafo_id)


@api.route('/ParrafoConsolidador/<parrafo_id>')
@api.param('id', 'id del parrafo')
@api.response(404, 'Anotaciones no encontradas')
class AnotacionConsultar(Resource):
    @api.doc('Lista de tratamientos')
    def get(self, parrafo_id):
        return obtener_anotaciones_politica_anotadores(parrafo_id)