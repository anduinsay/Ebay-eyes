# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from frontdata import UserInput,layout,preprocess
import plotly.plotly as py
import plotly.figure_factory as ff
import numpy as np
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


#fig1 =preprocess('galaxy s9')

#df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv")

app.layout = html.Div([
    dcc.Input(id='input-state', type='text', value='Search here'),
    html.Button(id='submit-button', n_clicks=0, children='Submit'),
    html.Div(id='output-state'),
    dcc.Graph(id='output-graph'),
    dcc.Graph(id = 'dis-graph'),
    dcc.Graph(id= 'pie-graph')
])


@app.callback(Output('output-state', 'children'),
              [Input('submit-button', 'n_clicks')],
              [State('input-state', 'value')]
              )

def update_output(click,input1):
    newlen,oldlen= layout(input1)
    return u'''
        Total nums of the items you search for is {}, brand new ones are {},used ones are {}
    '''.format(len(UserInput(input1)),newlen,oldlen)

@app.callback(
     Output('output-graph', 'figure'),
     [Input('submit-button', 'n_clicks')],
     [State('input-state', 'value')])

def display_forecast_data(click,input1):
     if int(click):
         fig1 = preprocess(input1)
     return fig1

@app.callback(
     Output('dis-graph', 'figure'),
     [Input('submit-button', 'n_clicks')],
     [State('input-state', 'value')])

#figure
def display_forecast_data(click,input1):
     if int(click):
         df2 = UserInput(input1)
         df2 = df2[df2.price <= 3 * (df2.price.mean())]
         df2 = df2[df2.price >= 0.3 * (df2.price.mean())]
         new = df2[df2['itemcondition'] == 'new']
         old = df2[df2['itemcondition'] != 'new']

         xnew = new.price.values

         xold = old.price.values

         hist_data = [xnew,xold]
         group_labels = ['new item with avg price '+ str(int(np.mean(xnew))),'used item with avg price '+ str(int(np.mean(xold)))]

         results = ff.create_distplot(hist_data, group_labels,show_hist=True)
     return results

@app.callback(
     Output('pie-graph', 'figure'),
     [Input('submit-button', 'n_clicks')],
     [State('input-state', 'value')])

def display_forecast_data(click,input1):
     if int(click):
         df3 = UserInput(input1)
         new = df3[df3['itemcondition'] == 'new']
         old = df3[df3['itemcondition'] != 'new']
         nlabels = new.itemname.value_counts().index.values #nlabels = new labels
         nvalues = new.itemname.value_counts().values #nvalues = new values
         olabels = old.itemname.value_counts().index.values  # olabels = used items labels
         ovalues = old.itemname.value_counts().values  # ovalues = used items values

         fig3 = {
             "data": [
                 {
                     "values": nvalues,
                     "labels": nlabels,
                     "domain": {"column": 0},
                     "name": input1,
                     "hoverinfo": "label+percent+name",
                     "hole": .4,
                     "type": "pie"
                 },
                 {
                     "values": ovalues,
                     "labels": olabels,
                     "domain": {"column": 1},
                     "name": input1,
                     "hoverinfo": "label+percent+name",
                     "hole": .4,
                     "type": "pie"
                 }],
             "layout": {
                 "title": "Categorys of your search item",
                 "grid": {"rows": 1, "columns": 2},
                 "annotations": [
                     {
                         "font": {
                             "size": 20
                         },
                         "showarrow": False,
                         "text": "New",
                         "x": 0.20,
                         "y": 0.5
                     },
                     {
                         "font": {
                             "size": 20
                         },
                         "showarrow": False,
                         "text": "Used",
                         "x": 0.8,
                         "y": 0.5
                     }
                 ]
             }
         }
     return fig3


if __name__ == '__main__':
    app.run_server(debug=False)