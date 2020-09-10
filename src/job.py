
#import pymongo
#import werkzeug
from connexion import NoContent
from SchedulerJobs.MSSQLQuery import MSSQLQuery
from flask import make_response, abort, jsonify, Response
import json
import crypt
from bson import json_util
from bson.json_util import dumps
from bson.objectid import ObjectId
from scheduler import Scheduler
from mongodb import MongoDB



def get_data(self,data):
     data['_id'] = str(data['_id'])


def listJob():
    
    mDB = MongoDB()
    
    Col = mDB.DB["Jobs"]
    jobs = Col.find()
     
    resp = json.loads(dumps(jobs))
    
    return resp,200

def addJob(body):
    
    body['dbUsername'] = crypt.encrypt(body['dbUsername'])
    body['dbPassword'] = crypt.encrypt(body['dbPassword'])
    
    mDB = MongoDB()
    Col = mDB.DB["Jobs"]
    
    jobid = Col.insert_one(body).inserted_id
    resp = json.loads(dumps(jobid))

    x = Scheduler()
    x.addJob(jobid)
    return resp,(200)

def updateJob():
    return

def deleteJob(job_id):
    mDB = MongoDB()
    Col = mDB.DB["Jobs"]
    Col.delete_one({"_id": ObjectId(job_id)})

    x = Scheduler()
    x.deleteJob(job_id)
    

def getJobById(job_id):
    mDB = MongoDB()
    Col = mDB.DB["Jobs"]
    resp = Col.find_one({"_id": ObjectId(job_id)})
    resp = json.loads(dumps(resp))
    return resp,(200)
