import pandas as pd
from app_modules.visualizations_app import create_geospatial, create_time_series

def test_create_geospatial():
    sample_data = pd.DataFrame({
        'lat': [34.0522, 36.1699, 40.7128],
        'lng': [-118.2437, -115.1398, -74.0060],
        'Flock Size': [10, 20, 30]
    })

    fig = create_geospatial(sample_data)

    assert fig and len(fig.data) > 0, "Geospatial plot should contain data points."

def test_create_time_series():
    egg_price_df = pd.DataFrame({
        'Date': pd.date_range(start='2020-01-01', periods=5),
        'Avg_Price': [1, 2, 3, 4, 5]
    }).set_index('Date')

    stock_price_df = pd.DataFrame({
        'Date': pd.date_range(start='2020-01-01', periods=5),
        'Close/Last': [10, 20, 30, 40, 50]
    }).set_index('Date')

    fig = create_time_series(egg_price_df, stock_price_df)

    assert fig and len(fig.data) == 2, "Time series should contain two lines."
