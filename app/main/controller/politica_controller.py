from flask_restplus import Resource
from flask import request
from ..util.dto import PoliticaDto
from..service.politica_service import previsualizar_politica, guardar_politica, guardar_usuario_politica, \
    actualizar_usuario_politica, politica_lista_para_consolidar_api, consultar_politicas_anotador_no_finalizadas,\
    consultar_politicas_consolidador_no_finalizadas

api = PoliticaDto.api
_politicaUsuarioGuardar = PoliticaDto.politicaUsuarioGuardar


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
    @api.expect(_politicaUsuarioGuardar, validate=True)
    def post(self):
        data = request.json
        return guardar_usuario_politica(data)

    @api.response(201, 'Poltica usuario actualizado')
    @api.doc('Actualizar usuario finalizo politica')
    def put(self):
        data = request.json
        return actualizar_usuario_politica(data)


@api.route('/ListaConsolidar/<politica_id>')
@api.param('politica_id', 'id de la politica a consolidar')
@api.response(404, 'Politica no encontrada')
class Politica(Resource):
    @api.response(201, 'Poltica lista')
    @api.doc('Consultar si politica lista para consolidar')
    def get(self, politica_id):
        return politica_lista_para_consolidar_api(politica_id)


@api.route('/Anotar/<usuario_id>')
@api.param('usuario_id', 'Politicas del usuario para anotar')
@api.response(404, 'Politica no encontrada')
class Politica(Resource):
    @api.doc('Consultar politicas por anotar')
    def get(self, usuario_id):
        return consultar_politicas_anotador_no_finalizadas(usuario_id)


@api.route('/Consolidar/<administrador_id>')
@api.param('administrador_id', 'Politicas del usuario para anotar')
@api.response(404, 'Politica no encontrada')
class Politica(Resource):
    @api.doc('Consultar politicas por consolidar')
    def get(self, administrador_id):
        return consultar_politicas_consolidador_no_finalizadas(administrador_id)


