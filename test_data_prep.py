import pytest
import pandas as pd
from io import StringIO
from data_prep import prep_bird_flu_data, prep_egg_price_data, prep_stock_price_data
from test_helper_data_prep import (
    create_stock_ex,
    create_egg_price_ex,
    create_bird_flu_ex,
)

def test_stock_price_columns_numeric():
    """
    Test that prep_stock_price_data produces numeric columns (e.g., 'Close/Last').
    """
    stock_df = pd.read_csv(StringIO(create_stock_ex()))

    df = prep_stock_price_data(stock_df)

    assert pd.api.types.is_numeric_dtype(df["Close/Last"]), "Close/Last must be numeric."

def test_egg_price_date_col_is_datetime():
    """
    Test that prep_egg_price_data sets the DataFrame index to a datetime.
    """
    egg_df = pd.read_csv(StringIO(create_egg_price_ex()))

    df = prep_egg_price_data(egg_df)

    assert isinstance(df.index, pd.DatetimeIndex), "Index should be a DatetimeIndex."

def test_bird_flu_has_lat_lng():
    """
    Test that prep_bird_flu_data returns a DataFrame with 'lat' and 'lng' columns.
    """
    bird_flu_df = pd.read_csv(StringIO(create_bird_flu_ex()))
    
    df = prep_bird_flu_data(bird_flu_df)


    assert "lat" in df.columns, "DataFrame must have 'lat' column."
    assert "lng" in df.columns, "DataFrame must have 'lng' column."

def test_bird_flu_flock_size_is_numeric():
    """
    Test that prep_bird_flu_data ensures 'Flock Size' is numeric.
    """
    bird_flu_df = pd.read_csv(StringIO(create_bird_flu_ex()))

    df = prep_bird_flu_data(bird_flu_df)
    
    assert pd.api.types.is_numeric_dtype(df["Flock Size"]), "Flock Size should be numeric."
