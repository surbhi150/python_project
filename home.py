import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Configuration (MUST be first) ---
st.set_page_config(
    layout="wide", 
    page_title="🏥 Health Center Data Dashboard",
    page_icon="🏥",
    initial_sidebar_state="expanded"
)

# --- CSS Fix for Full Width Display ---
st.markdown("""
<style>
.main .block-container {
    max-width: 100%;
    padding-top: 1rem;
    padding-right: 1rem;
    padding-left: 1rem;
    padding-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

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

    # Performance improvement: limit default selections for large datasets
    default_states = states[:10] if len(states) > 10 else states
    
    selected_states = st.sidebar.multiselect("Select State(s)", options=states, default=default_states)
    selected_operated_by = st.sidebar.multiselect("Select Operated By", options=operated_by, default=operated_by)

    # --- Apply Filters ---
    filtered_df = df[
        (df['State'].isin(selected_states)) &
        (df['Operated_By'].isin(selected_operated_by))
    ]

    # --- Data Preview ---
    st.subheader("🔍 Filtered Data Preview")
    # Performance improvement: limit displayed rows for better loading
    display_df = filtered_df.head(1000) if len(filtered_df) > 1000 else filtered_df
    st.dataframe(display_df, use_container_width=True)
    
    if len(filtered_df) > 1000:
        st.info(f"Showing first 1000 rows of {len(filtered_df)} total records")

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
        # Ensure proper sizing
        fig_state.update_layout(height=500)
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
        # Ensure proper sizing
        fig_op.update_layout(height=500)
        st.plotly_chart(fig_op, use_container_width=True)
    else:
        st.info("No data to display for the selected 'Operated By' filter.")

    st.markdown("---")
    st.info("🎯 Adjust the filters in the sidebar to explore different parts of the data!")

else:
    st.warning("The dataset could not be loaded. Please check the file and try again.")
