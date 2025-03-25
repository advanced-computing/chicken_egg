import streamlit as st
from data_prep import prep_bird_flu_data, prep_egg_price_data, prep_stock_price_data, prep_wild_bird_data
from viz import create_geospatial, create_time_series

def main():
    st.title("Data Visualization App")
    st.markdown("### Contributors")
    st.write("Arnav Sahai")
    st.write("Fred Lee")

    # Page selection
    page = st.selectbox("Choose a page", ["Project Proposal", "Bird Flu Data", "Egg Prices Data"])

    if page == "Project Proposal":
        
        st.image("rooster.jpg", caption="What came first, the chicken or the egg?", use_container_width=True)

        st.header("Project Proposal")
        st.markdown("# Overview")
        st.markdown("""
        This project explores the relationship between bird flu outbreaks, egg price fluctuations, and the financial performance of key egg producers. 
        Our analysis aims to address several research questions, including:
        """)
        st.markdown("""
        1. **What is the relationship between the increase of bird flu outbreaks and increases in Grade A egg prices? Is there a time lag?**
        2. **How does the stock price of Cal-Maine Foods (the largest egg company in the USA) respond to bird flu outbreaks?**
        3. **What areas are at risk based on the integration of wild bird and commercial flock data?** *(Updated from wild bird infection data)*
        4. **How are non-caged egg producers such as Vital Farms affected by egg prices and bird flu outbreaks?** *(New question)*
        5. **How is the largest processor of value-added eggs, Michael Foods, affected by egg prices and bird flu outbreaks?** *(New question)*
        """)
        
        st.markdown("## Current Insights")
        st.markdown("""
        - **Positive correlation:** Cal-Maine’s stock prices show a positive correlation with egg prices and bird flu incidents.
        - **Mixed effect on cage free chickens:** Vital Farm's profits took a big hit during the first outbreak in 2022, but saw huge increases in 2024
        - **Low effect on egg substitutes:** Post Holdings does not have a strong correlation with egg prices, but they did increase substantially post 2023 
        - **Lag Effect:** There seems to be a negligable lag between bird flu outbreaks and the subsequent rise in egg prices.
        - **Geospatial Concentration:** The highest losses in poultry (gross number) have been recorded in **California, Oregon, and Utah**, indicating these states face a higher risk of cross infection.
        - ** Regional Concentration:** There is one big center of infections near the intersection of **Nebraska, South Dakota, Iowa, and Wisconsin**
        """)
        
        st.markdown("## Future Directions")
        st.markdown("""
        - **API Integration:** Connect with live data feeds for real-time updates.
        - Incorporate additional datasets such as Consumer Price Index to explore broader economic impacts.
        - Perform correlation and causality analyses among key variables to refine predictive models.
        """)


    elif page == "Bird Flu Data":
        # loads geospatial data
        wild_bird_geo = prep_wild_bird_data()
        bird_data = prep_bird_flu_data()
        
       # st.write("Commercial Bird Flu Data:")
       # st.write(bird_data.head())
       # st.write("Wild Bird Flu Data:")
       # st.write(wild_bird_geo.head())
        
        total_chicken_deaths = bird_data['Flock Size'].sum()
        total_wild_bird_infections = len(wild_bird_geo)     
        latest_date_str = wild_bird_geo['Date Detected'].max()
          
        
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Cumulative Chicken Deaths", total_chicken_deaths)

        with col2:
            st.metric("Total Wild Bird Infections", total_wild_bird_infections)
        
        with col3:
            st.metric("Latest Wild Bird Detection", latest_date_str)

        # Create and display a geospatial plot using viz.py function
        fig_bird_flu = create_geospatial(bird_data)
        st.plotly_chart(fig_bird_flu, use_container_width=True)
        
        fig_wild_bird = create_geospatial(wild_bird_geo)
        st.plotly_chart(fig_wild_bird, use_container_width=True)

    elif page == "Egg Prices Data":
        # Prepare egg prices and stock prices data using data_prep.py functions
        egg_data = prep_egg_price_data()
        
        stock_option = st.selectbox(
            'Select Stock to Compare Against Egg Prices',
            options=['Cal-Maine', 'Post Holdings', 'Vital Farms']
        )
        
        st.markdown("""
            - **Cal-Maine** Largest egg producer in the US accounting for 20 percent of total production
            - **Post Holdings** Owns Michael Foods, largest producer of value-added egg products (liquid/precooked eggs)
            - **Vital Farms** Specializes in pasture raised eggs, leading brand in specialty eggs and 19th overall in US
                    """)
        
        # Map the selection to the corresponding file path
        stock_file_map = {
            "Cal-Maine": "CALM_prices.csv",
            "Post Holdings": "POST_prices.csv",
            "Vital Farms": "VITL_prices.csv"
        }
        
        selected_stock_data = prep_stock_price_data(stock_file_map[stock_option])  
        
        ## Arnav add st.metrics here for latest egg and stock prices  

        # Extract the latest egg price and stock price
        latest_egg_price = egg_data['Avg_Price'].iloc[-1]
        latest_stock_price = selected_stock_data['Close/Last'].iloc[-1]

        # Display the metrics
        col1, col2 = st.columns(2)

        with col1:
            st.metric("Current Egg Price", f"${latest_egg_price:.2f}")

        with col2:
            st.metric("Current Stock Price", f"${latest_stock_price:.2f}")

        
        # Commenting out. Can be used for validation if needed    
        #st.write("Egg Price Data Preview:")
        #st.write(egg_data.head())
        #st.write("Stock Price Data Preview:")
        #st.write(selected_stock_data.head())
        
        # Create and display a dual y-axis time series plot using viz.py function.
        # Default parameters assume egg_data has 'Date' and 'Avg_Price',
        # and stock_data has 'Date' and 'Close/Last'
        fig = create_time_series(egg_data, selected_stock_data)
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
