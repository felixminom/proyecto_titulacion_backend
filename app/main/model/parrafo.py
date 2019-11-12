from .. import db


class Parrafo(db.Model):
    "Parrafos de las politicas de privacidad"
    __tablename__ = "parrafo"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    secuencia = db.Column(db.Integer, nullable=False)
    texto = db.Column(db.String(15000), nullable=False)
    politica_id = db.Column(db.Integer, db.ForeignKey('politica.id'), primary_key=True)
    anotaciones = db.relationship('Anotacion', backref=db.backref('parrafo'))

    def __repr__(self):
        return "<parrafo {}>".format(self.texto)