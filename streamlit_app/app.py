"""
Olist Brazilian E-Commerce Analytics Dashboard
================================================
Author: Ayushi Singh, Data Analyst
Source: Kaggle olistbr/brazilian-ecommerce (CC BY-NC-SA 4.0)
Strictly Delivered Orders Scope
"""

import os
import json
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Page Configuration
st.set_page_config(
    page_title="Olist E-Commerce Analytics",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Colors
PRIMARY_NAVY = "#0F2040"
SLATE_BLUE = "#1E40AF"
CORAL_ACCENT = "#E11D48"
AMBER_ACCENT = "#D97706"
MUTED_GRAY = "#64748B"
LIGHT_BG = "#F8FAFC"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLEAN_DIR = os.path.join(BASE_DIR, "data", "clean")

# Load Clean Summary and Tables
@st.cache_data
def load_data():
    summary_path = os.path.join(CLEAN_DIR, "summary.json")
    with open(summary_path, "r", encoding="utf-8") as f:
        summary = json.load(f)
    
    monthly = pd.read_csv(os.path.join(CLEAN_DIR, "monthly.csv"))
    category = pd.read_csv(os.path.join(CLEAN_DIR, "category.csv"))
    state = pd.read_csv(os.path.join(CLEAN_DIR, "state.csv"))
    payment = pd.read_csv(os.path.join(CLEAN_DIR, "payment_type.csv"))
    deliv_rev = pd.read_csv(os.path.join(CLEAN_DIR, "delivery_vs_review.csv"))
    rfm_segments = pd.read_csv(os.path.join(CLEAN_DIR, "rfm_segments.csv"))
    cohort = pd.read_csv(os.path.join(CLEAN_DIR, "cohort_retention.csv"))
    rev_dist = pd.read_csv(os.path.join(CLEAN_DIR, "review_distribution.csv"))
    
    return summary, monthly, category, state, payment, deliv_rev, rfm_segments, cohort, rev_dist

summary, monthly_df, category_df, state_df, payment_df, deliv_rev_df, rfm_df, cohort_df, rev_dist_df = load_data()

# ----------------------------------------------------
# SIDEBAR
# ----------------------------------------------------
st.sidebar.title("📦 Olist Analytics")
st.sidebar.markdown("**Brazilian E-Commerce Public Dataset**")
st.sidebar.caption("Source: Kaggle (CC BY-NC-SA 4.0)")

page = st.sidebar.radio(
    "Navigation",
    ["Executive", "Category & Geography", "Delivery & Satisfaction", "Customers"],
    index=0
)

st.sidebar.markdown("---")
# Mandatory Verification Note on Every Page
st.sidebar.info("🔍 **Verification Note:**\nExecutive GMV must read **R$ 13,221,498.11** and orders **96,478**.")
st.sidebar.markdown(
    """
    **Project Scope Rules:**
    - **Revenue Scope:** Delivered orders only.
    - **Customer Identity:** Unique individuals via `customer_unique_id`.
    - **Historical Window:** Sep 2016 – Aug 2018 (Sep-Oct 2018 extract cutoff).
    """
)
st.sidebar.caption("Prepared by Ayushi Singh, Data Analyst")


# ----------------------------------------------------
# PAGE 1: EXECUTIVE
# ----------------------------------------------------
if page == "Executive":
    st.title("Executive Overview Dashboard")
    st.markdown("Macro-level revenue, order volumes, operational health, and historical sales trajectory.")

    # Year Multiselect Filter
    monthly_df["year"] = monthly_df["purchase_month"].str[:4]
    available_years = sorted(monthly_df["year"].unique())
    selected_years = st.multiselect("Filter by Purchase Year:", available_years, default=available_years)

    if not selected_years:
        st.warning("Please select at least one year to display metrics.")
        st.stop()

    filtered_monthly = monthly_df[monthly_df["year"].isin(selected_years)]
    
    # Calculate filtered aggregates
    total_gmv = filtered_monthly["gmv"].sum()
    total_orders = int(filtered_monthly["orders"].sum())
    aov = total_gmv / total_orders if total_orders > 0 else 0.0

    # Review Score Rule:
    # Full period avg review is 4.16 from summary.json (order-weighted).
    # When filtered, label as "Avg review (monthly mean)"
    all_years_selected = (set(selected_years) == set(available_years))
    if all_years_selected:
        avg_rev_display = summary["verification_gate_2"]["avg_review"]
        avg_rev_label = "Avg Review Score (Order-Weighted)"
    else:
        # compute monthly mean across months with orders
        valid_months = filtered_monthly[filtered_monthly["orders"] > 0]
        avg_rev_display = valid_months["avg_review"].mean() if len(valid_months) > 0 else 0.0
        avg_rev_label = "Avg Review (Monthly Mean)"

    # Top KPI Cards
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Delivered GMV", f"R$ {total_gmv:,.2f}")
    c2.metric("Delivered Orders", f"{total_orders:,}")
    c3.metric("Average Order Value (AOV)", f"R$ {aov:.2f}")
    c4.metric(avg_rev_label, f"{avg_rev_display:.2f} / 5.00")

    st.markdown("---")

    # Monthly GMV Line Chart
    st.subheader("Monthly Delivered GMV Trajectory (Sep 2016 – Oct 2018)")
    st.caption("Active sales window Sep 2016 – Aug 2018. Nov 2016 is a known data gap; Sep-Oct 2018 had 0 delivered orders due to extraction cutoff.")

    # Exclude tail zero months for visual clarity if full period selected
    plot_df = filtered_monthly[filtered_monthly["purchase_month"] <= "2018-08"].copy() if all_years_selected else filtered_monthly.copy()

    fig, ax = plt.subplots(figsize=(11, 4.5), dpi=200)
    x = range(len(plot_df))
    y = plot_df["gmv"]
    ax.plot(x, y, color=SLATE_BLUE, linewidth=2.5, marker="o", markersize=5, markerfacecolor=PRIMARY_NAVY, markeredgewidth=1.2, markeredgecolor="white")
    ax.fill_between(x, y, color=SLATE_BLUE, alpha=0.10)
    ax.set_xticks(x)
    ax.set_xticklabels(plot_df["purchase_month"], rotation=45, ha="right", fontsize=8.5, color=MUTED_GRAY)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda val, pos: f"R$ {val*1e-3:.0f}k" if val >= 1e3 else f"R$ {val:.0f}"))
    ax.set_ylabel("GMV (R$)", fontsize=9.5, fontweight="600", color=PRIMARY_NAVY)
    ax.grid(True, linestyle="--", alpha=0.6, color="#E2E8F0")

    # Annotate Black Friday 2017 if present
    if "2017-11" in plot_df["purchase_month"].values:
        idx_nov = plot_df[plot_df["purchase_month"] == "2017-11"].index[0]
        val_nov = plot_df.loc[idx_nov, "gmv"]
        ax.annotate(
            f"Black Friday 2017\nR$ {val_nov:,.0f}",
            xy=(idx_nov, val_nov),
            xytext=(idx_nov - 2.5, val_nov + 90000),
            arrowprops=dict(arrowstyle="->", color=CORAL_ACCENT, lw=1.2),
            fontsize=8.5, fontweight="bold", color=CORAL_ACCENT,
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=CORAL_ACCENT, lw=0.8)
        )

    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    # Monthly Summary Table
    with st.expander("View Monthly Performance Data Table"):
        display_m = filtered_monthly[[
            "purchase_month", "orders", "gmv", "freight", "avg_order_value", "late_orders", "late_rate", "avg_review"
        ]].copy()
        display_m["gmv"] = display_m["gmv"].map("R$ {:,.2f}".format)
        display_m["freight"] = display_m["freight"].map("R$ {:,.2f}".format)
        display_m["avg_order_value"] = display_m["avg_order_value"].map("R$ {:,.2f}".format)
        display_m["late_rate"] = display_m["late_rate"].map("{:.2f}%".format)
        display_m["avg_review"] = display_m["avg_review"].map("{:.2f}".format)
        st.dataframe(display_m, use_container_width=True)


