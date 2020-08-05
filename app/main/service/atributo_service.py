from app.main import db
from app.main.model.atributo import Atributo
from app.main.model.tratamiento import Tratamiento
from app.main.util.clases_auxiliares import AtributoConsultar
from app.main.util.dto import  AtributoDto
from flask_restplus import marshal

_atributoConsultar = AtributoDto.atributoConsultar
_atributoCompleto = AtributoDto.atributoCompleto


def guardar_atributo(atributo):
    atributo_consultar = (db.session.query(Atributo).
                          filter(Atributo.descripcion == (atributo['descripcion']),
                                 Atributo.tratamiento_id == atributo['tratamiento_id']).first())
    if not atributo_consultar:
        nuevo_atributo = Atributo(
            descripcion= atributo['descripcion'],
            tratamiento_id= atributo['tratamiento_id']
        )
        guardar_cambios(nuevo_atributo)
        respuesta = {
            'estado': 'exito',
            'mensaje': 'Atributo creado exitosamente'
        }
        return respuesta, 201
    else:
        respuesta = {
            'estado': 'fallido',
            'mensaje': 'La descripcion del atributo ya existe para este tratamiento'
        }
        return respuesta, 409


def editar_atributo(data):
    atributo = Atributo.query.filter_by(id=data['id']).first()
    if not atributo:
        respuesta = {
            'estado': 'fallido',
            'mensaje': 'No existe el atributo'
        }
        return respuesta, 409
    else:
        atributo.descripcion = data['descripcion']
        guardar_cambios(atributo)
        respuesta = {
            'estado': 'exito',
            'mensaje': 'Atributo editado exitosamente'
        }
        return respuesta, 201


def eliminar_atributo(id):
    try:
        Atributo.query.filter_by(id=id).delete()
    except:
        db.session.rollback()
        respuesta = {
            'estado': 'fallido',
            'mensaje': 'No existe el atributo'
        }
        return respuesta, 409
    else:
        db.session.commit()
        respuesta = {
            'estado': 'exito',
            'mensaje': 'Atributo eliminado exitosamente'
        }
        return respuesta, 201


def obtener_todos_atributos():
    db.session.configure(autoflush=False)
    atributos = [AtributoConsultar]
    atributos_consultar = (db.session.query(Atributo, Tratamiento)
                           .outerjoin(Tratamiento, Atributo.tratamiento_id == Tratamiento.id).all())
    i = 0
    atributos.clear()
    if not atributos_consultar:
        respuesta = {
            'estado': 'Fallido',
            'mensaje': 'No existen valores'
        }
        return respuesta, 404
    else:
        for item in atributos_consultar:
            atributos.insert(i, item[0])
            atributos[i].color_primario = item[1].color_tratamiento.codigo
            i += 1
        return atributos, 201


def obtener_atributos_tratamiento(tratamiento_id):
    atributos = []
    atributos_consultar = (db.session.query(Atributo, Tratamiento).
                           outerjoin(Tratamiento, Atributo.tratamiento_id == Tratamiento.id)
                           .filter(Atributo.tratamiento_id == tratamiento_id).all())
    i = 0
    atributos.clear()
    if not atributos_consultar:
        response_object = {
            'estado': 'fallido',
            'mensaje': 'No existen atributos para este tratamiento'
        }
        return response_object, 404
    else:
        for item in atributos_consultar:
            atributos.insert(i, item[0])
            atributos[i].color_primario = item[1].color_tratamiento.codigo
            i += 1
        return marshal(atributos, _atributoConsultar), 201


def obtener_atributos_tratamiento_completo(tratamiento_id):
    atributos = []
    atributos_consultar = (db.session.query(Atributo, Tratamiento).
                           outerjoin(Tratamiento, Atributo.tratamiento_id == Tratamiento.id)
                           .filter(Atributo.tratamiento_id == tratamiento_id).all())
    i = 0
    atributos.clear()
    for item in atributos_consultar:
        atributos.insert(i, item[0])
        atributos[i].color_primario = item[1].color_tratamiento.codigo
        i += 1
    return atributos


def guardar_cambios(data):
    db.session.add(data)
    db.session.commit()
