from .. import db

rol_usuario_modulo_relacion = db.Table(
    'rol_modulo', db.metadata,
    db.Column('rol_usuario_id', db.Integer, db.ForeignKey('rol_usuario.id')),
    db.Column('modulo_id', db.Integer, db.ForeignKey('modulo.id'))
)


class RolUsuario(db.Model):
    """Roles de usuario para manejo de modulos"""
    __tablename__ = "rol_usuario"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    descripcion = db.Column(db.String(255))
    modulos = db.relationship("Modulo", secondary=rol_usuario_modulo_relacion, backref='roles_usuario')

    def __repr__(self):
        return "<Rol de usuario '{}'".format(self.nombre)
