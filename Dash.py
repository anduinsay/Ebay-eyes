# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pytz
import os
import numpy as np
import pandas as pd
from AWSDB import engine
import pdb
from datetime import datetime as dt
from datetime import timedelta
#from







def get_all_topics():
    topic_sql = 'select topic_id, topic_name from volttron.topics;'
    ti_df = pd.read_sql(topic_sql, engine, index_col='topic_name')
    return ti_df

def get_data(topicsVisualize, ti_df,start,end):
    topic_ids = ti_df.loc[topicsVisualize].topic_id.values
    data_sql = 'select ts, topic_id, value_string from volttron.data where topic_id in (' + ', '.join([ str(vt) for vt in topic_ids]) + ') and ts>="'+start+'" and '+'ts<="'+end+'";'
    data = pd.read_sql(data_sql, engine, index_col='ts')
    return data

def get_forecast24h_data(start,end):
    topic_ids = Forecast_topics
    data_sql = 'select ts, topic_id, value_string from volttron.data where topic_id in (' + ', '.join(
        [str(vt) for vt in topic_ids]) + ') and ts>="' + start + '" and ' + 'ts<="' + end + '";'
    data2 = pd.read_sql(data_sql, engine, index_col='ts')
    return data2

def get_monitor_data(topicsVisualize, ti_df):
    l = len(topicsVisualize)

    topic_ids = ti_df.loc[topicsVisualize].topic_id.values
 #   topic_idsplus = ti_df.loc[['Site1low/recloser.status.Status','datalogger/Executive/OperatingMode']].topic_id.values

    data_sql = 'select ts, topic_id, value_string from volttron.data where topic_id in (' + ', '.join([ str(vt) for vt in topic_ids]) + ') order by ts desc limit '+str(l)+';'
  #  data_plus = 'select ts, topic_id, value_string from volttron.data where topic_id in (5) order by ts desc limit 1;'
  #  data_plus2 = 'select ts, topic_id, value_string from volttron.data where topic_id in (' + ', '.join([ str(vt) for vt in topic_idsplus]) + ') order by ts desc limit 2;'
  #  data_sql = 'select ts, topic_id, value_string from volttron.data where topic_id in (' + ', '.join([ str(vt) for vt in topic_ids]) + ') group by topic_id desc '+';'

    data = pd.read_sql(data_sql, engine, index_col='ts')
  #  dataplus = pd.read_sql(data_plus, engine, index_col='ts')
  #  dataplus2 = pd.read_sql(data_plus2,engine,index_col='ts')
  #  data  = pd.concat([data,dataplus,dataplus2])

    return data

def get_monitor_data2(topicsVisualize, ti_df):


    topic_ids = ti_df.loc[topicsVisualize].topic_id.values



    data_sql1 = 'select ts, topic_id, value_string from volttron.data where topic_id ='+str(topic_ids[0])+' order by ts desc limit 1;'
    data_sql2 = 'select ts, topic_id, value_string from volttron.data where topic_id =' + str(
        topic_ids[1]) + ' order by ts desc limit 1;'
    data1 = pd.read_sql(data_sql1, engine, index_col='ts')
    data2 = pd.read_sql(data_sql2, engine, index_col='ts')
  #  data_plus = 'select ts, topic_id, value_string from volttron.data where topic_id in (5) order by ts desc limit 1;'
  #  data_plus2 = 'select ts, topic_id, value_string from volttron.data where topic_id in (' + ', '.join([ str(vt) for vt in topic_idsplus]) + ') order by ts desc limit 2;'
  #  data_sql = 'select ts, topic_id, value_string from volttron.data where topic_id in (' + ', '.join([ str(vt) for vt in topic_ids]) + ') group by topic_id desc '+';'


  #  dataplus = pd.read_sql(data_plus, engine, index_col='ts')
  #  dataplus2 = pd.read_sql(data_plus2,engine,index_col='ts')
    data  = pd.concat([data1,data2])

    return data



