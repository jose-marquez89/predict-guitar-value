# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Imports from this application
from app import app

# 2 column layout. 1st column width = 4/12
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
        dcc.Markdown(
            """
        
            ## How Much Will eBayers Pay?

            Despite MSRP's, guitars often sell for unexpected prices on one of the world's largest
            online marketplaces. These prices are unlikely to be driven by normal market expectations.

            Color, wood, country of manufacturing, brand...these differences can sway the minds and emotions of guitar buyers on eBay.

            You can use [**Machine Learning**](https://en.wikipedia.org/wiki/Machine_learning) in this app to predict these price fluctuations.

            """
        ),
        dcc.Link(dbc.Button('Predict Resale Price', color='primary'), href='/predictions')
    ],
    md=4,
)

column2 = dbc.Col(
    [
        html.Img(src='assets/man-browsing-at-a-guitar-shop.jpg', className='img-fluid'),
        # Photo by <a href="https://burst.shopify.com/@ji_n_yc?utm_campaign=photo_credit&amp;utm_content=Free+Man+Browsing+At+A+Guitar+Shop+Photo+%E2%80%94+High+Res+Pictures&amp;utm_medium=referral&amp;utm_source=credit">Jinnifer Douglass</a> from <a href="https://burst.shopify.com/retail?utm_campaign=photo_credit&amp;utm_content=Free+Man+Browsing+At+A+Guitar+Shop+Photo+%E2%80%94+High+Res+Pictures&amp;utm_medium=referral&amp;utm_source=credit">Burst</a>
    ]
)

layout = dbc.Row([column1, column2])
