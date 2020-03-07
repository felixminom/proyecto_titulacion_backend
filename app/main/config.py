import os

# uncomment the line below for postgres database url from environment variable
mysql_local_base = 'mysql+pymysql://root:Benalcazar_11@127.0.0.1:3306/politica_anotacion?charset=utf8mb4'
mysql_aws = 'mysql+pymysql://admin:Herramienta_2020@' \
            'herramienta-anotacion.cicb7kkmbijy.us-west-2.rds.amazonaws.com:3306/herramientaAnotacion?charset=utf8mb4'

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'Herramienta_2020')
    DEBUG = False


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = mysql_local_base
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = mysql_aws
    SQLALCHEMY_TRACK_MODIFICATIONS = True


config_by_name = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY