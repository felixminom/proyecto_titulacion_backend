from flask_restplus import Resource
from app.main.util.dto import VisualizacionDto
from app.main.service.visualizacion_service import consultar_politicas_visualizar, consultar_politica_visualizar

api = VisualizacionDto.api


@api.route('/<id>')
@api.param('id', 'id de política')
class Politica(Resource):
    @api.response(201, '', VisualizacionDto.politicaVisualizacion)
    @api.doc('Consultar política con sus secciones y anotaciones')
    def get(self, id):
        return consultar_politica_visualizar(politica_id=id)


@api.route('/Politicas')
class Politicas(Resource):
    @api.response(201, '', VisualizacionDto.listaPoliticas)
    @api.doc('Consultar políticas que han finalizado el proceso de anotación')
    def get(self):
        return consultar_politicas_visualizar()
