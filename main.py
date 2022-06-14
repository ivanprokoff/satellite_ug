import datetime

import dash
import threading
from dash import dcc, html
import plotly
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
import schedule
import datetime
import plotly.express as px
import numpy as np
import shapely.geometry
import dash_leaflet as dl

import pandas as pd

external_scripts = []

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, external_scripts=external_scripts)

patterns = []
df = pd.read_csv("LOG00194.csv")
coords = df[['lattitude', 'longitude']].values.tolist()
polyline = dl.Polyline(positions=coords)
marker_pattern = dl.PolylineDecorator(children=polyline, patterns=patterns)
# Rotated custom marker.

'''@app.callback(Output('live-update-text1', 'children'),
              Input('interval-component', 'n_intervals'))'''


def update_metrics(n):
    df = pd.read_csv("LOG00194.csv")
    lon = df['temperature_electronics'].to_list()[-1]
    lat = df['temperature_battery'].to_list()[-1]
    alt = df['temperature_outside'].to_list()[-1]
    style = {'padding': '5px', 'fontSize': '16px'}
    return [
        dbc.Card(
            [
                dbc.CardHeader("Electronics temperature"),
                dbc.CardBody(
                    [
                        html.H4(f'{alt} m', className="card-title"),
                        html.P("На текущий момент", className="card-text"),
                    ]
                ),
            ],
            style={"width": "18rem", 'margin': '24px', 'margin-top': '0px'},
        ),
        dbc.Card(
            [
                dbc.CardHeader("Battery temperature"),
                dbc.CardBody(
                    [
                        html.H4(f'{lat}', className="card-title"),
                        html.P("На текущий момент", className="card-text"),
                    ]
                ),
            ],
            style={"width": "18rem", 'margin': '24px'},
        ),
        dbc.Card(
            [
                dbc.CardHeader("Temperature outside"),
                dbc.CardBody(
                    [
                        html.H4(f'{lon}', className="card-title"),
                        html.P("На текущий момент", className="card-text"),
                    ]
                ),
            ],
            style={"width": "18rem", 'margin': '24px'},
        ),
    ]


'''@app.callback(Output('live-update-pie', 'figure'),
              Input('interval-component', 'n_intervals'))'''


def update_pie_live(n):
    df = pd.read_csv("LOG00194.csv")
    labels = ['LPG', 'CH4', 'CO', 'H2', 'CO2']
    values = [df['LPG'].sum().tolist(), df['CH4'].sum().tolist(), df['CO'].sum().tolist(), df['H2'].sum().tolist(),
              df['CO2'].sum().tolist()]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.update_layout(height=285)
    return fig


'''@app.callback(Output('live-update-pie1', 'figure'),
              Input('interval-component', 'n_intervals'))'''


def update_pie_live1():
    df = pd.read_csv("LOG00194.csv")
    labels = ['LPG(2)', 'CH4(2)', 'CO(2)', 'H2(2)']
    values = [df['LPG(2)'].sum().tolist(), df['CH4(2)'].sum().tolist(),
              df['CO(2)'].sum().tolist(),
              df['H2(2)'].sum().tolist()]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.update_layout(height=285)
    return fig


'''@app.callback(Output('live-update-text', 'children'),
              Input('interval-component', 'n_intervals'))'''


def update_metrics1():
    df = pd.read_csv("LOG00194.csv")
    lon = df['longitude'].to_list()[-1]
    lat = df['lattitude'].to_list()[-1]
    alt = df['altitude_GPS'].to_list()[-1]
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
'''@app.callback(Output('live-update-graph', 'figure'),
              Input('interval-component', 'n_intervals'))'''


