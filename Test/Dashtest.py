
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from frontdata import preprocess
import pandas as pd
import plotly.graph_objs as go

df = pd.read_csv(
    'https://raw.githubusercontent.com/plotly/'
    'datasets/master/gapminderDataFiveYear.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Graph(id='graph-with-slider',figure = preprocess('galaxy s9')),
    dcc.Slider(
        id='year-slider',
        min=0,
        max=10,
        value=9,
        marks={str(year): str(year) for year in range(10)},
        step=None
    )
])


@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('year-slider', 'value')])
def update_figure(selected_year):
    input = 'galaxy s'+ str(selected_year)
    preprocess(input)
    return



if __name__ == '__main__':
    app.run_server(debug=False)