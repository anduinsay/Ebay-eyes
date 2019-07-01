### Engine to communicate with database in AWS

###config
DB_HOST ='anduinsay.cf8iw71rmwv3.us-east-1.rds.amazonaws.com'
DB_PORT = 3306
DB_USER ="anduinsaymaster"
DB_PASSWD = "3217642626"
DB_NAME = "ebay"

from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine

def createDefaultEngine(credential_path = '~/.my.cnf'):
    myDB = URL(drivername='mysql+pymysql',username = 'anduinsaymaster',
               password = '3217642626',
               host= DB_HOST,
               database='ebay',
               query={ 'read_default_file' : credential_path })
    engine = create_engine(myDB)
    return engine

engine = createDefaultEngine()