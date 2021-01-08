from flask_restplus import marshal
from app.main import db
from app.main.model.tratamiento import Tratamiento
from app.main.model.color import Color
from ..service.atributo_service import obtener_atributos_tratamiento_completo
from ..service.valor_service import obtener_valores_atributo_completo
from ..util.clases_auxiliares import TratamientoConsultar, TratamientoCompleto, AtributoCompleto
from ..util.dto import TratamientoDto


def guardar_tratamiento(data):
    tratamiento_descripcion = Tratamiento.query.filter_by(descripcion=data['descripcion']).first()
    tratamiento_color = Tratamiento.query.filter_by(color_primario=data['color_primario']).first()
    if not tratamiento_descripcion:
        if not tratamiento_color:
            color = Color.query.filter_by(id=data['color_primario']).first()
            color.disponible = False
            nuevo_tratamiento = Tratamiento(
                descripcion=data['descripcion'],
                color_primario=data['color_primario']
            )
            guardar_cambios(nuevo_tratamiento)
            guardar_cambios(color)
            respuesta = {
                'estado': 'exito',
                'mensaje': 'Tratamiento registrado exitosamente.'
            }
            return respuesta, 201
        else:
            respuesta = {
                'estado': 'fallido',
                'mensaje': 'El color ya esta asignado a otro tratamiento'
            }
            return respuesta, 409
    else:
        respuesta = {
            'estado': 'fallido',
            'mensaje': 'La descripcion del tratamiento ya existe'
        }
        return respuesta, 409


def editar_tratamiento(data):
    tratamiento = Tratamiento.query.filter_by(id=data['id']).first()
    if tratamiento:
        color_antiguo = Color.query.filter_by(id=tratamiento.color_primario).first()
        color_antiguo.disponible = True
        color_nuevo = Color.query.filter_by(id=data['color_primario']).first()
        color_nuevo.disponible = False
        tratamiento.descripcion = data['descripcion']
        tratamiento.color_primario = data['color_primario']
        db.session.commit()
        respuesta = {
            'estado': 'exito',
            'mensaje': 'Se edito exitosamente el tratamiento'
        }
        return respuesta, 200
    else:
        respuesta = {
            'estado': 'fallido',
            'mensaje': 'No se pudo encontrar el tratamiento'
        }
        return respuesta, 409


def eliminar_tratamiento(id):
    tratamiento = Tratamiento.query.filter_by(id=id).first()
    try:
        tratamiento.color_tratamiento.disponible = True
        Tratamiento.query.filter_by(id=id).delete()
    except:
        db.session.rollback()
        respuesta = {
            'estado': 'fallido',
            'mensaje': 'No se pudo eliminar el tratamiento'
        }
        return respuesta, 409
    else:
        db.session.commit()
        respuesta = {
            'estado': 'exito',
            'mensaje': 'Se elimino exitosamente el tratamiento'
        }
        return respuesta, 200


def obtener_tratamientos():
    """Obtiene todos los tratamientos de datos en la base de datos"""
    tratamientos = [TratamientoConsultar]
    tratamientos_aux = Tratamiento.query.all()
    i = 0
    tratamientos.clear()

    if not tratamientos_aux:
        return [], 201
    else:
        for item in tratamientos_aux:
            tratamientos.insert(i, item)
            tratamientos[i].color_id = item.color_tratamiento.id
            tratamientos[i].color_primario_codigo = item.color_tratamiento.codigo
            i += 1
        return marshal(tratamientos, TratamientoDto.tratamientoConsultar), 201


def obtener_tratamientos_completos():
    """Obtiene los tratamientos de datos junto a sus atributos y valores"""
    db.session.configure(autoflush=False)
    tratamientos = [TratamientoCompleto]
    tratamientos_aux = Tratamiento.query.all()
    i = 0
    tratamientos.clear()
    for item in tratamientos_aux:
        if item.atributos:
            if item.atributos.valores:
                atributos_aux = obtener_atributos_tratamiento_completo(item.id)
                atributos = [AtributoCompleto]
                j = 0
                atributos.clear()
                for item2 in atributos_aux:
                    if item2.valores:
                        valores_aux = obtener_valores_atributo_completo(item2.id)
                        atributo = AtributoCompleto(item2.id, item2.descripcion, item2.color_primario, valores_aux)
                        atributos.insert(j, atributo)
                        j += 1
                tratamiento_aux = TratamientoCompleto(item.id, item.descripcion, item.color_tratamiento.codigo, atributos)
                tratamientos.insert(i, tratamiento_aux)
                i += 1
    return tratamientos


def guardar_cambios(data):
    db.session.add(data)
    db.session.commit()
