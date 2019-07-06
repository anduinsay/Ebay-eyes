import pandas as pd
import numpy as np
Itemtable = pd.read_csv('LaptopModel.csv')[["LaptopModel"]].reset_index().rename(columns = {'index':'itemid','LaptopModel':'itemname'})
name = pd.read_csv('LaptopModel.csv').LaptopModel.values


namePhone = pd.read_csv('Phones.csv').Value.values
#print(namePhone.V)


Iphone = [i for i in namePhone if i.startswith('Apple')]
Samsung = [i for i in namePhone if i.startswith('Samsung Galaxy S')]


from dataprocess import Process



    #break;


DB_HOST ='anduinsay.cf8iw71rmwv3.us-east-1.rds.amazonaws.com'
DB_PORT = 3306
DB_USER ="anduinsaymaster"
DB_PASSWD = "3217642626"
DB_NAME = "ebay"


# from sqlalchemy.engine.url import URL
# from sqlalchemy import create_engine
# import pandas as pd
# from dataprocess import Process
# #from test2 import Itemtable,namePhone
#
#
# def createDefaultEngine(credential_path = '~/.my.cnf'):
#     myDB = URL(drivername='mysql+pymysql',username = 'anduinsaymaster',
#                password = '3217642626',
#                host= DB_HOST,
#                database='ebay',
#                query={ 'read_default_file' : credential_path })
#     engine = create_engine(myDB)
#     return engine
#
# engine = createDefaultEngine()

# for id, i in enumerate(Itemtable.itemname):
#     file = str(i) + str(1) + '.json'
#     data = Process(file)
#
#     if data is not None:
#         print(file)
#         data['Name'] = i
#         data['id'] = id
#         print(data)
#         data.to_sql('Quickstore',con = engine,schema='ebay',if_exists = "append",index = False)

