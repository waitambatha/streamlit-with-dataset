
---

# Mortality Data Dashboard

## Overview

The Mortality Data Dashboard is a Streamlit application designed to visualize and analyze mortality data from different countries over time. This application allows users to interact with data through various functionalities, including data overview, country-wise trends, age group comparisons, and more. Additionally, users can add, modify, and delete records in the Supabase PostgreSQL database, and view the stored data directly within the app.

## Features

1. **Data Overview**: View a summary of the dataset.
2. **Country-wise Mortality Trends**: Visualize mortality trends for a selected country.
3. **Age Group Comparison**: Compare mortality rates across different age groups within a selected country.
4. **Top N Countries by Mortality**: Display the top N countries by number of deaths for the latest year.
5. **Gender-wise Mortality Trends**: View mortality trends based on gender.
6. **Mortality Distribution**: Visualize the distribution of mortality rates using a histogram.
7. **Custom Filters**: Apply filters to view data based on selected countries and age groups.
8. **Mortality Rank Tracking**: Track and view the mortality rank for selected countries and years.
9. **Yearly Changes Visualization**: Visualize changes in mortality rates over the years for selected countries.
10. **Download Report**: Download a CSV report for a selected country.
11. **Add New Data**: Insert new records into the database.
12. **Modify Existing Data**: Update existing records in the database.
13. **Delete Data**: Remove records from the database.
14. **Display Data**: View data stored in the Supabase PostgreSQL database.

## Installation

### Prerequisites

1. **Python 3.x**: Ensure that Python 3.x is installed on your system.
2. **Supabase PostgreSQL Database**: You need access to a Supabase PostgreSQL database. 

### Setup

1. **Clone the Repository**

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install Dependencies**

   Create a virtual environment and install the required packages:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**

   Create a `.env` file in the root directory and add your Supabase database URL:

   ```env
   SUPABASE_DB_URL=your_supabase_database_url
   ```

4. **Prepare the Database**

   Ensure the `mortality_data` table exists in your Supabase PostgreSQL database with the appropriate schema.

5. **Run the App**

   ```bash
   streamlit run app.py
   ```

## Usage

1. **Access the App**

   Open your web browser and navigate to `http://localhost:8501` to access the Streamlit application.

2. **Interact with the Dashboard**

   - Use the navigation headers to access different functionalities.
   - Apply filters, view trends, and visualize data as per your needs.
   - Use the forms to add, modify, or delete data in the database.

3. **Download Reports**

   Select a country and download the mortality report in CSV format.

