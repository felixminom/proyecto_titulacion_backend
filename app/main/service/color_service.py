from app.main import db
from app.main.model.color import Color


def guardar_nuevo_color(color):
    color_aux = Color.query.filter_by(codigo=color['codigo']).first()
    if not color_aux:
        nuevo_color = Color(
            codigo=color['codigo'],
            disponible=True
        )
        guardar_cambios(nuevo_color)
        response_object = {
            'estado': 'exito',
            'mensaje': 'Color creado exitosamente'
        }
        return response_object, 201
    else:
        response_object = {
            'estado': 'fallido',
            'mensaje': 'El color ya existe, no puede ser creado'
        }
        return response_object, 409


def obtener_todos_colores():
    return Color.query.all()


def obtener_color(id):
    return Color.query.filter_by(id=id).first()


def obtener_colores_disponibles():
    return Color.query.filter_by(disponible=True).all()


def guardar_cambios(data):
    db.session.add(data)
    db.session.commit()