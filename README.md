
# ETL Process with Visualizations using Supabase PostgreSQL

This is a Streamlit-based application that performs an ETL (Extract, Transform, Load) process on a dataset, followed by data visualization. The app allows users to load data from a CSV file, clean and transform it, and store the processed data into a **Supabase PostgreSQL** database. Users can also visualize the data using various charts and add new data entries directly to the database.

## Features

### 1. **Extract**
- Load data from a CSV file.
- Preview the first few rows of the dataset.

### 2. **Transform**
- Drop rows with missing values.
- Rename columns as needed.
- Preview the transformed data.

### 3. **Visualize**
- Generate a **bar chart** for categorical data.
- Create a **line chart** for time-based data.
- Plot a **histogram** for numerical data.
- Display a **scatter plot** for two numerical columns.

### 4. **Load**
- Save the transformed data to a **Supabase PostgreSQL** database table (`mortality_data`).
- Fetch and display the data stored in the PostgreSQL database.

### 5. **Add Data**
- Insert new rows of data into the **Supabase PostgreSQL** database.

## Prerequisites

- Python 3.8+
- A Supabase PostgreSQL database
- A `.env` file with the following variables:

```bash
SUPABASE_DB_URL=postgresql://<USER>:<PASSWORD>@<HOST>:<PORT>/<DBNAME>
```

Replace `<USER>`, `<PASSWORD>`, `<HOST>`, `<PORT>`, and `<DBNAME>` with your Supabase credentials.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-repository/etl-streamlit-supabase.git
cd etl-streamlit-supabase
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory and add your Supabase connection URL:

```bash
SUPABASE_DB_URL=postgresql://<USER>:<PASSWORD>@<HOST>:<PORT>/<DBNAME>
```

4. Download the dataset you want to use (e.g., `IHME_GBD_2010_MORTALITY_AGE_SPECIFIC_BY_COUNTRY_1970_2010.csv`) and place it in the root folder or update the file path in the code.

## Running the App

1. Run the Streamlit app:

```bash
streamlit run app.py
```

2. Open your browser and go to the URL provided by Streamlit (usually `http://localhost:8501/`).

## How to Use

- **Extract**: Start by loading the CSV file, which is displayed in the "Dataset Preview" section.
- **Transform**: Use the transformation options to clean and rename the data.
- **Visualize**: Select a column to generate a bar chart, line chart, histogram, or scatter plot.
- **Load**: Once the data is cleaned, click the "Load Data into Supabase PostgreSQL" button to store it in the PostgreSQL database.
- **Display**: Fetch and display data stored in the `mortality_data` table by selecting the checkbox.
- **Add Data**: Add new rows to the table via input fields.

## Technologies Used

- **Streamlit**: A web framework for building interactive data-driven applications.
- **Pandas**: Used for data manipulation and analysis.
- **SQLAlchemy**: For connecting to the Supabase PostgreSQL database.
- **Matplotlib**: For creating visualizations.
- **Supabase**: PostgreSQL database for storing the transformed data.

