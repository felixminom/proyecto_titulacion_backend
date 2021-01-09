from .. import db


class Color(db.Model):
    """ Tabla que almacena los colores que se pueden asignar a un tratamiento """
    __tablename__ = "color"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo = db.Column(db.String(7), nullable=False)
    disponible = db.Column(db.Boolean, nullable=False)
    tratamiento_color = db.relationship("Tratamiento", backref=db.backref("color"))

    def __repr__(self):
        return 'Color: {}'.format(self.codigo)
