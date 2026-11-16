"""
The Great Memory Squeeze
Global RAM Shortage Crisis Intelligence Dashboard
--------------------------------------------------------------------------
B.Tech CSE Data Science Project (Streamlit)

Run with:  streamlit run app.py
Place 'Ultimate_Memory_Shortage_Crisis_Dataset_10k.csv' in the same folder.
"""

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# --------------------------------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="THE GLOBAL MEMORY CHIP CRISIS",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------------------------------
# DATA LOADING
# --------------------------------------------------------------------------
@st.cache_data
def load_data(file):
    df = pd.read_csv(file, parse_dates=["timestamp"])
    df["year_month"] = df["timestamp"].dt.to_period("M").dt.to_timestamp()
    df["year"] = df["timestamp"].dt.year
    return df


DEFAULT_PATH = "Ultimate_Memory_Shortage_Crisis_Dataset_10k.csv"

try:
    df = load_data(DEFAULT_PATH)
except FileNotFoundError:
    st.error(
        "Dataset not found. Place "
        "`Ultimate_Memory_Shortage_Crisis_Dataset_10k.csv` in the same folder as this app."
    )
    st.stop()

# --------------------------------------------------------------------------
# HEADER
# --------------------------------------------------------------------------
st.title("THE GLOBAL MEMORY CHIP CRISIS")
st.write(
    "Tracking the global DDR4 → DDR5 → DDR6 DRAM shortage as AI/HBM demand "
    "collides with consumer supply (2024 – 2027)"
)
st.markdown("---")

# --------------------------------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------------------------------
st.sidebar.header("🔎 Filters")

default_regions = sorted(df["region"].unique())
default_generations = sorted(df["generation"].unique())
default_brands = sorted(df["brand"].unique())
default_segments = sorted(df["market_segment"].unique())
default_price_status = sorted(df["price_status"].unique())
default_price_range = (float(df["price_usd"].min()), float(df["price_usd"].max()))
default_date_range = (df["timestamp"].min().to_pydatetime(),
                       df["timestamp"].max().to_pydatetime())

