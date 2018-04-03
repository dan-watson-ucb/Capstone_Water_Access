import dash
import dash_core_components as dcc
import dash_html_components as html
import datetime
from collections import deque
import plotly.graph_objs as go
import psycopg2
import pandas as pd
from dash.dependencies import Output, Event, Input, State
import dash_table_experiments as dt

## Connect and pull initial df
conn = psycopg2.connect("dbname='water_db' user='dan' host='postgres-instance2.clhlqrsuvowr.us-east-1.rds.amazonaws.com' password='berkeley'")
query = "SELECT lat_deg, lon_deg, status_id, district, sub_district, country_name, fuzzy_water_source, fuzzy_water_tech, management from final_all WHERE country_name = 'Sierra Leone'"
df_init = pd.read_sql_query(query, conn)
df = pd.read_sql_query(query, conn)
conn.close()
mapbox_access_token = 'pk.eyJ1IjoiZHdhdHNvbjgyOCIsImEiOiJjamVycHp0b3cxY2dyMnhsdGc4eHBkcW85In0.uGPxMK4_u-nAs_J74yw70A'

## query for countries, districts, subdistricts
conn = psycopg2.connect("dbname='water_db' user='dan' host='postgres-instance2.clhlqrsuvowr.us-east-1.rds.amazonaws.com' password='berkeley'")
q2 = "SELECT country_name, district, sub_district, status_id, fuzzy_water_tech, fuzzy_water_source, management from final_all"
df2 = pd.read_sql_query(q2, conn)
conn.close()
### Color Scale

#function for colors
def color_col(x):
    if x == "yes":
        return "rgb(0,255,0)"
    if x == "no":
        return "rgb(255,0,0)"
    if x == "unknown":
        return "rgb(255, 153, 51)"

## insertion point for css and js
external_css = [
    'https://codepen.io/chriddp/pen/bWLwgp.css',
    'https://api.tiles.mapbox.com/mapbox-gl-js/v0.44.1/mapbox-gl.css',
    'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css'
]

external_js = [
    'https://api.tiles.mapbox.com/mapbox-gl-js/v0.44.1/mapbox-gl.js',
    'https://code.jquery.com/jquery-3.2.1.slim.min.js',
    'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js',
    'https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js'
]

def generate_table(dataframe):
    return dt.DataTable(
        id='filter-table',
        rows=dataframe.to_dict('records'),

        # optional - sets the order of columns
        columns=sorted(dataframe.columns),

        row_selectable=True,
        filterable=True,
        sortable=True,
        selected_row_indices=[],
    )


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
        html.H1("Water Map", className="text-center", style = {'width':'100%'}),
        ], style = {'textAlign':'center'}, className="col-md-12 row"),
        # Row: Title
        html.Div([
        # Row: Map
        html.Div([
        dcc.Dropdown(className = "dropdown", id = 'country-select',
            options=[
             {'label': i, 'value': i} for i in df2.country_name.sort_values().unique()],
             #value = df2.country_name."sort_values().unique()[0], 
             placeholder = "Select a Country",     
        ),
        ], style = {"padding":"5px"}),
        html.Div([
        dcc.Dropdown(id = 'district-select',
            options = [
            #This will have to be updated based on country- need master table
            {'label': i, 'value': i} for i in df_init.district.sort_values().unique()],
            #value = df_init['district'].sort_values().unique()[0:2],
            placeholder = 'Select a District',
            multi= True
        ),
        ], style = {"padding":"5px"}),
        html.Div([
        dcc.Dropdown(id = 'sub-district-select',
            options = [
            {'label': i, 'value': i} for i in df_init.sub_district.sort_values().unique()],
            placeholder = 'Select a Sub-District',
            multi = True
        ),
        ], style = {"padding":"5px"}),
        html.Div([
        dcc.Dropdown(id = 'status-select',
            options = [
            {'label': i, 'value': i} for i in df_init.status_id.sort_values().unique()],
            # options = [
            # {'label': 'Working' , 'value': 'yes'},
            # {'label': 'Not Working' , 'value': 'no'},
            # {'label': 'Unknown' , 'value': 'unknown'}
            # ],
            #value =['no', 'yes'],
            placeholder = "Last known status",
            multi = True
        ),
        ], style = {"padding":"5px"}),
        #fix to update only to available
        html.Div([
        dcc.Dropdown(id = 'watersource-select',
            options=[
             {'label': i, 'value': i} for i in df_init.fuzzy_water_source.sort_values().unique()],
             #value = df_init.fuzzy_water_source.sort_values().unique()[0:2], 
             placeholder = "Select a Water Source",
             multi= True       
        ),
        ], style = {"padding":"5px"}),
        #fix to update only to available
        html.Div([
        dcc.Dropdown(id = 'watertech-select',
            options=[
             {'label': i, 'value': i} for i in df_init.fuzzy_water_tech.sort_values().unique()],
             #value = df_init.fuzzy_water_tech.sort_values().unique()[0:2], 
             placeholder = "Select a Water Tech",
             multi = True       
        ),
        ], style = {"padding":"5px"}),
        #Fix to update only to available
        html.Div([
        dcc.Dropdown(id = 'management-select',
            options=[
             {'label': i, 'value': i} for i in df_init.management.sort_values().unique()],
             #value =  df_init.management.sort_values().unique()[0:2],
             placeholder = "Select Water Point Management",
             multi = True       
        ),
        ], style = {"padding":"5px"}),
        html.Div([
        html.Button('submit', id= 'submit-button'),
        ], style = {"padding":"5px"}),
        ], className="col-md-4"),
    html.Div([
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
                        "opacity": 1.0,
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
    ], className="col-md-8", style = {'border':'1px solid black'}),
    html.Div([
        generate_table(df)
        ], className="col-md-12", style = {"font-size":"small"}),

], className="container-fluid row")



