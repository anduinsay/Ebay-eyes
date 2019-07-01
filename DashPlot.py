# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from frontdata import UserInput,preprocess
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


#fig1 =preprocess('galaxy s9')

#df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv")

app.layout = html.Div([
    dcc.Input(id='input-state', type='text', value='Search here'),
    html.Button(id='submit-button', n_clicks=0, children='Submit'),
    html.Div(id='output-state'),
    dcc.Graph(id='output-graph')

])


@app.callback(Output('output-state', 'children'),
              [Input('submit-button', 'n_clicks')],
              [State('input-state', 'value')]
              )

def update_output(n_clicks, input1):
    return u'''
        The Button has been pressed {} times,
        "{}" num is issisisisi is "{}",
    '''.format(n_clicks, input1,len(UserInput(input1)))

@app.callback(
     Output('output-graph', 'figure'),
     [Input('submit-button', 'n_clicks')],
     [State('input-state', 'value')])

def display_forecast_data(click,input1):
     if int(click):
         fig1 = preprocess(input1)
     return fig1


if __name__ == '__main__':
    app.run_server(debug=False)