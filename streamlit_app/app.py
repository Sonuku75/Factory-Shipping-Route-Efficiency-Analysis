import streamlit as st
import pandas as pd



# Page Configuration

st.set_page_config(
    page_title="Factory Shipping Dashboard",
    page_icon="🚚",
    layout="wide"
)


# Load Dataset

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "processed" / "feature_engineered_dataset.csv"

df = pd.read_csv(DATA_PATH)

# =====================================================
# Sidebar Filters
# =====================================================

st.sidebar.header("🔍 Dashboard Filters")

selected_region = st.sidebar.multiselect(
    "Select Region",
    options=sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

selected_ship_mode = st.sidebar.multiselect(
    "Select Ship Mode",
    options=sorted(df["Ship Mode"].unique()),
    default=sorted(df["Ship Mode"].unique())
)

filtered_df = df[
    (df["Region"].isin(selected_region)) &
    (df["Ship Mode"].isin(selected_ship_mode))
]


# Dashboard Title

st.title("🚚 Factory Shipping Route Efficiency Dashboard")

st.markdown("---")


# KPI Calculations

total_shipments = len(filtered_df)
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Gross Profit"].sum()
avg_lead_time = filtered_df["Shipping Lead Time"].mean()


# KPI Cards

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📦 Total Shipments", f"{total_shipments:,}")

with col2:
    st.metric("💰 Total Sales", f"${total_sales:,.2f}")

with col3:
    st.metric("📈 Total Profit", f"${total_profit:,.2f}")

with col4:
    st.metric("🚚 Avg Lead Time", f"{avg_lead_time:.2f} Days")

st.markdown("---")


# Sales by Region


import plotly.express as px

sales_region = (
    filtered_df.groupby("Region")["Sales"]
      .sum()
      .reset_index()
      .sort_values(by="Sales", ascending=False)
)

fig = px.bar(
    sales_region,
    x="Region",
    y="Sales",
    text="Sales",
    title="Sales by Region"
)


# Sales by Region


sales_region = (
    filtered_df.groupby("Region")["Sales"]
      .sum()
      .reset_index()
      .sort_values(by="Sales", ascending=False)
)


# Profit by Region


profit_region = (
    filtered_df.groupby("Region")["Gross Profit"]
      .sum()
      .reset_index()
      .sort_values(by="Gross Profit", ascending=False)
)

left_col, right_col = st.columns(2)

with left_col:

    fig_sales = px.bar(
        sales_region,
        x="Region",
        y="Sales",
        text="Sales",
        title="📊 Sales by Region"
    )

    st.plotly_chart(fig_sales, use_container_width=True)

with right_col:

    fig_profit = px.pie(
        profit_region,
        names="Region",
        values="Gross Profit",
        title="🥧 Profit Distribution by Region",
        hole=0.45
    )

    st.plotly_chart(fig_profit, use_container_width=True)
    
# Ship Mode Analysis


ship_mode_summary = (
    filtered_df.groupby("Ship Mode")
      .agg(
          Total_Shipments=("Ship Mode", "count"),
          Average_Lead_Time=("Shipping Lead Time", "mean")
      )
      .reset_index()
)

st.markdown("---")

left_col, right_col = st.columns(2)


# Shipments by Ship Mode


with left_col:

    fig_shipments = px.bar(
        ship_mode_summary,
        x="Ship Mode",
        y="Total_Shipments",
        text="Total_Shipments",
        title="📦 Shipments by Ship Mode"
    )

    st.plotly_chart(fig_shipments, use_container_width=True)


# Average Lead Time


with right_col:

    fig_lead = px.bar(
        ship_mode_summary,
        x="Ship Mode",
        y="Average_Lead_Time",
        text="Average_Lead_Time",
        title="🚚 Average Lead Time by Ship Mode"
    )

    st.plotly_chart(fig_lead, use_container_width=True)
    
    
# Top Products and Top Routes

st.markdown("---")

# Top 10 Products

top_products = (
    filtered_df.groupby("Product Name")["Sales"]
      .sum()
      .reset_index()
      .sort_values(by="Sales", ascending=False)
      .head(10)
)

# Top 10 Routes


top_routes = (
    filtered_df.groupby("Factory_to_State")
      .agg(
          Total_Sales=("Sales", "sum")
      )
      .reset_index()
      .sort_values(by="Total_Sales", ascending=False)
      .head(10)
)

left_col, right_col = st.columns(2)

# Top Products Chart

with left_col:

    fig_products = px.bar(
        top_products,
        x="Sales",
        y="Product Name",
        orientation="h",
        text="Sales",
        title="📦 Top 10 Products by Sales"
    )

    st.plotly_chart(fig_products, use_container_width=True)

# Top Routes Chart


with right_col:

    fig_routes = px.bar(
        top_routes,
        x="Total_Sales",
        y="Factory_to_State",
        orientation="h",
        text="Total_Sales",
        title="🛣️ Top 10 Factory Routes"
    )

    st.plotly_chart(fig_routes, use_container_width=True)
    
# Download Filtered Data


st.markdown("---")

st.subheader("📥 Download Filtered Dataset")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇ Download CSV",
    data=csv,
    file_name="filtered_shipping_data.csv",
    mime="text/csv"
)


# Project Summary


st.markdown("---")

st.subheader("📋 Dashboard Summary")

col1, col2 = st.columns(2)

with col1:
    st.info("""
### Key Highlights

- Total Shipments Analysed
- Route Efficiency Evaluated
- Regional Sales Comparison
- Ship Mode Performance
- Product Sales Analysis
""")

with col2:
    st.success("""
### Technologies Used

- Python
- Pandas
- Plotly
- Streamlit
""")