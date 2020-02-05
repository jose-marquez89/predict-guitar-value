# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
from joblib import load

# Imports from this application
from app import app

# 2 column layout. 1st column width = 4/12
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
df = pd.read_csv('data/web-app-guitars.csv')

available_brands = sorted(df['Brand'].unique())
available_models = sorted(df['Model'].unique())
available_colors = sorted(df['Body Color'].unique())
available_materials = sorted(df['Body Material'].unique())
available_btypes = sorted(df['Body Type'].unique())
available_sizes = sorted(df['Size'].unique())
available_countries = sorted(df['Country/Region of Manufacture'].unique())
available_sconfigs = sorted(df['String Configuration'].unique())
available_plines = sorted(df['Product Line'].unique())
orientations = df['Orientation'].unique()
conditions = df['Condition'].unique()

style = {'padding': '1.5em'}

column1 = dbc.Col([
        dcc.Markdown(
            """
            ## **Make a Prediction**
            If a choice doesn't apply to your instrument, select "OTHER"
            from the drop-down list."""
        ),
        
        # TODO: This is where you'll start putting drop downs
        # You need to ask for Model, Body Color, Brand, Body Material
        # Body Type, Size, Country/Region of Manufacture, String Configuration
        # Product Line and Condition. 
        
        # TODO: You also need a model year slider and two radio buttons for orientation
        html.Div([
			dcc.Markdown("###### Select Brand"),
			dcc.Dropdown(
				id='brand-dd', 
				options=[
					{'label': i, 'value': i} for i in available_brands],
			)
		]),
		html.Div([
			dcc.Markdown("###### Select Model"),
			dcc.Dropdown(
				id='model-dd', 
				options=[
					{'label': i, 'value': i} for i in available_models],
			)
		]),
		html.Div([
			dcc.Markdown("###### Select Color"),
			dcc.Dropdown(
				id='color-dd', 
				options=[
					{'label': i, 'value': i} for i in available_colors],
			)
		]),
		html.Div([
			dcc.Markdown("###### Select Material"),
			dcc.Dropdown(
				id='material-dd', 
				options=[
					{'label': i, 'value': i} for i in available_materials],
			)
		]),
		html.Div([
			dcc.Markdown("###### Select Body Type"),
			dcc.Dropdown(
				id='btype-dd', 
				options=[
					{'label': i, 'value': i} for i in available_btypes],
			)
		]),
		html.Div([
			dcc.Markdown("###### Select Size"),
			dcc.Dropdown(
				id='sizes-dd', 
				options=[
					{'label': i, 'value': i} for i in available_sizes],
			)
		]),
	],
	md=3
)

