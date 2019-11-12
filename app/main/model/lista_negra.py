from .. import db
import datetime


class TokenListaNegra(db.Model):
    """modelo de token para almacenar JWT"""
    __tablename__ = 'lista_negra_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"))

    def __init__(self, token, usuario_id):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()
        self.usuario_id = usuario_id

    def __repr__(self):
        return '<id: token: {}>'.format(self.token)

    @staticmethod
    def revisar_lista_negra(auth_token):
        #chequear si el token de auth ha sido puesto en lista negra
        resultado = TokenListaNegra.query.filter_by(token=str(auth_token)).first()
        if resultado:
            return True
        else:
            return False
