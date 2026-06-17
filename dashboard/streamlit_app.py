import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


st.set_page_config(
    page_title="RetailIQ Dashboard",
    page_icon="📊",
    layout="wide"
)


SEGMENTED_DATA_PATH = Path("data/processed/customer_segments.csv")
FEATURE_DATA_PATH = Path("data/processed/final_features.csv")


@st.cache_data
def load_data():
    """
    Load segmented customer data if available.
    Otherwise load final feature data.
    """
    if SEGMENTED_DATA_PATH.exists():
        return pd.read_csv(SEGMENTED_DATA_PATH)

    if FEATURE_DATA_PATH.exists():
        return pd.read_csv(FEATURE_DATA_PATH)

    raise FileNotFoundError(
        "No processed data found. Please run feature engineering and segmentation first."
    )


def show_kpi_cards(df):
    total_customers = df["customer_id"].nunique()
    total_revenue = df["total_spend"].sum()
    avg_spend = df["total_spend"].mean()
    churn_rate = df["churn"].mean() * 100

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Customers", f"{total_customers:,}")
    col2.metric("Total Revenue", f"${total_revenue:,.2f}")
    col3.metric("Average Spend", f"${avg_spend:,.2f}")
    col4.metric("Churn Rate", f"{churn_rate:.2f}%")


def show_customer_overview(df):
    st.subheader("Customer Overview")

    col1, col2 = st.columns(2)

    with col1:
        gender_count = df["gender"].value_counts().reset_index()
        gender_count.columns = ["gender", "count"]

        fig = px.pie(
            gender_count,
            values="count",
            names="gender",
            title="Customer Distribution by Gender"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        membership_count = df["membership_type"].value_counts().reset_index()
        membership_count.columns = ["membership_type", "count"]

        fig = px.bar(
            membership_count,
            x="membership_type",
            y="count",
            title="Customers by Membership Type",
            text_auto=True
        )
        st.plotly_chart(fig, use_container_width=True)


def show_churn_analysis(df):
    st.subheader("Churn Analysis")

    col1, col2 = st.columns(2)

    with col1:
        churn_count = df["churn"].value_counts().reset_index()
        churn_count.columns = ["churn", "count"]
        churn_count["churn"] = churn_count["churn"].map({
            0: "No Churn",
            1: "Churn Risk"
        })

        fig = px.pie(
            churn_count,
            values="count",
            names="churn",
            title="Churn Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        churn_by_membership = (
            df.groupby("membership_type")["churn"]
            .mean()
            .reset_index()
        )
        churn_by_membership["churn_rate"] = churn_by_membership["churn"] * 100

        fig = px.bar(
            churn_by_membership,
            x="membership_type",
            y="churn_rate",
            title="Churn Rate by Membership Type",
            text_auto=".2f"
        )
        st.plotly_chart(fig, use_container_width=True)


def show_segment_analysis(df):
    if "segment_name" not in df.columns:
        st.warning("Customer segmentation data not found. Run segmentation model first.")
        return

    st.subheader("Customer Segmentation Analysis")

    segment_summary = (
        df.groupby("segment_name")
        .agg(
            customers=("customer_id", "count"),
            avg_total_spend=("total_spend", "mean"),
            avg_items_purchased=("items_purchased", "mean"),
            avg_rating=("average_rating", "mean"),
            churn_rate=("churn", "mean")
        )
        .reset_index()
    )

    segment_summary["churn_rate"] = segment_summary["churn_rate"] * 100

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(
            segment_summary,
            x="segment_name",
            y="customers",
            title="Customers by Segment",
            text_auto=True
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(
            segment_summary,
            x="segment_name",
            y="churn_rate",
            title="Churn Rate by Segment",
            text_auto=".2f"
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Segment Summary Table")
    st.dataframe(segment_summary, use_container_width=True)


def show_business_recommendations():
    st.subheader("Business Recommendations")

    recommendations = {
        "At Risk Customers": "Prioritize retention offers, feedback calls, and satisfaction recovery campaigns.",
        "Low Engagement Customers": "Run re-engagement campaigns, personalized product recommendations, and limited-time offers.",
        "Satisfied Regular Customers": "Encourage repeat purchases, membership upgrades, and bundled product offers.",
        "High Value Customers": "Protect with loyalty rewards, premium access, and personalized communication."
    }

    for segment, action in recommendations.items():
        st.markdown(f"**{segment}:** {action}")


def main():
    st.title("RetailIQ: E-commerce Customer Intelligence Dashboard")
    st.markdown(
        "An industry-style dashboard for customer churn analysis, segmentation, and business decision-making."
    )

    df = load_data()

    st.sidebar.title("Dashboard Filters")

    selected_membership = st.sidebar.multiselect(
        "Select Membership Type",
        options=sorted(df["membership_type"].unique()),
        default=sorted(df["membership_type"].unique())
    )

    selected_city = st.sidebar.multiselect(
        "Select City",
        options=sorted(df["city"].unique()),
        default=sorted(df["city"].unique())
    )

    filtered_df = df[
        (df["membership_type"].isin(selected_membership)) &
        (df["city"].isin(selected_city))
    ]

    show_kpi_cards(filtered_df)

    st.divider()

    show_customer_overview(filtered_df)

    st.divider()

    show_churn_analysis(filtered_df)

    st.divider()

    show_segment_analysis(filtered_df)

    st.divider()

    show_business_recommendations()


if __name__ == "__main__":
    main()