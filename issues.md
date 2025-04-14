Issues
[] No data for local egg prices
[x] resampling for stock data; need to revisit
[x] remove extra line on time series graph for Cal-Maine price
[x] how to use beautiful soup for API (resolved)

Data
[x] Organize data into a folder? (Temporary until APIs ready, may not be worth it)
[x] set up API for Bird Flu data (clickable link)
    - will wait for the other APIs until it's clear how it is integrated into AirFlow
[] set up API for Cal-Main data (clickable link)
[] set up API for POST data
[] set up API for VITL data
[] set up API for egg prices from BLS (clickable link)
[] set up API for Wild Bird data
[] find additional dataset for consumption that can be used to calculate demand elasticity over time at the national level
[x] compile data onto two dataframes: one for time-series/national data and the other for geographical data
[x] add geospatial data for visualizations
[x] clean Cal-Main food price data
[] Need to incorporate county data into cloropleth
[] Add egg data into combined dashboard. Secondary dashboard underneath?
[] Store valid states as a literal somewhere
[] Upload fips to Big Query
[] fix fips matching for NaN fips values

# Code Organization (what else can be refactored?)
[x] seperate main for app
[x] put streamlit functions into viz.py
[x] put data cleaning functions into data_prep.py
[x] testing code 
    - check for date column, lng, lat
    - see if numbers are numerical
    - check for invalid data values in cols
[x] test cases
[x] move streamlit functions to seperate module
[x] create new module for adding geospatial data
[] update test_helper_viz.py with examples?
[x] fix references in prep_bird_data
[] Write test cases for visualizations and prep_wild_bird_data()
[] refactor prep_stock_data to work with validation and csv file inputs (wait until database)

# Visualizations
[x] Add st.metric
    [x] current stock prices
    [x] current egg prices
[x] Create time series data plotting egg prices, stock price
[x] resample time series to monthly
[x] add second y axis for stock prices
[x] fix x axis for the time series plot
[x] Create US map with bird flu (modify to streamlit plot?) 
[x] Add slider that allow for different time periods on map
[x] add additional stock data to X axis
[x] add additional layers to map data
[] fix the latest date detected column to take the column as datetime and return the latest date
    - currently it does a string comparison
[] What other elements to add to map?
[] Add correlation map w/ egg prices and different stocks (scatter or regression)

Other Considerations
[] Which states are key egg producing states
[] Could incorporate the Producer Price Index or Consumer Price Index, specifically for baked goods
[] Add S&P 500 for comparison on time series graph?
[] Box plot for different egg-based product prices?
[X] Consider whether to include other egg companies or local producers (how to source/aggregate data?)
[] Correlation between different stocks?
[] Incorporate human infection or cow infection data?
[] How to use the National Agricultural Statistics Service (REST API) Data?