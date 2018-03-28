import dash
import dash_core_components as dcc
import dash_html_components as html
import datetime
from collections import deque
import plotly.graph_objs as go
import psycopg2
import pandas as pd
from dash.dependencies import Output, Event, Input, State

conn = psycopg2.connect("dbname='water_db' user='dan' host='postgres-instance2.clhlqrsuvowr.us-east-1.rds.amazonaws.com' password='berkeley'")
query = "SELECT lat_deg, lon_deg, status_id from water_django WHERE country_name = 'Ethiopia'"
df = pd.read_sql_query(query, conn)
mapbox_access_token = 'pk.eyJ1IjoiZHdhdHNvbjgyOCIsImEiOiJjamVycHp0b3cxY2dyMnhsdGc4eHBkcW85In0.uGPxMK4_u-nAs_J74yw70A'

q2 = "SELECT distinct(country_name) from water_django"
df2 = pd.read_sql_query(q2, conn)

external_css = [
    'https://codepen.io/chriddp/pen/bWLwgp.css',
    'https://api.tiles.mapbox.com/mapbox-gl-js/v0.44.1/mapbox-gl.css'
]

external_js = [
    'https://api.tiles.mapbox.com/mapbox-gl-js/v0.44.1/mapbox-gl.js'
]




app = dash.Dash()
app.title = "water site"
for js in external_js:
    app.scripts.append_script({'external_url': js})

for css in external_css:
    app.css.append_css({'external_url': css})

app.layout = html.Div([
    # Column: Title + Map
    html.Div([
        # Row: Title
        html.Div([
            html.H1("Water Map", className="text-center")
        ], className="row"),
        # Row: Map
        dcc.Dropdown(id = 'country-select',
	    	options=[
	         {'label': i, 'value': i} for i in df2.country_name.sort_values().unique()],
             value = "Ethiopia",		
		),
        dcc.Checklist(id = 'status-select',
            options = [
            {'label': 'Working' , 'value': 'yes'},
            {'label': 'Not Working' , 'value': 'no'},
            {'label': 'Unknown' , 'value': 'unknown'}
            ],
            values =['no'] ),
        html.Button('submit', id= 'submit-button'),
        dcc.Graph(id = "output-graph",
        figure ={"data": [
                {
                    "type": "mapbox-gl-js",
                    "lat": df.lat_deg,
                    "lon": df.lon_deg,
                    "text": df.status_id,
                    "cluster": True,
                    "mode": "markers",
                    "marker": {
                        "size": 8,
                        "opacity": 1.0
                    }
                }
            ],
        "layout": {
            "autosize": True,
            "hovermode": "closest",
            "mapbox": {
                "accesstoken": mapbox_access_token,
                "center": {
                    "lat": df.lat_deg.mean(),
                    "lon": df.lon_deg.mean()
                },
                "cluster": True,
                "pitch": 0,
                "zoom": 3,
                "style": "outdoors"
            }
        }
    })
    ], className="col-md-12"),

], className="container-fluid")




@app.callback(Output('output-graph', 'figure'), [Input('submit-button', 'n_clicks')], state= [State('country-select', 'value'),
 State('status-select', 'values')])
def run_query(n_clicks, country, status):
	conn = psycopg2.connect("dbname='water_db' user='dan' host='postgres-instance2.clhlqrsuvowr.us-east-1.rds.amazonaws.com' password='berkeley'")
	query = "SELECT lat_deg, lon_deg, status_id from water_django WHERE country_name = '{}' and status_id in ({})".format(country, ', '.join("'" + i + "'" for i in status))
	df = pd.read_sql_query(query, conn)
	mapbox_access_token = 'pk.eyJ1IjoiZHdhdHNvbjgyOCIsImEiOiJjamVycHp0b3cxY2dyMnhsdGc4eHBkcW85In0.uGPxMK4_u-nAs_J74yw70A'
	figure = { "data": [
                {
                    "type": "scattermapbox",
                    "lat": df.lat_deg,
                    "lon": df.lon_deg,
                    "text": df.status_id,

                    "mode": "markers",
                    "marker": {
                        "size": 8,
                        "opacity": 1.0
                    }
                }
            ],
        "layout": {
            "autosize": True,
            "hovermode": "closest",
            "mapbox": {
                "accesstoken": mapbox_access_token,
                "center": {
                    "lat": df.lat_deg.mean(),
                    "lon": df.lon_deg.mean()
                },
                "pitch": 0,
                "zoom": 3,
                "style": "outdoors",
                "cluster": True,
            }
        }
    }
        return figure




if __name__ == '__main__':
    app.run_server(debug=True)