####function to process the forecast data
def Dataprocess(source):
    source['value_string'] = source['value_string'].replace('[]', method='ffill')
    sourcedata = source.value_string.str.split(",", expand=True)
    sourcedata['topic_id'] = source['topic_id']
    l = len(sourcedata.columns) - 1
    sourcedata[0] = sourcedata[0].str[1:]
    sourcedata[l - 1] = sourcedata[l - 1].str[:-1]
    sourcedata = sourcedata.rename(columns={'topic_id': -1})
    sourcedata = sourcedata[np.arange(-1, l)]
    # sourcedata[-1]=pd.to_datetime(sourcedata[-1])
    sourcedata.iloc[:, 1:] = sourcedata.iloc[:, 1:].apply(pd.to_numeric)
    sourcedata = sourcedata.rename(columns={-1: 'topic_id'})
    # sourcedata = sourcedata[1:]
    #  sourcedata = sourcedata.iloc[:,1:].T
    return sourcedata


def generate_graph_data_from_df(data_df, visualizedTopics):
    lines = []
    for topic in visualizedTopics:
        tid = ti_df.loc[topic].values[0]
        cutout = data_df.loc[data_df.topic_id == tid]
        line = {'x': cutout.index, 'y': cutout.value_string, 'type': 'line', 'name': topic}
        lines.append(line)
    return lines

def generate_forecast(data2,topics):
    lines = []
    for topic in topics:
        tid = ti_df.loc[topic].values[0]


        cutout = data2.loc[data2.topic_id == tid]
        line = {'x': cutout.index, 'y': cutout.value_string, 'type': 'line', 'name': topic}
        lines.append(line)
    return lines

