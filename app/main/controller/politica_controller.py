from flask_restplus import Resource
from flask import request
from ..util.dto import PoliticaDto
from..service.politica_service import previsualizar_politica, guardar_politica, guardar_usuario_politica, \
    actualizar_usuario_politica_asignada, consultar_politicas_anotador_no_finalizadas,\
    consultar_politicas_consolidador_no_finalizadas, consultar_politica_parrafos, consultar_politicas, \
    eliminar_politica, editar_politica, actualizar_politica_asignada

api = PoliticaDto.api
_politicaUsuarioGuardar = PoliticaDto.politicaUsuarioGuardar


@api.route('/')
class Politica(Resource):
    @api.response(201, 'Poltica procesada y creada')
    @api.doc('Crear nueva politica de privacidad')
    def post(self):
        return guardar_politica()

    @api.response(201, 'Lista de politicas')
    @api.doc('Consultar politicas de privacidad existentes')
    def get(self):
        return consultar_politicas()

    @api.response(201, 'Politica editada con exito')
    @api.doc('Editar política')
    def patch(self):
        data = request.json
        return editar_politica(data)


@api.route('/Asignada')
class Politica(Resource):
    @api.response(201, 'Politica asignada editada con exito')
    @api.doc('Marcar política como asignada')
    def patch(self):
        data = request.json
        return actualizar_politica_asignada(data)


@api.route('/<id>')
@api.param('id', 'Identificador de la politica')
@api.response(404, 'Politica no encontrada')
class Politica(Resource):
    @api.response(201, 'Politica eliminado con exito')
    @api.doc('Eliminar política por id')
    def delete(self, id):
        return eliminar_politica(id=id)


@api.route('/Previsualizacion')
class PoliticaPrevisualizar(Resource):
    @api.response(201, 'Poltica procesada y creada')
    @api.doc('Preprocesa la politica de privacidad '
             'y la separa por secciones. No guarda la política')
    def post(self):
        return previsualizar_politica()


@api.route('/Usuarios')
class Politica(Resource):
    @api.response(201, 'Usuarios ingresados')
    @api.doc('Asignar politica a usuarios (anotadoresy consolidador)')
    @api.expect(_politicaUsuarioGuardar, validate=True)
    def post(self):
        data = request.json
        return guardar_usuario_politica(data)


@api.route('/Anotador')
class Politica(Resource):
    @api.response(201, 'Poltica usuario actualizado')
    @api.doc('Actualizar si usuario finalizó la anotación de la política')
    @api.expect(_politicaUsuarioGuardar, validate=True)
    def patch(self):
        data = request.json
        return actualizar_usuario_politica_asignada(data)


@api.route('/Anotar/<usuario_id>')
@api.param('usuario_id', 'Politicas del usuario para anotar')
@api.response(404, 'Politica no encontrada')
class Politica(Resource):
    @api.doc('Consultar politicas por anotar de un usuario')
    def get(self, usuario_id):
        return consultar_politicas_anotador_no_finalizadas(usuario_id)


@api.route('/Consolidar/<administrador_id>')
@api.param('administrador_id', 'Politicas del usuario para anotar')
@api.response(404, 'Politica no encontrada')
class Politica(Resource):
    @api.doc('Consultar politicas por consolidar de un usuario')
    def get(self, administrador_id):
        return consultar_politicas_consolidador_no_finalizadas(administrador_id)


@api.route('/Parrafos/<politica_id>')
@api.param('politica_id', 'Id de la poitica')
@api.response(404, 'Politica no encontrada')
class Politica(Resource):
    @api.doc('Consultar parrafos de una política')
    def get(self, politica_id):
        return consultar_politica_parrafos(politica_id)
