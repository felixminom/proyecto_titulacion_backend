from .. import db


class Tratamiento(db.Model):
    """Modelo de tratamiento"""
    __tablename__ = "tratamiento"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descripcion = db.Column(db.String(512), unique=True, nullable=False)
    color_primario = db.Column(db.Integer, db.ForeignKey('color.id'))
    color_tratamiento = db.relationship("Color", backref=db.backref("tratamiento", uselist=False))
    atributos = db.relationship("Atributo")

    def __repr__(self):
        return "<Tratamiento '{}'>".format(self)