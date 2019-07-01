from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine
import pandas as pd
from test2 import Itemtable
def createDefaultEngine(credential_path = '~/.my.cnf'):
    myDB = URL(drivername='mysql+pymysql',username = 'root',
               password = '3217642626',
               host= 'localhost',
               database='ebay',
               query={ 'read_default_file' : credential_path })
    engine = create_engine(myDB)
    return engine

engine = createDefaultEngine()

print(pd.read_sql('select * from ebay.item', engine))
#print(Itemtable)
print(Itemtable)

Itemtable.to_sql('item',con = engine,schema='ebay',if_exists = "replace",index = False)


