from app.main import db
from app.main.model.anotacion import Anotacion
from app.main.model.valor import Valor
from app.main.model.atributo import Atributo
from app.main.model.tratamiento import Tratamiento
from app.main.model.usuario import Usuario
from app.main.model.parrafo import Parrafo
from app.main.model.politica import Politica, PoliticaUsuarioRelacion
from app.main.util.dto import AnotacionDto
from app.main.util.clases_auxiliares import AnotacionConsultar
from flask_restplus import marshal
import datetime

_anotacionesConsultar = AnotacionDto.anotacionConsultar


def guardar_anotacion(data):
    nueva_anotacion= Anotacion(
        fecha_anotado=datetime.datetime.isoformat(datetime.datetime.now()),
        texto=data['texto'],
        texto_html=data['texto_html'],
        comentario=data['comentario'],
        valor_id=data['valor_id'],
        parrafo_id=data['parrafo_id'],
        usuario_id=data['usuario_id']
    )
    guardar_cambios(nueva_anotacion)
    response_object = {
        'estado': 'exito',
        'mensaje': 'Anotacion registrada exitosamente.'
    }
    return response_object, 201


def obtener_anotaciones_parrafo(parrafo_id):
    anotaciones = Anotacion.query.filter_by(parrafo_id=parrafo_id).all()
    return anotaciones


def obtener_anotaciones_politica_anotadores(politica_id):
    anotaciones = [AnotacionConsultar]
    anotaciones_consultar = (db.session.query(Anotacion, Valor, Atributo, Tratamiento, Usuario, Parrafo, Politica)
                             .outerjoin(Parrafo, Anotacion.parrafo_id == Parrafo.id)
                             .outerjoin(Politica, Parrafo.politica_id == Politica.id)
                             .outerjoin(Valor, Anotacion.valor_id == Valor.id)
                             .outerjoin(Atributo, Valor.atributo_id == Atributo.id)
                             .outerjoin(Tratamiento, Atributo.tratamiento_id == Tratamiento.id)
                             .outerjoin(Usuario, Anotacion.usuario_id == Usuario.id)
                             .filter(Politica.id == politica_id, Usuario.rol_usuario == 2).all())
    anotaciones.clear()
    i = 0
    if not anotaciones_consultar:
        respuesta = {
            'estado': 'fallido',
            'mensaje': 'no existen anotaciones para esta politica'
        }
        return respuesta, 404
    else:
        for item in anotaciones_consultar:
            anotaciones.insert(i, item[0])
            anotaciones[i].valor_descripcion = item[1].descripcion
            anotaciones[i].atributo_id = item[2].id
            anotaciones[i].atributo_descripcion = item[2].descripcion
            anotaciones[i].tratamiento_id = item[3].id
            anotaciones[i].tratamiento_descripcion = item[3].descripcion
            anotaciones[i].usuario_nombre = item[4].email
            i += 1
        return marshal(anotaciones, _anotacionesConsultar), 201


def obtener_anotaciones_parrafo_anotadores(parrafo_id):
    anotaciones = [AnotacionConsultar]
    anotaciones_consultar = (db.session.query(Anotacion, Valor, Atributo, Tratamiento, Usuario)
                             .outerjoin(Valor, Anotacion.valor_id == Valor.id)
                             .outerjoin(Atributo, Valor.atributo_id == Atributo.id)
                             .outerjoin(Tratamiento, Atributo.tratamiento_id == Tratamiento.id)
                             .outerjoin(Usuario, Anotacion.usuario_id == Usuario.id)
                             .filter(Anotacion.parrafo_id == parrafo_id, Usuario.rol_usuario == 2).all())
    anotaciones.clear()
    i = 0
    if not anotaciones_consultar:
        return 404
    else:
        for item in anotaciones_consultar:
            anotaciones.insert(i, item[0])
            anotaciones[i].valor_descripcion = item[1].descripcion
            anotaciones[i].atributo_id = item[2].id
            anotaciones[i].atributo_descripcion = item[2].descripcion
            anotaciones[i].tratamiento_id = item[3].id
            anotaciones[i].tratamiento_descripcion = item[3].descripcion
            anotaciones[i].usuario_nombre = item[4].email
            i += 1
        return anotaciones, 201


def obtener_anotaciones_politica_consolidador(parrafo_id):
    anotaciones = [AnotacionConsultar]
    anotaciones_consultar = (db.session.query(Anotacion, Valor, Atributo, Tratamiento, Usuario)
                             .outerjoin(Valor, Anotacion.valor_id == Valor.id)
                             .outerjoin(Atributo, Valor.atributo_id == Atributo.id)
                             .outerjoin(Tratamiento, Atributo.tratamiento_id == Tratamiento.id)
                             .outerjoin(Usuario, Anotacion.usuario_id == Usuario.id)
                             .filter(Anotacion.parrafo_id == parrafo_id, Usuario.rol_usuario == 1).all())
    anotaciones.clear()
    i = 0
    if not anotaciones_consultar:
        respuesta = {
            'estado': 'fallido',
            'mensaje': 'no existen anotaciones para esta politica'
        }
        return respuesta, 404
    else:
        for item in anotaciones_consultar:
            anotaciones.insert(i, item[0])
            anotaciones[i].valor_descripcion = item[1].descripcion
            anotaciones[i].atributo_id = item[2].id
            anotaciones[i].atributo_descripcion = item[2].descripcion
            anotaciones[i].tratamiento_id = item[3].id
            anotaciones[i].tratamiento_descripcion = item[3].descripcion
            anotaciones[i].usuario_nombre = item[4].email
            i += 1
        return anotaciones, 201


def consultar_ultima_anotacion_usuario_politica(politica_id, usuario_id, consolidar):
    ultimo_parrafo_anotado = (db.session.query(Anotacion.parrafo_id.distinct(), Parrafo, Politica)
                              .outerjoin(Parrafo, Anotacion.parrafo_id == Parrafo.id)
                              .outerjoin(Politica, Parrafo.politica_id == Politica.id)
                              .filter(Politica.id == politica_id,
                                      Anotacion.usuario_id == usuario_id,
                                      Anotacion.consolidar == consolidar).count())
    return ultimo_parrafo_anotado


def guardar_cambios(data):
    db.session.add(data)
    db.session.commit()