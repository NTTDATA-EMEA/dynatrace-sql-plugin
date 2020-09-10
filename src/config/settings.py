from decouple import config

class BaseConfig():
   API_PREFIX = '/api'
   TESTING = False
   DEBUG = False


class DevConfig(BaseConfig):
   FLASK_ENV = 'development'
   DEBUG = True
   MONGOHOST = config('MONGOHOST')
   MONGOUSER = config('MONGOUSER')
   MONGOPASSWORD = config('MONGOPASSWORD')
   MONGOAUTHSOURCE = config('MONGOAUTHSOURCE')
   MONGODATABASE = config('MONGODATABASE')
   APSCHEDULERCOLLECTION = config('APSCHEDULERCOLLECTION')
   PORT = config('PORT')
   DTURL = config('DTURL')
   DTAPITOKEN = config('DTAPITOKEN')
   SECRET = config('SECRET')
   MSSQL = config('MSSQL')
   MYSQL = config('MYSQL')
   POSTGRES = config('POSTGRES')
   ORACLE = config('ORACLE')

class ProductionConfig(BaseConfig):
   FLASK_ENV = 'production'
   MONGOHOST = '192.168.8.120'
   MONGOUSER = 'mongoadmin'
   MONGOPASSWORD = 'mongo123'
   MONGOAUTHSOURCE = 'admin'
   APSCHEDULERDB = 'Scheduler'
   APSCHEDULERCOLLECTION = 'jobs'
   DTURL = config('DTURL')
   DTAPITOKEN = config('DTAPITOKEN')
   SECRET = config('SECRET')

class TestConfig(BaseConfig):
   FLASK_ENV = 'development'
   TESTING = True
   DEBUG = True
