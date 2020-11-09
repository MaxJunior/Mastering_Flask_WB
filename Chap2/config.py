class Config(object):
    pass

class ProdConfig(Config):
    pass

class DevConfig(Config):
    DEBUG = True 
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:1234@localhost/masterwb"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    