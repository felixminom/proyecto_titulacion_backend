from .. import db


class Atributo(db.Model):
    __tablename__ = "atributo"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descripcion = db.Column(db.Integer, nullable=False)
    tratamiento_id = db.Column(db.Integer, db.ForeignKey('tratamiento.id'))

    def __repr__(self):
        return 'atributo {}'.format(self.descripcion)