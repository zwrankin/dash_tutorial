import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

################################################################################################################
# LOAD AND PROCESS DATA
df0 = pd.read_csv('./data/IHME_GBD_2017_HEALTH_SDG_1990_2030_SCALED_Y2018M11D08.CSV')
loc_meta = pd.read_csv('./data/location_metadata.csv')

# Indicator Value by country in wide format
df = df0.pivot(index='location_name', columns='indicator_short', values='scaled_value')
df = pd.merge(loc_meta, df.reset_index())
indicators = df0.indicator_short.unique().tolist()
indicator_key = df0.drop_duplicates('indicator_short').set_index('indicator_short')[
    'ihme_indicator_description'].to_dict()

################################################################################################################


top_markdown_text = '''
### Dash Tutorial - Sustainable Development Goals
#### Zane Rankin, 2/17/2019
The [Institute for Health Metrics and Evaluation](http://www.healthdata.org/) publishes estimates for 41 health-related SDG indicators for 
195 countries and territories.  
I downloaded the [data](http://ghdx.healthdata.org/record/global-burden-disease-study-2017-gbd-2017-health-related-sustainable-development-goals-sdg) 
for a tutorial on Medium and Github   
**Indicators are scaled 0-100, with 0 being worst observed (e.g. highest mortality) and 100 being best.**  
'''

app.layout = html.Div([

    # HEADER
    dcc.Markdown(children=top_markdown_text),

    # SCATTERPLOT
    dcc.Dropdown(
        id='x-varname',
        options=[{'label': i, 'value': i} for i in indicators],
        value='SDG Index'
    ),
    dcc.Markdown(id='x-description'),
    dcc.Dropdown(
        id='y-varname',
        options=[{'label': i, 'value': i} for i in indicators],
        value='Under-5 Mort'
    ),
    dcc.Markdown(id='y-description'),
    dcc.Graph(id='scatterplot'),

])


@app.callback(
    Output('x-description', 'children'),
    [Input('x-varname', 'value')])
def x_description(i):
    return f'{indicator_key[i]}'


@app.callback(
    Output('y-description', 'children'),
    [Input('y-varname', 'value')])
def y_description(i):
    return f'{indicator_key[i]}'


@app.callback(
    Output('scatterplot', 'figure'),
    [Input('x-varname', 'value'),
     Input('y-varname', 'value'),
     ])
def update_graph(x_varname, y_varname):
    return {
        'data': [
            go.Scatter(
                x=df[df['super_region_name'] == i][x_varname],
                y=df[df['super_region_name'] == i][y_varname],
                text=df[df['super_region_name'] == i]['location_name'],
                mode='markers',
                opacity=0.7,
                marker={
                    'size': 12,
                    'line': {'width': 0.5, 'color': 'white'}
                },
                name=i
            ) for i in df.super_region_name.unique()
        ],
        'layout': go.Layout(
            height=500,
            xaxis={'title': x_varname},
            yaxis={'title': y_varname},
            # margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            # legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)