# ----------------------------------------------------
# PAGE 2: CATEGORY & GEOGRAPHY
# ----------------------------------------------------
elif page == "Category & Geography":
    st.title("Category & Geographic Performance")
    st.markdown("Breakdown of merchandise demand across English-translated product categories and Brazilian state territories.")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Top Product Categories")
        top_n = st.slider("Select Top N Categories:", min_value=5, max_value=20, value=10, step=1)
        top_cat = category_df.head(top_n).iloc[::-1]

        fig, ax = plt.subplots(figsize=(6, 5), dpi=200)
        bars = ax.barh(top_cat["category_en"], top_cat["gmv"], color=SLATE_BLUE, height=0.65)
        bars[-1].set_color(CORAL_ACCENT)
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda val, pos: f"R$ {val*1e-6:.1f}M" if val >= 1e6 else f"R$ {val*1e-3:.0f}k"))
        ax.set_xlabel("Delivered GMV (R$)", fontsize=9, fontweight="600")
        ax.grid(True, linestyle="--", alpha=0.5, color="#E2E8F0")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with col2:
        st.subheader("Top 10 States by Customer GMV")
        st.caption("São Paulo (SP) represents 38.3% of national GMV, followed by Rio de Janeiro (RJ) and Minas Gerais (MG).")
        top_states = state_df.head(10).iloc[::-1]

        fig, ax = plt.subplots(figsize=(6, 5), dpi=200)
        bars = ax.barh(top_states["customer_state"], top_states["gmv"], color=SLATE_BLUE, height=0.65)
        bars[-1].set_color(PRIMARY_NAVY)
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda val, pos: f"R$ {val*1e-6:.1f}M" if val >= 1e6 else f"R$ {val*1e-3:.0f}k"))
        ax.set_xlabel("Delivered GMV (R$)", fontsize=9, fontweight="600")
        ax.grid(True, linestyle="--", alpha=0.5, color="#E2E8F0")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    st.markdown("---")
    t1, t2 = st.tabs(["Product Categories Table", "State Logistics Table"])

    with t1:
        disp_cat = category_df.copy()
        disp_cat["gmv"] = disp_cat["gmv"].map("R$ {:,.2f}".format)
        disp_cat["freight"] = disp_cat["freight"].map("R$ {:,.2f}".format)
        disp_cat["avg_item_price"] = disp_cat["avg_item_price"].map("R$ {:,.2f}".format)
        disp_cat["share_of_gmv"] = disp_cat["share_of_gmv"].map("{:.2f}%".format)
        st.dataframe(disp_cat, use_container_width=True)

    with t2:
        disp_state = state_df.copy()
        disp_state["gmv"] = disp_state["gmv"].map("R$ {:,.2f}".format)
        disp_state["freight"] = disp_state["freight"].map("R$ {:,.2f}".format)
        disp_state["late_rate"] = disp_state["late_rate"].map("{:.2f}%".format)
        disp_state["avg_delivery_days"] = disp_state["avg_delivery_days"].map("{:.2f} days".format)
        disp_state["avg_review"] = disp_state["avg_review"].map("{:.2f}".format)
        disp_state["share_of_gmv"] = disp_state["share_of_gmv"].map("{:.2f}%".format)
        st.dataframe(disp_state, use_container_width=True)


