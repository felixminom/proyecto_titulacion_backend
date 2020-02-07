from flask_restplus import Resource
from flask import request
from ..util.dto import PoliticaDto
from..service.politica_service import previsualizar_politica, guardar_politica, guardar_usuario_politica, \
    actualizar_usuario_politica, politica_lista_para_consolidar_api, consultar_politica_anotadores_no_finalizadas

api = PoliticaDto.api


@api.route('/')
class Politica(Resource):
    @api.response(201, 'Poltica procesada y creada')
    @api.doc('Crear nueva politica de privacidad')
    def post(self):
        return guardar_politica()


@api.route('/Previsualizacion')
class PoliticaPrevisualizar(Resource):
    @api.response(201, 'Poltica procesada y creada')
    @api.doc('Preprocesa la politica de privacidad')
    def post(self):
        return previsualizar_politica()


@api.route('/Usuarios')
class Politica(Resource):
    @api.response(201, 'Usuarios ingresados')
    @api.doc('Asignar politica a usuarios')
    def post(self):
        data = request.json
        return guardar_usuario_politica(data)

    @api.response(201, 'Poltica usuario actualizado')
    @api.doc('Actualizar usuario finalizo politica')
    def put(self):
        data = request.json
        return actualizar_usuario_politica(data)


@api.route('/Anotar/<usuario_id>')
@api.param('politica_id', 'id de la politica a consolidar')
@api.response(404, 'Politica no encontrada')
class Politica(Resource):
    @api.response(201, 'Poltica lista')
    @api.doc('Consultar si politica lista para consolidar')
    def get(self, usuario_id):
        return consultar_politica_anotadores_no_finalizadas(usuario_id)


