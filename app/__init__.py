from flask_restplus import Api
from flask import Blueprint

from .main.controller.tratamiento_controller import api as tratamiento_ns
from .main.controller.usuario_controller import api as usuario_ns
from .main.controller.modulo_controller import api as modulo_ns
from .main.controller.rol_usuario_controller import api as rol_usuario_ns
from .main.controller.auth_controller import api as auth_ns
from .main.controller.color_controller import api as color_ns
from .main.controller.atributo_controller import api as atributo_ns
from .main.controller.valor_controller import api as valor_ns
from .main.controller.politica_controller import api as politica_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='Backend herramienta de anotacion',
          version='1.0',
          description='Herramienta de anotacion para tratamintos de datos de politicas de privacidad en español en un contexto GDPR'
          )

api.add_namespace(auth_ns)
api.add_namespace(atributo_ns, path='/Atributo')
api.add_namespace(color_ns, path='/Color')
api.add_namespace(modulo_ns, path='/Modulo')
api.add_namespace(rol_usuario_ns, path='/RolUsuario')
api.add_namespace(tratamiento_ns, path='/Tratamiento')
api.add_namespace(usuario_ns, path='/Usuario')
api.add_namespace(valor_ns, path='/Valor')
api.add_namespace(politica_ns, path='/Politica')




