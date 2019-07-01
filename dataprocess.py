
import json
import pandas as pd


def Process(jsonfile,schedule ='today'):
    ##schedule
    with open(jsonfile) as json_data:
        data = json.load(json_data)
        json_data.close()
    p =[]
    et = []
    totalsum = data["findCompletedItemsResponse"][0]['paginationOutput'][0]['totalEntries'][0]
   # print(type(totalsum))
    if int(totalsum) != 0:
        for item in data["findCompletedItemsResponse"][0]["searchResult"][0]["item"]:
            price = int(float(item["sellingStatus"][0]["convertedCurrentPrice"][0]['__value__']))
            title = item["title"][0]
            StartTime = item['listingInfo'][0]['startTime'][0]
            EndTime = item['listingInfo'][0]['endTime'][0]
            p.append(price)
            et.append(EndTime)
        df = pd.DataFrame()
        df['price'] =p
        df['Time'] = et
        df['Time'] = pd.to_datetime(df.Time)
        df['totalnum'] = totalsum
        return df
    else:
        return None




# mysql -h anduinsay.cf8iw71rmwv3.us-east-1.rds.amazonaws.com -P 3306 -u anduinsaymaster -p






