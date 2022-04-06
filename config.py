import os 


class Config:
    DEBUG=False
    DEVELOPMENT=False
    SECRET_KEY= os.getenv("SECRET_KEY","JadKrNIjmXiYmoqWr54EtBQUcpqk4j2H")

class ProductionConfig(Config):
    pass

class StagingConfig(Config):
    DEBUG = True

class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT= True