from app.main import db
from app.main.model.modulo import Modulo


def guardar_nuevo_tratamiento(data):
    modulo = Modulo.query.filter_by(nombre=data['nombre']).first()
    if not modulo:
        nuevo_modulo = Modulo(
            nombre=data['nombre'],
            icono=data['icono'],
            padre_id=data['padre_id']
        )
        guardar_cambios(nuevo_modulo)
        response_object = {
            'estado': 'exito',
            'mensaje': 'Modulo creado exitosamente'
        }
        return response_object, 201
    else:
        response_object = {
            'estado': 'fallido',
            'mensaje': 'El modulo ya existe, no puede ser creado'
        }
        return response_object, 409


def obtener_todos_modulos():
    return Modulo.query.all()


def obtener_un_modulo(id):
    return Modulo.query.filter_by(id=id).first()


def guardar_cambios(data):
    db.session.add(data)
    db.session.commit()