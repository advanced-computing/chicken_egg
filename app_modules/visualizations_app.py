# app_modules/visualizations_app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
from app_modules.functions_app import (
    prep_bird_flu_data,
    prep_wild_bird_data,
    prep_egg_price_data,
    prep_stock_price_data,
)


# === New Function: CREATE GEOSPATIAL PLOT ===
def create_geospatial(data):
    """
    Creates a geospatial plot using latitude, longitude, and flock size.
    """
    fig = px.scatter_mapbox(
        data,
        lat="lat",
        lon="lng",
        size="Flock Size",
        color="Flock Size",
        color_continuous_scale="Viridis",
        mapbox_style="carto-positron",
        zoom=3,
        title="Geospatial Visualization"
    )
    return fig


# === New Function: CREATE TIME SERIES PLOT ===
def create_time_series(egg_price_df, stock_price_df):
    """
    Creates a time series plot comparing egg prices and stock prices.
    """
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(x=egg_price_df.index, y=egg_price_df["Avg_Price"], name="Egg Price"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=stock_price_df.index, y=stock_price_df["Close/Last"], name="Stock Price"),
        secondary_y=True,
    )

    fig.update_layout(
        title="Egg Prices vs Stock Prices",
        xaxis_title="Date",
        height=500,
    )

    fig.update_yaxes(title_text="Egg Price (USD)", secondary_y=False)
    fig.update_yaxes(title_text="Stock Price (USD)", secondary_y=True)

    return fig


# === 1. EGG PRICE vs STOCK PRICE TIME SERIES ===
def show_price_comparison(egg_df, stock_df, stock_name="Selected Stock"):
    """
    Plots a dual-axis time series chart comparing egg prices with a selected stock.
    Inputs must be DataFrames with a 'Date' index and appropriate price columns.
    """
    # Resample stock prices to monthly average to match egg data
    stock_df = stock_df.set_index("Date").resample("M").mean().reset_index()

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(x=egg_df.index, y=egg_df["Avg_Price"], name="Egg Price (Grade A)"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=stock_df["Date"], y=stock_df["Close_Last"], name=f"{stock_name} Stock Price"),
        secondary_y=True,
    )

    fig.update_layout(
        title=f"📈 Egg Prices vs {stock_name} Stock Prices",
        xaxis_title="Date",
        height=500,
    )

    fig.update_yaxes(title_text="Egg Price (USD)", secondary_y=False)
    fig.update_yaxes(title_text="Stock Price (USD)", secondary_y=True)

    st.plotly_chart(fig, use_container_width=True)

# === 2. AVIAN FLU OUTBREAK TRENDS ===
def show_bird_flu_trends():
    flu_df = prep_bird_flu_data('bird_flu')
    flu_df.rename(columns={"Outbreak Date": "Date"}, inplace=True)

    # Aggregate daily flock sizes
    daily = flu_df.groupby("Date")["Flock Size"].sum().reset_index()

    fig = px.area(
        daily,
        x="Date",
        y="Flock Size",
        title="Daily Flock Deaths due to Avian Flu",
        labels={"Flock Size": "Number of Birds"},
    )

    st.plotly_chart(fig, use_container_width=True)

# === 3. COMBINED OVERVIEW ===
def show_combined_dashboard():
    # Loading data
    egg_df = prep_egg_price_data("egg_prices")
    calm_df, _, _ = prep_stock_price_data("calmaine")
    for col in ["Close_Last", "Open", "High", "Low"]:
        calm_df[col] = calm_df[col].replace(r'[\$,]', '', regex=True).astype(float)
    flu_df = prep_bird_flu_data("bird_flu")
    
    # Prepping bird flu
    flu_df.rename(columns={"Outbreak Date": "Date"}, inplace=True)
    flu_df = flu_df.groupby("Date")["Flock Size"].sum().reset_index()
    flu_df = flu_df.set_index("Date").resample("M").sum().reset_index()
    
    # Resample stocks
    calm_df = calm_df.set_index("Date").resample("M").mean().reset_index()

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Bar(x=flu_df["Date"], y=flu_df["Flock Size"], name="Flock Deaths (Flu)"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=calm_df["Date"], y=calm_df["Close_Last"], name="Cal-Maine Stock Price"),
        secondary_y=True,
    )

    fig.update_layout(
        title="Bird Flu vs Cal-Maine Stock (Monthly Overview)",
        xaxis_title="Date",
        barmode="overlay",
        height=550,
    )

    fig.update_yaxes(title_text="Flock Size (Bird Flu)", secondary_y=False)
    fig.update_yaxes(title_text="Stock Price (USD)", secondary_y=True)

    st.plotly_chart(fig, use_container_width=True)
