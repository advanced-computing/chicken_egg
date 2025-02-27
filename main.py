import streamlit as st
from data_prep import prep_bird_flu_data, prep_egg_price_data, prep_stock_price_data
from viz import create_geospatial, create_time_series

def main():
    st.title("Data Visualization App")
    st.sidebar.title("Contributors")
    st.sidebar.write("Arnav Sahai")
    st.sidebar.write("Fred Lee")

    # Page selection
    page = st.sidebar.selectbox("Choose a page", ["Bird Flu Data", "Egg Prices Data"])

    if page == "Bird Flu Data":
        # Imports cleaned bird_flu. Still not set up with API
        bird_data = prep_bird_flu_data()
        st.write("Bird Flu Data Head:")
        st.write(bird_data.head())

        # Create and display a geospatial plot using viz.py function
        fig = create_geospatial(bird_data)
        st.plotly_chart(fig)

    elif page == "Egg Prices Data":
        # Prepare egg prices and stock prices data using data_prep.py functions
        egg_data = prep_egg_price_data()
        stock_data = prep_stock_price_data()
        
        st.write("Egg Price Data Preview:")
        st.write(egg_data.head())
        st.write("Stock Price Data Preview:")
        st.write(stock_data.head())
        
        # Create and display a dual y-axis time series plot using viz.py function.
        # Default parameters assume egg_data has 'Date' and 'Avg_Price',
        # and stock_data has 'Date' and 'Close/Last'
        fig = create_time_series(egg_data, stock_data)
        st.plotly_chart(fig)

if __name__ == "__main__":
    main()
