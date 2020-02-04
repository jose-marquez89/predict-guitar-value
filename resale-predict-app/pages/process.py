# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Imports from this application
from app import app

# 1 column layout
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
        dcc.Markdown(
            """
        
            ## Process
            
            Here, you should explain a bit about your process, and maybe
            include some of the code from the notebooks. I really like the 
            app with the book reviews. I was simple and to the point, but you
            need to decide whether or not you want to have a more "visual" 
            process explanation, rather than a bunch of code.


            """
        ),

    ],
)

layout = dbc.Row([column1])
