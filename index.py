import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import bubble, country, region


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dbc.NavbarSimple(
        children=[dbc.NavItem(dbc.NavLink("Bubble Chart", href="/bubble")),
                  dbc.NavItem(dbc.NavLink("Country Comparison", href="/country")),
                  dbc.NavItem(dbc.NavLink("Region Comparison", href="/region")),
                  dbc.NavItem(
                      dbc.NavLink("About Oxford Stringency Index", href="https://player.vimeo.com/video/463163595"))
                  ],
        brand="Oxford Government Response Tracker",
        brand_href="https://covidtracker.bsg.ox.ac.uk/",
        color="primary",
        dark=True,
    ),
    html.Div(id='page-content', children=[])
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/bubble':
        return bubble.layout
    if pathname == '/country':
        return country.layout
    if pathname == '/region':
        return region.layout
    else:
        return bubble.layout


if __name__ == '__main__':
    app.run_server(debug=True, port=8151)