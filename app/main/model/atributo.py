from .. import db


class Atributo(db.Model):
    __tablename__ = "atributo"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tratamiento_id = db.Column(db.Integer, db.ForeignKey('tratamiento.id'))
    descripcion = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return 'atributo {}'.format(self.descripcion)