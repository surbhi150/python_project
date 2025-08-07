import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page config ---
st.set_page_config(page_title="Health Dashboard", layout="wide")
st.title("🚀 Health Center Data Visualizations")

# --- Load Data ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("final_dataset.csv")
        df.columns = df.columns.str.strip().str.replace(r"\s+", "_", regex=True)
        return df
    except Exception as e:
        st.error(f"Failed to load CSV: {e}")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.warning("❌ No data found. Check file name or content.")
else:
    st.success("✅ Data loaded successfully!")
    st.dataframe(df.head())

    st.markdown("---")

    # --- Chart 1: Top 10 States by Health Centers ---
    st.subheader("📊 Top 10 States by Health Centers")
    state_counts = df['State'].value_counts().reset_index()
    state_counts.columns = ['State', 'Count']
    fig1 = px.bar(state_counts.head(10), x='State', y='Count', color='Count',
                  title="Top 10 States with Most Health Centers",
                  template='plotly_white')
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("---")

    # --- Chart 2: Pie Chart by Operated_By ---
    st.subheader("🥧 Distribution by Operating Organization")
    op_counts = df['Operated_By'].value_counts().reset_index()
    op_counts.columns = ['Operated_By', 'Count']
    fig2 = px.pie(op_counts, names='Operated_By', values='Count', hole=0.4,
                  title='Health Centers Operated By')
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # --- Chart 3: Line Chart: Top 10 States ---
    st.subheader("📈 Line Chart: Health Centers in Top 10 States")
    fig3 = px.line(state_counts.head(10), x='State', y='Count', markers=True,
                   title="Line Chart: Top 10 States by Health Centers",
                   template='plotly_white')
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("---")

    # --- Chart 4: Total Hospitals by State ---
    st.subheader("🏥 Bar Chart: Health Centers by State")
    fig4 = px.bar(state_counts.sort_values(by='Count', ascending=False),
                  x='State', y='Count', color='Count',
                  title='Total Health Centers by State',
                  template='plotly_white')
    st.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")

    # --- Chart 5: Improved Bar Chart - Health Centers by Operating Organization ---
    st.subheader("🏥 Top Operating Organizations by Health Centers (Improved View)")

    top_ops = op_counts.sort_values(by='Count', ascending=False).head(8)
    fig5 = px.bar(
        top_ops,
        x='Count',
        y='Operated_By',
        orientation='h',
        color='Count',
        color_continuous_scale='Blues',
        title='Top 8 Operating Organizations by Number of Health Centers',
        template='plotly_white',
        text='Count'
    )

    fig5.update_layout(
        xaxis_title="Number of Health Centers",
        yaxis_title="Operating Organization",
        yaxis=dict(tickfont=dict(size=13)),
        margin=dict(t=60, b=40),
        height=500
    )

    fig5.update_traces(textposition='outside')
    st.plotly_chart(fig5, use_container_width=True)

    st.markdown("---")

    # --- Chart 6: Top 10 Districts (if exists) ---
    if 'District' in df.columns:
        st.subheader("📍 Top 10 Districts by Health Centers")
        dist_counts = df['District'].value_counts().reset_index()
        dist_counts.columns = ['District', 'Count']
        fig6 = px.bar(dist_counts.head(10), x='District', y='Count',
                      color='Count', title='Top 10 Districts with Most Health Centers',
                      template='plotly_white')
        st.plotly_chart(fig6, use_container_width=True)
        st.markdown("---")

    # --- Chart 7: Pie Chart of Health Centers in Top 5 States ---
    st.subheader("🍰 Pie Chart: Health Centers in Top 5 States")
    fig7 = px.pie(state_counts.head(5), names='State', values='Count',
                  title="Proportion of Health Centers in Top 5 States",
                  hole=0.3)
    st.plotly_chart(fig7, use_container_width=True)

    st.markdown("---")

    st.info("✅ Explore more insights by filtering or modifying the dataset as needed.")
