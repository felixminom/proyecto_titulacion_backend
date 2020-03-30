from .. import db


class PoliticaUsuarioRelacion(db.Model):
    __tablename__ = 'politica_usuario'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    politica_id = db.Column(db.Integer, db.ForeignKey('politica.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    consolidar = db.Column(db.Boolean, nullable=False, default=False)
    finalizado = db.Column(db.Boolean, nullable=False, default=False)

    politica = db.relationship("Politica", backref=db.backref("politicas"))
    usuario = db.relationship("Usuario", backref=db.backref("usuarios"))


class Politica(db.Model):
    __tablename__ = "politica"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(128), unique=True, nullable=False)
    url = db.Column(db.String(128), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    asignada = db.Column(db.Boolean, nullable=False)
    parrafos = db.relationship("Parrafo", backref=db.backref("politica"))

    def __repr__(self):
        return "<Politica '{}'>".format(self.nombre)