# ----------------------------------------------------
# PAGE 3: DELIVERY & SATISFACTION
# ----------------------------------------------------
elif page == "Delivery & Satisfaction":
    st.title("Delivery Logistics & Customer Satisfaction")
    
    # Headline Late vs On-Time Text
    st.error("🚨 **Headline Finding:** On-time orders average **4.30 stars** vs Late orders **2.57 stars** (Late Rate: 8.11%).")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Review Score by Delivery Bucket")
        st.caption("Sharp satisfaction cliff: 0–5d orders average 4.45★ (69.4% 5★) vs 30d+ orders 2.25★ (15.9% 5★).")

        fig, ax = plt.subplots(figsize=(6, 4.5), dpi=200)
        x = range(len(deliv_rev_df))
        bars = ax.bar(x, deliv_rev_df["avg_review"], color=SLATE_BLUE, width=0.55)
        bars[-1].set_color(CORAL_ACCENT)
        ax.set_xticks(x)
        ax.set_xticklabels(deliv_rev_df["delivery_bucket"], fontsize=9, fontweight="bold")
        ax.set_ylabel("Average Review Score", fontsize=9, fontweight="600")
        ax.set_ylim(0, 5.0)
        ax.axhline(4.16, color=AMBER_ACCENT, linestyle="--", label="National Mean: 4.16")
        ax.legend(loc="lower left", fontsize=8)
        ax.grid(True, linestyle="--", alpha=0.5, color="#E2E8F0")

        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, h + 0.12, f"{h:.2f}★", ha="center", va="bottom", fontsize=8.5, fontweight="bold", color=PRIMARY_NAVY)

        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with col2:
        st.subheader("Order Review Score Distribution")
        st.caption("58.6% of all delivered orders received 5 stars (56,521 orders).")

        fig, ax = plt.subplots(figsize=(6, 4.5), dpi=200)
        colors = ["#EF4444", "#F97316", "#FBBF24", "#34D399", "#10B981"]
        ax.bar(rev_dist_df["review_score"].astype(str) + "★", rev_dist_df["count"], color=colors, width=0.55)
        ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))
        ax.set_ylabel("Orders Count", fontsize=9, fontweight="600")
        ax.grid(True, linestyle="--", alpha=0.5, color="#E2E8F0")

        for idx, row in rev_dist_df.iterrows():
            ax.text(idx, row["count"] + 1500, f"{row['count']:,}\n({row['pct_of_delivered_orders']:.1f}%)", ha="center", va="bottom", fontsize=8, fontweight="bold", color=PRIMARY_NAVY)

        ax.set_ylim(0, rev_dist_df["count"].max() * 1.15)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    st.markdown("---")

    # Delivery Buckets Table & Payments Table
    t1, t2 = st.tabs(["Delivery Buckets Table", "Delivered Payments Breakdown"])

    with t1:
        disp_b = deliv_rev_df.copy()
        disp_b["pct_5star"] = disp_b["pct_5star"].map("{:.1f}%".format)
        disp_b["share_of_orders"] = disp_b["share_of_orders"].map("{:.2f}%".format)
        disp_b["avg_review"] = disp_b["avg_review"].map("{:.2f} / 5.00".format)
        st.dataframe(disp_b, use_container_width=True)

    with t2:
        st.markdown("**Delivered Order Payment Methods & Financing Behavior:**")
        disp_p = payment_df.copy()
        disp_p["total_value"] = disp_p["total_value"].map("R$ {:,.2f}".format)
        disp_p["avg_installments"] = disp_p["avg_installments"].map("{:.2f}".format)
        disp_p["share_of_total"] = disp_p["share_of_total"].map("{:.2f}%".format)
        st.dataframe(disp_p, use_container_width=True)


