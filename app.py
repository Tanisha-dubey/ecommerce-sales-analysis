import streamlit as st
import pandas as pd
import plotly.express as px


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="E-Commerce Sales & Profitability Dashboard",
    page_icon="📊",
    layout="wide"
)


# =========================================================
# TITLE
# =========================================================

st.title("📊 E-Commerce Sales & Profitability Dashboard")

st.markdown(
    """
    **Interactive analysis of Superstore data using Python, Pandas and Plotly.**

    Explore sales, profitability, product categories and customer segments
    using the filters below.
    """
)


# =========================================================
# LOAD DATA
# =========================================================

try:
    data = pd.read_csv(
        "Sample - Superstore.csv",
        encoding="latin1"
    )

except FileNotFoundError:
    st.error(
        "❌ Sample - Superstore.csv was not found. "
        "Make sure the CSV file is in the same folder as app.py."
    )
    st.stop()


# =========================================================
# DATA PREPARATION
# =========================================================

data["Order Date"] = pd.to_datetime(data["Order Date"])
data["Ship Date"] = pd.to_datetime(data["Ship Date"])

data["Order Year"] = data["Order Date"].dt.year

data["Year Month"] = (
    data["Order Date"]
    .dt.to_period("M")
    .astype(str)
)


# =========================================================
# SIDEBAR FILTERS
# =========================================================

st.sidebar.header("🔎 Dashboard Filters")

years = sorted(data["Order Year"].unique())

selected_years = st.sidebar.multiselect(
    "📅 Select Year",
    options=years,
    default=years
)


categories = sorted(data["Category"].unique())

selected_categories = st.sidebar.multiselect(
    "📦 Select Category",
    options=categories,
    default=categories
)


regions = sorted(data["Region"].unique())

selected_regions = st.sidebar.multiselect(
    "🌎 Select Region",
    options=regions,
    default=regions
)


segments = sorted(data["Segment"].unique())

selected_segments = st.sidebar.multiselect(
    "👥 Select Customer Segment",
    options=segments,
    default=segments
)


# =========================================================
# FILTER DATA
# =========================================================

filtered_data = data[
    (data["Order Year"].isin(selected_years))
    &
    (data["Category"].isin(selected_categories))
    &
    (data["Region"].isin(selected_regions))
    &
    (data["Segment"].isin(selected_segments))
]


# =========================================================
# EMPTY DATA CHECK
# =========================================================

if filtered_data.empty:

    st.warning(
        "⚠️ No data available for the selected filters."
    )

    st.stop()


# =========================================================
# KPI CALCULATIONS
# =========================================================

total_sales = filtered_data["Sales"].sum()

total_profit = filtered_data["Profit"].sum()

total_orders = filtered_data["Order ID"].nunique()

total_customers = filtered_data["Customer ID"].nunique()

profit_margin = (
    total_profit / total_sales * 100
    if total_sales != 0
    else 0
)


# =========================================================
# KPI SECTION
# =========================================================

st.subheader("📌 Key Performance Indicators")

col1, col2, col3, col4, col5 = st.columns(5)


with col1:

    st.metric(
        "💰 Total Sales",
        f"${total_sales:,.2f}"
    )


with col2:

    st.metric(
        "📈 Total Profit",
        f"${total_profit:,.2f}"
    )


with col3:

    st.metric(
        "📦 Total Orders",
        f"{total_orders:,}"
    )


with col4:

    st.metric(
        "👥 Customers",
        f"{total_customers:,}"
    )


with col5:

    st.metric(
        "📊 Profit Margin",
        f"{profit_margin:.2f}%"
    )


st.divider()


# =========================================================
# MONTHLY SALES ANALYSIS
# =========================================================

st.subheader("📈 Monthly Sales Analysis")


sales_by_month = (
    filtered_data
    .groupby("Year Month")["Sales"]
    .sum()
    .reset_index()
)


fig_sales_month = px.line(
    sales_by_month,
    x="Year Month",
    y="Sales",
    markers=True,
    title="Monthly Sales Trend"
)


fig_sales_month.update_layout(
    xaxis_title="Month",
    yaxis_title="Sales"
)


st.plotly_chart(
    fig_sales_month,
    use_container_width=True
)


# =========================================================
# SALES ANALYSIS
# =========================================================

col1, col2 = st.columns(2)


with col1:

    st.subheader("🥧 Sales by Category")


    sales_by_category = (
        filtered_data
        .groupby("Category")["Sales"]
        .sum()
        .reset_index()
    )


    fig_category = px.pie(
        sales_by_category,
        values="Sales",
        names="Category",
        hole=0.45,
        title="Sales Distribution by Category"
    )


    fig_category.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )


    st.plotly_chart(
        fig_category,
        use_container_width=True
    )


with col2:

    st.subheader("📊 Sales by Sub-Category")


    sales_by_subcategory = (
        filtered_data
        .groupby("Sub-Category")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )


    fig_subcategory = px.bar(
        sales_by_subcategory,
        x="Sub-Category",
        y="Sales",
        title="Sales by Sub-Category"
    )


    fig_subcategory.update_layout(
        xaxis_title="Sub-Category",
        yaxis_title="Sales"
    )


    st.plotly_chart(
        fig_subcategory,
        use_container_width=True
    )


