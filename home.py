import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Configuration ---
st.set_page_config(layout="wide", page_title="🏥 Health Center Data Dashboard")

# --- Load Data Function with Caching ---
@st.cache_data
def load_data(file_path):
    """Loads and cleans the CSV data into a DataFrame."""
    try:
        df = pd.read_csv(file_path)
        # Clean column names
        df.columns = df.columns.str.strip().str.replace(r'\s+', '_', regex=True).str.replace(r'[^\w]', '', regex=True)
        return df
    except FileNotFoundError:
        st.error(f"Error: The file '{file_path}' was not found.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"An error occurred while loading the data: {e}")
        return pd.DataFrame()

# --- Load the dataset ---
with st.spinner("Loading Health Center Data..."):
    df = load_data('final_dataset.csv')

# --- If data is loaded ---
if not df.empty:
    st.title("🏥 Health Center Data Dashboard")

    # --- Sidebar Filters ---
    st.sidebar.header("Filter Options")
    states = sorted(df['State'].dropna().unique())
    operated_by = sorted(df['Operated_By'].dropna().unique())

    selected_states = st.sidebar.multiselect("Select State(s)", options=states, default=states)
    selected_operated_by = st.sidebar.multiselect("Select Operated By", options=operated_by, default=operated_by)

    # --- Apply Filters ---
    filtered_df = df[
        (df['State'].isin(selected_states)) &
        (df['Operated_By'].isin(selected_operated_by))
    ]

    # --- Data Preview ---
    st.subheader("🔍 Filtered Data Preview")
    st.dataframe(filtered_df, use_container_width=True)

    # --- Download Button ---
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Filtered Data as CSV", csv, "filtered_health_centers.csv", "text/csv")

    st.markdown("---")

    # --- Bar Chart: Centers per State ---
    st.subheader("📊 Number of Health Centers per State")
    if not filtered_df.empty:
        state_counts = filtered_df['State'].value_counts().reset_index()
        state_counts.columns = ['State', 'Count']
        fig_state = px.bar(
            state_counts,
            x='State',
            y='Count',
            title='Health Centers by State',
            labels={'Count': 'Number of Health Centers'},
            color='Count',
            template='plotly_white'
        )
        st.plotly_chart(fig_state, use_container_width=True)
    else:
        st.info("No data to display for the selected State filter.")

    st.markdown("---")

    # --- Bar Chart: Centers by Operated By ---
    st.subheader("📊 Number of Health Centers by Operating Organization")
    if not filtered_df.empty:
        op_counts = filtered_df['Operated_By'].value_counts().reset_index()
        op_counts.columns = ['Operated_By', 'Count']
        fig_op = px.bar(
            op_counts,
            x='Operated_By',
            y='Count',
            title='Health Centers by Operating Body',
            labels={'Count': 'Number of Health Centers'},
            color='Count',
            template='plotly_white'
        )
        st.plotly_chart(fig_op, use_container_width=True)
    else:
        st.info("No data to display for the selected 'Operated By' filter.")

    st.markdown("---")
    st.info("🎯 Adjust the filters in the sidebar to explore different parts of the data!")

else:
    st.warning("The dataset could not be loaded. Please check the file and try again.")
