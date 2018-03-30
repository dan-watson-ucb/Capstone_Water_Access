import dash
import dash_core_components as dcc
import dash_html_components as html
import datetime
from collections import deque
import plotly.graph_objs as go
import psycopg2
import pandas as pd
from dash.dependencies import Output, Event, Input, State

## Connect and pull initial df
conn = psycopg2.connect("dbname='water_db' user='dan' host='postgres-instance2.clhlqrsuvowr.us-east-1.rds.amazonaws.com' password='berkeley'")
query = "SELECT lat_deg, lon_deg, status_id, district, sub_district, country_name, fuzzy_water_source, fuzzy_water_tech, management from final_all WHERE country_name = 'Sierra Leone'"
df_init = pd.read_sql_query(query, conn)
mapbox_access_token = 'pk.eyJ1IjoiZHdhdHNvbjgyOCIsImEiOiJjamVycHp0b3cxY2dyMnhsdGc4eHBkcW85In0.uGPxMK4_u-nAs_J74yw70A'

## query for countries, districts, subdistricts
q2 = "SELECT country_name, district, sub_district from final_all"
df2 = pd.read_sql_query(q2, conn)


## insertion point for css and js
external_css = [
    'https://codepen.io/chriddp/pen/bWLwgp.css',
    'https://api.tiles.mapbox.com/mapbox-gl-js/v0.44.1/mapbox-gl.css'
]

external_js = [
    'https://api.tiles.mapbox.com/mapbox-gl-js/v0.44.1/mapbox-gl.js'
]




app = dash.Dash()
app.title = "water site"
##JS and CSS app integration
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
             #value = df2.country_name.sort_values().unique()[0], 
             placeholder = "Select a Country"       
        ),
        dcc.Dropdown(id = 'district-select',
            options = [
            #This will have to be updated based on country- need master table
            {'label': i, 'value': i} for i in df_init.district.sort_values().unique()],
            #value = df_init['district'].sort_values().unique()[0:2],
            placeholder = 'Select a District',
            multi= True
        ),
        dcc.Dropdown(id = 'sub-district-select',
            options = [
            {'label': i, 'value': i} for i in df_init.sub_district.sort_values().unique()],
            placeholder = 'Select a Sub-District',
            multi = True
        ),
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
                    "lat": (df_init.lat_deg.max()- df_init.lat_deg.min())/2,
                    "lon": (df_init.lon_deg.max()- df_init.lon_deg.min())/2
                },
                "cluster": True,
                "pitch": 0,
                "zoom": 7,
                "style": "outdoors"
            }
        }
    })
    ], className="col-md-12"),

], className="container-fluid")



## Update graph with query from filters above
@app.callback(Output('output-graph', 'figure'), [Input('submit-button', 'n_clicks')], state= [State('country-select', 'value'),
 State('status-select', 'value'), State('district-select', 'value'), State('sub-district-select', 'value'), State('watersource-select', 'value'), State('watertech-select', 'value'),
 State('management-select', 'value')])
def run_query(n_clicks, country, status, district, sub_district, fuzzy_water_source, fuzzy_water_tech, management):
    conn = psycopg2.connect("dbname='water_db' user='dan' host='postgres-instance2.clhlqrsuvowr.us-east-1.rds.amazonaws.com' password='berkeley'")
    query = "SELECT lat_deg, lon_deg, status_id from final_all WHERE \
    country_name = '{}' and \
    status_id in ({}) and \
    district in ({}) and \
    sub_district in ({}) and \
    fuzzy_water_source in ({}) and \
    fuzzy_water_tech in ({}) and \
    management in ({})".format(country, \
        ', '.join("'" + i + "'" for i in status),\
        ', '.join("'" + i + "'" for i in district), \
        ', '.join("'" + i + "'" for i in sub_district), \
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

##update districts menu
@app.callback(Output('district-select', 'options'), [Input('country-select', 'value')])
def update_district(country_name):
    return[{'label': i, 'value': i} for i in df2.district[df2.country_name== country_name].sort_values().unique()]

##update sub-districts menu- tried to do this like the above example but got errors- think it becomes somewhat circular?
@app.callback(Output('sub-district-select', 'options'), [Input('district-select', 'value'), Input('country-select', 'value')])
def update_subdistrict(district_name, country):
    conn = psycopg2.connect("dbname='water_db' user='dan' host='postgres-instance2.clhlqrsuvowr.us-east-1.rds.amazonaws.com' password='berkeley'")
    query = "SELECT distinct(sub_district) from final_all \
    WHERE country_name = '{}' and \
    district in ({})".format(country, \
    ', '.join("'" + i + "'" for i in district_name))
    df_subdistricts = pd.read_sql_query(query, conn)
    return [{'label': i, 'value': i} for i in df_subdistricts.sub_district.sort_values().unique()]   



if __name__ == '__main__':
    app.run_server(debug=True)
