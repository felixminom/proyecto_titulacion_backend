from .. import db, flask_bcrypt
from app.main.model.lista_negra import TokenListaNegra
from ..config import key
import jwt
import datetime


class Usuario(db.Model):
    """" Tabla que almacena los usuarios de la herramienta de anotación"""
    __tablename__ = "usuario"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    hora_registro = db.Column(db.DateTime, nullable=False)
    rol_usuario = db.Column(db.Integer, db.ForeignKey('rol_usuario.id'))
    clave_hash = db.Column(db.String(100))
    activo = db.Column(db.Boolean)
    entrenamiento = db.Column(db.Boolean)
    anotaciones = db.relationship("Anotacion", backref=db.backref("usuario"))

    #Restringue que la clave sea leida en código
    #este campo solo puede ser escrito
    @property
    def clave(self):
        raise AttributeError('clave: campo solo de escritura')

    #Se ejecuta antes de guardar una clave en la base de datos
    #se utiliza el algoritmo bcrypt
    @clave.setter
    def clave(self, clave):
        self.clave_hash = flask_bcrypt.generate_password_hash(clave).decode('utf-8')

    #Se ejecuta cuando un usuario intenta ingresar al sistema
    #se comprueba la clave que ha sido enviada
    def comparar_clave(self, clave):
        return flask_bcrypt.check_password_hash(self.clave_hash, clave)

    #Genera un token para la sesión del usuario
    @staticmethod
    def codificar_auth_token(usuario_id):
        try:
            payload = {
                'iat': datetime.datetime.utcnow(),
                'sub': usuario_id
            }
            return jwt.encode(
                payload,
                key,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    #Verifica si un token aún es valido
    #si es que es valido devuelve el campo sub del token que contiene el id del usuario
    #caso contrario se devuelve un mensaje de error
    @staticmethod
    def decodificar_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token, key, algorithms='HS256')
            en_lista_negra = TokenListaNegra.verificar_token_lista_negra(auth_token)
            if en_lista_negra:
                return 'Token en lista negra, por favor inicie sesion nuevamente'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Firma expirada, por favor inicie sesion nuevamente'
        except jwt.InvalidTokenError as e:
            return '{}'.format(e)

    def __repr__(self):
        return "<User '{}'>".format(self.email)