# =========================================================
# MONTHLY PROFIT
# =========================================================

st.subheader("💰 Monthly Profit Analysis")


profit_by_month = (
    filtered_data
    .groupby("Year Month")["Profit"]
    .sum()
    .reset_index()
)


fig_profit_month = px.line(
    profit_by_month,
    x="Year Month",
    y="Profit",
    markers=True,
    title="Monthly Profit Trend"
)


fig_profit_month.update_layout(
    xaxis_title="Month",
    yaxis_title="Profit"
)


st.plotly_chart(
    fig_profit_month,
    use_container_width=True
)


# =========================================================
# PROFIT ANALYSIS
# =========================================================

col1, col2 = st.columns(2)


with col1:

    st.subheader("💵 Profit by Category")


    profit_by_category = (
        filtered_data
        .groupby("Category")["Profit"]
        .sum()
        .reset_index()
    )


    fig_profit_category = px.pie(
        profit_by_category,
        values="Profit",
        names="Category",
        hole=0.45,
        title="Profit Distribution by Category"
    )


    fig_profit_category.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )


    st.plotly_chart(
        fig_profit_category,
        use_container_width=True
    )


with col2:

    st.subheader("📊 Profit by Sub-Category")


    profit_by_subcategory = (
        filtered_data
        .groupby("Sub-Category")["Profit"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )


    fig_profit_subcategory = px.bar(
        profit_by_subcategory,
        x="Sub-Category",
        y="Profit",
        title="Profit by Sub-Category"
    )


    fig_profit_subcategory.update_layout(
        xaxis_title="Sub-Category",
        yaxis_title="Profit"
    )


    st.plotly_chart(
        fig_profit_subcategory,
        use_container_width=True
    )


# =========================================================
# CUSTOMER SEGMENT
# =========================================================

st.subheader("👥 Sales & Profit by Customer Segment")


segment_analysis = (
    filtered_data
    .groupby("Segment")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
    .reset_index()
)


fig_segment = px.bar(
    segment_analysis,
    x="Segment",
    y=["Sales", "Profit"],
    barmode="group",
    title="Sales and Profit by Customer Segment"
)


fig_segment.update_layout(
    xaxis_title="Customer Segment",
    yaxis_title="Amount"
)


st.plotly_chart(
    fig_segment,
    use_container_width=True
)


# =========================================================
# SALES-TO-PROFIT RATIO
# =========================================================

st.subheader("📐 Sales-to-Profit Analysis")


ratio_data = (
    filtered_data
    .groupby("Segment")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
    .reset_index()
)


ratio_data["Sales-to-Profit Ratio"] = (
    ratio_data["Sales"]
    /
    ratio_data["Profit"].replace(0, pd.NA)
)


st.dataframe(
    ratio_data,
    use_container_width=True
)


# =========================================================
# KEY BUSINESS INSIGHTS
# =========================================================

st.divider()

st.subheader("💡 Key Business Insights")


# Highest sales category
highest_sales_category = (
    filtered_data
    .groupby("Category")["Sales"]
    .sum()
    .idxmax()
)


highest_sales_value = (
    filtered_data
    .groupby("Category")["Sales"]
    .sum()
    .max()
)


# Highest profit category
highest_profit_category = (
    filtered_data
    .groupby("Category")["Profit"]
    .sum()
    .idxmax()
)


highest_profit_value = (
    filtered_data
    .groupby("Category")["Profit"]
    .sum()
    .max()
)


# Best sub-category by profit
best_subcategory = (
    filtered_data
    .groupby("Sub-Category")["Profit"]
    .sum()
    .idxmax()
)


best_subcategory_profit = (
    filtered_data
    .groupby("Sub-Category")["Profit"]
    .sum()
    .max()
)


# Best customer segment by sales
best_segment = (
    filtered_data
    .groupby("Segment")["Sales"]
    .sum()
    .idxmax()
)


best_segment_sales = (
    filtered_data
    .groupby("Segment")["Sales"]
    .sum()
    .max()
)


# Display insights

st.info(
    f"""
    **1. Highest Sales Category:** {highest_sales_category}

    This category generated approximately **${highest_sales_value:,.2f}**
    in sales.

    **2. Most Profitable Category:** {highest_profit_category}

    This category generated approximately **${highest_profit_value:,.2f}**
    in profit.

    **3. Most Profitable Sub-Category:** {best_subcategory}

    It generated approximately **${best_subcategory_profit:,.2f}**
    in profit.

    **4. Leading Customer Segment:** {best_segment}

    This segment generated approximately **${best_segment_sales:,.2f}**
    in sales.

    **5. Overall Profit Margin:** {profit_margin:.2f}%
    """
)


# =========================================================
# DATA PREVIEW
# =========================================================

st.divider()

with st.expander("🔍 View Filtered Dataset"):

    st.write(
        f"Showing **{len(filtered_data):,} records** "
        "after applying the selected filters."
    )

    st.dataframe(
        filtered_data,
        use_container_width=True
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "E-Commerce Sales & Profitability Dashboard | "
    "Python • Pandas • Plotly • Streamlit"
)