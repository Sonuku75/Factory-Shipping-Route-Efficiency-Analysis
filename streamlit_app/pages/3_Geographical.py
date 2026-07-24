import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


# Page Configuration


st.set_page_config(
    page_title="Geographical Analysis",
    page_icon="🌍",
    layout="wide"
)


# Load Dataset


BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_PATH = BASE_DIR / "data" / "processed" / "feature_engineered_dataset.csv"

df = pd.read_csv(DATA_PATH)


# Page Title


st.title("🌍 Geographical Analysis Dashboard")
st.markdown("---")


# State Summary


state_summary = (
    df.groupby("State/Province")
      .agg(
          Total_Sales=("Sales", "sum"),
          Total_Profit=("Gross Profit", "sum"),
          Average_Lead_Time=("Shipping Lead Time", "mean"),
          Total_Orders=("Order ID", "count")
      )
      .reset_index()
)


# Factory Summary


factory_summary = (
    df.groupby("Factory")
      .agg(
          Total_Sales=("Sales", "sum"),
          Total_Profit=("Gross Profit", "sum"),
          Average_Lead_Time=("Shipping Lead Time", "mean"),
          Total_Orders=("Order ID", "count")
      )
      .reset_index()
)


# Region Summary


region_summary = (
    df.groupby("Region")
      .agg(
          Total_Sales=("Sales", "sum"),
          Total_Profit=("Gross Profit", "sum"),
          Average_Lead_Time=("Shipping Lead Time", "mean"),
          Total_Orders=("Order ID", "count")
      )
      .reset_index()
)


# KPI Cards


total_states = state_summary["State/Province"].nunique()
total_factories = factory_summary["Factory"].nunique()
total_sales = df["Sales"].sum()
total_profit = df["Gross Profit"].sum()
avg_lead = df["Shipping Lead Time"].mean()

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("🌍 States", total_states)

with col2:
    st.metric("🏭 Factories", total_factories)

with col3:
    st.metric("💰 Sales", f"${total_sales:,.0f}")

with col4:
    st.metric("📈 Profit", f"${total_profit:,.0f}")

with col5:
    st.metric("🚚 Avg Lead Time", f"{avg_lead:.2f} Days")

st.markdown("---")


# Top States by Sales


top_sales_states = (
    state_summary.sort_values(
        by="Total_Sales",
        ascending=False
    )
    .head(10)
)

fig_sales = px.bar(
    top_sales_states,
    x="Total_Sales",
    y="State/Province",
    orientation="h",
    text="Total_Sales",
    color="Total_Sales",
    title="💰 Top 10 States by Sales"
)

fig_sales.update_layout(yaxis=dict(categoryorder="total ascending"))


# Top States by Profit


top_profit_states = (
    state_summary.sort_values(
        by="Total_Profit",
        ascending=False
    )
    .head(10)
)

fig_profit = px.bar(
    top_profit_states,
    x="Total_Profit",
    y="State/Province",
    orientation="h",
    text="Total_Profit",
    color="Total_Profit",
    title="📈 Top 10 States by Profit"
)

fig_profit.update_layout(yaxis=dict(categoryorder="total ascending"))

left_col, right_col = st.columns(2)

with left_col:
    st.plotly_chart(fig_sales, use_container_width=True)

with right_col:
    st.plotly_chart(fig_profit, use_container_width=True)

st.markdown("---")


# Factory Analysis


top_factory_sales = (
    factory_summary
    .sort_values(by="Total_Sales", ascending=False)
    .head(10)
)

top_factory_profit = (
    factory_summary
    .sort_values(by="Total_Profit", ascending=False)
    .head(10)
)

fig_factory_sales = px.bar(
    top_factory_sales,
    x="Factory",
    y="Total_Sales",
    text="Total_Sales",
    color="Total_Sales",
    title="🏭 Top Factories by Sales"
)

fig_factory_profit = px.bar(
    top_factory_profit,
    x="Factory",
    y="Total_Profit",
    text="Total_Profit",
    color="Total_Profit",
    title="📈 Top Factories by Profit"
)

left_col, right_col = st.columns(2)

with left_col:
    st.plotly_chart(fig_factory_sales, use_container_width=True)

with right_col:
    st.plotly_chart(fig_factory_profit, use_container_width=True)

st.markdown("---")


# Region Analysis


fig_region_sales = px.pie(
    region_summary,
    names="Region",
    values="Total_Sales",
    hole=0.45,
    title="🌎 Sales Distribution by Region"
)

fig_region_profit = px.pie(
    region_summary,
    names="Region",
    values="Total_Profit",
    hole=0.45,
    title="💰 Profit Distribution by Region"
)

left_col, right_col = st.columns(2)

with left_col:
    st.plotly_chart(fig_region_sales, use_container_width=True)

with right_col:
    st.plotly_chart(fig_region_profit, use_container_width=True)

st.markdown("---")


# Average Shipping Lead Time by Region


fig_lead = px.bar(
    region_summary.sort_values(
        by="Average_Lead_Time",
        ascending=False
    ),
    x="Region",
    y="Average_Lead_Time",
    text="Average_Lead_Time",
    color="Average_Lead_Time",
    title="🚚 Average Shipping Lead Time by Region"
)

st.plotly_chart(fig_lead, use_container_width=True)

st.markdown("---")


# Summary Table


st.subheader("📋 State-wise Performance Summary")

summary_table = (
    state_summary.sort_values(
        by="Total_Sales",
        ascending=False
    )
)

st.dataframe(
    summary_table,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")


# Download Summary


csv = summary_table.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Geographical Report (CSV)",
    data=csv,
    file_name="geographical_analysis_report.csv",
    mime="text/csv"
)

st.markdown("---")


# Top Performing States


highest_sales_state = (
    state_summary.sort_values(
        by="Total_Sales",
        ascending=False
    )
    .iloc[0]
)

highest_profit_state = (
    state_summary.sort_values(
        by="Total_Profit",
        ascending=False
    )
    .iloc[0]
)

fastest_state = (
    state_summary.sort_values(
        by="Average_Lead_Time",
        ascending=True
    )
    .iloc[0]
)

slowest_state = (
    state_summary.sort_values(
        by="Average_Lead_Time",
        ascending=False
    )
    .iloc[0]
)


# Business Insights


st.subheader("💡 Business Insights")

st.success(
    f"""
**🏆 Highest Sales State**

**{highest_sales_state['State/Province']}**

Sales: **${highest_sales_state['Total_Sales']:,.0f}**
"""
)

st.info(
    f"""
**📈 Highest Profit State**

**{highest_profit_state['State/Province']}**

Profit: **${highest_profit_state['Total_Profit']:,.0f}**
"""
)

st.warning(
    f"""
**⚡ Fastest Shipping State**

**{fastest_state['State/Province']}**

Average Lead Time: **{fastest_state['Average_Lead_Time']:.2f} Days**
"""
)

st.error(
    f"""
**🐢 Slowest Shipping State**

**{slowest_state['State/Province']}**

Average Lead Time: **{slowest_state['Average_Lead_Time']:.2f} Days**
"""
)

st.markdown("---")


# Dashboard Footer


st.caption(
    "Factory Shipping Route Efficiency Analysis | Geographical Dashboard | Developed using Streamlit & Plotly"
)