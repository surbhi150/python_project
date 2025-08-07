import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    """Loads and cleans the CSV data into a DataFrame."""
    try:
        df = pd.read_csv('final_dataset.csv')
        # Clean column names
        df.columns = df.columns.str.strip().str.replace(r'\s+', '_', regex=True).str.replace(r'[^\w]', '', regex=True)
        return df
    except FileNotFoundError:
        st.error("Error: The file 'final_dataset.csv' was not found.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"An error occurred while loading the data: {e}")
        return pd.DataFrame()
