import pymongo
import config


Client = pymongo.MongoClient(host='172.18.0.1', 
                                username='mongoAdmin',
                                password='mongo123',
                                authSource='admin')

test = Client.list_database_names()
DB = Client["Jobs"]