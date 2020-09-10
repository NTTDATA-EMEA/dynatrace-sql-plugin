import pymongo
import config

_register = {}

def singleton(cls):
   def wrapper(*args, **kw):
       if cls not in _register:
           instance = cls(*args, **kw)
           _register[cls] = instance
       return _register[cls] 

   wrapper.__name__ = cls.__name__
   return wrapper

...
@singleton
class MongoDB:
    def __init__(self):
        Client = pymongo.MongoClient(host=config.MONGOHOST, 
                                        username=config.MONGOUSER,
                                        password=config.MONGOPASSWORD,
                                        authSource=config.MONGOAUTHSOURCE)
        self.DB = Client[config.MONGODATABASE]
        