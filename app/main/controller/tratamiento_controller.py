from flask import request
from flask_restplus import Resource
from ..util.dto import TratamientoDto
from ..service.tratamiento_service import guardar_tratamiento, obtener_todos_tratamientos, \
    obtener_tratamientos_completos, obtener_un_tratamiento, editar_tratamiento, eliminar_tratamiento

api = TratamientoDto.api
_tratamiento = TratamientoDto.tratamiento
_tratamientoEditar = TratamientoDto.tratamientoEditar
_tratamientoConsultar = TratamientoDto.tratamientoConsultar
_tratamientoCompleto = TratamientoDto.tratamientoCompleto


@api.route('/')
class TratamientoList(Resource):
    @api.doc('Lista de tratamientos')
    def get(self):
        """Lista de tratamientos registrados"""
        return obtener_todos_tratamientos()

    @api.response(201, 'Tratamiento creado exitosamente')
    @api.doc('Crear nuevo tratamiento')
    @api.expect(_tratamiento, validate=True)
    def post(self):
        """Crea un nuevo tratamiento"""
        data = request.json
        return guardar_tratamiento(data=data)

    @api.response(200, 'Edicion exitosa de tratamiento')
    @api.doc('Editar tratamiento')
    @api.expect(_tratamientoEditar, validate=True)
    def patch(self):
        "Edita el tratamiento por id"
        data = request.json
        return editar_tratamiento(data=data)


@api.route('/TratamientosCompletos')
class TratamientoCompleto(Resource):
    @api.doc('Lista de tratamientos completos')
    @api.marshal_list_with(_tratamientoCompleto)
    def get(self):
        """Lista de tratamientos completos"""
        tratamientos_completos = obtener_tratamientos_completos()
        if not tratamientos_completos:
            api.abort(404)
        else:
            return tratamientos_completos


@api.route('/<id>')
@api.param('id', 'id de tratamiento')
@api.response(404, 'Tratamiento no encontrado')
class Tratamiento(Resource):
    @api.doc('Obtener tratamiento')
    def get(self, id):
        """obtener tratamiento por id"""
        tratamiento = obtener_un_tratamiento(id)
        if not tratamiento:
            api.abort(404)
        else:
            return tratamiento



    @api.response(200, 'Tratamiento eliminado con exito')
    @api.doc('Eliminar tratamiento')
    def delete(self, id):
        "Eliminar tratamiento"
        return eliminar_tratamiento(id=id)

