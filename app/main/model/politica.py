from .. import db

politica_usuario_relacion = db.Table(
    'politica_usuario', db.metadata,
    db.Column('politica_id', db.Integer, db.ForeignKey('politica.id')),
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuario.id')),
    db.Column('consolidar', db.Boolean, nullable=False),
    db.Column('anotar', db.Boolean, nullable=False),
    db.Column('finalizado', db.Boolean, nullable=False)
)


class Politica(db.Model):
    __tablename__ = "politica"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(128), unique=True, nullable=False)
    url = db.Column(db.String(128), unique=True, nullable=False)
    fecha = db.Column (db.Date, nullable=False)
    parrafos = db.relationship("Parrafo", backref=db.backref("politica"))
    usuarios = db.relationship("Usuario", secondary=politica_usuario_relacion, backref='polticas')

    def __repr__(self):
        return "<Politica '{}'>".format(self.nombre)