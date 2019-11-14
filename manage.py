import os
import unittest
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from app.main import create_app, db
from app import blueprint
from flask_cors import CORS

from app.main.model import anotacion
from app.main.model import atributo
from app.main.model import color
from app.main.model import lista_negra
from app.main.model import modulo
from app.main.model import parrafo
from app.main.model import politica
from app.main.model import rol_usuario
from app.main.model import tratamiento
from app.main.model import usuario
from app.main.model import valor


app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
app.register_blueprint(blueprint)

app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db, compare_type=True)

manager.add_command('db', MigrateCommand)

CORS(app, resources='/*')


@manager.command
def run():
    app.run()


@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    manager.run()