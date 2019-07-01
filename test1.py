import json, requests
from config import key
key = "HaoWu-PriceDec-PRD-d5207d993-3fae3a19"
#searchTerm = ("Iphone")
condition = ("3000")
minPrice =("0")
maxPrice =("10000")

searchTerm = ('Macbook Pro 2017')

print ("\n1 = keyboard \n2 = CompletedItems")

operation = input("\nSelect Item Status: ")
if operation == "1":
  operation = "findItemsByKeywords"
elif operation == "2":
  operation = "findCompletedItems"
else:
  print ("You did not select a valid operation")


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
&paginationInput.pageNumber=" + str(1+1) + "\
&sortOrder=BestMatch\
&keywords=" + searchTerm)


results = requests.get(active_url)
raw = results.json()
print(raw["findCompletedItemsResponse"][0]['paginationOutput'][0]['totalEntries'][0])
#with open('test+'+str(1+1)+'.json', 'w') as json_file:
     #   json.dump(raw, json_file)
