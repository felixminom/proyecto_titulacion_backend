from .. import db


class Modulo(db.Model):
    """Modelo de modulos para definir roles de usuario"""
    __tablename__ = "modulo"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), unique=True, nullable=False)
    icono = db.Column(db.String(50))
    path = db.Column(db.String(255))
    padre_id = db.Column(db.Integer, db.ForeignKey('modulo.id'))
    hijos = db.relationship("Modulo")

    def __repr__(self):
        return "<Modulo '{}'>".format(self.nombre)