def figure_generator(res):
    return {
            'data': res,
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
def figure_generator_forecast(res):
    return {
            'data': res,
            'layout': {
                'title': 'Forecast Data Visualization'
            }
        }

def generate_table(dataframe, max_rows=5):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


path = '~/.my.cnf_reader'
# path = '/home/cstark/.my.cnf_reader'
engine = createDefaultEngine(path)
ti_df = get_all_topics()
defaultStartdate = dt.now()-timedelta(days =13)
defaultEnddate = dt.now()
defaultData = Dataprocess(get_forecast24h_data(str(defaultStartdate), str(defaultEnddate)))
defaultData.to_pickle('defaultData')
Forecastdropdownname = shortname[shortname.topic_name.isin(ti_df[ti_df.topic_id.isin(Forecast_topics)].index.values)].Name
app = dash.Dash()
app.config.suppress_callback_exceptions = True



###app layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

index_page = html.Div([
    dcc.Link('Go to DashBoard', href='/page-1'),
    html.Br(),
    dcc.Link('Go to Monitor', href='/page-2'),
])



page_1_layout = html.Div(children=[

    html.H1(children='Fraunhofer CSE Dashboard',
            style= {
                'textAlign':'center'
            }),

    html.Div(children='\nData Analysis platform of Sundial Project',style= {
                'textAlign':'center'
            }),





    html.Label('Actual values'),
 #   dcc.Dropdown(
  #      id='yaxis-column',
  #      options=[{'label': i, 'value': i} for i in ti_df.index.values],
  #      value=defaultTopics,
  #      multi=True
  #  ),

    ###for raw and Logical, currently we are using another checkbox to view the data:
  #  dcc.RadioItems(
  #              id='crossfilter-xaxis-type',
   #             options=[{'label': i, 'value': i} for i in ['Raw', 'Logical']],
 #               value='Raw',
 #               labelStyle={'display': 'inline-block'}
 #   ),

 #   html.Label('Checkboxes'),

    dcc.Checklist(
        id = 'checkbox',
        options=[
            {'label':'Show All','value':'Show All'},
 #           {'label':'Battery','value':'Battery'},
  #          {'label':'Forecast','value':'Forecast'},
  #          {'label':'PV','value':'PV'},
   #         {'label':'Load','value':'Load'}
        ],
        values = ['Show All'],
        labelStyle = {'display':'inline-block'},
      #  multi = False
    ),

    html.Div([
    dcc.Dropdown(
        id='shooter',
        options=[{'label': i, 'value': i} for i in names],
        value=['Battery'],
        multi=True
    ),]),

    html.Div([
        dcc.Dropdown(
            id='opt',
            multi=True),
    ],
    ),

    dcc.RadioItems(
                id='resample',
                options=[{'label': 'No resample', 'value': 'O'},
                         {'label': '5mins', 'value': '5'},
                         {'label': '15mins', 'value': '15'},
                         {'label': '30mins', 'value': '30'},
                         {'label': '60mins', 'value': '60'}],
                value='O',
                labelStyle={'display': 'inline-block'}
    ),


    dcc.DatePickerRange(
        id ='date-picker-Range',
        min_date_allowed = dt(2018,8,27),
        max_date_allowed = dt.now()+timedelta(days= 1),
        start_date = dt.now()-timedelta(days=1),
        end_date = dt.now()


    ),


    dcc.Graph(
        id='example-graph',
    ),

    html.Label('Forecast Values'),
    dcc.Dropdown(
        id='Forecast',
        options=[{'label': i, 'value': j} for i,j in zip(Forecastdropdownname,ti_df[ti_df.topic_id.isin(Forecast_topics)].index.values)],
        value =default1,
        multi=True
    ),

    dcc.Graph(
        id='Forecast_graph',
    ),


    html.Div(dcc.Slider(
        id='slider',
        min=0,
        max=23,
        value=0,
        step=None,
        marks={str(h): str(h) for h in np.arange(24)},
    ), style={'width': '98%', 'padding': '0px 20px 20px 20px'}),

    html.Div(id='page-1-content'),
    html.Br(),
    dcc.Link('Go to Monitor', href='/page-2'),
    html.Br(),
    dcc.Link('Go back to home', href='/'),

 #   html.Div(dcc.Slider(
  #      id='crossfilter-year--slider',
  #      min=offlinedata.index.min(),
  #      max=offlinedata.index.max(),
   #     value=offlinedata.index.max(),
   #     step=None,
   #     marks={str(year): str(year) for year in offlinedata.index.unique()}
   # ), style={'width': '49%', 'padding': '0px 20px 20px 20px'})
])

@app.callback(
    dash.dependencies.Output('opt', 'options'),
    [dash.dependencies.Input('shooter', 'value'),
     dash.dependencies.Input('checkbox', 'values')]
)

def update_date_dropdown(name,checkcheck):

#    box = []
 #   for namex in name:
  #      box = box+ fnameDict[namex]
  #      if type(box) == 'str':
   #         box = [box]
    labelbox = list(Topics.loc[Topics[name].dropna(how='all').index].LabelName.values)
    box = list(Topics.loc[Topics[name].dropna(how='all').index].Name.values)
 #   only = [{'label': i, 'value': j} for i, j in zip(labelbox, box)]
    if checkcheck == ['Show All']:
        labelbox = list(Topics.LabelName.values)
        box = list(Topics.Name.values)
    only = [{'label': i, 'value': j} for i, j in zip(labelbox, box)]

    return only
  #  return [{'label': i, 'value': i} for i in box]


####This is a dead one to make sure the B won't disappear
####This is a dead one to make sure the B won't disappear
@app.callback(
    dash.dependencies.Output('display-selected-values', 'children'),
    [dash.dependencies.Input('opt', 'value')]
)
def set_display_children(selected_value):
    return 'you have selected {} option'.format(selected_value)

####This is a dead one to make sure the B won't disappear
####This is a dead one to make sure the B won't disappear

@app.callback(
    Output('example-graph', 'figure'),
 #   [Input('shooter', 'value'),
    [Input('date-picker-Range', 'start_date'),
     Input('date-picker-Range', 'end_date'),
     Input('opt', 'value'),
     Input('resample','value')])
def display_hover_data(date1,date2,check,sample):
    date1 = str(date1)
    date2 = str(date2)


    data = get_data(check, ti_df,date1,date2)
    data.value_string = pd.to_numeric(data.value_string,errors= 'coerce').fillna(0)
   # data = data[data.topic_id.isin(indexdata)]
    data.index += delta
  #  data = data[data.index>=date1]
  #  data = data[data.index<=date2]
    if sample != 'O':
        samplesize = str(sample)+'T'
        data = data.groupby('topic_id').resample(samplesize).mean().drop(['topic_id'],axis=1).reset_index().set_index('ts')
    res = generate_graph_data_from_df(data,check)
    figure = figure_generator(res)
    return figure

@app.callback(
    Output('Forecast_graph', 'figure'),
    [Input('Forecast', 'value'),
     Input('date-picker-Range', 'start_date'),
     Input('slider', 'value')])

def display_forecast_data(topics,date1,i):
    if pd.to_datetime(date1)<= pd.to_datetime(defaultStartdate):
        data2 = get_forecast24h_data(str(date1), str(defaultEnddate))
        data2 = Dataprocess(data2)
    else:
        data2 = pd.read_pickle('defaultData')
    data3 = data2[['topic_id',i]]
    data3 =data3.rename(columns= {i:'value_string'})
    data3.index += timedelta(hours=i)
    data3.index += delta

    #data3 = data3.groupby('topic_id').resample('H').mean().drop(['topic_id'],axis=1).reset_index().set_index('ts') #used for resample
    res = generate_forecast(data3, topics)
    figure = figure_generator_forecast(res)
    return figure




page_2_layout = html.Div(
    html.Div([
        html.H4('Fraunhofer Live data Monitor',style= {
                'textAlign':'center'
            }),
        html.Div(id='live-update-text'),
        html.Label('Status'),
        html.Div(id='second-live-update-text'),

        dcc.Interval(
            id='interval-component',
            interval=10 * 1000,  # in milliseconds
            n_intervals=0
        ),
        html.Div(id='page-2-content'),
        html.Br(),
        dcc.Link('Go to Dashboard', href='/page-1'),
        html.Br(),
        dcc.Link('Go back to home', href='/')
    ]),





)




@app.callback(Output('live-update-text', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_metrics(n):
    df = get_monitor_data(defaultTopics2, ti_df)
    df['value_string']=df['value_string'].apply(pd.to_numeric)
    df['value_string'] = df['value_string'].round(2)
    df = df.reset_index()
    Label = shortname[shortname.topic_id.isin(df.topic_id.values)][['Name','topic_id']]
    df = pd.merge(Label, df, left_on='topic_id', right_on='topic_id')
    df = df.set_index('Name').drop(columns='topic_id').T

    return [

        html.Table([html.Tr([html.Th(col) for col in df.columns])] + [html.Tr([html.Td(df.iloc[i][col]) for col in df.columns]) for i in range(min(len(df), 5))])
        ###the ramge is supoorting for more values view
    ]


@app.callback(Output('second-live-update-text', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_metrics(n):
    df = get_monitor_data2(defaultTopics3, ti_df)
    df['value_string']=df['value_string'].apply(pd.to_numeric)
 #   df['value_string'] = df['value_string'].round(2)
    df = df.reset_index()
    Label = shortname[shortname.topic_id.isin(df.topic_id.values)][['Name','topic_id']]
    df = pd.merge(Label, df, left_on='topic_id', right_on='topic_id')
    df = df.set_index('Name').drop(columns='topic_id').T

    return [

        html.Table([html.Tr([html.Th(col) for col in df.columns])] + [html.Tr([html.Td(df.iloc[i][col]) for col in df.columns]) for i in range(min(len(df), 5))])
        ###the ramge is supoorting for more values view
    ]



#def update_table(n):
  #  df = get_monitor_data(defaultTopics, ti_df)
  #  df = df.set_index('topic_id').T


















# html.Table([html.Tr([html.Th(col) for col in df.columns])] +[html.Tr([html.Td(df.iloc[i][col]) for col in df.columns]) for i in range(min(len(df), 5))])



@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    else:
        return index_page
    # You could also return a 404 "URL not found" page here

app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})


  #  data = data[data.index>=date1]
  #  data = data[data.index<=date2]




server = app.server

if __name__ == '__main__':
    app.run_server(debug=False, host='127.0.0.1', port=8000)