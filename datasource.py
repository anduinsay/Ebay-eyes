# Displays Raw JSON Data for Active Listings
import json, requests
from config import key
#key = "HaoWu-PriceDec-PRD-d5207d993-3fae3a19"
#searchTerm = ("Iphone")
#condition = ("3000")
minPrice =("0")
maxPrice =("100000")
path = "/home/anduin/PycharmProjects/WisePrice/Macbook/"
def Get_data(searchTerm,length,condition,cID,opt='2'):

    ##opt == option, provide the option to find completed items or items still in list

    if opt == '1':
        operation = "findItemsByKeywords"
    elif opt == '2':\
        operation = "findCompletedItems"
    else:
        print("You did not select a valid operation")

    if condition == '1000':
        d = 'new'
    else:
        d = 'used'

    for i in range(length):
        active_url = ("http://svcs.ebay.com/services/search/FindingService/v1\
?OPERATION-NAME=" + operation + "\
&SERVICE-VERSION=1.7.0\
&SECURITY-APPNAME=" + key +"&RESPONSE-DATA-FORMAT=JSON\
&REST-PAYLOAD\
&categoryId=" + str(cID) + "\
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
&sortOrder=EndTimeSoonest\
&keywords=" + searchTerm)
       # print(active_url)
        results = requests.get(active_url)
        raw = results.json()
        #print(raw)
        totalnum = raw["findCompletedItemsResponse"][0]['paginationOutput'][0]['totalEntries'][0]
        print(totalnum)
        ## check if no values

        if totalnum == 0:
            return int(totalnum)
            break

        with open(path + searchTerm+d+' set'+str(i+1)+'.json', 'w') as json_file:
           # print(path + searchTerm++' set'+str(i+1)+'.json')
            json.dump(raw, json_file)

        if int(totalnum) <= 100 * (i + 1):
            return int(totalnum)
            break

    return int(totalnum)





#from test2 import name
#for laptop in name:
#    st = (laptop)
#    Get_data(st,2,condition = '3000')

#st = ('I')
#Get_data(st,1,condition= '3000',cID= 9355)


#from test2 import namePhone
#for phone in namePhone:
  #  st = (phone)
   # Get_data(st,length= 100,cID=9355,condition = '1000')


###get Iphone
# from test2 import namePhone,Iphone,Samsung
# t = 0
# for n,i in enumerate(namePhone):
#     bigpig = Iphone+ Samsung
#     if (i not in bigpig) and (n>461):
#         t += int(Get_data(i,length = 100,cID = 9355,condition='1000')/100)
#         print('total call times'+str(t))



#Get_data('Iphone',1,cID = 9355, condition = '3000')

#111422





