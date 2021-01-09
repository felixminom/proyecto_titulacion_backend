from flask import request
from flask_restplus import Resource
from ..util.dto import TratamientoDto
from ..service.tratamiento_service import guardar_tratamiento, obtener_tratamientos, \
    obtener_tratamientos_completos, editar_tratamiento, eliminar_tratamiento

api = TratamientoDto.api
_tratamiento = TratamientoDto.tratamiento
_tratamientoEditar = TratamientoDto.tratamientoEditar
_tratamientoConsultar = TratamientoDto.tratamientoConsultar
_tratamientoCompleto = TratamientoDto.tratamientoCompleto


@api.route('/')
class TratamientoList(Resource):
    @api.doc('Lista de todos los tratamientos')
    def get(self):
        return obtener_tratamientos()

    @api.response(201, 'Tratamiento creado exitosamente')
    @api.doc('Crear nuevo tratamiento')
    @api.expect(_tratamiento, validate=True)
    def post(self):
        data = request.json
        return guardar_tratamiento(data=data)

    @api.response(200, 'Edicion exitosa de tratamiento')
    @api.doc('Editar tratamiento')
    @api.expect(_tratamientoEditar, validate=True)
    def patch(self):
        data = request.json
        return editar_tratamiento(data=data)


@api.route('/TratamientosCompletos')
class TratamientoCompleto(Resource):
    @api.doc('Lista de tratamientos con sus atributo y valores')
    @api.marshal_list_with(_tratamientoCompleto)
    def get(self):
        tratamientos_completos = obtener_tratamientos_completos()
        if not tratamientos_completos:
            api.abort(404)
        else:
            return tratamientos_completos


@api.route('/<id>')
@api.param('id', 'id de tratamiento')
@api.response(404, 'Tratamiento no encontrado')
class Tratamiento(Resource):
    @api.response(200, 'Tratamiento eliminado con exito')
    @api.doc('Eliminar tratamiento por id')
    def delete(self, id):
        return eliminar_tratamiento(id=id)
