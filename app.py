import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Database connection setup
SUPABASE_DB_URL = os.getenv('SUPABASE_DB_URL')
engine = create_engine(SUPABASE_DB_URL)


def load_data():
    # Load the data from the Supabase PostgreSQL database into a DataFrame
    query = "SELECT * FROM mortality_data;"
    df = pd.read_sql(query, engine)

    # Convert relevant columns to numeric
    df['Number of Deaths'] = pd.to_numeric(df['Number of Deaths'], errors='coerce')
    df['Death Rate Per 100,000'] = pd.to_numeric(df['Death Rate Per 100,000'], errors='coerce')

    return df


# Load data
data = load_data()

# Functionality 1: Data Overview
st.title("Mortality Data Dashboard")
st.header("1. Data Overview")
st.write(data.head())

# Functionality 2: Country-wise Mortality Trends
st.header("2. Country-wise Mortality Trends")
country = st.selectbox('Select a Country', data['Country Name'].unique())
yearly_data = data[data['Country Name'] == country]

# Ensure the lengths of x and y are consistent before plotting
if not yearly_data.empty:
    st.subheader(f"Mortality Trends in {country}")
    plt.figure(figsize=(10, 5))
    plt.plot(yearly_data['Year'], yearly_data['Number of Deaths'], marker='o')
    plt.title(f'Mortality Trends in {country}')
    plt.xlabel('Year')
    plt.ylabel('Mortality Rate')
    st.pyplot(plt)
else:
    st.warning(f"No data available for {country}.")

# Functionality 3: Age Group Comparison
st.header("3. Age Group Comparison")
age_groups = data['Age Group'].unique()
selected_age_group = st.selectbox('Select Age Group', age_groups)
age_group_data = data[(data['Country Name'] == country) & (data['Age Group'] == selected_age_group)]

# Ensure the lengths of x and y are consistent before plotting
if not age_group_data.empty:
    st.subheader(f"Mortality Rates for {selected_age_group} in {country}")
    plt.figure(figsize=(10, 5))
    plt.bar(age_group_data['Year'], age_group_data['Number of Deaths'], color='skyblue')
    plt.title(f'Mortality Rates for {selected_age_group} in {country}')
    plt.xlabel('Year')
    plt.ylabel('Number of Deaths')
    st.pyplot(plt)
else:
    st.warning(f"No data available for {selected_age_group} in {country}.")

# Functionality 4: Top N Countries by Mortality
st.header("4. Top N Countries by Mortality")

# Convert 'Number of Deaths' to numeric, forcing errors to NaN (if any)
data['Number of Deaths'] = pd.to_numeric(data['Number of Deaths'], errors='coerce')

# Use a slider to select the number of top countries to display
n_countries = st.slider('Select number of countries', 1, 10, 5)

# Find the latest year in the data
latest_year = data['Year'].max()

# Filter the data for the latest year and find the top N countries by number of deaths
top_countries = data[data['Year'] == latest_year].nlargest(n_countries, 'Number of Deaths')

# Display the result
st.write(top_countries)

# Ensure there is data before plotting
if not top_countries.empty:
    st.subheader(f'Top {n_countries} Countries by Mortality in {latest_year}')
    plt.figure(figsize=(10, 5))
    plt.bar(top_countries['Country Name'], top_countries['Number of Deaths'], color='green')
    plt.title(f'Top {n_countries} Countries by Mortality in {latest_year}')
    plt.xlabel('Country Name')
    plt.ylabel('Number of Deaths')
    plt.xticks(rotation=45)
    st.pyplot(plt)
else:
    st.warning(f"No data available for top {n_countries} countries in {latest_year}.")

# Functionality 5: Gender-wise Mortality Trends
st.header("5. Gender-wise Mortality Trends")
selected_gender = st.radio('Select Gender', ['Male', 'Female'])
gender_data = data[(data['Country Name'] == country) & (data['Sex'] == selected_gender)]

# Ensure the lengths of x and y are consistent before plotting
if not gender_data.empty:
    st.subheader(f'{selected_gender} Mortality Trends in {country}')
    plt.figure(figsize=(10, 5))
    plt.plot(gender_data['Year'], gender_data['Number of Deaths'], marker='o', color='red')
    plt.title(f'{selected_gender} Mortality Trends in {country}')
    plt.xlabel('Year')
    plt.ylabel('Number of Deaths')
    st.pyplot(plt)
else:
    st.warning(f"No data available for {selected_gender} in {country}.")

# Functionality 6: Mortality Distribution
st.header("6. Distribution of Mortality Rates")
st.subheader("Mortality Rate Histogram")
plt.figure(figsize=(10, 5))
plt.hist(data['Number of Deaths'], bins=50, color='purple')
plt.title('Distribution of Mortality Rates')
plt.xlabel('Mortality Rate')
plt.ylabel('Frequency')
st.pyplot(plt)

# Functionality 7: Custom Filters
st.header("7. Custom Filters")
filter_country = st.multiselect('Select Country', data['Country Name'].unique())
filter_age_group = st.multiselect('Select Age Group', data['Age Group'].unique())
filtered_data = data[data['Country Name'].isin(filter_country) & data['Age Group'].isin(filter_age_group)]
st.write(filtered_data)

