import streamlit as st
from data_prep import prep_bird_flu_data, prep_egg_price_data, prep_stock_price_data
from viz import create_geospatial, create_time_series

def main():
    st.title("Data Visualization App")
    st.sidebar.title("Contributors")
    st.sidebar.write("Arnav Sahai")
    st.sidebar.write("Fred Lee")

    # Page selection
    page = st.sidebar.selectbox("Choose a page", ["Project Proposal", "Bird Flu Data", "Egg Prices Data"])

    if page == "Project Proposal":
        
        st.image("rooster.jpg", caption="What came first, the chicken or the egg?", use_column_width=True)

        st.header("Project Proposal")
        st.markdown("# Overview")
        st.markdown("""
        This project explores the relationship between bird flu outbreaks, egg price fluctuations, and the financial performance of key egg producers. 
        Our analysis aims to address several research questions, including:
        """)
        st.markdown("""
        1. **What is the relationship between the increase of bird flu outbreaks and increases in Grade A egg prices? Is there a time lag?**
        2. **How does the stock price of Cal-Maine Foods (the largest egg company in the USA) respond to bird flu outbreaks?**
        3. **What areas are at risk based on the integration of wild bird and commercial flock data?** *(Updated from human infection data)*
        4. **How are non-caged egg producers such as Vital Farms affected by egg prices and bird flu outbreaks?** *(New question)*
        5. **How is the largest processor of value-added eggs, Michael Foods, affected by egg prices and bird flu outbreaks?** *(New question)*
        """)
        
        st.markdown("## Current Insights")
        st.markdown("""
        - **Positive correlation:** Cal-Maine’s stock prices show a positive correlation with egg prices and bird flu incidents.
        - **Lag Effect:** A **2-3 month time lag** is observed between bird flu outbreaks and the subsequent rise in egg prices.
        - **Geospatial Concentration:** The highest losses in poultry (gross number) have been recorded in **California, Oregon, and Utah**, indicating these states face a higher risk of cross infection.
        """)
        
        st.markdown("## Future Directions")
        st.markdown("""
        - **API Integration:** Connect with live data feeds for real-time updates.
        - Incorporate additional datasets such as Consumer Price Index to explore broader economic impacts.
        - Perform correlation and causality analyses among key variables to refine predictive models.
        """)


    elif page == "Bird Flu Data":
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
