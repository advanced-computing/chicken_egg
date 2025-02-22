import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function to load data from a CSV file
@st.cache_data
def load_data_from_file(file_path):
    data = pd.read_csv(file_path)
    return data

# Need to change this to a map! Import folium 
# Function to create a plot based on data types
def create_plot(data, x_column, y_column):
    fig, ax = plt.subplots()
    if pd.api.types.is_numeric_dtype(data[x_column]) and pd.api.types.is_numeric_dtype(data[y_column]):
        sns.scatterplot(data=data, x=x_column, y=y_column, ax=ax)
    elif pd.api.types.is_categorical_dtype(data[x_column]) or pd.api.types.is_object_dtype(data[x_column]):
        sns.barplot(data=data, x=x_column, y=y_column, ax=ax)
    else:
        sns.lineplot(data=data, x=x_column, y=y_column, ax=ax)
    return fig

def create_time_series_plot(df1, df2, x_col, y_col1, y_col2, labels):
    fig, ax = plt.subplots()

    sns.lineplot(data=df1, x=x_col, y=y_col1, ax=ax, label=labels[0])
    sns.lineplot(data=df2, x=x_col, y=y_col2, ax=ax, label=labels[1])

    ax.set_xlabel("Date")
    ax.set_ylabel("Values")
    ax.set_title("Time Series Comparison")
    plt.xticks(rotation=45)
    ax.legend()

    return fig

# Streamlit app
def main():
    st.title("Data Visualization App")
    st.sidebar.title("Contributors")
    st.sidebar.write("Arnav Sahai")
    st.sidebar.write("Fred Lee")

    # Page selection
    page = st.sidebar.selectbox("Choose a page", ["Bird Flu Data", "Egg Prices Data"])

    if page == "Bird Flu Data":
        # Load bird_flu.csv
        data = load_data_from_file('bird_flu_final.csv')
        st.write("Data Preview:")
        st.write(data.head())

        # Select columns for visualization
        x_column = st.selectbox("Select the X-axis column", data.columns)
        y_column = st.selectbox("Select the Y-axis column", data.columns)

        st.write("Data Visualization:")
        fig = create_plot(data, x_column, y_column)
        st.pyplot(fig)

    elif page == "Egg Prices Data":
        # Load egg prices and CALM stock prices
        price_data = load_data_from_file('egg_price_long.csv')
        stock_data = load_data_from_file('stock_prices.csv')
        
        st.write("Egg Price Preview:")
        st.write(price_data.head())
        
        st.write("Stock Price Preview:")
        st.write(stock_data.head())

        # **Automatically detect and format the Date column (instead of user selection)**
        for df in [price_data, stock_data]:
            if "Date" in df.columns:
                df["Date"] = pd.to_datetime(df["Date"], errors='coerce')

        y_column_egg = st.selectbox("Select the Y-axis column for Egg Prices", price_data.columns)
        y_column_stock = st.selectbox("Select the Y-axis column for Stock Prices", stock_data.columns)
        


        st.write("Data Visualization:")
        fig = create_time_series_plot(price_data, stock_data, "Date", y_column_egg, y_column_stock, ["Egg Prices", "Stock Prices"])
        st.pyplot(fig)

if __name__ == "__main__":
    main()