if st.sidebar.button("🔄 Reset Filters", use_container_width=True):
    for key in ["regions", "generations", "brands", "segments",
                "price_status", "price_range", "date_range"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

regions = st.sidebar.multiselect(
    "Region", default_regions, default=default_regions, key="regions"
)
generations = st.sidebar.multiselect(
    "Generation", default_generations, default=default_generations, key="generations"
)
brands = st.sidebar.multiselect(
    "Brand", default_brands, default=default_brands, key="brands"
)
segments = st.sidebar.multiselect(
    "Market Segment", default_segments, default=default_segments, key="segments"
)
price_status = st.sidebar.multiselect(
    "Price Status", default_price_status, default=default_price_status, key="price_status"
)
price_range = st.sidebar.slider(
    "Price (USD)", default_price_range[0], default_price_range[1],
    default_price_range, key="price_range"
)
date_range = st.sidebar.slider(
    "Listing Date", default_date_range[0], default_date_range[1],
    default_date_range, key="date_range"
)

mask = (
    df["region"].isin(regions)
    & df["generation"].isin(generations)
    & df["brand"].isin(brands)
    & df["market_segment"].isin(segments)
    & df["price_status"].isin(price_status)
    & df["price_usd"].between(*price_range)
    & df["timestamp"].between(date_range[0], date_range[1])
)
fdf = df[mask].copy()

if fdf.empty:
    st.warning("No records match the current filters. Please widen your selection.")
    st.stop()

# --------------------------------------------------------------------------
# KPI ROW
# --------------------------------------------------------------------------
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("📦 Listings", f"{len(fdf):,}")
k2.metric("💰 Avg Price/GB", f"${fdf['price_per_gb'].mean():,.2f}")
k3.metric(
    "🔥 Shortage-Inflated",
    f"{(fdf['price_status'] == 'Shortage-Inflated').mean() * 100:.1f}%"
)
k4.metric("📉 Avg Inventory (wks)", f"{fdf['global_inventory_weeks'].mean():.1f}")
k5.metric("🏭 Avg Fab Utilization", f"{fdf['fab_utilization_rate'].mean() * 100:.1f}%")

st.markdown("---")

# ==========================================================================
# SECTION 0 : EXECUTIVE SUMMARY
# ==========================================================================
st.header("📋 Executive Summary")
st.write(
    """
    The global semiconductor industry is in the middle of an unprecedented
    memory crisis. As AI data centers race to secure High Bandwidth Memory
    (HBM) for GPUs, fabrication capacity once dedicated to consumer DRAM
    (DDR4/DDR5) is being redirected — driving prices up, inventories down,
    and forcing a chaotic early rollout of DDR6. This dashboard analyzes a
    10,000-record market dataset covering RAM kits from 14 major brands
    across 6 global regions between 2024 and 2027, to uncover how this
    shortage is reshaping the memory market.
    """
)

st.subheader("Key Objectives:")
st.markdown(
    """
    - Track how average prices evolve across DDR4, DDR5, and DDR6 (Preview) generations over time
    - Quantify the scale of shortage-driven price inflation vs. normal-priced listings
    - Examine the relationship between GPU/HBM demand growth and fab utilization rates
    - Compare pricing and inventory patterns across brands, regions, and die manufacturers
    - Distinguish Enterprise/AI segment impact from Consumer segment impact
    - Explore technical trade-offs: speed vs. latency, capacity distribution, ECC adoption
    """
)

st.subheader("Expected Deliverables:")
st.markdown(
    """
    - Interactive visualizations showcasing the global RAM market landscape
    - Real-time KPI tracking (avg price/GB, % shortage-inflated, fab utilization, inventory weeks)
    - Statistical analysis connecting AI/HBM demand growth to consumer RAM price inflation
    - Actionable insights for buyers, OEMs, retailers, and supply-chain analysts
    - Downloadable filtered datasets for further analysis
    """
)

st.subheader("Problem Statement")
st.write(
    """
    The global memory (RAM) industry is highly volatile and reactive, with
    manufacturers, buyers, and policymakers constantly navigating shifting
    prices, fab capacity constraints, and surging AI-driven demand. This
    project leverages a comprehensive DRAM market dataset to provide
    data-driven insights that can help:
    """
)
st.markdown(
    """
    - **Hardware Buyers / System Builders:** Time purchases around price trends and avoid shortage-inflated listings
    - **OEMs & Retailers:** Anticipate inventory pressure and pricing shifts across brands and regions
    - **Industry Analysts:** Quantify how AI/HBM demand is reshaping the broader consumer memory market
    - **Policy & Supply-Chain Researchers:** Understand fab capacity allocation trade-offs between AI and consumer products
    """
)

st.subheader("Dataset Overview")
st.markdown(
    """
    The dataset contains comprehensive information about RAM kits including:

    **Core Product Info:** brand, model name, region, generation (DDR4/DDR5/DDR6 Preview), form factor, capacity, module count

    **Performance Specs:** speed (MT/s), CAS latency, voltage, true latency, die manufacturer & type

    **Pricing & Market:** price (USD), price per GB, price status (Normal/Shortage-Inflated/Listing-Error), market segment

    **Supply-Chain Signals:** global inventory weeks, fab utilization rate, GPU/HBM demand trend
    """
)

# ==========================================================================
# SECTION 1 : CRISIS OVERVIEW
# ==========================================================================
st.header("📈 Crisis Overview")

trend = fdf.groupby(["year_month", "generation"])["price_usd"].mean().reset_index()
fig = px.line(
    trend, x="year_month", y="price_usd", color="generation",
    markers=True, title="Average Price Trend by Generation Over Time",
    labels={"year_month": "Month", "price_usd": "Avg Price (USD)"}
)
st.plotly_chart(fig, use_container_width=True)

vol = fdf.groupby("year_month").size().reset_index(name="listings")
fig = px.bar(
    vol, x="year_month", y="listings",
    title="Monthly Listing Volume Over Time",
    labels={"year_month": "Month", "listings": "Number of Listings"}
)
st.plotly_chart(fig, use_container_width=True)

pie = px.pie(
    fdf, names="price_status", hole=0.5,
    title="Price Status Breakdown", color="price_status",
    color_discrete_map={
        "Shortage-Inflated": "#f85149",
        "Normal": "#3fb950",
        "Listing-Error": "#8b949e"
    }
)
st.plotly_chart(pie, use_container_width=True)

fab = fdf.groupby("year_month")["fab_utilization_rate"].mean().reset_index()
fig = px.area(
    fab, x="year_month", y="fab_utilization_rate",
    title="Fab Utilization Rate Over Time",
    labels={"fab_utilization_rate": "Utilization", "year_month": "Month"}
)
st.plotly_chart(fig, use_container_width=True)

hbm = fdf.groupby("year_month")["gpu_hbm_trend_gb"].mean().reset_index()
fig = px.area(
    hbm, x="year_month", y="gpu_hbm_trend_gb",
    title="GPU / HBM Demand Trend (GB)",
    color_discrete_sequence=["#d29922"],
    labels={"gpu_hbm_trend_gb": "HBM Trend (GB)", "year_month": "Month"}
)
st.plotly_chart(fig, use_container_width=True)

# ==========================================================================
# SECTION 2 : PRICE & SHORTAGE ANALYSIS
# ==========================================================================
st.header("💸 Price & Shortage Analysis")

fig = px.box(
    fdf, x="generation", y="price_usd", color="price_status",
    title="Price Distribution by Generation & Status", points=False
)
st.plotly_chart(fig, use_container_width=True)

fig = px.violin(
    fdf, x="generation", y="price_per_gb", color="generation", box=True,
    title="Price per GB Distribution by Generation"
)
st.plotly_chart(fig, use_container_width=True)

fig = px.scatter(
    fdf.sample(min(2000, len(fdf)), random_state=1),
    x="global_inventory_weeks", y="price_per_gb", color="price_status",
    size="capacity_gb", hover_data=["brand", "model_name"],
    title="Inventory Weeks vs Price/GB", opacity=0.7
)
st.plotly_chart(fig, use_container_width=True)

sample = fdf.sample(min(2000, len(fdf)), random_state=1)
fig = px.scatter(
    sample, x="fab_utilization_rate", y="gpu_hbm_trend_gb", color="generation",
    title="Fab Utilization vs GPU/HBM Demand (does AI eat the fabs?)"
)
x_vals = sample["fab_utilization_rate"].values
y_vals = sample["gpu_hbm_trend_gb"].values
if len(x_vals) > 1:
    coeffs = np.polyfit(x_vals, y_vals, 1)
    x_line = np.linspace(x_vals.min(), x_vals.max(), 100)
    y_line = coeffs[0] * x_line + coeffs[1]
    fig.add_trace(
        go.Scatter(
            x=x_line, y=y_line, mode="lines", name="Trend Line",
            line=dict(color="black", width=3, dash="dash")
        )
    )
st.plotly_chart(fig, use_container_width=True)

seg = fdf.groupby(["market_segment", "price_status"]).size().reset_index(name="count")
fig = px.bar(
    seg, x="market_segment", y="count", color="price_status", barmode="group",
    title="Shortage Impact: Enterprise/AI vs Consumer"
)
st.plotly_chart(fig, use_container_width=True)

sp = fdf.groupby("generation")["speed_premium_ratio"].mean().reset_index()
fig = px.bar(
    sp, x="generation", y="speed_premium_ratio",
    title="Average Speed Premium Ratio by Generation", color="generation"
)
st.plotly_chart(fig, use_container_width=True)

# ==========================================================================
# SECTION 3 : BRAND & REGION INSIGHTS
# ==========================================================================
st.header("🌍 Brand & Region Insights")

b = fdf.groupby("brand")["price_per_gb"].mean().sort_values().reset_index()
fig = px.bar(
    b, x="price_per_gb", y="brand", orientation="h",
    title="Average Price per GB by Brand", color="price_per_gb",
    color_continuous_scale="Reds"
)
st.plotly_chart(fig, use_container_width=True)

r = fdf["region"].value_counts().reset_index()
r.columns = ["region", "count"]
fig = px.treemap(
    r, path=["region"], values="count",
    title="Listing Volume by Region", color="count",
    color_continuous_scale="Blues"
)
st.plotly_chart(fig, use_container_width=True)

rg = fdf.groupby("region")["price_usd"].mean().sort_values().reset_index()
fig = px.bar(
    rg, x="region", y="price_usd",
    title="Average Price (USD) by Region", color="price_usd",
    color_continuous_scale="Oranges"
)
st.plotly_chart(fig, use_container_width=True)

d = fdf.groupby("die_manufacturer")["price_usd"].mean().reset_index()
fig = px.pie(
    d, names="die_manufacturer", values="price_usd",
    title="Avg Price Share by Die Manufacturer", hole=0.4
)
st.plotly_chart(fig, use_container_width=True)

heat = fdf.groupby(["region", "generation"]).size().reset_index(name="count")
heat_pivot = heat.pivot(index="region", columns="generation", values="count").fillna(0)
fig = px.imshow(
    heat_pivot, text_auto=True, color_continuous_scale="Purples",
    title="Listing Count: Region vs Generation"
)
st.plotly_chart(fig, use_container_width=True)

top = (
    fdf.groupby("brand")
    .agg(listings=("kit_id", "count"), avg_price=("price_usd", "mean"))
    .sort_values("listings", ascending=False).reset_index()
)
st.markdown("**Top Brands by Listing Volume**")
st.dataframe(top, use_container_width=True, hide_index=True)

# ==========================================================================
# SECTION 4 : TECH SPECS
# ==========================================================================
st.header("⚙️ Tech Specs")

fig = px.histogram(
    fdf, x="capacity_gb", color="generation",
    title="Capacity (GB) Distribution", nbins=30, barmode="overlay", opacity=0.6
)
st.plotly_chart(fig, use_container_width=True)

fig = px.scatter(
    fdf.sample(min(2000, len(fdf)), random_state=2),
    x="speed_mts", y="true_latency_ns", color="generation",
    title="Speed (MT/s) vs True Latency (ns)",
    hover_data=["brand", "model_name"]
)
st.plotly_chart(fig, use_container_width=True)

fig = px.scatter(
    fdf.sample(min(2000, len(fdf)), random_state=3),
    x="cas_latency", y="speed_mts", color="generation",
    title="CAS Latency vs Speed (MT/s)",
    hover_data=["brand", "model_name"]
)
st.plotly_chart(fig, use_container_width=True)

ecc = fdf["is_ecc"].value_counts().reset_index()
ecc.columns = ["is_ecc", "count"]
ecc["is_ecc"] = ecc["is_ecc"].map({True: "ECC", False: "Non-ECC"})
fig = px.bar(
    ecc, x="is_ecc", y="count",
    title="ECC vs Non-ECC Modules", color="is_ecc"
)
st.plotly_chart(fig, use_container_width=True)

ff = fdf["form_factor"].value_counts().reset_index()
ff.columns = ["form_factor", "count"]
fig = px.pie(
    ff, names="form_factor", values="count",
    title="Form Factor Distribution (DIMM / SODIMM / LRDIMM)", hole=0.4
)
st.plotly_chart(fig, use_container_width=True)

ru = fdf["recommended_usage"].value_counts().reset_index()
ru.columns = ["recommended_usage", "count"]
fig = px.bar(
    ru, x="recommended_usage", y="count",
    title="Listings by Recommended Usage", color="recommended_usage"
)
st.plotly_chart(fig, use_container_width=True)

vd = fdf.groupby("generation")["voltage"].mean().reset_index()
fig = px.bar(
    vd, x="generation", y="voltage",
    title="Average Voltage by Generation", color="generation"
)
st.plotly_chart(fig, use_container_width=True)

bpd = fdf.groupby("brand")["bandwidth_per_dollar"].mean().sort_values(ascending=False).reset_index()
fig = px.bar(
    bpd, x="brand", y="bandwidth_per_dollar",
    title="Average Bandwidth per Dollar by Brand (Best Value)", color="bandwidth_per_dollar",
    color_continuous_scale="Greens"
)
st.plotly_chart(fig, use_container_width=True)

num_cols = ["capacity_gb", "speed_mts", "cas_latency", "true_latency_ns",
            "price_per_gb", "price_usd", "global_inventory_weeks",
            "fab_utilization_rate", "gpu_hbm_trend_gb"]
corr = fdf[num_cols].corr()
fig = px.imshow(
    corr, text_auto=".2f", color_continuous_scale="RdBu_r",
    title="Correlation Heatmap of Key Metrics"
)
st.plotly_chart(fig, use_container_width=True)

# ==========================================================================
# SECTION 5 : EXPLORE DATA
# ==========================================================================
st.header("🗂️ Explore Data")
st.write(f"**Filtered records:** {len(fdf):,} / {len(df):,}")
st.dataframe(fdf, use_container_width=True, height=450)

csv = fdf.to_csv(index=False).encode("utf-8")
st.download_button(
    "⬇️ Download Filtered Data as CSV", csv,
    "filtered_memory_crisis_data.csv", "text/csv"
)

# --------------------------------------------------------------------------
# FOOTER
# --------------------------------------------------------------------------
st.markdown("---")
st.caption(
    "The Great Memory Squeeze | B.Tech CSE Data Science Project | "
    "Built with Streamlit + Plotly | Dataset: Ultimate Memory Shortage Crisis (10k records)"
)