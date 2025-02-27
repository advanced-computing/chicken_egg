#This file contains the vizualizations used in main
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_geospatial(data, lat_col='lat', lon_col='lng', color_col='Flock Size'):
    '''
    Creates a geospatial scatter plot using Plotly Express.
    Flock size is the number of birds that died at each location
    Note: Considering adding a time element (is that possible?)
    '''
    # Ensure that the latitude and longitude columns exist
    if lat_col not in data.columns or lon_col not in data.columns:
        raise ValueError("missing geospatial data :(")
    
    fig = px.scatter_mapbox(
        data,
        lat=lat_col,
        lon=lon_col,
        color=color_col,
        mapbox_style="open-street-map",  # No token required
        zoom=3,
        height=600,
        title="Bird Flu Incidents in the USA"
    )
    # Remove extra white space around the map
    fig.update_layout(margin={"r": 0, "t": 30, "l": 0, "b": 0})
    return fig

def create_time_series(
    df1, df2,  
    y_col1 = 'Avg_Price', 
    y_col2 = 'Close/Last', 
    labels = ['Egg Price', 'Stock Price']):
    
    '''
    Creates dual y-axis time series plot
    DF1 = Egg Prices (y axis on left)
    DF2 = Stock Prices (y axis on right)
    Note: Rescale y-axes!
    '''
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    #time series for egg prices
    fig.add_trace(
        go.Scatter(x=df1.index, y=df1[y_col1], name=labels[0]),
        secondary_y=False,
    )
    
    #time series for stock prices
    fig.add_trace(
        go.Scatter(x=df2.index, y=df2[y_col2], name=labels[1]),
        secondary_y=True,
    )   

    fig.update_xaxes(title_text='Date', range=[pd.to_datetime("2015-01-01"), df1.index.max()], tickformat = '%m-%d-%Y')
    fig.update_yaxes(title_text=labels[0], secondary_y=False)
    fig.update_yaxes(title_text=labels[1], secondary_y=True)
    
    fig.update_layout(title_text="Price per Dozen Eggs vs. Cal-Main Stock Price")
    
    return fig
    



