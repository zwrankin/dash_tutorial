import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

top_markdown_text = '''
### Dash Boilerplate
This template is on the `boilerplate` branch of the tutorial [Github repo](https://github.com/zwrankin/dash_tutorial)  
See the `master` branch to build an interactive visualization app
'''

app.layout = html.Div([

    dcc.Markdown(children=top_markdown_text),

])

if __name__ == '__main__':
    app.run_server(debug=True)
