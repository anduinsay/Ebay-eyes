##code to extract the data from database

from AWSDB import engine
import pandas as pd
import numpy as np
import plotly.graph_objs as go



#search by word, get data from db
def UserInput(iname):
    iname = '%%'+ iname + '%%'
    item_sql = 'select itemname,price,time,totalnum,transaction.condition as itemcondition from item right join transaction on item.itemid = transaction.itemid' \
               ' where itemname like '+ '"' +iname +'";'
    print(item_sql)
    data = pd.read_sql(item_sql, engine)
    print(data)
    return data


def layout(input):
    df = UserInput(input)
    df = df[df.price <= 3 * (df.price.mean())]
    df = df[df.price >= 0.3 * (df.price.mean())]

    dfnew = df[df['itemcondition'] == 'new']
    dfused = df[df['itemcondition'] == 'old']

    dfnew = dfnew.groupby('time').agg({'price': np.mean}).reset_index()
    dfused = dfnew.groupby('time').agg({'price': np.mean}).reset_index()
    return dfnew,dfused

def preprocess(names):
    df = UserInput(names)
    df = df[df.price <= 3 * (df.price.mean())]
    df = df[df.price >= 0.3 * (df.price.mean())]

    dfnew = df[df['itemcondition'] == 'new']
    dfold = df[df['itemcondition'] == 'old']
    dfnew = dfnew.groupby('time').agg({'price': np.mean}).reset_index()
    dfold = dfnew.groupby('time').agg({'price': np.mean}).reset_index()
    trace_high = go.Scatter(
        x=dfnew.time,
        y=dfnew.price,
        name=names + "  brand new",
        line=dict(color='#17BECF'),
        opacity=0.8)
    trace_low = go.Scatter(
        x=dfold.time,
        y=dfold.price,
        name=names + " Used",
        line=dict(color='#7F7F7F'),
        opacity=0.8)

    data = [trace_high, trace_low]
    layout = dict(
        title='Price Trend',
        xaxis=dict(
            rangeselector=dict(
                buttons=list([dict(count=1, label='1 day', step='day', stepmode='backward'),
                              dict(count=6, label='6 day', step='day', stepmode='backward'), dict(step='6 day')])
            ), rangeslider=dict(), type='date')
    )
    fig = dict(data=data, layout=layout)

    return fig

#UserInput('iphone')

#select * from item where item.itemname like '%iphone%'


#select item.itemid as itemid,itemname from item right join transaction on item.itemid = transaction.itemid where itemname like "%iphone X%";