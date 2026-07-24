import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# =====================================================
# Page Configuration
# =====================================================

st.set_page_config(
    page_title="Ship Mode Analysis",
    page_icon="🚚",
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

st.title("🚚 Ship Mode Analysis Dashboard")

st.markdown("---")

# =====================================================
# Ship Mode Summary
# =====================================================

ship_mode_summary = (
    df.groupby("Ship Mode")
      .agg(
          Total_Shipments=("Ship Mode", "count"),
          Average_Lead_Time=("Shipping Lead Time", "mean"),
          Total_Sales=("Sales", "sum"),
          Total_Profit=("Gross Profit", "sum")
      )
      .reset_index()
)

# =====================================================
# KPI Cards
# =====================================================

total_modes = ship_mode_summary["Ship Mode"].nunique()
total_shipments = ship_mode_summary["Total_Shipments"].sum()
average_lead = ship_mode_summary["Average_Lead_Time"].mean()
total_profit = ship_mode_summary["Total_Profit"].sum()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🚚 Ship Modes", total_modes)

with col2:
    st.metric("📦 Total Shipments", f"{total_shipments:,}")

with col3:
    st.metric("⏱ Avg Lead Time", f"{average_lead:.2f} Days")

with col4:
    st.metric("💰 Total Profit", f"${total_profit:,.2f}")

st.markdown("---")

# =====================================================
# Ship Mode Charts
# =====================================================

left_col, right_col = st.columns(2)

# -----------------------------
# Shipments by Ship Mode
# -----------------------------

with left_col:

    fig_shipments = px.bar(
        ship_mode_summary,
        x="Ship Mode",
        y="Total_Shipments",
        text="Total_Shipments",
        title="📦 Shipments by Ship Mode"
    )

    st.plotly_chart(fig_shipments, use_container_width=True)

# -----------------------------
# Average Lead Time
# -----------------------------

with right_col:

    fig_lead = px.bar(
        ship_mode_summary,
        x="Ship Mode",
        y="Average_Lead_Time",
        text="Average_Lead_Time",
        title="🚚 Average Lead Time by Ship Mode"
    )

    st.plotly_chart(fig_lead, use_container_width=True)

st.markdown("---")

# =====================================================
# Sales & Profit Analysis
# =====================================================

left_col, right_col = st.columns(2)

# -----------------------------
# Sales by Ship Mode
# -----------------------------

with left_col:

    fig_sales = px.bar(
        ship_mode_summary,
        x="Ship Mode",
        y="Total_Sales",
        text="Total_Sales",
        title="💰 Total Sales by Ship Mode",
        color="Total_Sales"
    )

    st.plotly_chart(fig_sales, use_container_width=True)

# -----------------------------
# Profit by Ship Mode
# -----------------------------

with right_col:

    fig_profit = px.bar(
        ship_mode_summary,
        x="Ship Mode",
        y="Total_Profit",
        text="Total_Profit",
        title="📈 Total Profit by Ship Mode",
        color="Total_Profit"
    )

    st.plotly_chart(fig_profit, use_container_width=True)

st.markdown("---")

# =====================================================
# Ship Mode Summary Table
# =====================================================

st.subheader("📋 Ship Mode Summary")

display_df = ship_mode_summary.copy()

display_df["Average_Lead_Time"] = display_df["Average_Lead_Time"].round(2)
display_df["Total_Sales"] = display_df["Total_Sales"].round(2)
display_df["Total_Profit"] = display_df["Total_Profit"].round(2)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# =====================================================
# Download Summary
# =====================================================

csv = display_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Ship Mode Summary",
    data=csv,
    file_name="ship_mode_summary.csv",
    mime="text/csv"
)

st.markdown("---")

# =====================================================
# Business Insights
# =====================================================

st.subheader("💡 Business Insights")

best_sales = ship_mode_summary.loc[
    ship_mode_summary["Total_Sales"].idxmax(),
    "Ship Mode"
]

best_profit = ship_mode_summary.loc[
    ship_mode_summary["Total_Profit"].idxmax(),
    "Ship Mode"
]

fastest_mode = ship_mode_summary.loc[
    ship_mode_summary["Average_Lead_Time"].idxmin(),
    "Ship Mode"
]

slowest_mode = ship_mode_summary.loc[
    ship_mode_summary["Average_Lead_Time"].idxmax(),
    "Ship Mode"
]

col1, col2 = st.columns(2)

with col1:
    st.success(f"""
### ✅ Key Findings

- Highest Sales : **{best_sales}**
- Highest Profit : **{best_profit}**
- Fastest Shipping : **{fastest_mode}**
- Slowest Shipping : **{slowest_mode}**
""")

with col2:
    st.info("""
### 📈 Recommendations

- Increase usage of high-profit shipping modes.
- Optimize slow shipping methods.
- Monitor delivery performance regularly.
- Balance cost with customer satisfaction.
""")