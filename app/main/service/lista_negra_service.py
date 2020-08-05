from app.main import db
from app.main.model.lista_negra import TokenListaNegra


def guardar_token(token, usuario_id):
    token_lista_negra = TokenListaNegra(token=token, usuario_id=usuario_id)
    try:
        db.session.add(token_lista_negra)
        db.session.commit()
        response_object = {
            'estado': 'exito',
            'mensaje': 'Sesion cerrada exitosamente'
        }
        return response_object, 200
    except Exception as e:
        response_object = {
            'estado': 'exito',
            'mensaje': e
        }
        return response_object, 400
