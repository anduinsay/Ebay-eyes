##tools to update

def update_itemdb(itemfile):
    n = pd.read_sql('select count(itemid) as idsum from item', engine).idsum
    newdata = pd.read(itemfile)
    newdata['itemid'] = phone['itemid']+ int(n)
    newdata.to_sql('item',con = engine,schema='ebay',if_exists = "append",index = False)


def update_transactiondb(Jsonfile):
    newdata2 = Process(Jsonfile)
    newdata2.to_sql

Itemtable.to_sql('item',con = engine,schema='ebay',if_exists = "replace",index = False)