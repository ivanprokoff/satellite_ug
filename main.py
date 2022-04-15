import datetime

import dash
from dash import dcc, html
import plotly
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import shapely.geometry

import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
cards = html.Div(
    [
        html.Div(
            [html.Div(dbc.Card(
                [dbc.CardBody(
                    [
                        dcc.Graph(id='live-update-graph')
                    ]
                ), ],
                className="mb-3", ), style={'margin': '15px'}
            ),
                html.Div(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dcc.Graph(id='live-update-graph1')
                            ]
                        ),
                        className="",
                    ), style={'margin': '15px'}),
                html.Div(dbc.Card(
                    [dbc.CardBody(
                        [
                            dcc.Graph(id='live-update-graph2')
                        ]
                    ), ],
                    className="mb-3",
                ), style={'margin': '15px'}),
                html.Div(dbc.Card(
                    [dbc.CardBody(
                        [
                            dcc.Graph(id='live-update-graph3')
                        ]
                    ), ]
                    ,
                    className="mb-3",
                ), style={'margin': '15px'})], style={'float': 'left'}),
        html.Div(id='live-update-text', style={'display': 'block', 'width': '20%', 'float': 'left'}),
        html.Div(dcc.Graph(id='live-update-map'), style={'display': 'block', 'width': '30%', 'float': 'left'}),
        html.Div(dbc.Card(
            [dbc.CardBody(
                [
                    dcc.Graph(id='live-update-pie')
                ]
            ), ],
            className="mb-3", ), style={'margin': '15px', 'float': 'left', 'width': '30%'}
        ),
        dcc.Interval(
            id='interval-component',
            interval=1 * 1000,  # in milliseconds
            n_intervals=0
        ),
    ],
)
app.layout = html.Div(
    html.Div([
        html.H4('Satellite Live Feed'),
        cards,
    ])

)


@app.callback(Output('live-update-pie', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_pie_live(n):
    labels = ['Oxygen', 'Hydrogen', 'Carbon_Dioxide', 'Nitrogen']
    values = [4500, 2500, 1053, 500]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.update_layout(height=275)
    return fig


@app.callback(Output('live-update-map', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_map_live(n):
    df = pd.read_csv("data.csv")
    fig = go.Figure(px.line_geo(lat=df['latitude'], lon=df['longitude']))
    fig.update_layout(height=335)
    return fig


@app.callback(Output('live-update-text', 'children'),
              Input('interval-component', 'n_intervals'))
def update_metrics(n):
    df = pd.read_csv("data.csv")
    lon = df['longitude'].to_list()[-1]
    lat = df['latitude'].to_list()[-1]
    alt = df['altitude'].to_list()[-1]
    style = {'padding': '5px', 'fontSize': '16px'}
    return [
        dbc.Card(
            [
                dbc.CardHeader("Altitude"),
                dbc.CardBody(
                    [
                        html.H4(f'{alt} m', className="card-title"),
                        html.P("На текущий момент", className="card-text"),
                    ]
                ),
            ],
            style={"width": "18rem", 'margin': '20px'},
        ),
        dbc.Card(
            [
                dbc.CardHeader("Latitude"),
                dbc.CardBody(
                    [
                        html.H4(f'{lat}', className="card-title"),
                        html.P("На текущий момент", className="card-text"),
                    ]
                ),
            ],
            style={"width": "18rem", 'margin': '20px'},
        ),
        dbc.Card(
            [
                dbc.CardHeader("Longtitude"),
                dbc.CardBody(
                    [
                        html.H4(f'{lon}', className="card-title"),
                        html.P("На текущий момент", className="card-text"),
                    ]
                ),
            ],
            style={"width": "18rem", 'margin': '20px'},
        ),
    ]


# Multiple components can update everytime interval gets fired.
@app.callback(Output('live-update-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    df = pd.read_csv("data.csv")
    # Create the graph with subplots
    fig = make_subplots(rows=1, cols=1)
    fig['layout']['margin'] = {
        'l': 30, 'r': 10, 'b': 30, 't': 10
    }
    fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}

    fig.append_trace({
        'x': df['time'].to_list(),
        'y': df['altitude'].to_list(),
        'name': 'Altitude',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 1, 1)
    fig.update_layout(height=125)
    return fig


@app.callback(Output('live-update-graph1', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    df = pd.read_csv("data.csv")
    fig = make_subplots(rows=1, cols=1)
    fig['layout']['margin'] = {
        'l': 30, 'r': 10, 'b': 30, 't': 10
    }
    fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}

    fig.append_trace({
        'x': df['longitude'].to_list(),
        'y': df['latitude'].to_list(),
        'text': df['time'].to_list(),
        'name': 'Longitude vs Latitude',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 1, 1)
    fig.update_layout(height=125)
    return fig


# Multiple components can update everytime interval gets fired.
@app.callback(Output('live-update-graph2', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    df = pd.read_csv("data.csv")

    # Create the graph with subplots
    fig = make_subplots(rows=1, cols=1)
    fig['layout']['margin'] = {
        'l': 30, 'r': 10, 'b': 30, 't': 10
    }
    fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}

    fig.append_trace({
        'x': df['time'].to_list(),
        'y': df['altitude'].to_list(),
        'name': 'Altitude',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 1, 1)
    fig.update_layout(height=125)
    return fig


# Multiple components can update everytime interval gets fired.
@app.callback(Output('live-update-graph3', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    df = pd.read_csv("data.csv")
    # Create the graph with subplots
    fig = make_subplots(rows=1, cols=1)
    fig['layout']['margin'] = {
        'l': 30, 'r': 10, 'b': 30, 't': 10
    }
    fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}

    fig.append_trace({
        'x': df['time'].to_list(),
        'y': df['altitude'].to_list(),
        'name': 'Altitude',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 1, 1)
    fig.update_layout(height=125)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
