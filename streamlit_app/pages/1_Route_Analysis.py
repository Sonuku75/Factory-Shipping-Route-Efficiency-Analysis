import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# =====================================================
# Page Configuration
# =====================================================

st.set_page_config(
    page_title="Route Analysis",
    page_icon="🛣️",
    layout="wide"
)

# =====================================================
# Load Dataset
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_PATH = BASE_DIR / "data" / "processed" / "feature_engineered_dataset.csv"

df = pd.read_csv(DATA_PATH)

# =====================================================
# Page Title
# =====================================================

st.title("🛣️ Route Analysis Dashboard")
st.markdown("---")

# =====================================================
# Route KPIs
# =====================================================

total_routes = df["Factory_to_State"].nunique()

average_route_sales = (
    df.groupby("Factory_to_State")["Sales"]
      .sum()
      .mean()
)

average_route_profit = (
    df.groupby("Factory_to_State")["Gross Profit"]
      .sum()
      .mean()
)

average_route_lead = (
    df.groupby("Factory_to_State")["Shipping Lead Time"]
      .mean()
      .mean()
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🛣️ Total Routes", total_routes)

with col2:
    st.metric("💰 Avg Route Sales", f"${average_route_sales:,.2f}")

with col3:
    st.metric("📈 Avg Route Profit", f"${average_route_profit:,.2f}")

with col4:
    st.metric("🚚 Avg Lead Time", f"{average_route_lead:.2f} Days")

st.markdown("---")

# =====================================================
# Fastest Routes
# =====================================================

fastest_routes = (
    df.groupby("Factory_to_State")
      .agg(
          Average_Lead_Time=("Shipping Lead Time", "mean"),
          Total_Sales=("Sales", "sum")
      )
      .reset_index()
      .sort_values(by="Average_Lead_Time")
      .head(10)
)

fig_fastest = px.bar(
    fastest_routes,
    x="Average_Lead_Time",
    y="Factory_to_State",
    orientation="h",
    text="Average_Lead_Time",
    title="⚡ Top 10 Fastest Routes"
)

# =====================================================
# Slowest Routes
# =====================================================

slowest_routes = (
    df.groupby("Factory_to_State")
      .agg(
          Average_Lead_Time=("Shipping Lead Time", "mean"),
          Total_Sales=("Sales", "sum")
      )
      .reset_index()
      .sort_values(by="Average_Lead_Time", ascending=False)
      .head(10)
)

fig_slowest = px.bar(
    slowest_routes,
    x="Average_Lead_Time",
    y="Factory_to_State",
    orientation="h",
    text="Average_Lead_Time",
    title="🐢 Top 10 Slowest Routes"
)

# =====================================================
# Route Comparison
# =====================================================

left_col, right_col = st.columns(2)

with left_col:
    st.plotly_chart(fig_fastest, use_container_width=True)

with right_col:
    st.plotly_chart(fig_slowest, use_container_width=True)

st.markdown("---")

# =====================================================
# Route Summary Table
# =====================================================

route_summary = (
    df.groupby("Factory_to_State")
      .agg(
          Average_Lead_Time=("Shipping Lead Time", "mean"),
          Total_Sales=("Sales", "sum"),
          Total_Profit=("Gross Profit", "sum"),
          Total_Shipments=("Sales", "count")
      )
      .reset_index()
      .sort_values(by="Average_Lead_Time")
)

st.subheader("📋 Route Summary")

st.dataframe(
    route_summary,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# =====================================================
# Download Route Summary
# =====================================================

csv = route_summary.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Route Summary",
    data=csv,
    file_name="route_summary.csv",
    mime="text/csv"
)

st.markdown("---")

# =====================================================
# Route Insights
# =====================================================

st.subheader("📌 Route Insights")

col1, col2 = st.columns(2)

with col1:
    st.info(
        """
### Analysis

- Fastest shipping routes identified
- Slowest shipping routes identified
- Route sales evaluated
- Route shipment count calculated
"""
    )

with col2:
    st.success(
        """
### Business Value

- Improve delivery efficiency
- Reduce shipping delays
- Optimize logistics planning
- Identify high-performing routes
"""
    )