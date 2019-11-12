from .. import db


class Valor(db.Model):

    __tablename__ = "valor"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descripcion = db.Column(db.String(512), nullable=False)
    atributo_id = db.Column(db.Integer, db.ForeignKey('atributo.id'))

    def __repr__(self):
        return 'Valor {}'.format(self.descripcion)