## Update graph with query from filters above
@app.callback(Output('output-graph', 'figure'), [Input('submit-button', 'n_clicks')], state= [State('country-select', 'value'),
 State('status-select', 'value'), State('district-select', 'value'), State('sub-district-select', 'value'), State('watersource-select', 'value'), State('watertech-select', 'value'),
 State('management-select', 'value')])
def run_query(n_clicks, country, status, district, sub_district, fuzzy_water_source, fuzzy_water_tech, management):
    conn = psycopg2.connect("dbname='water_db' user='dan' host='postgres-instance2.clhlqrsuvowr.us-east-1.rds.amazonaws.com' password='berkeley'")
    clause = [status, district, sub_district, fuzzy_water_source, fuzzy_water_tech, management]
    base_query = "SELECT lat_deg, lon_deg, status_id from final_all WHERE country_name =" + "'" + str(country) + "'"


    if not clause[0]:
        pass
    else:
        base_query = base_query + " and status_id in (" + ', '.join("'" + i + "'" for i in status) + ")"

    if not clause[1]:
        pass
    else:
        base_query = base_query +" and district in (" + ', '.join("'" + i + "'" for i in district) + ")"

    if not clause[2]:
        pass
    else:
        base_query = base_query +" and sub_district in (" + ', '.join("'" + i + "'" for i in sub_district) + ")"

    if not clause[3]:
        pass
    else:
        base_query = base_query +" and fuzzy_water_source in (" + ', '.join("'" + i + "'" for i in fuzzy_water_source) + ")"

    if not clause[4]:
        pass
    else:
        base_query = base_query +" and fuzzy_water_tech in (" + ', '.join("'" + i + "'" for i in fuzzy_water_tech) + ")"

    if not clause[5]:
        pass
    else:
        base_query = base_query +" and management in (" + ', '.join("'" + i + "'" for i in management) + ")"


    df = pd.read_sql_query(base_query, conn)
    df["color"] = df["status_id"].apply(color_col)
    conn.close()
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
                        "opacity": .8,
                        "color" : df['color']                        
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

## Update graph with query from filters above
@app.callback(Output('filter-table', 'rows'), [Input('submit-button', 'n_clicks')], state= [State('country-select', 'value'),
 State('status-select', 'value'), State('district-select', 'value'), State('sub-district-select', 'value'), State('watersource-select', 'value'), State('watertech-select', 'value'),
 State('management-select', 'value')])
