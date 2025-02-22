import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function to load data from a CSV file
@st.cache_data
def load_data_from_file(file_path):
    data = pd.read_csv(file_path)
    return data

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
        data = load_data_from_file('bird_flu.csv')
        st.write("Data Preview:")
        st.write(data.head())

        # Select columns for visualization
        x_column = st.selectbox("Select the X-axis column", data.columns)
        y_column = st.selectbox("Select the Y-axis column", data.columns)

        st.write("Data Visualization:")
        fig = create_plot(data, x_column, y_column)
        st.pyplot(fig)

    elif page == "Egg Prices Data":
        # Load egg_prices.csv
        data = load_data_from_file('egg_prices.csv')
        st.write("Data Preview:")
        st.write(data.head())

        # Select columns for visualization
        x_column = st.selectbox("Select the X-axis column", data.columns)
        y_column = st.selectbox("Select the Y-axis column", data.columns)

        st.write("Data Visualization:")
        fig = create_plot(data, x_column, y_column)
        st.pyplot(fig)

if __name__ == "__main__":
    main()