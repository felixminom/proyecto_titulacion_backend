import os

mysql_local_base = 'mysql+pymysql://root:Benalcazar_11@127.0.0.1:3306/herramienta_anotacion?charset=utf8mb4'
mysql_aws = 'mysql+pymysql://admin:Herramienta_2020@' \
            'herramienta-anotacion.cicb7kkmbijy.us-west-2.rds.amazonaws.com:3306/herramienta_anotacion_epn?charset=utf8mb4'


class Config:
    """Una llave aleatoria, en producción deberia cambiarse"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'Herramienta_2020')
    DEBUG = False


class DevelopmentConfig(Config):
    """Configuracion para el ambiente local de desarrollo"""
    SQLALCHEMY_DATABASE_URI = mysql_local_base
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

#Se podría incrementar un tercer ambiente de pruebas en un futuro

class ProductionConfig(Config):
    """Configuracion para el ambiente de produccion"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = mysql_aws
    SQLALCHEMY_TRACK_MODIFICATIONS = True


config_by_name = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
