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


Instructions for Application Setup

1) Download github repository into a local repository folder

2) Create a virtual environment

3) Activate virtual environment 

4) Install requirements.txt (pip install -r /path/to/requirements.txt)

5) Set up permissions secrets.toml within .streamlit folder for BigQuery. This is referenced in query_gbq.py to load the data. If there's any issues, it will likely occur in this step. 

(you've already been added as a reader on "sipa-adv-c-arnav-fred")
Link here: https://console.cloud.google.com/welcome?invt=Abt4HQ&project=sipa-adv-c-arnav-fred

6) Run streamlit run main_app.py in terminal