def run_query(n_clicks, country, status, district, sub_district, fuzzy_water_source, fuzzy_water_tech, management):
    conn = psycopg2.connect("dbname='water_db' user='dan' host='postgres-instance2.clhlqrsuvowr.us-east-1.rds.amazonaws.com' password='berkeley'")
    clause = [status, district, sub_district, fuzzy_water_source, fuzzy_water_tech, management]
    base_query = "SELECT lat_deg, lon_deg, status_id, district, sub_district, country_name, fuzzy_water_source, fuzzy_water_tech, management from final_all WHERE country_name =" + "'" + str(country) + "'"


    if not clause[0]:
        pass
    else:
        base_query = base_query + " and status_id in (" + ', '.join("'" + i + "'" for i in status) + ")"

    if not clause[1]:
        pass
    else:
        base_query = base_query +" and district in (" + ', '.join("'" + i + "'" for i in district) + ")"

    if not clause[2]:
        pass
    else:
        base_query = base_query +" and sub_district in (" + ', '.join("'" + i + "'" for i in sub_district) + ")"

    if not clause[3]:
        pass
    else:
        base_query = base_query +" and fuzzy_water_source in (" + ', '.join("'" + i + "'" for i in fuzzy_water_source) + ")"

    if not clause[4]:
        pass
    else:
        base_query = base_query +" and fuzzy_water_tech in (" + ', '.join("'" + i + "'" for i in fuzzy_water_tech) + ")"

    if not clause[5]:
        pass
    else:
        base_query = base_query +" and management in (" + ', '.join("'" + i + "'" for i in management) + ")"


    df = pd.read_sql_query(base_query, conn)
    conn.close()
    df["color"] = df["status_id"].apply(color_col)
    return df.to_dict('records')

##update districts menu
@app.callback(Output('district-select', 'options'), [Input('country-select', 'value')])
def update_district(country):
    #return[{'label': i, 'value': i} for i in df2.district[df2.country_name== country_name].sort_values().unique()]
    return[{'label': i, 'value': i} for i in df2[df2.country_name== country].district.sort_values().unique()]

#update sub-districts menu- tried to do this like the above example but got errors- think it becomes somewhat circular?
@app.callback(Output('sub-district-select', 'options'), [Input('district-select', 'value'), Input('country-select', 'value')])
def update_subdistrict(district_name, country):
     return[{'label': i, 'value': i} for i in df2[df2.country_name == country][df2.district.isin(district_name)].sub_district.sort_values().unique()]
    
@app.callback(Output('status-select', 'options'), [Input('district-select', 'value'), Input('country-select', 'value'), Input('sub-district-select', 'value')])
def update_status(district_name, country, sub_district):
    return[{'label': i, 'value': i} for i in df2[df2.country_name == country][df2.district.isin(district_name)]\
    [df2.sub_district.isin(sub_district)].status_id.sort_values().unique()]#check this
    
@app.callback(Output('watersource-select', 'options'), [Input('district-select', 'value'), Input('country-select', 'value'), Input('sub-district-select', 'value'), Input('status-select', 'value')])
def update_watersource(district_name, country, sub_district, status_id):
    return[{'label': i, 'value': i} for i in df2[df2.country_name == country][df2.district.isin(district_name)]\
     [df2.sub_district.isin(sub_district)][df2.status_id.isin(status_id)].fuzzy_water_source.sort_values().unique()]

@app.callback(Output('watertech-select', 'options'), [Input('district-select', 'value'), Input('country-select', 'value'), Input('sub-district-select', 'value'), Input('status-select', 'value'), Input('watersource-select', 'value')])
def update_watertech(district_name, country, sub_district, status_id, fuzzy_water_source):
     return[{'label': i, 'value': i} for i in df2.fuzzy_water_tech[df2.country_name == country][df2.district.isin(district_name)]\
     [df2.sub_district.isin(sub_district)][df2.status_id.isin(status_id)]\
     [df2.fuzzy_water_source.isin(fuzzy_water_source)].sort_values().unique()]

@app.callback(Output('management-select', 'options'), [Input('district-select', 'value'), Input('country-select', 'value'), Input('sub-district-select', 'value'), Input('status-select', 'value'), Input('watersource-select', 'value'), Input('watertech-select', 'value')])
def update_subdistrict(district_name, country, sub_district,  status_id, fuzzy_water_source, fuzzy_water_tech):
     return[{'label': i, 'value': i} for i in df2.management[df2.country_name == country][df2.district.isin(district_name)]\
     [df2.sub_district.isin(sub_district)][df2.status_id.isin(status_id)]\
     [df2.fuzzy_water_source.isin(fuzzy_water_source)][df2.fuzzy_water_tech.isin(fuzzy_water_tech)].sort_values().unique()]



if __name__ == '__main__':
    app.run_server(debug=True)



