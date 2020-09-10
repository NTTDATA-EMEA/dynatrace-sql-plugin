import json
import config

from bson.json_util import dumps
from mongodb import MongoDB
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler import events
from apscheduler.events import EVENT_ALL
from SchedulerJobs.MSSQLQuery import MSSQLQuery
from SchedulerJobs.DynatraceAPI import DynatraceAPI


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
class Scheduler:
    
    
    def __init__(self):
        pass
    def sched_listener(self,event):
         print(event)   
        #if (event.exception):
        #    print('Exception: {}'.format(event.exception))

    def startEngine(self):
        self.jobstores = {'default': MongoDBJobStore(host=config.MONGOHOST,
                                                     username=config.MONGOUSER,
                                                     password=config.MONGOPASSWORD,
                                                     authSource=config.MONGOAUTHSOURCE,
                                                     database=config.MONGODATABASE,
                                                     collection=config.APSCHEDULERCOLLECTION
                                                     )}
        self.scheduler = BackgroundScheduler(jobstores=self.jobstores)
        self.scheduler.add_listener(self.sched_listener, EVENT_ALL)

        self.scheduler.start()


    def getJobs(self):
        
        print(self.scheduler.get_jobs())
    
    def removeAllJobs(self):
        self.scheduler.remove_all_jobs()
    
    def stopEnginge(self):
        self.scheduler.shutdown()

    def addJob(self,jobid):
        mDB = MongoDB()
        Col = mDB.DB["Jobs"]
        jobdata = Col.find_one({'_id':jobid})
        jobid = json.loads(dumps(jobid))
        print(jobid["$oid"])
        for test in jobdata['tests']:
            sqljob = MSSQLQuery({'server':jobdata['dbServer'],
                                'database':jobdata['dbDatabase'],
                                'username':jobdata['dbUsername'],
                                'password':jobdata['dbPassword'],
                                'steps':test['steps'],
                                'dbtype':jobdata['dbType'],
                                'querytype':jobdata['category'],
                                'testinfo':test,
                                'jobid':jobid
                                })
            
            self.scheduler.add_job(MSSQLQuery.query,args=[sqljob], trigger='interval', seconds=test['scheduleIntervalInSeconds'], id=jobid["$oid"] + test['id'])

    def addDTAPI(self):
        JIDs = [j.id for j in self.scheduler.get_jobs()]
        
        if 'DynatraceAPI' not in JIDs:
            dtAPI = DynatraceAPI({'DTAPIURL':config.DTURL,
                            'dtAPIToken':config.DTAPITOKEN
                            })
            self.scheduler.add_job(DynatraceAPI.POSTSyntheticResults,args=[dtAPI], trigger='interval', seconds=120, id='DynatraceAPI')

    def deleteJob(self,jobid):
        mDB = MongoDB()
        Col = mDB.DB[config.APSCHEDULERCOLLECTION]
        res = Col.find({"_id": {"$regex": jobid}})
        for row in res:
            self.scheduler.remove_job(row["_id"])
            