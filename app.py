import streamlit as st
import pandas as pd
import plotly.express as px

# ---------- Streamlit Page Config ----------
st.set_page_config(page_title="Health Centers Dashboard", layout="wide")

st.title("🏥 Health Centers Dashboard")

# ---------- Load and preprocess data ----------
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("final dataset.csv")  # Update if renamed
        df.columns = df.columns.str.strip().str.replace(" ", "_")
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        df.drop_duplicates(inplace=True)

        # ZIP split and area code
        df[['ZIP_5', 'ZIP_4']] = df['ZIP_Code'].str.split('-', expand=True)
        df['ZIP_5'] = pd.to_numeric(df['ZIP_5'], errors='coerce')
        df['ZIP_4'] = pd.to_numeric(df['ZIP_4'], errors='coerce')
        df['Area_Code'] = df['Telephone_Number'].str.extract(r'(\d{3})')
        df['Area_Code'] = pd.to_numeric(df['Area_Code'], errors='coerce')

        # Title case text columns
        text_cols = ['Health_Center_Name', 'Operated_By', 'Street_Address', 'City', 'State']
        df[text_cols] = df[text_cols].applymap(lambda x: x.title() if isinstance(x, str) else x)

        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

df = load_data()

# ---------- Show Data ----------
if df.empty:
    st.warning("No data loaded. Please check the file path or content.")
else:
    st.subheader("📋 Preview of Health Centers Data")
    st.dataframe(df.head(), use_container_width=True)

    # ---------- Example Plot ----------
    st.subheader("📍 Health Centers by State")
    state_count = df['State'].value_counts().reset_index()
    state_count.columns = ['State', 'Health Center Count']

    fig = px.bar(state_count, x='State', y='Health Center Count', color='State',
                 title="Number of Health Centers per State")
    st.plotly_chart(fig, use_container_width=True)
