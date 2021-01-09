from .. import db


class Parrafo(db.Model):
    """ Tabla que almacena los párrafos/secciones de una política """
    __tablename__ = "parrafo"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    secuencia = db.Column(db.Integer, nullable=False)
    titulo = db.Column(db.TEXT)
    texto = db.Column(db.TEXT, nullable=False)
    texto_html = db.Column(db.TEXT, nullable=False)
    politica_id = db.Column(db.Integer, db.ForeignKey('politica.id'), primary_key=True)
    anotaciones = db.relationship('Anotacion', backref=db.backref('parrafo'))

    def __repr__(self):
        return "<parrafo {}>".format(self.texto)
