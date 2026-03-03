import streamlit as st
import pandas as pd
from data_processing import load_data, preprocess_data
from model import train_model
from optimizer import simulate_factory_change

st.set_page_config(page_title="Factory Optimization", layout="wide")

st.title("🏭 Nassau Candy Factory Reallocation & Shipping Optimization")

# Load Data
data_path = "Nassau Candy Distributor.csv"
df = load_data(data_path)
df = preprocess_data(df)

st.write("### 📊 Dataset Overview")
st.write("Rows:", df.shape[0])
st.write("Columns:", df.shape[1])

# Train Model
model = train_model(df)

if model is None:
    st.error("Not enough data to train model.")
    st.stop()

# Sidebar Controls
st.sidebar.header("⚙ Optimization Controls")

product_list = df['Product Name'].unique()
selected_product = st.sidebar.selectbox("Select Product", product_list)

if st.sidebar.button("Run Optimization"):

    result = simulate_factory_change(df, model, selected_product)

    if result:

        current_lead_time, recommendations_df = result

        st.subheader("📈 Current Performance")
        st.metric("Average Lead Time", round(current_lead_time, 2))

        st.subheader("🏆 Factory Reallocation Recommendations")
        st.dataframe(recommendations_df)

        best_option = recommendations_df.iloc[0]

        st.success(
            f"✅ Recommended Factory: {best_option['Factory']} "
            f"with {best_option['Improvement %']}% improvement"
        )

    else:
        st.error("No data available for selected product.")

# KPI Section
st.subheader("📊 Key Performance Indicators")

col1, col2, col3 = st.columns(3)

col1.metric("Avg Lead Time", round(df['Lead_Time'].mean(), 2))
col2.metric("Avg Sales", round(df['Sales'].mean(), 2))
col3.metric("Avg Gross Profit", round(df['Gross Profit'].mean(), 2))
