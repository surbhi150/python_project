import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Configuration (MUST be first) ---
st.set_page_config(
    page_title="🏥 Health Center Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS for Full Width ---
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

# --- Navigation ---
def main():
    # Sidebar Navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a page", ["Home", "Explore Data", "Total Charts"])
    
    # Load data once
    with st.spinner("Loading Health Center Data..."):
        df = load_data('final_dataset.csv')
    
    if df.empty:
        st.error("Dataset could not be loaded. Please check the file path.")
        return
    
    # Page routing
    if page == "Home":
        show_home_page(df)
    elif page == "Explore Data":
        show_explore_data_page(df)
    elif page == "Total Charts":
        show_total_charts_page(df)

def show_home_page(df):
    st.title("🏥 Health Center Data Dashboard")
    
    # --- Sidebar Filters ---
    st.sidebar.header("Filter Options")
    states = sorted(df['State'].dropna().unique())
    operated_by = sorted(df['Operated_By'].dropna().unique())

    selected_states = st.sidebar.multiselect("Select State(s)", options=states, default=states[:5])  # Limit default selection
    selected_operated_by = st.sidebar.multiselect("Select Operated By", options=operated_by, default=operated_by)

    # --- Apply Filters ---
    filtered_df = df[
        (df['State'].isin(selected_states)) &
        (df['Operated_By'].isin(selected_operated_by))
    ]

    # --- Data Preview ---
    st.subheader("🔍 Filtered Data Preview")
    st.dataframe(filtered_df.head(100), use_container_width=True)  # Limit rows for performance

    # --- Download Button ---
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Filtered Data as CSV", csv, "filtered_health_centers.csv", "text/csv")

    st.markdown("---")

    # --- Charts in Columns ---
    col1, col2 = st.columns(2)
    
    with col1:
        # --- Bar Chart: Centers per State ---
        st.subheader("📊 Health Centers per State")
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

    with col2:
        # --- Bar Chart: Centers by Operated By ---
        st.subheader("📊 Health Centers by Organization")
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

def show_explore_data_page(df):
    st.title("🔍 Explore Data")
    
    # Basic info
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Records", len(df))
    with col2:
        st.metric("Total States", df['State'].nunique())
    with col3:
        st.metric("Total Organizations", df['Operated_By'].nunique())
    
    st.markdown("---")
    
    # Data exploration
    st.subheader("Dataset Overview")
    st.dataframe(df.describe(), use_container_width=True)
    
    st.subheader("Sample Data")
    st.dataframe(df.head(20), use_container_width=True)

def show_total_charts_page(df):
    st.title("📈 Visual Analysis: Max Chart")

    # --- Sidebar ---
    with st.sidebar:
        st.write("👇 Click below to display chart with highest counts")
        show_chart = st.button("Show Max Health Centers Chart")

    # --- Show Charts ---
    if show_chart:
        # --- Bar Chart ---
        st.subheader("🏆 Top 10 States with Max Health Centers")
        state_counts = df['State'].value_counts().reset_index()
        state_counts.columns = ['State', 'Health Center Count']
        fig_bar = px.bar(
            state_counts.head(10),
            x='State',
            y='Health Center Count',
            color='Health Center Count',
            title="Top 10 States by Health Centers",
            color_continuous_scale="viridis",
            template="plotly_white"
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown("---")

        # --- Pie Chart ---
        st.subheader("🥧 Pie Chart: Distribution of Health Centers by 'Operated By'")
        pie_data = df['Operated_By'].value_counts().reset_index()
        pie_data.columns = ['Operated_By', 'Count']
        fig_pie = px.pie(
            pie_data,
            names='Operated_By',
            values='Count',
            title='Health Centers by Operating Organization',
            hole=0.4
        )
        st.plotly_chart(fig_pie, use_container_width=True)

        st.markdown("---")

        # --- Heatmap ---
        st.subheader("🌡️ Correlation Heatmap of Numerical Columns")
        numeric_df = df.select_dtypes(include='number')

        if not numeric_df.empty and len(numeric_df.columns) >= 2:
            corr_matrix = numeric_df.corr().round(2)
            fig_heatmap = px.imshow(
                corr_matrix,
                text_auto=True,
                color_continuous_scale='RdBu_r',
                title="Correlation Heatmap",
                aspect="auto"
            )
            st.plotly_chart(fig_heatmap, use_container_width=True)
        else:
            st.warning("Not enough numerical columns in the data to display a heatmap.")
    else:
        st.info("Click the button in the sidebar to display the charts.")

if __name__ == "__main__":
    main()