def update_graph_live():
    df = pd.read_csv("LOG00194.csv")
    # Create the graph with subplots
    fig = make_subplots(rows=1, cols=1)
    fig['layout']['margin'] = {
        'l': 30, 'r': 10, 'b': 30, 't': 10
    }
    fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}
    fig.append_trace({
        'x': df['time'].to_list(),
        'y': df['altitude_GPS'].to_list(),
        'name': 'Altitude',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 1, 1)
    fig.update_layout(height=125)
    return fig


'''@app.callback(Output('live-update-graph1', 'figure'),
              Input('interval-component', 'n_intervals'))'''


def update_graph_live1():
    df = pd.read_csv("LOG00194.csv")
    fig = make_subplots(rows=1, cols=1)
    fig['layout']['margin'] = {
        'l': 30, 'r': 10, 'b': 30, 't': 10
    }
    fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}

    fig.append_trace({
        'x': df['time'].to_list(),
        'y': df['radiation_dinamic'].to_list(),
        'text': df['time'].to_list(),
        'name': 'Longitude vs Latitude',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 1, 1)
    fig.update_layout(height=125)
    return fig


# Multiple components can update everytime interval gets fired.
'''@app.callback(Output('live-update-graph2', 'figure'),
              Input('interval-component', 'n_intervals'))'''


def update_graph_live2():
    df = pd.read_csv("LOG00194.csv")

    # Create the graph with subplots
    fig = make_subplots(rows=1, cols=1)
    fig['layout']['margin'] = {
        'l': 30, 'r': 10, 'b': 30, 't': 10
    }
    fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}
    fig.append_trace({
        'x': df['time'].to_list(),
        'y': df['temperature_pres_sens'].to_list(),
        'name': 'Altitude',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 1, 1)
    fig.update_layout(height=125)
    return fig


# Multiple components can update everytime interval gets fired.
'''@app.callback(Output('live-update-graph3', 'figure'),
              Input('interval-component', 'n_intervals'))'''


def update_graph_live3():
    df = pd.read_csv("LOG00194.csv")
    # Create the graph with subplots
    fig = make_subplots(rows=1, cols=1)
    fig['layout']['margin'] = {
        'l': 30, 'r': 10, 'b': 30, 't': 10
    }
    fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}
    fig.append_trace({
        'x': df['time'].to_list(),
        'y': df['pressure'].to_list(),
        'name': 'Altitude',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 1, 1)
    fig.update_layout(height=125)
    return fig


cards = html.Div(
    [
        html.Div(
            [html.Div(dbc.Card(
                [dbc.CardHeader("Battery temperature"),
                 dbc.CardBody(
                     [
                            dcc.Graph(figure=update_graph_live())
                     ]
                 ), ],
                className="mb-3", ), style={'margin': '15px', 'width': '650px'}
            ),
                html.Div(
                    dbc.Card([dbc.CardHeader("Battery temperature"),
                              dbc.CardBody(
                                  [
                                      dcc.Graph(figure=update_graph_live1())
                                  ]
                              )],
                             className="",
                             ), style={'margin': '15px'}),
                html.Div(dbc.Card(
                    [dbc.CardHeader("Battery temperature"), dbc.CardBody(
                        [
                            dcc.Graph(figure=update_graph_live2())
                        ]
                    ), ],
                    className="mb-3",
                ), style={'margin': '15px'}),
                html.Div(dbc.Card(
                    [dbc.CardHeader("Battery temperature"), dbc.CardBody(
                        [
                            dcc.Graph(figure=update_graph_live3())
                        ]
                    ), ]
                    ,
                    className="mb-3",
                ), style={'margin': '15px'})], style={'float': 'left'}),
        html.Div([html.Div(id='live-update-text', style={'display': 'block', 'float': 'left'}),
                  html.Div(dl.Map(center=[56.752016, 39.449476], zoom=9, children=[dl.TileLayer(), marker_pattern,
                                                                                   dl.Marker(
                                                                                       position=[56.920100, 39.3164]),
                                                                                   dl.Marker(
                                                                                       position=[56.634232, 39.132600]),
                                                                                   # dl.MeasureControl(position="topleft",
                                                                                   #                  primaryLengthUnit="kilometers",
                                                                                   #                  primaryAreaUnit="hectares",
                                                                                   #                  activeColor="#214097",
                                                                                   #                  completedColor="#972158"),
                                                                                   dl.FeatureGroup([
                                                                                       dl.EditControl(
                                                                                           id="edit_control"),
                                                                                       dl.Marker(position=[56, 10])]),
                                                                                   ]),
                           style={"width": "37%", "height": "300px", 'display': 'block', 'float': 'left', 'margin':
                               '19px'})]),
        html.Div(dbc.Card(
            [dbc.CardBody(
                [
                    dcc.Graph(id='live-update-pie')
                ]
            ), ],
            className="mb-3", ), style={'float': 'left', 'width': '18%', 'margin-left': '19px', 'margin-right': '19px'}
        ),
        html.Div(dbc.Card(
            [dbc.CardBody(
                [
                    dcc.Graph(id='live-update-pie1')
                ]
            ), ],
            className="mb-3", ), style={'float': 'left', 'width': '18%'}
        ),
        html.Div(id='live-update-text1', style={'display': 'block', 'float': 'left'}),
        # html.Div(dash.dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])),
    ],
)
app.layout = html.Div(
    html.Div([
        html.H4('Satellite Live Feed'),
        cards,
    ])

)


def dump_coords_to_json():
    df = pd.read_csv("LOG00194.csv")
    df = df[['lattitude', 'longitude']]
    with open('formatted.json', 'w') as outfile:
        df.to_json(outfile)
    return


if __name__ == '__main__':
    app.run_server(debug=True)
