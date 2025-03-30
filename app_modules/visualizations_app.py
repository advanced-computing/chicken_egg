# app_modules/visualizations_app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
from .functions_app import (
    prep_bird_flu_data,
    prep_stock_price_data,
)



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
    flu_df = prep_bird_flu_data('bird_flu', group_by_state=False)

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
    
    #Loading data; got rid of egg data for now
    calm_df, _, _ = prep_stock_price_data("calmaine")
    flu_df = prep_bird_flu_data("bird_flu", group_by_state=False)

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

def show_wild_bird_map(wild_grouped, flock_grouped, valid_states):
    """
    Displays a cumulative-progressive map:
    State color = chicken deaths (Sum of Flock Size)
    Circles = wild bird infections (Sum of Wild Birds)
    Data accumulates progressively from Jan 2022.
    Requires https://raw.githubusercontent.com/advanced-computing/chicken_egg/main/app_data/us_states.geojson
    """

    # Cargar el GeoJSON de estados
    url = "https://raw.githubusercontent.com/advanced-computing/chicken_egg/main/app_data/us_states.geojson"
    response = requests.get(url)
    geojson = response.json()

    # creating features for map
    geojson["features"] = [
        f for f in geojson["features"]
        if f["properties"]["NAME"] in valid_states]

    # Combining dataframes
    merged = pd.merge(flock_grouped, 
                      wild_grouped, 
                      on=['Month', 'State'], 
                      how='left',
                      suffixes=('', '_wild')
    )
    
    merged['Wild Count'] = merged['Wild Count'].fillna(0)

    # Month selector
    month_options = merged[['Month', 'Month_str']].drop_duplicates().sort_values('Month')
    month_strs = month_options['Month_str'].tolist()
    selected_label = st.select_slider(
        "Progressive Timeline (Cumulative to...)", 
        options=month_strs, 
        value=month_strs[-1]
    )
    
    selected_cutoff = pd.to_datetime(selected_label, format='%b %Y')

    cumulative_view = merged[merged['Month'] <= selected_cutoff]

    if cumulative_view.empty:
        st.info("No data available up to this date.")
        return

    # Sum by state
    view = cumulative_view.groupby("State").agg({
        "Flock Size": "sum",
        "Wild Count": "sum",
        "lat": "mean",
        "lng": "mean"
    }).reset_index()

    # Hover info
    view["Hover"] = (
        "State: " + view["State"] +
        "<br>Wild Infections: " + view["Wild Count"].astype(int).astype(str) +
        "<br>Flock Deaths: " + view["Flock Size"].astype(int).astype(str)
    )

    # Flock Size Choropleth (could use county maybe)
    fig = px.choropleth_mapbox(
        view,
        geojson=geojson,
        locations="State",
        featureidkey="properties.NAME",
        color="Flock Size",
        color_continuous_scale="YlOrRd",
        range_color=(0, view["Flock Size"].max()),
        mapbox_style="carto-darkmatter",
        zoom=3,
        center={"lat": 37.8, "lon": -96},
        opacity=0.6,
        labels={"Flock Size": "Flock Deaths"},
        height=600
    )

    # Add cirlces for Wild Count
    fig.add_scattermapbox(
        lat=view["lat"],
        lon=view["lng"],
        mode="markers",
        marker=px.scatter_mapbox(
            view,
            lat="lat",
            lon="lng",
            size="Wild Count",
            size_max=50
        ).data[0].marker,
        text=view["State"] + "<br>Wild Cases: " + view["Wild Count"].astype(int).astype(str),
        hoverinfo="text",
        name="Wild Bird Infections"
    )

    fig.update_layout(
        title=f"📍 Wild Bird Infections & Chicken Deaths – Cumulative until {selected_label}",
        margin={"r": 0, "t": 50, "l": 0, "b": 0},
        paper_bgcolor="#111111",
        font_color="white",
        legend_title_text="Chicken Deaths (State Color)",
    )

    # Description
    st.markdown("""
    **Map Explanation**  
    - **State Color**: Number of chickens lost due to outbreaks (Flock Size)  
    - **Bubble Size**: Number of wild bird infections detected  
    - Use the slider to view how both have progressed from Jan 2022 until now.
    """)
    
    st.plotly_chart(fig, use_container_width=True)
