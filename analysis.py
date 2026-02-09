# ===================== IMPORTS =====================
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ===================== PAGE CONFIG =====================
st.set_page_config(
    page_title="🌱 Variety Performance & G×E Dashboard",
    layout="wide"
)

st.title("🌱 Variety Performance & G×E Analysis Dashboard")
st.subheader("📊 Plant Breeding | Multi-Location Trials | Decision Support Tool")

st.markdown("---")

# ===================== DATA INPUT =====================
st.sidebar.header("📂 Data Input")

data_source = st.sidebar.radio(
    "Choose data source:",
    ["Use example dataset", "Upload CSV file"]
)

if data_source == "Upload CSV file":
    uploaded_file = st.sidebar.file_uploader(
        "Upload CSV (Trial Data)",
        type=["csv"]
    )
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.sidebar.success("✅ Data uploaded")
    else:
        st.stop()
else:
    df = pd.DataFrame({
        "Year": [2022, 2022, 2022, 2023, 2023, 2023, 2023],
        "Location": ["Bhakkar", "Bhakkar", "Layyah", "Bhakkar", "Layyah", "Multan", "Multan"],
        "Genotype": ["Line-1", "Line-2", "Line-1", "Line-2", "Line-1", "Line-2", "Line-3"],
        "Yield": [2400, 2650, 2300, 2700, 2350, 2750, 2600],
        "Days_to_Flowering": [92, 95, 90, 94, 91, 93, 96],
        "Disease_Score": [3, 2, 4, 2, 3, 1, 2]
    })

st.header("👀 Dataset Preview")
st.dataframe(df, use_container_width=True)

# ===================== FILTERS =====================
st.markdown("---")
st.header("🎯 Filters")

c1, c2, c3 = st.columns(3)

with c1:
    years = st.multiselect("📅 Year", df["Year"].unique(), df["Year"].unique())
with c2:
    locations = st.multiselect("📍 Location", df["Location"].unique(), df["Location"].unique())
with c3:
    genotypes = st.multiselect("🧬 Genotype", df["Genotype"].unique(), df["Genotype"].unique())

filtered_df = df[
    (df["Year"].isin(years)) &
    (df["Location"].isin(locations)) &
    (df["Genotype"].isin(genotypes))
]

# ===================== SUMMARY =====================
st.markdown("---")
st.header("📈 Performance Summary")

summary = (
    filtered_df
    .groupby("Genotype")
    .agg(
        Mean_Yield=("Yield", "mean"),
        Yield_SD=("Yield", "std"),
        Mean_Flowering=("Days_to_Flowering", "mean"),
        Mean_Disease=("Disease_Score", "mean")
    )
    .reset_index()
)

st.dataframe(summary, use_container_width=True)

# ===================== YIELD COMPARISON =====================
st.markdown("---")
st.header("🌾 Yield Performance")

fig_yield = px.box(
    filtered_df,
    x="Genotype",
    y="Yield",
    color="Location",
    points="all",
    template="plotly_white",
    title="🌾 Yield Distribution Across Locations"
)
st.plotly_chart(fig_yield, use_container_width=True)

# ===================== G×E INTERACTION =====================
st.markdown("---")
st.header("🔬 G×E Interaction (Genotype × Environment)")

gxE = (
    filtered_df
    .groupby(["Genotype", "Location"])
    .agg(Mean_Yield=("Yield", "mean"))
    .reset_index()
)

fig_gxe = px.line(
    gxE,
    x="Location",
    y="Mean_Yield",
    color="Genotype",
    markers=True,
    template="plotly_white",
    title="🔬 G×E Interaction Plot"
)
st.plotly_chart(fig_gxe, use_container_width=True)

# ===================== STABILITY ANALYSIS =====================
st.markdown("---")
st.header("⚖️ Stability Analysis")

fig_stability = px.scatter(
    summary,
    x="Yield_SD",
    y="Mean_Yield",
    color="Genotype",
    size="Mean_Yield",
    template="plotly_white",
    title="⚖️ Yield Stability (Low SD = More Stable)",
    labels={
        "Yield_SD": "Yield Variability (SD)",
        "Mean_Yield": "Mean Yield"
    }
)

st.plotly_chart(fig_stability, use_container_width=True)

# ===================== BEST GENOTYPE =====================
st.markdown("---")
st.header("🏆 Recommendation")

best = summary.sort_values(
    ["Mean_Yield", "Yield_SD"],
    ascending=[False, True]
).iloc[0]

st.success(
    f"🏆 **Recommended Genotype:** {best['Genotype']}  \n"
    f"🌾 Mean Yield: {best['Mean_Yield']:.1f} kg/ha  \n"
    f"⚖️ Yield Stability (SD): {best['Yield_SD']:.2f}  \n"
    f"🦠 Disease Score: {best['Mean_Disease']:.1f}"
)

st.caption("Developed by **Muhammad Usman** | Plant Breeding × Data Science 🌱📊")
