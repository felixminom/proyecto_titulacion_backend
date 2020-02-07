from .. import db


class Anotacion(db.Model):
    __tablename__ ="anotacion"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fecha_anotado = db.Column(db.DateTime, nullable=False)
    texto = db.Column(db.TEXT, nullable=False)
    texto_html = db.Column(db.TEXT, nullable=False)
    comentario = db.Column(db.TEXT)
    valor_id = db.Column(db.Integer, db.ForeignKey('valor.id'))
    parrafo_id = db.Column(db.Integer, db.ForeignKey('parrafo.id'))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))

    def __repr__(self):
        return 'anotacion: {}'.format(self.texto)