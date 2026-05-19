import streamlit as st
import pandas as pd
import plotly.express as px

# Page setup
st.set_page_config(
    page_title="InsightOps AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------
# Load data
# -----------------------------
@st.cache_data
def load_data():
    reviews = pd.read_csv("data/insightops_reviews_step4_dashboard_ready.csv")
    issue_risk = pd.read_csv("data/issue_risk_summary.csv")
    product_risk = pd.read_csv("data/product_risk_summary.csv")
    monthly_trend = pd.read_csv("data/monthly_issue_trend.csv")
    emerging = pd.read_csv("data/emerging_issues.csv")

    reviews["review_date"] = pd.to_datetime(reviews["review_date"], errors="coerce")

    return reviews, issue_risk, product_risk, monthly_trend, emerging


reviews, issue_risk, product_risk, monthly_trend, emerging = load_data()

# -----------------------------
# Title
# -----------------------------
st.title("InsightOps AI: Customer Risk & Growth Decision Platform")

st.write(
    "This dashboard turns customer reviews into product risk alerts, issue trends, "
    "and business action recommendations."
)

# -----------------------------
# Sidebar filters
# -----------------------------
st.sidebar.header("Filters")

min_reviews = st.sidebar.slider(
    "Minimum reviews per product",
    min_value=3,
    max_value=50,
    value=5,
    step=1
)

issue_options = sorted(reviews["issue_category"].dropna().unique())

selected_issues = st.sidebar.multiselect(
    "Select issue categories",
    options=issue_options,
    default=issue_options
)

filtered_reviews = reviews[reviews["issue_category"].isin(selected_issues)]

filtered_products = product_risk[
    (product_risk["total_reviews"] >= min_reviews) &
    (product_risk["main_issue"].isin(selected_issues))
]

# -----------------------------
# Executive Overview
# -----------------------------
st.header("Executive Overview")

total_reviews = len(filtered_reviews)
avg_rating = filtered_reviews["rating"].mean()
high_risk_rate = filtered_reviews["high_risk_flag"].mean() * 100
avg_risk_score = filtered_reviews["improved_risk_score"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Reviews", f"{total_reviews:,}")
col2.metric("Average Rating", f"{avg_rating:.2f}")
col3.metric("High-Risk Review Rate", f"{high_risk_rate:.2f}%")
col4.metric("Average Risk Score", f"{avg_risk_score:.2f}")

# -----------------------------
# Risk Distribution
# -----------------------------
st.header("Risk Distribution")

risk_counts = filtered_reviews["risk_label"].value_counts().reset_index()
risk_counts.columns = ["Risk Label", "Count"]

fig_risk = px.bar(
    risk_counts,
    x="Risk Label",
    y="Count",
    text="Count",
    title="Review Risk Distribution"
)

st.plotly_chart(fig_risk, use_container_width=True)

# -----------------------------
# Issue Risk Summary
# -----------------------------
st.header("Highest-Risk Customer Issue Categories")

issue_risk_filtered = issue_risk[
    issue_risk["issue_category"].isin(selected_issues)
].sort_values("avg_risk_score", ascending=False)

fig_issue = px.bar(
    issue_risk_filtered,
    x="avg_risk_score",
    y="issue_category",
    orientation="h",
    text="avg_risk_score",
    title="Average Risk Score by Issue Category",
    labels={
        "avg_risk_score": "Average Risk Score",
        "issue_category": "Issue Category"
    }
)

fig_issue.update_layout(yaxis={"categoryorder": "total ascending"})

st.plotly_chart(fig_issue, use_container_width=True)

st.dataframe(
    issue_risk_filtered[
        [
            "issue_category",
            "total_reviews",
            "avg_rating",
            "high_risk_reviews",
            "high_risk_rate",
            "avg_risk_score",
            "total_helpful_votes"
        ]
    ],
    use_container_width=True
)

# -----------------------------
# Product Risk Radar
# -----------------------------
st.header("Product Risk Radar")

st.write(
    "This section ranks products by customer risk. Use the minimum-review filter "
    "on the left to avoid overreacting to products with very few reviews."
)

top_products = filtered_products.sort_values(
    "avg_risk_score",
    ascending=False
).head(20)

st.dataframe(
    top_products[
        [
            "product_id",
            "total_reviews",
            "avg_rating",
            "high_risk_reviews",
            "high_risk_rate",
            "avg_risk_score",
            "total_helpful_votes",
            "main_issue",
            "recommended_action"
        ]
    ],
    use_container_width=True
)

fig_product = px.bar(
    top_products,
    x="avg_risk_score",
    y="product_id",
    orientation="h",
    color="main_issue",
    title="Top High-Risk Products",
    labels={
        "avg_risk_score": "Average Risk Score",
        "product_id": "Product ID"
    }
)

fig_product.update_layout(yaxis={"categoryorder": "total ascending"})

st.plotly_chart(fig_product, use_container_width=True)

# -----------------------------
# Issue Trend Detection
# -----------------------------
st.header("Issue Trend Detection")

complaint_reviews = filtered_reviews[
    filtered_reviews["issue_category"] != "Positive feedback"
]

top_issues = complaint_reviews["issue_category"].value_counts().head(5).index.tolist()

trend_data = monthly_trend[
    monthly_trend["issue_category"].isin(top_issues)
]

fig_trend = px.line(
    trend_data,
    x="review_month",
    y="review_count",
    color="issue_category",
    title="Monthly Trend of Top Customer Issue Categories",
    labels={
        "review_month": "Review Month",
        "review_count": "Review Count",
        "issue_category": "Issue Category"
    }
)

st.plotly_chart(fig_trend, use_container_width=True)

# -----------------------------
# Emerging Issue Alerts
# -----------------------------
st.header("Emerging Issue Alerts")

emerging_filtered = emerging[
    emerging["issue_category"].isin(selected_issues)
].sort_values("growth_rate_percent", ascending=False)

st.dataframe(
    emerging_filtered[
        [
            "review_month",
            "issue_category",
            "review_count",
            "previous_month_count",
            "growth_count",
            "growth_rate_percent"
        ]
    ].head(20),
    use_container_width=True
)

# -----------------------------
# Top Risky Reviews
# -----------------------------
st.header("Top Risky Customer Reviews")

top_reviews = filtered_reviews.sort_values(
    "improved_risk_score",
    ascending=False
).head(10)

st.dataframe(
    top_reviews[
        [
            "product_id",
            "rating",
            "risk_label",
            "sentiment_label",
            "issue_category",
            "helpful_count",
            "word_count",
            "improved_risk_score",
            "clean_text",
            "recommended_action"
        ]
    ],
    use_container_width=True
)

# -----------------------------
# AI Executive Summary
# -----------------------------
st.header("AI Executive Summary")

if len(issue_risk_filtered) > 0:
    top_issue = issue_risk_filtered.iloc[0]["issue_category"]
    top_issue_score = issue_risk_filtered.iloc[0]["avg_risk_score"]
else:
    top_issue = "No issue selected"
    top_issue_score = 0

if len(top_products) > 0:
    top_product = top_products.iloc[0]["product_id"]
    top_product_score = top_products.iloc[0]["avg_risk_score"]
    product_sentence = (
        f"The highest-risk product is **{top_product}**, with an average risk score of "
        f"**{top_product_score:.2f}**."
    )
else:
    product_sentence = "No product meets the selected review threshold."

if len(emerging_filtered) > 0:
    emerging_issue = emerging_filtered.iloc[0]["issue_category"]
    emerging_growth = emerging_filtered.iloc[0]["growth_rate_percent"]
    emerging_month = emerging_filtered.iloc[0]["review_month"]
    emerging_sentence = (
        f"The strongest emerging issue is **{emerging_issue}**, which increased by "
        f"**{emerging_growth:.2f}%** in **{emerging_month}**."
    )
else:
    emerging_sentence = "No major emerging issue spike was detected."

summary = f"""
The most serious customer issue in the current view is **{top_issue}**, 
with an average risk score of **{top_issue_score:.2f}**.

{product_sentence}

{emerging_sentence}

**Recommended business action:** prioritise high-risk issue categories first, especially those with 
low average ratings, high helpful votes, and fast complaint growth. Product, quality, and customer 
support teams should review these issues before they grow into larger customer experience problems.
"""

st.markdown(summary)

# -----------------------------
# Business Actions
# -----------------------------
st.header("Recommended Business Actions")

action_table = issue_risk_filtered[
    [
        "issue_category",
        "avg_rating",
        "high_risk_rate",
        "avg_risk_score"
    ]
].copy()

action_mapping = {
    "Scent or fragrance issue": "Review fragrance strength, product description accuracy, and customer expectation messaging.",
    "Skin reaction or irritation": "Escalate to product safety/quality team and review ingredient warnings.",
    "Product quality or effectiveness": "Investigate product performance claims, supplier quality, and refund patterns.",
    "Packaging or delivery issue": "Review packaging quality, fulfilment process, and delivery damage complaints.",
    "Price or value issue": "Review pricing, product size communication, and value perception.",
    "Texture or feel issue": "Review product formulation, texture expectations, and product description accuracy.",
    "Size or quantity issue": "Improve product size visibility, images, and quantity information.",
    "Positive feedback": "Use positive feedback themes in marketing and product positioning.",
    "General negative complaint": "Manually review negative complaints and identify repeated issue patterns.",
    "General mixed feedback": "Monitor mixed feedback for emerging dissatisfaction themes."
}

action_table["recommended_action"] = action_table["issue_category"].map(action_mapping)

st.dataframe(action_table, use_container_width=True)