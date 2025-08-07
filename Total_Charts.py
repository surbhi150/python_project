import streamlit as st
import plotly.express as px
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import load_data

# Load the data
def load_data():
    import pandas as pd
    df = pd.read_csv("final_dataset.csv")  # Or however you're loading the data
    return df

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



