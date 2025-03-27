import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from pandas.testing import assert_frame_equal

# app_modules/test_visualizations_app.py

from app_modules.visualizations_app import (
    show_price_comparison,
    show_bird_flu_trends,
    show_combined_dashboard,
    show_wild_bird_map,
)

@patch("streamlit.plotly_chart")
def test_show_price_comparison(mock_plotly_chart):
    egg_data = pd.DataFrame({"Date": pd.date_range("2023-01-01", periods=3, freq="M"), "Avg_Price": [2.5, 3.0, 3.2]})
    stock_data = pd.DataFrame({"Date": pd.date_range("2023-01-01", periods=3, freq="M"), "Close/Last": [100, 110, 120]})
    egg_data.set_index("Date", inplace=True)

    show_price_comparison(egg_data, stock_data, stock_name="Test Stock")

    mock_plotly_chart.assert_called_once()

@patch("streamlit.plotly_chart")
@patch("pandas.read_csv")
def test_show_bird_flu_trends(mock_read_csv, mock_plotly_chart):
    mock_read_csv.return_value = pd.DataFrame({
        "Outbreak Date": pd.date_range("2023-01-01", periods=3, freq="D"),
        "Flock Size": [100, 200, 300],
    })

    show_bird_flu_trends()

    mock_plotly_chart.assert_called_once()

@patch("streamlit.plotly_chart")
@patch("pandas.read_csv")
def test_show_combined_dashboard(mock_read_csv, mock_plotly_chart):
    def mock_csv_side_effect(url, *args, **kwargs):
        if "egg_price_monthly" in url:
            return pd.DataFrame({"Date": pd.date_range("2023-01-01", periods=3, freq="M"), "Avg_Price": [2.5, 3.0, 3.2]})
        elif "calmaine_prices_daily" in url:
            from app_modules.visualizations_app import (
                show_price_comparison,
                show_bird_flu_trends,
                show_combined_dashboard,
                show_wild_bird_map,
            )

            # === Fixtures ===
            @pytest.fixture
            def sample_egg_data():
                return pd.DataFrame({"Date": pd.date_range("2023-01-01", periods=3, freq="M"), "Avg_Price": [2.5, 3.0, 3.2]}).set_index("Date")

            @pytest.fixture
            def sample_stock_data():
                return pd.DataFrame({"Date": pd.date_range("2023-01-01", periods=3, freq="M"), "Close/Last": [100, 110, 120]})

            @pytest.fixture
            def sample_flu_data():
                return pd.DataFrame({
                    "Outbreak Date": pd.date_range("2023-01-01", periods=3, freq="D"),
                    "Flock Size": [100, 200, 300],
                })

            @pytest.fixture
            def sample_geo_data():
                return pd.DataFrame({
                    "State": ["Test State"],
                    "Date Detected": ["2023-01-01"],
                })

            @pytest.fixture
            def sample_bird_data():
                return pd.DataFrame({
                    "State": ["Test State"],
                    "Outbreak Date": ["2023-01-01"],
                    "Flock Size": [100],
                    "lat": [37.8],
                    "lng": [-96.0],
                })

            # === Tests ===
            @patch("streamlit.plotly_chart")
            def test_show_price_comparison(mock_plotly_chart, sample_egg_data, sample_stock_data):
                show_price_comparison(sample_egg_data, sample_stock_data, stock_name="Test Stock")
                mock_plotly_chart.assert_called_once()

            @patch("streamlit.plotly_chart")
            @patch("pandas.read_csv")
            def test_show_bird_flu_trends(mock_read_csv, mock_plotly_chart, sample_flu_data):
                mock_read_csv.return_value = sample_flu_data
                show_bird_flu_trends()
                mock_plotly_chart.assert_called_once()

            @patch("streamlit.plotly_chart")
            @patch("pandas.read_csv")
            def test_show_combined_dashboard(mock_read_csv, mock_plotly_chart):
                def mock_csv_side_effect(url, *args, **kwargs):
                    if "egg_price_monthly" in url:
                        return pd.DataFrame({"Date": pd.date_range("2023-01-01", periods=3, freq="M"), "Avg_Price": [2.5, 3.0, 3.2]})
                    elif "calmaine_prices_daily" in url:
                        return pd.DataFrame({"Date": pd.date_range("2023-01-01", periods=3, freq="D"), "Close/Last": ["$100", "$110", "$120"]})
                    elif "bird_flu_daily" in url:
                        return pd.DataFrame({"Outbreak Date": pd.date_range("2023-01-01", periods=3, freq="D"), "Flock Size": [100, 200, 300]})
                    return pd.DataFrame()

                mock_read_csv.side_effect = mock_csv_side_effect
                show_combined_dashboard()
                mock_plotly_chart.assert_called_once()

            @patch("streamlit.plotly_chart")
            @patch("requests.get")
            def test_show_wild_bird_map(mock_requests_get, mock_plotly_chart, sample_geo_data, sample_bird_data):
                mock_requests_get.return_value.json.return_value = {
                    "features": [{"properties": {"NAME": "Test State"}}]
                }
                show_wild_bird_map(sample_geo_data, sample_bird_data)
                mock_plotly_chart.assert_called_once()

            # === Additional Tests ===
            @patch("streamlit.plotly_chart")
            def test_show_price_comparison_empty_data(mock_plotly_chart):
                empty_egg_data = pd.DataFrame(columns=["Date", "Avg_Price"]).set_index("Date")
                empty_stock_data = pd.DataFrame(columns=["Date", "Close/Last"])
                show_price_comparison(empty_egg_data, empty_stock_data, stock_name="Test Stock")
                mock_plotly_chart.assert_called_once()

            @patch("streamlit.plotly_chart")
            @patch("pandas.read_csv")
            def test_show_bird_flu_trends_empty_data(mock_read_csv, mock_plotly_chart):
                mock_read_csv.return_value = pd.DataFrame(columns=["Outbreak Date", "Flock Size"])
                show_bird_flu_trends()
                mock_plotly_chart.assert_called_once()

            @patch("streamlit.plotly_chart")
            @patch("pandas.read_csv")
            def test_show_combined_dashboard_missing_columns(mock_read_csv, mock_plotly_chart):
                def mock_csv_side_effect(url, *args, **kwargs):
                    if "egg_price_monthly" in url:
                        return pd.DataFrame({"Date": pd.date_range("2023-01-01", periods=3, freq="M")})  # Missing Avg_Price
                    elif "calmaine_prices_daily" in url:
                        return pd.DataFrame({"Date": pd.date_range("2023-01-01", periods=3, freq="D")})  # Missing Close/Last
                    elif "bird_flu_daily" in url:
                        return pd.DataFrame({"Outbreak Date": pd.date_range("2023-01-01", periods=3, freq="D")})  # Missing Flock Size
                    return pd.DataFrame()

                mock_read_csv.side_effect = mock_csv_side_effect
                show_combined_dashboard()
                mock_plotly_chart.assert_called_once()

    mock_plotly_chart.assert_called_once()