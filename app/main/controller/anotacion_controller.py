from flask_restplus import Resource
from flask import request
from ..util.dto import AnotacionDto
from ..service.anotacion_service import guardar_anotacion, \
    consultar_anotaciones_anotadores, obtener_total_anotaciones_parrafo_anotador, \
    obtener_anotaciones_parrafo_usuario, eliminar_anotacion, editar_anotacion, consultar_inconsistencia_notificacion,\
    consultar_detalles_anotacion_politica

api = AnotacionDto.api
_anotacion = AnotacionDto.anotacion
_anotacionConsultar = AnotacionDto.anotacionConsultar
_anotacionNotificacion = AnotacionDto.anotacionNotificacion


@api.route('/')
class Anotacion(Resource):
    @api.response(201, 'Anotacion creada con exito')
    @api.doc('Crear nueva anotación de un párrafo')
    @api.expect(_anotacion, validate=True)
    def post(self):
        data = request.json
        return guardar_anotacion(data)

    @api.response(201, 'Anotacion editada con exito')
    @api.doc('Editar anotación de un párrafo')
    def patch(self):
        data = request.json
        return editar_anotacion(data)


@api.route('/Detalles')
class Anotacion(Resource):
    @api.response(201, AnotacionDto.detallesAnotacionPolitica)
    @api.doc('Consultar coeficiente interanotador de una política')
    def post(self):
        data = request.json
        return consultar_detalles_anotacion_politica(data)


@api.route('/Notificacion')
class Anotacion(Resource):
    @api.response(201, 'Consultar incosistencia en anotacion')
    @api.doc('Consultar incosistencia en anotacion')
    @api.expect(_anotacionNotificacion, validate=True)
    def post(self):
        data = request.json
        return consultar_inconsistencia_notificacion(data)


@api.route('/<id>')
@api.param('id', 'id de anotación')
@api.response(404, 'Anotaciones no encontradas')
class AnotacionConsultar(Resource):
    @api.doc('Eliminar anotación por Id')
    def delete(self, id):
        return eliminar_anotacion(id)


@api.route('/Usuario')
class Anotacion(Resource):
    @api.response(201, 'Existen anotaciones')
    @api.doc('Consultar anotaciones de usuarios sobre un párrafo')
    def post(self):
        data = request.json
        return consultar_anotaciones_anotadores(data)


@api.route('/Total/Anotador')
class AnotacionTotal(Resource):
    @api.response(201, 'Existen anotaciones')
    @api.doc('Consultar total de anotaciones de usuario sobre un párrafo')
    @api.expect(AnotacionDto.consultarTotalAnotaciones, validate=True)
    def post(self):
        data = request.json
        return obtener_total_anotaciones_parrafo_anotador(data)


@api.route('/Usuario/Parrafo')
class Anotacion(Resource):
    @api.response(201, 'Existen anotaciones')
    @api.doc('Consultar anotaciones de usuarios sobre un párrafo')
    @api.expect(AnotacionDto.consultarTotalAnotaciones, validate=True)
    def post(self):
        data = request.json
        return obtener_anotaciones_parrafo_usuario(data)
