import dash_bootstrap_components as dbc
import dash_html_components as html
from app import app
import pickle
import pandas as pd
import plotly.express as px
import dash_core_components as dcc
from forex_python.converter import CurrencyRates

c = CurrencyRates()
rates = c.get_rates('GBP')
rates.update({'GBp': 100.0})

with open("assets/sector_tree.pkl", "rb") as f:
    tbic_port = pickle.load(f)

fig = px.treemap(tbic_port, path=['portfolio', 'gics_sector', 'gics_industry', 'name'],
                     values='value', color='Mth Chg %', color_continuous_scale='thermal',
                     height=700)

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

def stocks_table():
    tbic_port['value'] = tbic_port['quantity'] * tbic_port['close'] / tbic_port['display_currency'].map(rates)
    tbic_port.sort_values(by='value', ascending=False, inplace=True)
    table_data = tbic_port[['ticker', 'name', 'value', 'close', 'gics_sector', 'gics_industry', 'market_cap', 'trailing_pe', 'p/b', 'p/s', 'ebitda', 'revenue', 'currency', 'display_currency', 'pct_change']]
    table_data['value'] = table_data['value'].map('{:,.2f}'.format)
    table_data['market_cap'] = table_data['market_cap']/1000000000
    table_data['market_cap'] = table_data['market_cap'].map('{:,.1f}'.format)
    table_data['close'] = table_data['close'].map('{:,.2f}'.format)
    table_data['trailing_pe'] = table_data['trailing_pe'].map('{:,.2f}'.format)
    table_data['revenue'] = table_data['revenue'] / 1000000
    table_data['revenue'] = table_data['revenue'].map('{:,.0f}'.format)
    table_data['ebitda'] = table_data['ebitda'] / 1000000
    table_data['ebitda'] = table_data['ebitda'].map('{:,.0f}'.format)
    table_data['pct_change'] = table_data['pct_change']*100
    table_data['pct_change'] = table_data['pct_change'].map('{:,.2f}'.format)
    table_row=[]
    for k, v in table_data.iterrows():
        row = html.Tr([html.A(v['ticker'], href='page-1/' + v['ticker']),
                       html.Td(html.A(v['name'], href='page-2/' + v['ticker'])), html.Td(v['value']), html.Td(str(v['display_currency']) + " " + str(v['close'])),
                       html.Td(v['gics_sector']), html.Td(v['gics_industry']), html.Td(str(v['currency']) + " " + str(v['market_cap'])),
                       html.Td(v['trailing_pe']), html.Td(v['p/b']), html.Td(v['p/s']), html.Td(str(v['currency']) + " " + str(v['ebitda'])),
                       html.Td(str(v['currency']) + " " + str(v['revenue'])),
                       html.Td(v['pct_change'])])

        table_row.append(row)

    table_body = [html.Tbody(table_row)]
    table_header = [
        html.Thead(html.Tr([html.Th('Ticker'), html.Th('Name'), html.Th('£Value'), html.Th('Close'), html.Th('Sector'),
                            html.Th('Industry'), html.Th('Mkt Cap (Bn)'), html.Th('P/E'),
                            html.Th('P/B'), html.Th('P/S'), html.Th('Earnings (MM)'), html.Th('Revenue (MM)'), html.Th('30d change %')], style={'className': 'Dark'}))
        ]
    #table_data = table_data.style.format('{:,}')
    table = dbc.Table(table_header + table_body, size='sm', striped=True, bordered=True, hover=True, style = {
                'font_family': 'cursive',
                'font_size': '12px',
                'text_align': 'center'
            })
    return table
layout = html.Div([
            dbc.Spinner(dcc.Graph(figure=fig),
                    color="primary", type="border", fullscreen=True,
                    spinner_style={"width": "20rem", "height": "20rem"}),
            dbc.Row([
                dbc.Col(html.Div(), width=1),
                dbc.Col(html.Div(stocks_table()), width=10),
                dbc.Col(html.Div(), width=1),
            ])
])