from .. import db


class Modulo(db.Model):
    """ Tabla que almacena los módulos de la herramienta de anotación:
        Administración (usuarios, políticas, tratamientos, atributos y valores), Anotación y Consolidación.
        Esta tabla se relaciona con rol_usuario para dar acceso a los módulos basados en un rol"""
    __tablename__ = "modulo"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), unique=True, nullable=False)
    icono = db.Column(db.String(50))
    path = db.Column(db.String(255))
    padre_id = db.Column(db.Integer, db.ForeignKey('modulo.id'))
    hijos = db.relationship("Modulo")

    def __repr__(self):
        return "<Modulo '{}'>".format(self.nombre)
