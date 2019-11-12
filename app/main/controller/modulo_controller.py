from flask import request
from flask_restplus import Resource

from ..util.dto import ModuloDto
from ..service.modulo_service import guardar_nuevo_tratamiento, obtener_todos_modulos, obtener_un_modulo

api = ModuloDto.api
_modulo = ModuloDto.modulo
_moduloConsultar = ModuloDto.moduloConsultar


@api.route('/')
class ListaModulos(Resource):
    @api.doc('lista de modulos regitrados')
    @api.marshal_list_with(_moduloConsultar)
    def get(self):
        return obtener_todos_modulos()

    @api.response(201,'Modulo creado exitosamente')
    @api.doc('Crear un nuevo modulo')
    @api.expect(_modulo, validate=True)
    def post(self):
        data = request.json
        return guardar_nuevo_tratamiento(data=data)


@api.route('/<id>')
@api.param('id', 'id del modulo')
@api.response(404,'Modulo no encontrado')
class Modulo(Resource):
    @api.doc('Obtener modulo por id')
    @api.marshal_with(_moduloConsultar)
    def get(self,id):
        modulo = obtener_un_modulo(id)
        if not modulo:
            api.abort(404)
        else:
            return modulo