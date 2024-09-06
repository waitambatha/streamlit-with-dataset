import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Supabase connection URL from .env file
pg_url = os.getenv("SUPABASE_DB_URL")

# Title of the app
st.title("STREAMLIT ETL Process with Visualizations (Supabase PostgreSQL)")

# Step 1: Extract - Load the predefined CSV file
st.header("Step 1: Extract")
file_path = 'IHME_GBD_2010_MORTALITY_AGE_SPECIFIC_BY_COUNTRY_1970_2010.csv'  # Update with your file path if necessary
df = pd.read_csv(file_path)

# Show the first few rows of the dataset
st.subheader("Dataset Preview")
st.write(df.head())

# Step 2: Transform - Data Cleaning and Transformation
st.header("Step 2: Transform")

# Option to drop missing values
if st.checkbox("Drop rows with missing values"):
    df.dropna(inplace=True)
    st.write("Dropped rows with missing values.")

# Option to rename columns
st.subheader("Rename Columns")
for col in df.columns:
    new_col_name = st.text_input(f"Rename column '{col}'", col)
    if new_col_name:
        df.rename(columns={col: new_col_name}, inplace=True)

# Show transformed data
st.subheader("Transformed Data Preview")
st.write(df.head())

# Visualization Section
st.header("Data Visualization")

# Bar chart
selected_column = st.selectbox("Select a column to visualize as a bar chart", df.columns)
if selected_column:
    st.bar_chart(df[selected_column].value_counts())

# Line chart
time_column = st.selectbox("Select a time-related column for line chart", df.columns)
if time_column:
    st.line_chart(df.groupby(time_column).size())

# Histogram
numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
selected_numeric_column = st.selectbox("Select a numeric column for histogram", numeric_columns)
if selected_numeric_column:
    st.write(df[selected_numeric_column].describe())

    # Create and display histogram using matplotlib
    fig, ax = plt.subplots()
    ax.hist(df[selected_numeric_column], bins=20, color='blue', edgecolor='black')
    ax.set_title(f'Histogram of {selected_numeric_column}')
    ax.set_xlabel(selected_numeric_column)
    ax.set_ylabel('Frequency')
    st.pyplot(fig)

# Pie chart
st.subheader("Pie Chart")
pie_column = st.selectbox("Select a column for Pie Chart", df.columns)
if pie_column:
    pie_data = df[pie_column].value_counts()
    fig, ax = plt.subplots()
    ax.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig)

# Stacked bar chart
st.subheader("Stacked Bar Chart")
x_column = st.selectbox("Select X-axis column for stacked bar chart", df.columns)
y_column = st.selectbox("Select Y-axis column for stacked bar chart", df.columns)
if x_column and y_column:
    grouped_data = df.groupby([x_column, y_column]).size().unstack(fill_value=0)
    st.bar_chart(grouped_data)

# Scatter plot
if len(numeric_columns) > 1:
    x_axis = st.selectbox("Select X-axis for scatter plot", numeric_columns)
    y_axis = st.selectbox("Select Y-axis for scatter plot", numeric_columns)
    if x_axis and y_axis:
        st.scatter_chart(df[[x_axis, y_axis]])

# Step 4: Load - Save Data to Supabase PostgreSQL
st.header("Step 3: Load")

# Fixed table name to 'mortality_data'
table_name_pg = "mortality_data"

if st.button("Load Data into Supabase PostgreSQL"):
    try:
        # Connect to Supabase PostgreSQL database
        engine = create_engine(pg_url)

        # Load data into Supabase PostgreSQL
        df.to_sql(table_name_pg, engine, if_exists='replace', index=False)
        st.success(f"Data loaded successfully into Supabase PostgreSQL (Table: {table_name_pg})")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Option to display SQL table from Supabase PostgreSQL
if st.checkbox("Display Data from Supabase PostgreSQL"):
    try:
        engine = create_engine(pg_url)
        query_pg = f"SELECT * FROM {table_name_pg}"
        result_df_pg = pd.read_sql(query_pg, engine)

        st.subheader(f"Data in {table_name_pg} Table (Supabase PostgreSQL)")
        st.write(result_df_pg)
    except Exception as e:
        st.error(f"An error occurred while fetching data: {e}")

# Add new row feature
st.header("Step 4: Add Data to the Supabase PostgreSQL Database")

if st.checkbox("Add a new row to the table"):
    new_data = {}
    for col in df.columns:
        new_data[col] = st.text_input(f"Enter value for {col}", "")

    if st.button("Add Data to Supabase PostgreSQL"):
        try:
            new_df = pd.DataFrame([new_data])
            new_df.to_sql(table_name_pg, engine, if_exists='append', index=False)
            st.success("New data added successfully to Supabase PostgreSQL")
        except Exception as e:
            st.error(f"An error occurred while adding data: {e}")
