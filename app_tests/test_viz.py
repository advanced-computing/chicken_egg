import pytest
import pandas as pd
from app_modules.visualizations_app import (
    create_geospatial,
    create_time_series,
    show_price_comparison,
    show_bird_flu_trends,
    show_combined_dashboard,
)
import streamlit as st


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


def test_show_price_comparison(mocker):
    egg_price_df = pd.DataFrame({
        'Date': pd.date_range(start='2020-01-01', periods=5),
        'Avg_Price': [1, 2, 3, 4, 5]
    }).set_index('Date')

    stock_price_df = pd.DataFrame({
        'Date': pd.date_range(start='2020-01-01', periods=5),
        'Close_Last': [10, 20, 30, 40, 50]
    })

    mocker.patch("streamlit.plotly_chart")  # Mock Streamlit's plotly_chart
    show_price_comparison(egg_price_df, stock_price_df, stock_name="Test Stock")

    st.plotly_chart.assert_called_once()  # Ensure the chart was rendered


def test_show_bird_flu_trends(mocker):
    mocker.patch("app_modules.visualizations_app.prep_bird_flu_data", return_value=pd.DataFrame({
        'Outbreak Date': pd.date_range(start='2020-01-01', periods=5),
        'Flock Size': [10, 20, 30, 40, 50]
    }))

    mocker.patch("streamlit.plotly_chart")  # Mock Streamlit's plotly_chart
    show_bird_flu_trends()

    st.plotly_chart.assert_called_once()  # Ensure the chart was rendered


def test_show_combined_dashboard(mocker):
    mocker.patch("app_modules.visualizations_app.prep_egg_price_data", return_value=pd.DataFrame({
        'Date': pd.date_range(start='2020-01-01', periods=5),
        'Avg_Price': [1, 2, 3, 4, 5]
    }))

    mocker.patch("app_modules.visualizations_app.prep_stock_price_data", return_value=(
        pd.DataFrame({
            'Date': pd.date_range(start='2020-01-01', periods=5),
            'Close_Last': [10, 20, 30, 40, 50],
            'Open': [5, 15, 25, 35, 45],
            'High': [15, 25, 35, 45, 55],
            'Low': [0, 10, 20, 30, 40]
        }),
        None,
        None
    ))

    mocker.patch("app_modules.visualizations_app.prep_bird_flu_data", return_value=pd.DataFrame({
        'Outbreak Date': pd.date_range(start='2020-01-01', periods=5),
        'Flock Size': [10, 20, 30, 40, 50]
    }))

    mocker.patch("streamlit.plotly_chart")  # Mock Streamlit's plotly_chart
    show_combined_dashboard()

    st.plotly_chart.assert_called()  # Ensure charts were rendered
