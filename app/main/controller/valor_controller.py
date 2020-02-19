from flask import request
from flask_restplus import Resource

from ..util.dto import ValorDto
from ..service.valor_service import guardar_valor, obtener_valor, obtener_todos_valores, obtener_valores_atributo, \
    obtener_valor_completo


api = ValorDto.api
_valor = ValorDto.valor
_valorConsultar = ValorDto.valorConsultar


@api.route('/')
class Valor(Resource):
    @api.doc('Lista de atributos')
    @api.marshal_list_with(_valorConsultar)
    def get(self):
        """Lista de todos los valores"""
        return obtener_todos_valores()

    @api.response(201, 'Valor creado exitosamente')
    @api.doc('Crear nuevo valor de un atributo')
    @api.expect(_valor, validate=True)
    def post(self):
        """Crear valor de un atributo"""
        data = request.json
        return guardar_valor(valor=data)


@api.route('/Atributo/<atributo_id>')
@api.param('atributo_id', 'id del atributo')
@api.response(404, 'No existen valores para este atributo')
class ValorAtributoId(Resource):
    @api.doc('Obtener tratamiento')
    @api.marshal_with(_valorConsultar)
    def get(self, atributo_id):
        """obtener valores por atributo"""
        return obtener_valores_atributo(atributo_id=atributo_id)


@api.route('/<id>')
@api.param('id','id de valor')
@api.response(404, 'Valor no encontrado')
class ValorId(Resource):
    @api.doc('Obtener valor por id')
    def get(self, id):
        """obtener valor por id"""
        return obtener_valor(id)


@api.route('/Completo/<id>')
@api.param('id','id de valor')
@api.response(404, 'Valor no encontrado')
class ValorId(Resource):
    @api.doc('Obtener valor por id')
    def get(self, id):
        """obtener valor por id"""
        return obtener_valor_completo(id)