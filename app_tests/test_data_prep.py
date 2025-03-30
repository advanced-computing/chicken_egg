import pytest
import pandas as pd
from io import StringIO
from app_modules.functions_app import (
    prep_bird_flu_data,
    prep_egg_price_data,
    prep_stock_price_data
)
from app_tests.test_helper_data_prep import (
    create_stock_ex,
    create_egg_price_ex,
    create_bird_flu_ex,
)

@pytest.mark.parametrize(
    "func, df, expected_exception",
    [
        (prep_stock_price_data, pd.DataFrame({"Open": [100, 101, 102]}), KeyError),  # Missing 'Close/Last'
        (prep_egg_price_data, pd.DataFrame({"Price": [2.5, 3.0, 3.2]}), ValueError),  # Missing 'Year'
        (prep_bird_flu_data, pd.DataFrame({"Flock Size": [10, 20]}), KeyError),  # Missing 'State'
    ]
)
def test_prep_functions_raise_errors(func, df, expected_exception):
    print("\n================ DEBUG INFO =================")
    print(f"Testing function: {func.__name__}")
    print("Expected exception:", expected_exception)
    print("Input DataFrame:")
    print(df)
    print("=============================================")
    
    with pytest.raises(expected_exception):
        func(df)

def test_stock_price_columns_numeric():
    stock_df = pd.read_csv(StringIO(create_stock_ex()))
    df = prep_stock_price_data(stock_df)
    assert pd.api.types.is_numeric_dtype(df["Close/Last"]), "Close/Last must be numeric."

def test_egg_price_date_col_is_datetime():
    egg_df = pd.read_csv(StringIO(create_egg_price_ex()))
    df = prep_egg_price_data(egg_df)
    assert isinstance(df.index, pd.DatetimeIndex), "Index should be a DatetimeIndex."

def test_bird_flu_has_lat_lng():
    bird_flu_df = pd.read_csv(StringIO(create_bird_flu_ex()))
    df = prep_bird_flu_data(bird_flu_df)
    assert "lat" in df.columns, "DataFrame must have 'lat' column."
    assert "lng" in df.columns, "DataFrame must have 'lng' column."

def test_bird_flu_flock_size_is_numeric():
    bird_flu_df = pd.read_csv(StringIO(create_bird_flu_ex()))
    df = prep_bird_flu_data(bird_flu_df)
    assert pd.api.types.is_numeric_dtype(df["Flock Size"]), "Flock Size should be numeric."
    

