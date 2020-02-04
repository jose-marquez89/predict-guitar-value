# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
# Imports from this application
from app import app

# 2 column layout. 1st column width = 4/12
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
df = pd.read_csv('../data/web-app-guitars.csv')

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
			dcc.Markdown("##### Select Brand"),
			dcc.Dropdown(
				id='brand-dd', 
				options=[
					{'label': i, 'value': i} for i in available_brands],
			)
		]),
		html.Div([
			dcc.Markdown("##### Select Model"),
			dcc.Dropdown(
				id='model-dd', 
				options=[
					{'label': i, 'value': i} for i in available_models],
			)
		]),
		html.Div([
			dcc.Markdown("##### Select Color"),
			dcc.Dropdown(
				id='color-dd', 
				options=[
					{'label': i, 'value': i} for i in available_colors],
			)
		]),
		html.Div([
			dcc.Markdown("##### Select Material"),
			dcc.Dropdown(
				id='material-dd', 
				options=[
					{'label': i, 'value': i} for i in available_materials],
			)
		]),
		html.Div([
			dcc.Markdown("##### Select Body Type"),
			dcc.Dropdown(
				id='btype-dd', 
				options=[
					{'label': i, 'value': i} for i in available_btypes],
			)
		]),
		html.Div([
			dcc.Markdown("##### Select Size"),
			dcc.Dropdown(
				id='sizes-dd', 
				options=[
					{'label': i, 'value': i} for i in available_sizes],
			)
		]),
	],
	md=3
)

# @app.callback(
    # Output(component_id='my-div', component_property='children'),
    # [Input(component_id='my-id', component_property='value')])

# def masterYoda(value):
	# return 'You entered "{}"'.format(value)
column2 = dbc.Col([
		html.Div([
			dcc.Markdown("##### Select Country of Manufacture"),
			dcc.Dropdown(
				id='country-dd', 
				options=[
					{'label': i, 'value': i} for i in available_countries]
			)
		]),
		html.Div([
			dcc.Markdown("##### Select String Configuration"),
			dcc.Dropdown(
				id='strings-dd', 
				options=[
					{'label': i, 'value': i} for i in available_sconfigs]
			)
		]),
		html.Div([
			dcc.Markdown("##### Select Product Line"),
			dcc.Dropdown(
				id='pline-dd', 
				options=[
					{'label': i, 'value': i} for i in available_plines]
			)
		]),
		html.Div([
			dcc.Markdown("##### Select Orientation"),
			dcc.Dropdown(
				id='orient-dd', 
				options=[
					{'label': i, 'value': i} for i in orientations]
			)
		]),
		# html.Div([
			# dcc.Markdown("##### Select Orientation"),
			# dcc.RadioItems(
				# id='right-or-left',
				# options=[
					# {'label': i, 'value': i} for i in ['LEFT-HANDED',
													   # 'RIGHT-HANDED',
													   # 'BOTH']],
		        # value='RIGHT-HANDED',
		    # )
		# ]),
													   
	],
	md=3
)
column3 = dbc.Col([
		dcc.Markdown("##### Set Approximate Year"),
		dcc.Slider(
			id='year-slide',
			min=1940,
			max=2020,
			step=10,
			value=2020,
			marks={n: f'{n:.0f}'for n in range(1940,2040,10)}
		)
	], 
	md=6
)

layout = dbc.Row([column1, column2, column3])
