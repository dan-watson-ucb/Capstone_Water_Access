import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas_datareader.data as web
import datetime as dt


app = dash.Dash()

app.layout= html.Div(children = [

	html.Div(children = '''
		symbol to graph:
		'''),

	dcc.Input(id = 'input', value = '', type= 'text'),
	dcc.RangeSlider(),

	html.Div(id = 'output-graph')	
	])


@app.callback(
	Output(component_id = 'output-graph', component_property='children'),
	[Input(component_id = 'input', component_property='value')]
	)
def update_graph(input_data):
	start = dt.datetime(2015,1,1)
	end = dt.datetime.now()
	df= web.DataReader(input_data.upper(), 'quandl', start, end)

	return dcc.Graph(
		id = 'stock-chart',
		figure= {
		'data':[
		{'x': df.index, 'y': df.Close, 'type': 'line', 'name':input_data.upper()}
		],
		'layout': {
			'title': "Stock Chart for {} from {} to {}".format(input_data.upper(), start, end)
		}
		})



if __name__ == '__main__':
	app.run_server(debug=True)