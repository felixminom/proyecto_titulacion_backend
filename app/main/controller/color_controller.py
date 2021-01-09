from flask import request
from flask_restplus import Resource

from ..util.dto import ColorDto
from ..service.color_service import guardar_color, obtener_todos_colores, \
    obtener_color, obtener_colores_disponibles, editar_color, eliminar_color

api = ColorDto.api
_color = ColorDto.color
_colorConsultar = ColorDto.colorConsultar
_colorEditar = ColorDto.colorEditar


@api.route('/')
class Color(Resource):
    @api.doc('lista de colores guardados')
    @api.marshal_list_with(_colorConsultar)
    def get(self):
        """Obtener todos lo colores registrados"""
        return obtener_todos_colores()

    @api.response(201, 'Color creado exitosamente')
    @api.doc('Crear nuevo color')
    @api.expect(_color, validate=True)
    def post(self):
        """Guardar un nuevo color"""
        color = request.json
        return guardar_color(color)

    @api.response(201, 'Color editado exitosamente')
    @api.doc('Editar código hexadecimal de color')
    @api.expect(_colorEditar, validate=True)
    def patch(self):
        """Editar color"""
        color = request.json
        return editar_color(color)


@api.route('/<id>')
@api.param('id', 'id del color')
@api.response(404, 'Color no encontrado')
class ColorId(Resource):
    @api.doc('Obtener color por id')
    @api.marshal_with(_color)
    def get(self, id):
        """Obtener color por id"""
        color = obtener_color(id)
        if not color:
            api.abort(404)
        else:
            return color

    @api.doc('Eliminar color')
    def delete(self, id):
        """Eliminar color por id"""
        return eliminar_color(id)


@api.route('/disponible')
class ColorDisponible(Resource):
    @api.doc('Obtener colores disponibles')
    @api.marshal_with(_colorConsultar)
    def get(self):
        """Obtener colores disponibles (no asignados a un tratamiento)"""
        colores = obtener_colores_disponibles()
        if not colores:
            api.abort(404)
        else:
            return colores
