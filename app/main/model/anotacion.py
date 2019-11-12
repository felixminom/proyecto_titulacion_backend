from .. import db


class Anotacion(db.Model):
    __tablename__ ="anotacion"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fecha_anotado = db.Column(db.DateTime, nullable=False)
    indice_inicio = db.Column(db.Integer, nullable=False)
    indice_fin = db.Column(db.Integer, nullable=False)
    texto = db.Column(db.String(15000), nullable=False)
    valor_id = db.Column(db.Integer, db.ForeignKey('valor.id'))
    parrafo_id = db.Column(db.Integer, db.ForeignKey('parrafo.id'))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))

    def __repr__(self):
        return 'anotacion: {}'.format(self.texto)