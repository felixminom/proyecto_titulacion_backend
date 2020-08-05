from app.main import db
from app.main.model.modulo import Modulo


def guardar_modulo(data):
    modulo = Modulo.query.filter_by(nombre=data['nombre']).first()
    if not modulo:
        nuevo_modulo = Modulo(
            nombre=data['nombre'],
            icono=data['icono'],
            path=data['path'],
            padre_id=data['padre_id']
        )
        guardar_cambios(nuevo_modulo)
        response_object = {
            'estado': 'exito',
            'mensaje': 'Módulo creado exitosamente'
        }
        return response_object, 201
    else:
        response_object = {
            'estado': 'fallido',
            'mensaje': 'El módulo ya existe, no puede ser creado'
        }
        return response_object, 409


def editar_modulo(modulo):
    modulo_aux = Modulo.query.filter_by(id=modulo['id']).first()
    if not modulo_aux:
        respuesta = {
            'estado': 'fallido',
            'mensaje': 'No existe el módulo'
        }
        return respuesta, 409
    else:
        modulo_aux.nombre = modulo['nombre']
        modulo_aux.icono = modulo['icono']
        modulo_aux.path = modulo['path']
        modulo_aux.padre_id = modulo['padre_id']
        guardar_cambios(modulo_aux)
        respuesta = {
            'estado': 'exito',
            'mensaje': 'Módulo editado exitosamente'
        }
        return respuesta, 201


def eliminar_modulo(id):
    try:
        Modulo.query.filter_by(id=id).delete()
    except:
        db.session.rollback()
        respuesta = {
            'estado': 'fallido',
            'mensaje': 'No existe el módulo'
        }
        return respuesta, 409
    else:
        db.session.commit()
        respuesta = {
            'estado': 'exito',
            'mensaje': 'Módulo eliminado exitosamente'
        }
        return respuesta, 201


def obtener_modulos():
    return Modulo.query.all()


def obtener_modulo(id):
    return Modulo.query.filter_by(id=id).first()


def guardar_cambios(data):
    db.session.add(data)
    db.session.commit()
