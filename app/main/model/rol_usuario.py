from .. import db

#Tabla que nace de la relación muchos a muchos entre módulo y rol de usuario
#Almacena los módulos a los que un rol de usuario tiene acceso
rol_usuario_modulo_relacion = db.Table(
    'rol_modulo', db.metadata,
    db.Column('rol_usuario_id', db.Integer, db.ForeignKey('rol_usuario.id')),
    db.Column('modulo_id', db.Integer, db.ForeignKey('modulo.id'))
)

class RolUsuario(db.Model):
    """ Tabla que almacena Roles de usuario de la herramienta de anotación"""
    __tablename__ = "rol_usuario"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    descripcion = db.Column(db.String(255))
    modulos = db.relationship("Modulo", secondary=rol_usuario_modulo_relacion, backref='roles_usuario')

    def __repr__(self):
        return "<Rol de usuario '{}'".format(self.nombre)
