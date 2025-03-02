# Will test functions used in viz.pyimport pytest
import pandas as pd
from viz import create_geospatial, create_time_series

# Will test functions used in viz.py

def test_create_geospatial():
    # Create a sample dataframe
    data = pd.DataFrame({
        'lat': [34.0522, 36.1699, 40.7128],
        'lng': [-118.2437, -115.1398, -74.0060],
        'Flock Size': [10, 20, 30]
    })
    
    # Call the function
    fig = create_geospatial(data)
    
    # Check if the figure has points on the map
    assert len(fig.data) > 0

def test_create_time_series():
    # Create sample dataframes
    df1 = pd.DataFrame({
        'Date': pd.date_range(start='1/1/2020', periods=5),
        'Avg_Price': [1, 2, 3, 4, 5]
    }).set_index('Date')
    
    df2 = pd.DataFrame({
        'Date': pd.date_range(start='1/1/2020', periods=5),
        'Close/Last': [10, 20, 30, 40, 50]
    }).set_index('Date')
    
    # Call the function
    fig = create_time_series(df1, df2)
    
    # Check if the figure has 2 lines
    assert len(fig.data) == 2