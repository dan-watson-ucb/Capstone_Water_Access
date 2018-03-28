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
query = "SELECT lat_deg, lon_deg, status_id, district, country_name, fuzzy_water_source, fuzzy_water_tech, management from final_all WHERE country_name = 'Sierra Leone'"
df_init = pd.read_sql_query(query, conn)
mapbox_access_token = 'pk.eyJ1IjoiZHdhdHNvbjgyOCIsImEiOiJjamVycHp0b3cxY2dyMnhsdGc4eHBkcW85In0.uGPxMK4_u-nAs_J74yw70A'

q2 = "SELECT distinct(country_name) from final_all"
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
             value = df2.country_name.sort_values().unique()[0], 
             placeholder = "Select a Country"       
        ),
        dcc.Dropdown(id = 'district-select',
            options = [
            #This will have to be updated based on country- need master table
            {'label': i, 'value': i} for i in df_init.district.sort_values().unique()],
            value = df_init['district'].sort_values().unique()[0:2],
            placeholder = 'Select a District',
            multi= True
        ),
        ##We can add sub-district here, but need to add another layer of callback
        # dcc.Dropdown(id = 'sub-district-select',
        #     options = [
        #     #This will have to be updated based on country- need master table
        #     {'label': i, 'value': i} for i in df_init.sub_district.sort_values().unique()],
        #     placeholder = 'Select a Sub-District'
        # ),
        dcc.Dropdown(id = 'status-select',
            options = [
            {'label': 'Working' , 'value': 'yes'},
            {'label': 'Not Working' , 'value': 'no'},
            {'label': 'Unknown' , 'value': 'unknown'}
            ],
            value =['no', 'yes'],
            placeholder = "Last known status",
            multi = True
        ),
        #fix to update only to available
        dcc.Dropdown(id = 'watersource-select',
            options=[
             {'label': i, 'value': i} for i in df_init.fuzzy_water_source.sort_values().unique()],
             value = df_init.fuzzy_water_source.sort_values().unique()[0:2], 
             placeholder = "Select a Water Source",
             multi= True       
        ),
        #fix to update only to available
        dcc.Dropdown(id = 'watertech-select',
            options=[
             {'label': i, 'value': i} for i in df_init.fuzzy_water_tech.sort_values().unique()],
             value = df_init.fuzzy_water_tech.sort_values().unique()[0:2], 
             placeholder = "Select a Water Tech",
             multi = True       
        ),
        #Fix to update only to available
        dcc.Dropdown(id = 'management-select',
            options=[
             {'label': i, 'value': i} for i in df_init.management.sort_values().unique()],
             value =  df_init.management.sort_values().unique()[0:2],
             placeholder = "Select Water Point Management",
             multi = True       
        ),


        html.Button('submit', id= 'submit-button'),
        dcc.Graph(id = "output-graph",
        figure ={"data": [
                {
                    "type": "mapbox-gl-js",
                    "lat": df_init.lat_deg,
                    "lon": df_init.lon_deg,
                    "text": df_init.status_id,
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
                    "lat": df_init.lat_deg.mean(),
                    "lon": df_init.lon_deg.mean()
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
 State('status-select', 'value'), State('district-select', 'value'), State('watersource-select', 'value'), State('watertech-select', 'value'),
 State('management-select', 'value')])
def run_query(n_clicks, country, status, district, fuzzy_water_source, fuzzy_water_tech, management):
    conn = psycopg2.connect("dbname='water_db' user='dan' host='postgres-instance2.clhlqrsuvowr.us-east-1.rds.amazonaws.com' password='berkeley'")
    query = "SELECT lat_deg, lon_deg, status_id from final_all WHERE \
    country_name = '{}' and \
    status_id in ({}) and \
    district in ({}) and \
    fuzzy_water_source in ({}) and \
    fuzzy_water_tech in ({}) and \
    management in ({})".format(country, \
        ', '.join("'" + i + "'" for i in status),\
        ', '.join("'" + i + "'" for i in district), \
        ', '.join("'" + i + "'" for i in fuzzy_water_source),\
        ', '.join("'" + i + "'" for i in fuzzy_water_tech),\
        ', '.join("'" + i + "'" for i in management))
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
