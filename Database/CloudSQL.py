###tools to manage Mysql databse at AWS RDS database (mysql)

from AWSDB import engine
from datasource import Get_data
import pandas as pd
from dataprocess import Process
from pathlib import Path ##check if file exists




def update_itemdb(itemfile,CategoryID):
    ##input a file, spcific the category id of the
    n = pd.read_sql('select count(itemid) as idsum from item', engine).idsum   ###current number of item data
    newdata = pd.read_csv(itemfile)   ##itemfile csv file
    newdata['itemid'] = newdata['itemid']+ int(n)
    newdata['CategoryId'] = CategoryID
    newdata.to_sql('item',con = engine,schema='ebay',if_exists = "append",index = False)


def update_transaction():

    updateitem = pd.read_sql('select itemname,categoryID from item',engine)

    itemname = updateitem.itemname.values
    category = updateitem.categoryID.values


    for i,j in zip(len(itemname),category):
        used = Process(Get_data(itemname[i],length = 1, condition = '3000',cID = j))
        new = Process(Get_data(itemname[i],length =1, condition ='1000',cID = j))

        used['itemid'] = i
        new['itemid'] = i
        used['condition'] ='used'
        new['condition'] = 'new'


        used.to_sql('transaction',con = engine,schema= 'ebay',if_exists = 'append',index = False)
        new.to_sql('transaction', con=engine, schema='ebay', if_exists='append', index=False)




if __name__ == "__main__":



    update_transaction()