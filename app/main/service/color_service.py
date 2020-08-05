from app.main import db
from app.main.model.color import Color


def guardar_color(color):
    color_aux = Color.query.filter_by(codigo=color['codigo']).first()
    if not color_aux:
        nuevo_color = Color(
            codigo=color['codigo'],
            disponible=True
        )
        guardar_cambios(nuevo_color)
        respuesta = {
            'estado': 'exito',
            'mensaje': 'Color creado exitosamente'
        }
        return respuesta, 201
    else:
        respuesta = {
            'estado': 'fallido',
            'mensaje': 'El color ya existe, no puede ser creado'
        }
        return respuesta, 409


def editar_color(color):
    color_aux = Color.query.filter_by(id=color['id']).first()
    if not color_aux:
        respuesta = {
            'estado': 'fallido',
            'mensaje': 'No existe el color'
        }
        return respuesta, 409
    else:
        color_aux.codigo = color['codigo']
        guardar_cambios(color_aux)
        respuesta = {
            'estado': 'exito',
            'mensaje': 'Color editado exitosamente'
        }
        return respuesta, 201


def eliminar_color(id):
    try:
        Color.query.filter_by(id=id).delete()
    except:
        db.session.rollback()
        respuesta = {
            'estado': 'fallido',
            'mensaje': 'No existe el color'
        }
        return respuesta, 409
    else:
        db.session.commit()
        respuesta = {
            'estado': 'exito',
            'mensaje': 'Color eliminado exitosamente'
        }
        return respuesta, 201


def obtener_todos_colores():
    return Color.query.all()


def obtener_color(id):
    return Color.query.filter_by(id=id).first()


def obtener_colores_disponibles():
    return Color.query.filter_by(disponible=True).all()


def guardar_cambios(data):
    db.session.add(data)
    db.session.commit()
