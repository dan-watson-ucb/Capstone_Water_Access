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
import urllib


#get rid of lat lon from the table - moved to the back
#predictions yes no instead of 0's and 1's
#color code based on today's prediction - done
#table columns - order - done
#Status_id should not be used - use status_binary

#function for colors
def color_col(x):
    if x == "yes":
        return "rgb(0,255,0)"
    if x == "no":
        return "rgb(255,0,0)"
    if x == "unknown":
        return "rgb(255, 153, 51)"

def color_col_pred(x):
    if x == "Not Working":
        return "rgb(255,0,0)"
    if x == "Working":
        return "rgb(0,255,0)"



## Connect and pull initial df
conn = psycopg2.connect("dbname='water_db' user='dan' host='postgres-instance2.clhlqrsuvowr.us-east-1.rds.amazonaws.com' password='berkeley'")
query = "SELECT country_name, district, sub_district, status_id, fuzzy_water_source, fuzzy_water_tech, management, CASE WHEN today_preds = 1 THEN 'Not Working' ELSE 'Working' end as today_preds_text, CASE WHEN one_year_preds = 1 THEN 'Not Working' ELSE 'Working' end as one_year_preds_text, one_km_population, lat_deg, lon_deg from final_all WHERE country_name = 'Sierra Leone'"
df_init = pd.read_sql_query(query, conn)
df = pd.read_sql_query(query, conn)
conn.close()
mapbox_access_token = 'pk.eyJ1IjoiZHdhdHNvbjgyOCIsImEiOiJjamVycHp0b3cxY2dyMnhsdGc4eHBkcW85In0.uGPxMK4_u-nAs_J74yw70A'

