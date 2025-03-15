# Egg Prices, Bird Flu, and Cal-Main Profits

This project aims to explore the relation between the bird flu and Egg Price fluctuations. The main research aims are the following:
1) What is the relationship between the increase of bird flu outbreaks and increases in Grade A egg prices? Is there a time lag?
2) How does the stock price of Cal-Main Foods (biggest egg company in USA) respond to bird flu outbreak?
3) What areas are at risk of human infection? UPDATE: New question that uses infections in wild birds + commercial flocks to determine high risk areas (wild bird data is new!)
4) How is the largest pasture-raised egg company, Vital Farms, affected by egg prices? How about bird flu (via chicken deaths?) UPDATE: NEW QUESTION
5) How is the largest processor of value-added eggs, Michael Foods (subsidiary of Post Holdings), affected by egg prices? How about bird flu? UPDATE: NEW QUESTION

Adjustments:
1) Updated Q3 to include wild birds instead of human infections. May still add human infections, but by that point it would be a lagging indicator
2) Added Q4. This was important to see the impact on non-caged egg producers and to see how a different segment of the egg market has responded to the supply shock
3) Added Q5. Similar to Q4 in how it will add additional insight into the 

Dropped questions:
1) What is the correlation between bird flu incidence and average egg prices? UPDATE: Need to drop; cannot find the data for local egg prices
2) How do consumer respond to egg price increases? What is the demand elasticity for eggs? (Need to find consumption data) - UPDATE: Need to drop this, not able to find the consumer data at a granular enough level

Current insights:
- There is a positive correlation between Cal-Maine's stock prices and egg prices oras well as bird flu deaths
- There is about a 2-3 month time lag between the outbreaks and the increase in egg prices
- The largest losses of chickens have ocurred in California, Oregon, and Utah. These states are at a highe risk of cross infection of bird flu



Issues
[] No data for local egg prices
[] No data for local 
[] resampling for stock data; need to revisit
[] remove extra line on time series graph for Cal-Maine price
[] how to use beautiful soup for API 

Data
[] Organize data into a folder? (Temporary until APIs ready, may not be worth it)
[] set up API for Bird Flu data (clickable link)
[] set up API for Cal-Main data (clickable link)
[] set up API for POST data
[] set up API for 
[] set up API for egg prices from BLS (clickable link)
[] set up API for National Agricultural Statistics Service (REST API) Keep? Integrate?
[] find additional dataset for consumption that can be used to calculate demand elasticity over time at the national level
[x] compile data onto two dataframes: one for time-series/national data and the other for geographical data
[x] add geospatial data for visualizations
[x] clean Cal-Main food price data

# Code Organization (what else can be refactored?)
[x] seperate main for app
[x] put streamlit functions into viz.py
[x] put data cleaning functions into data_prep.py
[x] testing code 
    - check for date column, lng, lat
    - see if numbers are numerical
    - check for invalid data values in cols
[x] test cases
[] move streamlit functions to seperate module
[] create new module for adding geospatial data
[] update test_helper_viz.py with examples?
[] fix references in prep_bird_data
[] Write test cases for visualizations and prep_wild_bird_data()
[] refactor prep_stock_data to work with validation and csv file inputs (or wait until database?)

# Visualizations
[] Add st.metric
    [] current stock prices
    [] current egg prices
    [] stock prices compared to two months after bird flu (incorporating lag) for % increase
    [] same for eggs
[x] Create time series data plotting egg prices, stock price
[x] resample time series to monthly
[x] add second y axis for stock prices
[x] fix x axis for the time series plot
[x] Create US map with bird flu (modify to streamlit plot?) 
[] Add slider that allow for different time periods on both graphs
[] add additional stock data to X axis
[] add additional layers to map data
    [x] created separate map for now, may try merging into one df later
[] fix the latest date detected column to take the column as datetime and return the latest date
    - currently it does a string comparison
[] What other elements to add to map?

Other Considerations
[] Which states are key egg producing states
[] Could incorporate the Producer Price Index or Consumer Price Index, specifically for baked goods
[] Add S&P 500 for comparison on time series graph?
[] Box plot for different egg-based product prices?
[X] Consider whether to include other egg companies or local producers (how to source/aggregate data?)
[] Correlation between different stocks?
[] Incorporate human infection or cow infection data?
[] How to use the National Agricultural Statistics Service (REST API) Data?