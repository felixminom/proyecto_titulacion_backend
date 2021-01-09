from .. import db


class Tratamiento(db.Model):
    """ Tabla que almacena los tratamientos de datos"""
    __tablename__ = "tratamiento"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descripcion = db.Column(db.String(512), unique=True, nullable=False)
    color_primario = db.Column(db.Integer, db.ForeignKey('color.id'))
    color_tratamiento = db.relationship("Color", backref=db.backref("tratamiento", uselist=False))
    atributos = db.relationship("Atributo", backref=db.backref("tratamiento"), uselist=False)

    def __repr__(self):
        return "<Tratamiento '{}'>".format(self.descripcion)
