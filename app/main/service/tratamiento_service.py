from app.main import db
from app.main.model.tratamiento import Tratamiento
from app.main.model.color import Color
from ..service.atributo_services import obtener_atributos_tratamiento_completo
from ..service.valor_service import obtener_valores_atributo_completo
from ..util.clases_auxiliares import TratamientoConsultar, TratamientoCompleto, AtributoCompleto


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
            response_object = {
                'estado': 'exito',
                'mensaje': 'Tratamiento registrado exitosamente.'
            }
            return response_object, 201
        else:
            response_object = {
                'estado': 'fallido',
                'mensaje': 'El color ya esta asignado a otro tratamiento'
            }
            return response_object, 409
    else:
        response_object = {
            'estado': 'fallido',
            'mensaje': 'La descripcion del tratamiento ya existe'
        }
        return response_object, 409


def obtener_todos_tratamientos():
    db.session.configure(autoflush=False)
    tratamientos = [TratamientoConsultar]
    tratamientosAux = Tratamiento.query.all()
    i = 0
    tratamientos.clear()
    for item in tratamientosAux:
        tratamientos.insert(i, item)
        tratamientos[i].color_primario = item.color_tratamiento.codigo
        i += 1
    return tratamientos


def obtener_un_tratamiento(id):
    db.session.configure(autoflush=False)
    tratamiento = Tratamiento.query.filter_by(id=id).first()
    tratamiento.color_primario = tratamiento.color_tratamiento.codigo
    return tratamiento


def editar_tratamiento(data, id):
    tratamiento = Tratamiento.query.filter_by(id=id).first()
    if tratamiento:
        color = Color.query.filter_by(id=tratamiento.color_primario).first()
        color.disponible = True
        tratamiento.descripcion = data['descripcion']
        tratamiento.color_primario = data['color_primario']
        db.session.commit()
        response_object = {
            'estado': 'exito',
            'mensaje': 'Se edito exitosamente el tratamiento'
        }
        return response_object, 200
    else:
        response_object = {
            'estado': 'fallido',
            'mensaje': 'No se pudo encontrar el tratamiento'
        }
        return response_object, 409


def obtener_tratamientos_completos():
    db.session.configure(autoflush=False)
    tratamientos = [TratamientoCompleto]
    tratamientos_aux = Tratamiento.query.all()
    i = 0
    tratamientos.clear()
    for item in tratamientos_aux:
        atributos_aux = obtener_atributos_tratamiento_completo(item.id)
        atributos = [AtributoCompleto]
        j = 0
        atributos.clear()
        if atributos_aux:
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
