import pymongo
from mongodb import MongoDB
from bson.objectid import ObjectId
import json
from time import time
import config
import requests

class DynatraceAPI:
    def __init__(self,config):
      self.server = config['DTAPIURL']
      self.token = config['dtAPIToken']
      self.Headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Api-Token ' + self.token
        }

    def POSTSyntheticResults(DTAPI):
        #Client = pymongo.MongoClient(host='192.168.8.167', username='mongoAdmin',password='mongo123',authSource='admin')
        mDB = MongoDB()
        
        #DB = Client.Client["NTTD_Dynatrace_Advanced_SQL_Extension"]
        Col = mDB.DB["JobResults"]

        JobResults = Col.find({'dtPushTimestamp':{"$exists":False}}).distinct('jobid')
        JobMetaCol = mDB.DB["Jobs"]
        
        Response = {}

        for Job in JobResults:
            JobMeta = JobMetaCol.find_one({"_id":ObjectId(Job)})
            JobMeta.pop('_id')
            
            Response['syntheticEngineName'] = JobMeta['dtSyntheticEngineName']
            Response['messageTimestamp'] = round(time()*1000)
            Response['locations'] = JobMeta['locations']
            Response['tests'] = JobMeta['tests']
            Response['testResults']=[]
       
            

            Results = Col.find({'dtPushTimestamp':{"$exists":False},'jobid':Job}).sort('startTimestamp')
            objectids = []
            for Result in Results:
              
                testresult={}
                testresult['id'] = Result['id']
                testresult['totalStepCount'] = Result['totalStepCount']
                testresult['locationResults'] = Result['locationResults']
                Response['testResults'].append(testresult)

                objectids.append(Result['_id'])
                 
            TestRes = Col.find({'_id': {'$in':objectids}})
            
            for x in TestRes:
                print(x)

            Headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Api-Token ' + config.DTAPITOKEN
                    }
            url = config.DTURL + '/api/v1/synthetic/ext/tests'
            r = requests.post(url,headers=Headers,data=json.dumps(Response))
            print(r.status_code)
            print(r.content)
            if r.status_code == 204:
                Col.update_many({'_id': {'$in':objectids}},{'$set':{'dtPushTimestamp':time()}})    
   