# Functionality 8: Mortality Rank Tracking
st.header("8. Mortality Rank Tracking")
rank_year = st.slider('Select Year for Ranking', int(data['Year'].min()), int(data['Year'].max()), step=1)
rank_data = data[data['Year'] == rank_year].sort_values('Number of Deaths', ascending=False)
st.write(rank_data[['Country Name', 'Number of Deaths']])

# Functionality 9: Yearly Changes Visualization
st.header("9. Yearly Changes in Mortality Rates")
filtered_year_data = data[(data['Country Name'].isin(filter_country)) & (data['Year'].isin(filtered_data['Year']))]

# Using Matplotlib for grouped bar chart
plt.figure(figsize=(10, 5))
for country in filter_country:
    country_data = filtered_year_data[filtered_year_data['Country Name'] == country]
    plt.bar(country_data['Year'], country_data['Number of Deaths'], label=country)
plt.title("Yearly Mortality Rate Changes for Selected Countries")
plt.xlabel('Year')
plt.ylabel('Mortality Rate')
plt.legend()
st.pyplot(plt)

# Functionality 10: Download Country-wise Mortality Report
st.header("10. Download Country-wise Mortality Report")


def generate_report(country):
    report_data = data[data['Country Name'] == country]
    return report_data.to_csv(index=False)


selected_country_report = st.selectbox('Select Country for Report', data['Country Name'].unique())
st.download_button(label="Download Report", data=generate_report(selected_country_report),
                   file_name=f"{selected_country_report}_mortality_report.csv")

# Functionality 11: Add New Data
st.header("11. Add New Data")
with st.form(key='add_data_form'):
    country_code = st.text_input('Country Code')
    country_name = st.text_input('Country Name')
    year = st.number_input('Year', min_value=1970, max_value=2010)
    age_group = st.text_input('Age Group')
    sex = st.radio('Sex', ['Male', 'Female'])
    number_of_deaths = st.number_input('Number of Deaths')
    death_rate = st.number_input('Death Rate Per 100,000')

    submit_button = st.form_submit_button(label='Add Data')

    if submit_button:
        new_data = {
            'Country Code': country_code,
            'Country Name': country_name,
            'Year': year,
            'Age Group': age_group,
            'Sex': sex,
            'Number of Deaths': number_of_deaths,
            'Death Rate Per 100,000': death_rate
        }
        df_new = pd.DataFrame([new_data])
        df_new.to_sql('mortality_data', engine, if_exists='append', index=False)
        st.success('Data added successfully!')
        data = load_data()  # Reload data

# Functionality 12: Modify Existing Data
st.header("12. Modify Existing Data")
with st.form(key='modify_data_form'):
    modify_country = st.selectbox('Select Country to Modify', data['Country Name'].unique())
    modify_year = st.number_input('Select Year to Modify', min_value=1970, max_value=2010)
    modify_age_group = st.text_input('Age Group to Modify')
    modify_sex = st.radio('Sex to Modify', ['Male', 'Female'])
    modify_number_of_deaths = st.number_input('New Number of Deaths')
    modify_death_rate = st.number_input('New Death Rate Per 100,000')

    modify_button = st.form_submit_button(label='Modify Data')

    if modify_button:
        update_query = f"""
        UPDATE mortality_data
        SET "Number of Deaths" = {modify_number_of_deaths},
            "Death Rate Per 100,000" = {modify_death_rate}
        WHERE "Country Name" = '{modify_country}' AND
              "Year" = {modify_year} AND
              "Age Group" = '{modify_age_group}' AND
              "Sex" = '{modify_sex}';
        """
        with engine.connect() as connection:
            connection.execute(update_query)
        st.success('Data modified successfully!')
        data = load_data()  # Reload data

# Functionality 13: Delete Data
st.header("13. Delete Data")
with st.form(key='delete_data_form'):
    delete_country = st.selectbox('Select Country to Delete Data', data['Country Name'].unique())
    delete_year = st.number_input('Select Year to Delete Data', min_value=1970, max_value=2010)
    delete_age_group = st.text_input('Age Group to Delete')
    delete_sex = st.radio('Sex to Delete', ['Male', 'Female'])

    delete_button = st.form_submit_button(label='Delete Data')

    if delete_button:
        delete_query = f"""
        DELETE FROM mortality_data
        WHERE "Country Name" = '{delete_country}' AND
              "Year" = {delete_year} AND
              "Age Group" = '{delete_age_group}' AND
              "Sex" = '{delete_sex}';
        """
        with engine.connect() as connection:
            connection.execute(delete_query)
        st.success('Data deleted successfully!')
        data = load_data()  # Reload data

# Functionality 14: View Data from Database
st.header("14. View Data from Database")
view_data = st.selectbox('Select Data to View', ['All Data', 'Filtered Data'])
if view_data == 'All Data':
    st.write(data)
elif view_data == 'Filtered Data':
    filter_country = st.multiselect('Select Country', data['Country Name'].unique())
    filter_age_group = st.multiselect('Select Age Group', data['Age Group'].unique())
    filtered_data = data[data['Country Name'].isin(filter_country) & data['Age Group'].isin(filter_age_group)]
    st.write(filtered_data)