# ----------------------------------------------------
# PAGE 4: CUSTOMERS
# ----------------------------------------------------
elif page == "Customers":
    st.title("Customer Intelligence: RFM & Cohort Retention")
    st.markdown("Individual buyer behavior, lifetime value segmentation, and monthly cohort retention dynamics.")

    # Headline Repeat & Champions Text
    st.warning("⚠️ **Customer Loyalty Gap:** Only **3.0% of delivered customers made a repeat purchase** (2,801 out of 93,358). Consequently, **no customer reached the 13/15 Champion score — the Champions segment is 0 (empty)**.")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Delivered GMV by RFM Segment")
        rfm_active = rfm_df[rfm_df["customers"] > 0].sort_values(by="total_gmv", ascending=True)

        fig, ax = plt.subplots(figsize=(6, 4.5), dpi=200)
        bars = ax.barh(rfm_active["segment"], rfm_active["total_gmv"], color=SLATE_BLUE, height=0.6)
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda val, pos: f"R$ {val*1e-6:.1f}M" if val >= 1e6 else f"R$ {val*1e-3:.0f}k"))
        ax.set_xlabel("Delivered GMV (R$)", fontsize=9, fontweight="600")
        ax.grid(True, linestyle="--", alpha=0.5, color="#E2E8F0")

        for bar, (_, row) in zip(bars, rfm_active.iterrows()):
            w = bar.get_width()
            ax.text(w + 50000, bar.get_y() + bar.get_height()/2, f"R$ {w:,.0f} ({int(row['customers']):,} cust)", ha="left", va="center", fontsize=8, fontweight="bold", color=PRIMARY_NAVY)

        ax.set_xlim(0, rfm_active["total_gmv"].max() * 1.35)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with col2:
        st.subheader("RFM Segments Summary Table")
        st.caption("Loyal customers: 3,699 people with average spend R$ 409.15.")
        disp_rfm = rfm_df.copy()
        disp_rfm["total_gmv"] = disp_rfm["total_gmv"].map("R$ {:,.2f}".format)
        disp_rfm["avg_spend"] = disp_rfm["avg_spend"].map("R$ {:,.2f}".format)
        disp_rfm["share_of_customers"] = disp_rfm["share_of_customers"].map("{:.2f}%".format)
        disp_rfm["share_of_gmv"] = disp_rfm["share_of_gmv"].map("{:.2f}%".format)
        st.dataframe(disp_rfm, use_container_width=True)

    st.markdown("---")

    # Cohort Retention Note and Matrix
    st.subheader("Cohort Retention Matrix")
    st.info("📌 **Cohort Statistical Note:** September 2016 (n=1) and December 2016 (n=1) are single-customer test cohorts and must **NOT** be read as standard cohort retention rates.")

    # Format cohort matrix for display
    display_cohort = cohort_df.copy()
    display_cohort = display_cohort.fillna(0)
    st.dataframe(display_cohort, use_container_width=True)