column2 = dbc.Col([
		html.Div([
			dcc.Markdown("###### Select Country of Manufacture"),
			dcc.Dropdown(
				id='country-dd', 
				options=[
					{'label': i, 'value': i} for i in available_countries]
			)
		]),
		html.Div([
			dcc.Markdown("###### Select String Configuration"),
			dcc.Dropdown(
				id='strings-dd', 
				options=[
					{'label': i, 'value': i} for i in available_sconfigs]
			)
		]),
		html.Div([
			dcc.Markdown("###### Select Product Line"),
			dcc.Dropdown(
				id='pline-dd', 
				options=[
					{'label': i, 'value': i} for i in available_plines]
			)
		]),
		html.Div([
			dcc.Markdown("###### Select Orientation"),
			dcc.Dropdown(
				id='orient-dd', 
				options=[
					{'label': i, 'value': i} for i in orientations]
			)
		]),
		html.Div([
			dcc.Markdown("###### Select Condition"),
			dcc.Dropdown(
				id='condition-dd', 
				options=[
					{'label': i, 'value': i} for i in conditions]
			)
		]),
		html.Div([
			dcc.Markdown("###### I Know My Guitar's Manufacturer Part Number:"),
			dcc.RadioItems(
				id='mpn-radio',
				options=[
					{'label': 'Yes', 'value': 'PROVIDED'},
					{'label': 'No', 'value': 'NOT PROVIDED'}],
		        value='NOT PROVIDED',
		        labelStyle={'display': 'inline-block'}
		    )
		]),
		html.Div([
			dcc.Markdown("###### I Know My Guitar's UPC:"),
			dcc.RadioItems(
				id='upc-radio',
				options=[
					{'label': 'Yes', 'value': 'PROVIDED'},
					{'label': 'No', 'value': 'NOT PROVIDED'}],
		        value='NOT PROVIDED',
		        labelStyle={'display': 'inline-block'}
		    ),
		    dcc.Markdown(
				"**Note:** *You can choose totally " +
				"unrealistic items for fun, like a pink Ibanez " +
				"Les Paul with 9 strings. Mouse over the grapth " +
				"to see the selections that affect the outcome.*"
			)
		]),
													   
	],
	md=3
)
column3 = dbc.Col([
		dcc.Markdown("##### Set Approximate Year"),
		dcc.Slider(
			id='year-slide',
			min=1940,
			max=2020,
			step=2,
			value=1940,
			marks={n: f'{n:.0f}'for n in range(1940,2040,10)}
		),
		html.H4(id='prediction-content', style={'fontWeight':'bold'}),
		html.Div(
			dcc.Graph(id='shap-plot')
		)
		
	], 
	md=6
)
@app.callback(
	[Output('prediction-content', 'children'),
	 Output('shap-plot', 'figure')],
	[Input('brand-dd', 'value'),
	 Input('model-dd', 'value'),
	 Input('color-dd', 'value'),
	 Input('material-dd', 'value'),
	 Input('btype-dd', 'value'),
	 Input('sizes-dd', 'value'),
	 Input('country-dd', 'value'),
	 Input('strings-dd', 'value'),
	 Input('pline-dd', 'value'),
	 Input('orient-dd', 'value'),
	 Input('year-slide', 'value'),
	 Input('condition-dd', 'value'),
	 Input('upc-radio', 'value'),
	 Input('mpn-radio', 'value')])
def predict_and_plot(
		brand, model, color, material, btype,
		sizes, country, strings, pline, orient,
		year, condition, upc, mpn):
	# Create prediction
	pred_df = pd.DataFrame(
		columns=['Model', 'MPN', 'Body Color', 'Brand', 'UPC',
				 'Body Material', 'Body Type', 'Model Year',
				 'Size', 'Country/Region of Manufacture', 
				 'String Configuration', 'Orientation', 'Product Line',
				 'Condition'],
		data=[[model, mpn, color, brand, upc, material, btype, year,
			   sizes, country, strings, orient, pline, condition]]
	)
	
	pipeline = load('model/pipeline.joblib')
	y_pred_log = pipeline.predict(pred_df)
	y_pred = np.expm1(y_pred_log)[0]
	
	pred_out = f"Current Value: ${y_pred:,.2f}"
	
	# Derive shap values from user input
	encoder = pipeline.named_steps['ordinalencoder']
	model = pipeline.named_steps['xgbregressor']
	pred_df_encoded = encoder.transform(pred_df)
	explainer = load('model/explainer.joblib')
	shap_vals = explainer.shap_values(pred_df_encoded)
	input_names = [i for i in pred_df.iloc[0]]
	
	# Create dataframe for shap plot
	shap_df = pd.DataFrame({'feature': pred_df.columns.to_list(),
							'shap-val': shap_vals[0],
							'val-name': input_names})
	# Create list of two different colors depending on shap-val
	colors = [
	'#0063D1' if value >= 0.0 else '#E43137' for value in shap_df['shap-val']
	]
	
	condensed_names = ['Model', 'MPN', 'Body Color', 'Brand', 
					   'UPC Avail.', 'Material', 'Body Type', 
					   'Year', 'Size', 'Country', 'No. Strings', 
					   'Orientation', 'Prod. Line', 'Condition']

	
	shap_plot = {
		'data': [
			{'x': shap_df['shap-val'], 'y': condensed_names,
			'type': 'bar', 'orientation':'h', 'hovertext': shap_df['val-name'],
			'marker': {'color': colors}, 'opacity': 0.8}],
		'layout': {
			'title': 'Atrribute Impact on Prediction',
			'transition': {'duration': 250}}
	}
	
	
	
	
	
	
	return pred_out, shap_plot

layout = dbc.Row([column1, column2, column3])