## query for countries, districts, subdistricts
conn = psycopg2.connect("dbname='water_db' user='dan' host='postgres-instance2.clhlqrsuvowr.us-east-1.rds.amazonaws.com' password='berkeley'")
q2 = "SELECT country_name, district, sub_district, status_id, fuzzy_water_tech, fuzzy_water_source, management, today_preds_text,one_year_preds_text, one_km_population from final"
df2 = pd.read_sql_query(q2, conn)
conn.close()
### Color Scale



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
        columns=dataframe.columns,

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
        dcc.Dropdown(id = 'today-pred-select',
            options=[
             {'label': i, 'value': i} for i in df_init.today_preds_text.sort_values().unique()],
             placeholder = "Select Today's Prediction",
             multi = True       
        ),
        ], style = {"padding":"5px"}),
        html.Div([
        dcc.Dropdown(id = 'one-year-pred-select',
            options=[
             {'label': i, 'value': i} for i in df_init.one_year_preds_text.sort_values().unique()],
             placeholder = "Select One year Prediction",
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
                    "text": df_init.today_preds_text,
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
    html.H6(children = "", id = "well_text"),
    html.Div([
        generate_table(df)
        ], className="col-md-12", style = {"font-size":"small"}),
    html.A(
        'Download Data',
        id='download-link',
        download="rawdata.csv",
        href="",
        target="_blank"
    )

], className="container-fluid row")



## Update graph with query from filters above
@app.callback(Output('output-graph', 'figure'), [Input('submit-button', 'n_clicks')], state= [State('country-select', 'value'),
 State('status-select', 'value'), State('district-select', 'value'), State('sub-district-select', 'value'), State('watersource-select', 'value'), State('watertech-select', 'value'),
 State('management-select', 'value'), State('today-pred-select', 'value'), State('one-year-pred-select', 'value')])
def run_query(n_clicks, country, status, district, sub_district, fuzzy_water_source, fuzzy_water_tech, management, today_preds_text, one_year_preds_text):
    conn = psycopg2.connect("dbname='water_db' user='dan' host='postgres-instance2.clhlqrsuvowr.us-east-1.rds.amazonaws.com' password='berkeley'")
    clause = [status, district, sub_district, fuzzy_water_source, fuzzy_water_tech, management, today_preds_text, one_year_preds_text]
    base_query = "SELECT lat_deg, lon_deg, status_id, today_preds_text from final WHERE country_name =" + "'" + str(country) + "'"


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

    if not clause[6]:
        pass
    else:
        base_query = base_query +" and today_preds_text in (" + ', '.join("'" + i + "'" for i in today_preds_text) + ")"

    if not clause[7]:
        pass
    else:
        base_query = base_query +" and one_year_preds_text in (" + ', '.join("'" + i + "'" for i in one_year_preds_text) + ")"


    df = pd.read_sql_query(base_query, conn)
    df["color"] = df["today_preds_text"].apply(color_col_pred)
    conn.close()
    mapbox_access_token = 'pk.eyJ1IjoiZHdhdHNvbjgyOCIsImEiOiJjamVycHp0b3cxY2dyMnhsdGc4eHBkcW85In0.uGPxMK4_u-nAs_J74yw70A'
    figure = { "data": [
                {
                    "type": "scattermapbox",
                    "lat": df.lat_deg,
                    "lon": df.lon_deg,
                    "text": df.today_preds_text,

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

## Update table with query from filters above
@app.callback(Output('filter-table', 'rows'), [Input('submit-button', 'n_clicks')], state= [State('country-select', 'value'),
 State('status-select', 'value'), State('district-select', 'value'), State('sub-district-select', 'value'), State('watersource-select', 'value'), State('watertech-select', 'value'),
 State('management-select', 'value'), State('today-pred-select', 'value'), State('one-year-pred-select', 'value')])
def run_query(n_clicks, country, status, district, sub_district, fuzzy_water_source, fuzzy_water_tech, management, today_preds_text, one_year_preds_text):
    conn = psycopg2.connect("dbname='water_db' user='dan' host='postgres-instance2.clhlqrsuvowr.us-east-1.rds.amazonaws.com' password='berkeley'")
    clause = [status, district, sub_district, fuzzy_water_source, fuzzy_water_tech, management, today_preds_text, one_year_preds_text]
    base_query = "SELECT country_name, district, sub_district, status_id, fuzzy_water_source, fuzzy_water_tech, management, CASE WHEN today_preds = 1 THEN 'Not Working' ELSE 'Working' end as today_preds_text, CASE WHEN one_year_preds = 1 THEN 'Not Working' ELSE 'Working' end as one_year_preds_text, one_km_population, lat_deg, lon_deg from final_all WHERE country_name =" + "'" + str(country) + "'"


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

    if not clause[6]:
        pass
    else:
        base_query = base_query +" and today_preds_text in (" + ', '.join("'" + i + "'" for i in today_preds_text) + ")"

    if not clause[7]:
        pass
    else:
        base_query = base_query +" and one_year_preds_text in (" + ', '.join("'" + i + "'" for i in one_year_preds_text) + ")"


    df = pd.read_sql_query(base_query, conn)
    conn.close()
    df["color"] = df["today_preds_text"].apply(color_col_pred)
    return df.to_dict('records')

## Update well_text for number of water points
@app.callback(Output("well_text", 'children'), [Input('filter-table', 'rows')])
def update_well_text(rows):
    return "Filters matched {} results".format(str(len(rows)))

##update districts menu
@app.callback(Output('district-select', 'options'), [Input('country-select', 'value')])
def update_district(country):
    #return[{'label': i, 'value': i} for i in df2.district[df2.country_name== country_name].sort_values().unique()]
    return[{'label': i, 'value': i} for i in df2[df2.country_name== country].district.sort_values().unique()]


##making sure that we clear input if country is none
@app.callback(Output('district-select', 'value'), [Input('country-select', 'value')])
def update_district(country):
    if country is None:
        return None

#update sub-districts menu- tried to do this like the above example but got errors- think it becomes somewhat circular?
@app.callback(Output('sub-district-select', 'options'), [Input('district-select', 'value'), Input('country-select', 'value')])
def update_subdistrict(district_name, country):
     return[{'label': i, 'value': i} for i in df2[df2.country_name == country][df2.district.isin(district_name)].sub_district.sort_values().unique()]

##making sure that we clear input if country is none
@app.callback(Output('sub-district-select', 'value'), [Input('district-select', 'value'), Input('country-select', 'value')])
def update_subdistrict(district_name, country):
    if district_name is None:
        return None

@app.callback(Output('status-select', 'options'), [Input('district-select', 'value'), Input('country-select', 'value'), Input('sub-district-select', 'value')])
def update_status(district_name, country, sub_district):
    return[{'label': i, 'value': i} for i in df2[df2.country_name == country][df2.district.isin(district_name)]\
    [df2.sub_district.isin(sub_district)].status_id.sort_values().unique()]#check this

#clearing
@app.callback(Output('status-select', 'value'), [Input('district-select', 'value'), Input('country-select', 'value'), Input('sub-district-select', 'value')])
def update_status(district_name, country, sub_district):
    if district_name is None:
        return None
    if sub_district is None:
        return None

    
@app.callback(Output('watersource-select', 'options'), [Input('district-select', 'value'), Input('country-select', 'value'), Input('sub-district-select', 'value'), Input('status-select', 'value')])
def update_watersource(district_name, country, sub_district, status_id):
    return[{'label': i, 'value': i} for i in df2[df2.country_name == country][df2.district.isin(district_name)]\
     [df2.sub_district.isin(sub_district)][df2.status_id.isin(status_id)].fuzzy_water_source.sort_values().unique()]

#clearing
@app.callback(Output('watersource-select', 'value'), [Input('district-select', 'value'), Input('country-select', 'value'), Input('sub-district-select', 'value'), Input('status-select', 'value')])
def update_watersource(district_name, country, sub_district, status_id):
    if district_name is None:
        return None
    if sub_district is None:
        return None

@app.callback(Output('watertech-select', 'options'), [Input('district-select', 'value'), Input('country-select', 'value'), Input('sub-district-select', 'value'), Input('status-select', 'value'), Input('watersource-select', 'value')])
def update_watertech(district_name, country, sub_district, status_id, fuzzy_water_source):
     return[{'label': i, 'value': i} for i in df2.fuzzy_water_tech[df2.country_name == country][df2.district.isin(district_name)]\
     [df2.sub_district.isin(sub_district)][df2.status_id.isin(status_id)]\
     [df2.fuzzy_water_source.isin(fuzzy_water_source)].sort_values().unique()]

@app.callback(Output('watertech-select', 'value'), [Input('district-select', 'value'), Input('country-select', 'value'), Input('sub-district-select', 'value'), Input('status-select', 'value'), Input('watersource-select', 'value')])
def update_watertech(district_name, country, sub_district, status_id, fuzzy_water_source):
    if district_name is None:
        return None
    if sub_district is None:
        return None

@app.callback(Output('management-select', 'options'), [Input('district-select', 'value'), Input('country-select', 'value'), Input('sub-district-select', 'value'), Input('status-select', 'value'), Input('watersource-select', 'value'), Input('watertech-select', 'value')])
def update_subdistrict(district_name, country, sub_district,  status_id, fuzzy_water_source, fuzzy_water_tech):
     return[{'label': i, 'value': i} for i in df2.management[df2.country_name == country][df2.district.isin(district_name)]\
     [df2.sub_district.isin(sub_district)][df2.status_id.isin(status_id)]\
     [df2.fuzzy_water_source.isin(fuzzy_water_source)][df2.fuzzy_water_tech.isin(fuzzy_water_tech)].sort_values().unique()]

@app.callback(Output('management-select', 'value'), [Input('district-select', 'value'), Input('country-select', 'value'), Input('sub-district-select', 'value'), Input('status-select', 'value'), Input('watersource-select', 'value'), Input('watertech-select', 'value')])
def update_subdistrict(district_name, country, sub_district,  status_id, fuzzy_water_source, fuzzy_water_tech):
    if district_name is None:
        return None
    if sub_district is None:
        return None


@app.callback(Output('today-pred-select', 'options'), [Input('district-select', 'value'), Input('country-select', 'value'), Input('sub-district-select', 'value'), Input('status-select', 'value'), Input('watersource-select', 'value'), Input('watertech-select', 'value'), Input('management-select', 'value')])
def update_today_pred(district_name, country, sub_district,  status_id, fuzzy_water_source, fuzzy_water_tech, management):
     return[{'label': i, 'value': i} for i in df2.today_preds_text[df2.country_name == country][df2.district.isin(district_name)]\
     [df2.sub_district.isin(sub_district)][df2.status_id.isin(status_id)]\
     [df2.fuzzy_water_source.isin(fuzzy_water_source)][df2.fuzzy_water_tech.isin(fuzzy_water_tech)][df2.management.isin(management)].sort_values().unique()]

@app.callback(Output('today-pred-select', 'value'), [Input('district-select', 'value'), Input('country-select', 'value'), Input('sub-district-select', 'value'), Input('status-select', 'value'), Input('watersource-select', 'value'), Input('watertech-select', 'value'), Input('management-select', 'value')])
def update_today_pred(district_name, country, sub_district,  status_id, fuzzy_water_source, fuzzy_water_tech, management):
    if sub_district is None:
        return None

@app.callback(Output('one-year-pred-select', 'options'), [Input('district-select', 'value'), Input('country-select', 'value'), Input('sub-district-select', 'value'), Input('status-select', 'value'), Input('watersource-select', 'value'), Input('watertech-select', 'value'), Input('management-select', 'value'), Input('today-pred-select', 'value')])
def update_one_year_pred(district_name, country, sub_district,  status_id, fuzzy_water_source, fuzzy_water_tech, management, today_preds_text):
     return[{'label': i, 'value': i} for i in df2.one_year_preds_text[df2.country_name == country][df2.district.isin(district_name)]\
     [df2.sub_district.isin(sub_district)][df2.status_id.isin(status_id)]\
     [df2.fuzzy_water_source.isin(fuzzy_water_source)][df2.fuzzy_water_tech.isin(fuzzy_water_tech)][df2.management.isin(management)][df2.today_preds_text.isin(today_preds_text)].sort_values().unique()]

@app.callback(Output('one-year-pred-select', 'value'), [Input('district-select', 'value'), Input('country-select', 'value'), Input('sub-district-select', 'value'), Input('status-select', 'value'), Input('watersource-select', 'value'), Input('watertech-select', 'value'), Input('management-select', 'value'), Input('today-pred-select', 'value')])
def update_one_year_pred(district_name, country, sub_district,  status_id, fuzzy_water_source, fuzzy_water_tech, management, one_year_preds_text):
    if sub_district is None:
        return None

# @app.callback(
#     dash.dependencies.Output('download-link', 'href'),
#     [dash.dependencies.Input('datatable-gapminder', 'selected_row_indices')])
# def update_download_link(selected_row_indices):
#     dff = filter_data(selected_row_indices)
#     csv_string = dff.to_csv(index=False, encoding='utf-8')
#     csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
#     return csv_string

@app.callback(Output('download-link', 'href'), [Input('submit-button', 'n_clicks')], state= [State('country-select', 'value'),
 State('status-select', 'value'), State('district-select', 'value'), State('sub-district-select', 'value'), State('watersource-select', 'value'), State('watertech-select', 'value'),
 State('management-select', 'value'), State('today-pred-select', 'value'), State('one-year-pred-select', 'value')])
def run_query(n_clicks, country, status, district, sub_district, fuzzy_water_source, fuzzy_water_tech, management, today_preds_text, one_year_preds_text):
    conn = psycopg2.connect("dbname='water_db' user='dan' host='postgres-instance2.clhlqrsuvowr.us-east-1.rds.amazonaws.com' password='berkeley'")
    clause = [status, district, sub_district, fuzzy_water_source, fuzzy_water_tech, management, today_preds_text, one_year_preds_text]
    base_query = "SELECT country_name, district, sub_district, status_id, fuzzy_water_source, fuzzy_water_tech, management, CASE WHEN today_preds = 1 THEN 'Not Working' ELSE 'Working' end as today_preds_text, CASE WHEN one_year_preds = 1 THEN 'Not Working' ELSE 'Working' end as one_year_preds_text, one_km_population, lat_deg, lon_deg from final_all WHERE country_name =" + "'" + str(country) + "'"


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

    if not clause[6]:
        pass
    else:
        base_query = base_query +" and today_preds_text in (" + ', '.join("'" + i + "'" for i in today_preds_text) + ")"

    if not clause[7]:
        pass
    else:
        base_query = base_query +" and one_year_preds_text in (" + ', '.join("'" + i + "'" for i in one_year_preds_text) + ")"


    df = pd.read_sql_query(base_query, conn)
    conn.close()
    df["color"] = df["today_preds_text"].apply(color_col_pred)
    csv_string = df.to_csv(index=False, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8," + urllib.quote(csv_string)

    return csv_string

if __name__ == '__main__':
    app.run_server(debug=True)