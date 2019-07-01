# Displays Raw JSON Data for Active Listings
import json, requests
from config import key
#key = "HaoWu-PriceDec-PRD-d5207d993-3fae3a19"
#searchTerm = ("Iphone")
#condition = ("3000")
minPrice =("0")
maxPrice =("100000")


class Getdata:
    def __init__(self,searchTerm,length,condition,opt):
        self.searchTerm = searchTerm
        self.length = length
        self.condition = condition
        self.opt = opt
    def get_data(self):
        if opt == '1':
            operation = "findItemsByKeywords"
        elif opt == '2':\
            operation = "findCompletedItems"
        else:
            print("You did not select a valid operation")
        for i in range(length):
            active_url = ("http://svcs.ebay.com/services/search/FindingService/v1\
?OPERATION-NAME=" + operation + "\
&SERVICE-VERSION=1.7.0\
&SECURITY-APPNAME=" + key +"&RESPONSE-DATA-FORMAT=JSON\
&REST-PAYLOAD\
&itemFilter(0).name=Condition\
&itemFilter(0).value=" + condition + "\
&itemFilter(1).name=MinPrice\
&itemFilter(1).value=" + minPrice +"&itemFilter(1).paramName=Currency\
&itemFilter(1).paramValue=USD\
&itemFilter(2).name=MaxPrice\
&itemFilter(2).value=" + maxPrice +"&itemFilter(2).paramName=Currency\
&itemFilter(2).paramValue=USD\
&itemFilter(3).name=ListingType\
&itemFilter(3).value(0)=AuctionWithBIN\
&itemFilter(3).value(1)=FixedPrice\
&paginationInput.entriesPerPage=100\
&paginationInput.pageNumber=" + str(i+1) + "\
&sortOrder=PricePlusShippingLowest\
&keywords=" + searchTerm)
       # print(active_url)
            results = requests.get(active_url)
            raw = results.json()
            print(raw["findCompletedItemsResponse"][0]['paginationOutput'][0]['totalEntries'][0])
            with open(searchTerm+str(i+1)+'.json', 'w') as json_file:
                json.dump(raw, json_file)
   # for i in range(100):


 # print(raw['findCompletedItemsResponse'][0]['searchResult'][0]['item'][i]['listingInfo'][0]['startTime'])
#  print(raw['findCompletedItemsResponse'][0]['searchResult'][0]['item'][i]['listingInfo'][0]['endTime'])
#with open('test.json','w') as json_file:
  #json.dump(raw,json_file)
#print (raw)

##for test
# get_data(st,1,condition = "3000")