import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


# Page Configuration


st.set_page_config(
    page_title="Product Analysis",
    page_icon="📦",
    layout="wide"
)


# Load Dataset


BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_PATH = BASE_DIR / "data" / "processed" / "feature_engineered_dataset.csv"

df = pd.read_csv(DATA_PATH)


# Page Title


st.title("📦 Product Analysis Dashboard")
st.markdown("---")


# Product Summary


product_summary = (
    df.groupby("Product Name")
      .agg(
          Total_Sales=("Sales", "sum"),
          Total_Profit=("Gross Profit", "sum"),
          Total_Units=("Units", "sum"),
          Average_Lead_Time=("Shipping Lead Time", "mean"),
          Total_Orders=("Order ID", "count")
      )
      .reset_index()
)


# KPI Cards


total_products = product_summary["Product Name"].nunique()
total_sales = df["Sales"].sum()
total_profit = df["Gross Profit"].sum()
total_units = df["Units"].sum()
avg_profit = product_summary["Total_Profit"].mean()

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("📦 Products", total_products)

with col2:
    st.metric("💰 Sales", f"${total_sales:,.0f}")

with col3:
    st.metric("📈 Profit", f"${total_profit:,.0f}")

with col4:
    st.metric("📊 Units Sold", f"{int(total_units):,}")

with col5:
    st.metric("⭐ Avg Profit/Product", f"${avg_profit:,.0f}")

st.markdown("---")


# Top 10 Products by Sales


top_sales_products = (
    product_summary
    .sort_values(by="Total_Sales", ascending=False)
    .head(10)
)

fig_sales = px.bar(
    top_sales_products,
    x="Total_Sales",
    y="Product Name",
    orientation="h",
    text="Total_Sales",
    color="Total_Sales",
    title="💰 Top 10 Products by Sales"
)

fig_sales.update_layout(
    yaxis=dict(categoryorder="total ascending")
)


# Top 10 Products by Profit


top_profit_products = (
    product_summary
    .sort_values(by="Total_Profit", ascending=False)
    .head(10)
)

fig_profit = px.bar(
    top_profit_products,
    x="Total_Profit",
    y="Product Name",
    orientation="h",
    text="Total_Profit",
    color="Total_Profit",
    title="📈 Top 10 Products by Profit"
)

fig_profit.update_layout(
    yaxis=dict(categoryorder="total ascending")
)

left_col, right_col = st.columns(2)

with left_col:
    st.plotly_chart(fig_sales, use_container_width=True)

with right_col:
    st.plotly_chart(fig_profit, use_container_width=True)

st.markdown("---")


# Top Products by Units Sold


top_units_products = (
    product_summary
    .sort_values(by="Total_Units", ascending=False)
    .head(10)
)

fig_units = px.bar(
    top_units_products,
    x="Product Name",
    y="Total_Units",
    text="Total_Units",
    color="Total_Units",
    title="📦 Top 10 Products by Units Sold"
)

st.plotly_chart(fig_units, use_container_width=True)

st.markdown("---")


# Bottom 10 Products by Sales

bottom_sales_products = (
    product_summary
    .sort_values(by="Total_Sales", ascending=True)
    .head(10)
)

fig_bottom_sales = px.bar(
    bottom_sales_products,
    x="Total_Sales",
    y="Product Name",
    orientation="h",
    text="Total_Sales",
    color="Total_Sales",
    title="📉 Bottom 10 Products by Sales"
)

fig_bottom_sales.update_layout(
    yaxis=dict(categoryorder="total descending")
)

st.plotly_chart(fig_bottom_sales, use_container_width=True)

st.markdown("---")


# Profit Margin Analysis


product_summary["Profit_Margin"] = (
    product_summary["Total_Profit"] /
    product_summary["Total_Sales"]
) * 100

product_summary["Profit_Margin"] = (
    product_summary["Profit_Margin"]
    .fillna(0)
    .round(2)
)

top_margin_products = (
    product_summary
    .sort_values(by="Profit_Margin", ascending=False)
    .head(10)
)

fig_margin = px.bar(
    top_margin_products,
    x="Profit_Margin",
    y="Product Name",
    orientation="h",
    text="Profit_Margin",
    color="Profit_Margin",
    title="💹 Top 10 Products by Profit Margin (%)"
)

fig_margin.update_layout(
    yaxis=dict(categoryorder="total ascending")
)

st.plotly_chart(fig_margin, use_container_width=True)

st.markdown("---")


# Product Performance Scatter Plot


fig_scatter = px.scatter(
    product_summary,
    x="Total_Sales",
    y="Total_Profit",
    size="Total_Units",
    color="Profit_Margin",
    hover_name="Product Name",
    title="📊 Product Performance (Sales vs Profit)"
)

st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("---")


# Product Performance Summary Table


st.subheader("📋 Product Performance Summary")

summary_table = (
    product_summary
    .sort_values(by="Total_Sales", ascending=False)
)

st.dataframe(
    summary_table,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")


# Download Report


csv = summary_table.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Product Analysis Report (CSV)",
    data=csv,
    file_name="product_analysis_report.csv",
    mime="text/csv"
)

st.markdown("---")


# Best & Worst Performing Products


highest_sales_product = (
    product_summary
    .sort_values(by="Total_Sales", ascending=False)
    .iloc[0]
)

highest_profit_product = (
    product_summary
    .sort_values(by="Total_Profit", ascending=False)
    .iloc[0]
)

highest_units_product = (
    product_summary
    .sort_values(by="Total_Units", ascending=False)
    .iloc[0]
)

lowest_sales_product = (
    product_summary
    .sort_values(by="Total_Sales", ascending=True)
    .iloc[0]
)


# Business Insights


st.subheader("💡 Business Insights")

col1, col2 = st.columns(2)

with col1:

    st.success(
        f"""
### 🏆 Highest Selling Product

**{highest_sales_product['Product Name']}**

💰 Sales : **${highest_sales_product['Total_Sales']:,.0f}**
"""
    )

    st.info(
        f"""
### 📈 Highest Profit Product

**{highest_profit_product['Product Name']}**

💵 Profit : **${highest_profit_product['Total_Profit']:,.0f}**
"""
    )

with col2:

    st.warning(
        f"""
### 📦 Most Sold Product

**{highest_units_product['Product Name']}**

Units Sold : **{int(highest_units_product['Total_Units']):,}**
"""
    )

    st.error(
        f"""
### 📉 Lowest Selling Product

**{lowest_sales_product['Product Name']}**

💰 Sales : **${lowest_sales_product['Total_Sales']:,.0f}**
"""
    )

st.markdown("---")


# Key Product Statistics


st.subheader("📊 Key Product Statistics")

stats_col1, stats_col2, stats_col3 = st.columns(3)

with stats_col1:
    st.metric(
        "Average Sales per Product",
        f"${product_summary['Total_Sales'].mean():,.0f}"
    )

with stats_col2:
    st.metric(
        "Average Profit per Product",
        f"${product_summary['Total_Profit'].mean():,.0f}"
    )

with stats_col3:
    st.metric(
        "Average Units per Product",
        f"{product_summary['Total_Units'].mean():,.1f}"
    )

st.markdown("---")


# Dashboard Footer


st.caption(
    "Factory Shipping Route Efficiency Analysis | Product Analysis Dashboard | Developed using Streamlit & Plotly"
)