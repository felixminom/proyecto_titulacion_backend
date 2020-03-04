from flask_restplus import Resource
from flask import request
from ..util.dto import PoliticaDto
from..service.politica_service import previsualizar_politica, guardar_politica, guardar_usuario_politica, \
    actualizar_anotador_politica, consultar_politicas_anotador_no_finalizadas,\
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
    @api.doc('Editar politica')
    def patch(self):
        """Editar una politica"""
        data = request.json
        return editar_politica(data)


@api.route('/Asignada')
class Politica(Resource):
    @api.response(201, 'Politica asignada editada con exito')
    @api.doc('Editar asignar politica')
    def patch(self):
        """Editar asignar de politica"""
        data = request.json
        return actualizar_politica_asignada(data)


@api.route('/<id>', methods=["DELETE"])
@api.param('id', 'Identificador de la politica')
@api.response(404,'Politica no encontrado')
class Politica(Resource):
    @api.response(201, 'Politica eliminado con exito')
    @api.doc('Eliminar politica')
    def delete(self, id):
        """Eliminar una politica"""
        return eliminar_politica(id=id)


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


@api.route('/Anotador')
class Politica(Resource):
    @api.response(201, 'Poltica usuario actualizado')
    @api.doc('Actualizar usuario finalizo politica')
    def patch(self):
        data = request.json
        return actualizar_anotador_politica(data)


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


@api.route('/Parrafos/<politica_id>')
@api.param('politica_id', 'Id de la poitica')
@api.response(404, 'Politica no encontrada')
class Politica(Resource):
    @api.doc('Consultar parrafospolitica')
    def get(self, politica_id):
        return consultar_politica_parrafos(politica_id)

