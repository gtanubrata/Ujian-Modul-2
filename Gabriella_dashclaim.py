import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import numpy as np
import pandas as pd
import seaborn as sns
import dash_table
from dash.dependencies import Input, Output, State


def generate_table(dataframe, page_size=10):
    return dash_table.DataTable(
        id='dataTable',
        columns=[{
            "name": i,
            "id": i
        } for i in dataframe.columns],
        data=dataframe.to_dict('records'),
        page_action="native",
        page_current=0,
        page_size=page_size,
        style_table={'overflowX': 'scroll'}
    )


np.random.seed(101)
claim = pd.read_csv('tsa_claims_dashboard_ujian.csv').drop(
    'Unnamed: 0', axis=1).dropna(how='any').sample(1000)

# pressed to read csv, fail to export to SQL

external_stylesheets = ['assets/1_bootstrap.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1('Ujian Modul 2 Dashboard TSA'),

    html.Div(children='''
        Created by: Gabriella
    '''),

    dcc.Tabs([
        dcc.Tab(value='tab-1', label='DataFrame Table', children=[
            html.H1('DATAFRAME TSA'
                    ),

            html.Div([html.P('Claim Site'),
                     dcc.Dropdown(value='All',
                                   id='filter-claim',
                                   options=[{'label': i, 'value': i}
                                            for i in claim['Claim Number']]
                                   )
                      ], className='col-3'),

            html.Div([html.P('Max Rows:'),
                      dcc.Input(id='filter-row',
                                type='number',
                                value=10)

                      ], className='col-3'),

            html.Div(children=[
                html.Button('search', id='search')
            ], className='col-4'),

            html.Div(id='div-table', children=[generate_table(claim)])
        ]),

        dcc.Tab(value='tab-2', label='Bar-Chart', children=[
            html.Div([
                html.Div([
                    html.Div([
                    html.P('Y1'),
                    dcc.Dropdown(id='filter-y1',
                                 options=[{'label': 'Claim Amount', 'value': 'Claim Amount'},
                                          {'label': 'Close Amount',
                                                    'value': 'Close Amount'},
                                          {'label': 'Day Differences',
                                                    'value': 'Day Differences'},
                                          {'label': 'Amount Differences', 'value': 'Amount Differences'}]
                                 ),
                ], className = 'col-3'),

                html.Div([
                    html.P('Y2'),
                    dcc.Dropdown(id='filter-y2',
                                 options=[{'label': 'Claim Amount', 'value': 'Claim Amount'},
                                          {'label': 'Close Amount',
                                                    'value': 'Close Amount'},
                                          {'label': 'Day Differences',
                                                    'value': 'Day Differences'},
                                          {'label': 'Amount Differences', 'value': 'Amount Differences'}]
                                 ),
                ], className = 'col-3'),

                html.Div([
                    html.P('X'),
                    dcc.Dropdown(id='filter-x',
                                 options=[{'label': 'Claim Type', 'value': 'Claim Type'},
                                          {'label': 'Claim Site',
                                                    'value': 'Claim Site'},
                                          {'label': 'Disposition',
                                                    'value': 'Disposition'}]
                                 ),
                ], className = 'col-3')
                ], className = 'row'),

                html.Div([
                    dcc.Graph(
                        id='example-graph',
                        figure={
                            'data': [
                                {'x': claim['Claim Type'], 'y': claim['Claim Amount'],
                                 'type': 'bar', 'name': 'bar1'},
                                 {'x': claim['Claim Type'], 'y': claim['Close Amount'],
                                 'type': 'bar', 'name': 'bar1'}
                            ],
                            'layout': {
                                'title': 'Bar Chart'
                            }
                        }
                    )
                ])

            ],
            )
        ]),

        dcc.Tab(value='tab-3', label='Scatter-Chart', children=[
            html.Div([
                html.Div([
                    dcc.Graph(
                id='scatter-chart',
                figure={'data': [
                    go.Scatter(
                        x=claim[claim['Claim Type'] == i]['Claim Amount'],
                        y=claim[claim['Claim Type'] == i]['Close Amount'],
                        mode='markers',
                        name='{}'.format(i)
                    ) for i in claim['Claim Type'].unique()
                ],
                    'layout':go.Layout(
                    xaxis={'title': 'Claim Amount'},
                    yaxis={'title': 'Close Amount'},
                    hovermode='closest'
                )
                }
            )
                ])
            ])
        ]),

        dcc.Tab(value='tab-4', label='Pie-Chart', children=[
            html.Div([
                html.Div([
                    dcc.Dropdown(id='filter-pie',
                                 options=[{'label': 'Claim Amount', 'value': 'Claim Amount'},
                                          {'label': 'Close Amount',
                                                    'value': 'Close Amount'},
                                          {'label': 'Day Differences',
                                                    'value': 'Day Differences'},
                                          {'label': 'Amount Differences', 'value': 'Amount Differences'}]
                                 )
                ], className = 'col-3'),

                html.Div([
                    dcc.Graph(
                id='pie-chart',
                figure={
                    'data': [
                        go.Pie(labels=[i for i in claim['Claim Type'].unique()],
                               values=[claim[claim['Claim Type'] == i]['Claim Amount'].mean()
                                       for i in claim['Claim Type'].unique()]
                               )],
                    'layout': go.Layout(title='Mean Pie Chart')}
            )
                ])
            ])
        ]),

    ], content_style={
        'fontFamily': 'Arial',
        'borderBottom': '1px solid #d6d6d6',
        'borderLeft': '1px solid #d6d6d6',
        'borderRight': '1px solid #d6d6d6',
        'padding': '44px'}

    )
], style={
    'maxWidth': '1200px',
    'margin': '0 auto'
}
)

# @app.callback(Output(component_id='div-table', component_property='children'),
#             [Input('filter-claim', 'value'),
#              Input('search', 'n_clicks')],
#             [State(component_id='div-table', component_property='children')]
#             )
# def update_table(fclaim, n_clicks, tsatable):
#     claim = pd.read_csv('tsa_claims_dashboard_ujian.csv').drop(
#         'Unnamed: 0', axis=1).dropna(how='any').sample(1000)
#     claim = claim[claim['Claim Number'] == fclaim]
#     children = [generate_table(claim)]
#     return children

@app.callback(Output('pie-chart', 'figure'),
              [Input('filter-pie', 'value')])
def update_pie(numerical):
    return {
        'data': [
            go.Pie(labels=[i for i in claim['Claim Type'].unique()],
                               values=[claim[claim['Claim Type'] == i][numerical].mean()
                                       for i in claim['Claim Type'].unique()]
                               )],
        'layout': go.Layout(title='Mean Pie Chart')}

if __name__ == '__main__':
    app.run_server(debug=True)
