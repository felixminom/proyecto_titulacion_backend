from app.main import db
from app.main.model.parrafo import Parrafo


def guardar_parrafo(data):
    parrafo_nuevo = Parrafo(
        secuencia=data.secuencia,
        titulo=data.titulo,
        texto=data.texto,
        texto_html=data.texto_html,
        politica_id=data.politica_id
    )
    guardar_cambios(parrafo_nuevo)


def guardar_cambios(data):
    db.session.add(data)
    db.session.commit()
