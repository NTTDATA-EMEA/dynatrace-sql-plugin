# NTTData dynatrace-sql-plugin EXPERIMENTAL
This is an EXPERIMENTAL Dynatrace Plugin which uses the Dynatrace 3rd Party Synthetic API to add Synthetic SQL Stats and pythons APScheduler to execute the Queries
The script can run either on a host or easily containerized.

## Prerequisits
### Dynatrace Tenant
Get your free 15-Days Trial here: www.dynatrace.ai/nttdata
### MongoDB
This plugin requires a MongoDB to store the JobData and JobResults
### ODBC Drivers
This plugin uses the pyodbc module which relies on the OS ODBC Driver for the given Databases
On Linux (or during the creation of a docker image) run installODBCDrivers.sh to get the drivers installed for MS-SQL, MySQL, Oracle and PostgreSQL
## Installation

```bash
pip install -r requirements.txt
```

### Environment Variables
Within the .env File adapt the variables according your needs

```bash
#GENERAL PARAMETER
SECRET=lJ9klQjvoKPqnMQRzaDHT4y4n6XaZ2cEF0nH73FxOoQ=
DTURL=https://yourdtid.live.dynatrace.com
DTAPITOKEN=yourdtapitoken
PORT=5000
#MONGODB-Setting
MONGOHOST = '127.0.0.1'
MONGOUSER = 'mongoAdmin'
MONGOPASSWORD = 'mongo123'
MONGOAUTHSOURCE = 'admin'
MONGODATABASE = 'NTTD_Dynatrace_Advanced_SQL_Extension'
APSCHEDULERCOLLECTION = 'apschedulerjobs'
#ODBC Driver Names (pyodbc.driver())
MSSQL='ODBC Driver 17 for SQL Server'
POSTGRES='PostgreSQL Unicode'
MYSQL='MySQL ODBC 8.0 Unicode Driver'
ORACLE='Oracle 19 ODBC driver'
```

## Run
```bash
python server.py
```

## Usage
To view, add or delete jobs a simple REST API is implemented, many parts are identical to Dynatrace' 3rd Party Synthetic API and can be reused.
The plugin comes with the swagger ui to look at the structure of requests goto http://yourhost:5000/api/ui/

http://localhost:5000/api/ui/

### Authorization
Type: API Key
Add to: Header
Key: "AuthKey"
Value: DynatraceAPIToken

### ListJobs
GET http://yourhost:5000/api/job

### GetSingleJob
GET http://yourhost:5000/api/job/<jobid>

### AddJob
POST http://yourhost:5000/api/job

### DeleteJob
DELETE http://yourhost:5000/api/job/<jobid>

## Limitations
The plugin currently only supports one Synthetic Location
No https implemented
No change job implemented (needs to be added and deleted)