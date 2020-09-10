import pyodbc
import time
import json
import crypt
from mongodb import MongoDB
import config

class MSSQLQuery:
  def __init__(self,config):
      self.server = config['server']
      self.database = config['database']
      self.username = crypt.decrypt(config['username'])
      self.password = crypt.decrypt(config['password'])
      self.steps = config['steps']
      self.dbtype = config['dbtype']
      self.querytype = config['querytype']
      self.testinfo = config['testinfo']
      self.jobid = config['jobid']

  def query(mssqlquery):
    
    starttimestamp = time.time()
    steps=[]
    testresult={}
    locations = []
    location = {}
    success=''

    testresult['id'] = mssqlquery.testinfo['id']
    testresult['totalStepCount'] = len(mssqlquery.steps)
    testresult['jobid'] = mssqlquery.jobid['$oid']

    location['id'] = mssqlquery.testinfo['locations'][0]['id']
    location['startTimestamp'] = round(starttimestamp*1000)

    connectionString = {
        "MSSQL": ('Driver={' + config.MSSQL + '};Server=' + mssqlquery.server + ';'
                        'Database=' + mssqlquery.database + ';'
                        'UID=' + mssqlquery.username +';'
                        'PWD=' + mssqlquery.password + ';'
                        'Trusted_Connection=no'),
        "MySQL": ('Driver={' + config.MYSQL + '};Server=' + mssqlquery.server + ';'
                        'Database=' + mssqlquery.database + ';'
                        'UID=' + mssqlquery.username +';'
                        'PWD=' + mssqlquery.password + ';'
                        'OPTION=3'),
        "Oracle": ('Driver={' + config.ORACLE + '};DBQ=' + mssqlquery.server + '/' + mssqlquery.database + ';'
                        'UID=' + mssqlquery.username +';'
                        'PWD=' + mssqlquery.password),
        "PostgreSQL": ('Driver={' + config.POSTGRES + '};Server=' + mssqlquery.server + ';'
                        'Database=' + mssqlquery.database + ';'
                        'UID=' + mssqlquery.username +';'
                        'PWD=' + mssqlquery.password + ';'
                        'PORT=5432')

    }
    try:
        conn = pyodbc.connect(connectionString[mssqlquery.dbtype])
        success='true'
    except pyodbc.Error as err:
        print(err)
        success = 'false'
        #Error Event to dynatrace should be posted here

    else:  
        cur = conn.cursor()
        
        for step in mssqlquery.steps:
            
            timeprior = time.time()
            stepresult={}
            stepresult['id'] = step['id']
            stepresult['startTimestamp'] = round(timeprior*1000)

            try:
                cur.execute(step['query'])
                timeafter = time.time()
                stepresult['responseTimeMillis'] = round((timeafter-timeprior)*1000)
            except pyodbc.Error as err:
                error={}
                error['code'] = err.args[0]
                error['message'] =err.args[1]
                stepresult['error'] = error
                
            steps.append(stepresult)
            location['stepResults'] = steps
        
#If we want to save the query return values...
#        row = cur.fetchone() 
#        while row: 
#            print(row[0])
#            row = cur.fetchone()
    
    finally:
        location['success'] = success    
        locations.append(location)
        testresult['locationResults'] = locations
        mDB = MongoDB()
        Col = mDB.DB["JobResults"]
        Col.insert_one(testresult).inserted_id

    

