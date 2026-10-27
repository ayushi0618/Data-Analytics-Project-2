"""
Generate High-Resolution Charts for Olist Analytics
=====================================================
Reads from data/clean/ only and produces 7 publication-grade charts in charts/:
1. monthly_gmv.png
2. top_categories.png
3. top_states.png
4. review_dist.png
5. rfm_gmv.png
6. delivery_review.png
7. cohort_heatmap.png
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLEAN_DIR = os.path.join(BASE_DIR, "data", "clean")
CHARTS_DIR = os.path.join(BASE_DIR, "charts")
os.makedirs(CHARTS_DIR, exist_ok=True)

# Visual styling
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams["font.sans-serif"] = ["Segoe UI", "DejaVu Sans", "Arial", "sans-serif"]
plt.rcParams["axes.edgecolor"] = "#CBD5E1"
plt.rcParams["axes.linewidth"] = 0.8
plt.rcParams["grid.color"] = "#F1F5F9"
plt.rcParams["grid.linestyle"] = "--"
plt.rcParams["grid.alpha"] = 0.8

PRIMARY_NAVY = "#0F2040"
SLATE_BLUE = "#1E40AF"
CORAL_ACCENT = "#E11D48"
AMBER_ACCENT = "#D97706"
MUTED_GRAY = "#64748B"
LIGHT_BG = "#F8FAFC"


def format_currency_brl(x, pos):
    if x >= 1e6:
        return f"R$ {x*1e-6:.1f}M"
    elif x >= 1e3:
        return f"R$ {x*1e-3:.0f}k"
    else:
        return f"R$ {x:.0f}"


# 1. Monthly GMV Line Chart
def chart_monthly_gmv():
    df = pd.read_csv(os.path.join(CLEAN_DIR, "monthly.csv"))
    # Exclude tail months 2018-09 and 2018-10 with 0 delivered orders for visualization clarity or plot full
    fig, ax = plt.subplots(figsize=(12, 6), dpi=300)
    
    # Active range Sep 2016 to Aug 2018 (24 months)
    active_df = df[df["purchase_month"] <= "2018-08"].copy()
    
    x = range(len(active_df))
    y = active_df["gmv"]
    
    ax.plot(x, y, color=SLATE_BLUE, linewidth=2.8, marker="o", markersize=6, markerfacecolor=PRIMARY_NAVY, markeredgewidth=1.5, markeredgecolor="white", zorder=4)
    ax.fill_between(x, y, color=SLATE_BLUE, alpha=0.10, zorder=3)
    
    ax.set_title("Delivered Monthly GMV (Sep 2016 – Aug 2018)\nTotal Delivered GMV: R$ 13,221,498.11 across 96,478 Orders", fontsize=14, fontweight="bold", color=PRIMARY_NAVY, pad=15)
    ax.set_xlabel("Purchase Month", fontsize=11, fontweight="600", color=PRIMARY_NAVY, labelpad=10)
    ax.set_ylabel("Delivered GMV (R$)", fontsize=11, fontweight="600", color=PRIMARY_NAVY, labelpad=10)
    
    ax.set_xticks(x)
    ax.set_xticklabels(active_df["purchase_month"], rotation=45, ha="right", fontsize=9, color=MUTED_GRAY)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(format_currency_brl))
    
    # Annotate Black Friday 2017 peak (2017-11)
    nov_idx = active_df[active_df["purchase_month"] == "2017-11"].index[0]
    nov_gmv = active_df.loc[nov_idx, "gmv"]
    ax.annotate(
        f"Black Friday 2017 Peak\nR$ {nov_gmv:,.0f}\n(7,289 orders)",
        xy=(nov_idx, nov_gmv),
        xytext=(nov_idx - 3.5, nov_gmv + 120000),
        arrowprops=dict(arrowstyle="->", color=CORAL_ACCENT, lw=1.5),
        fontsize=9, fontweight="bold", color=CORAL_ACCENT,
        bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=CORAL_ACCENT, lw=1)
    )
    
    # Annotate Nov 2016 gap
    nov16_idx = active_df[active_df["purchase_month"] == "2016-11"].index[0]
    ax.annotate(
        "Nov 2016 Gap (0 orders)",
        xy=(nov16_idx, 0),
        xytext=(nov16_idx + 0.5, 150000),
        arrowprops=dict(arrowstyle="->", color=MUTED_GRAY, lw=1.2),
        fontsize=8, color=MUTED_GRAY,
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=MUTED_GRAY, lw=0.8)
    )
    
    # Annotate extract cut-off note
    ax.text(
        0.02, 0.05,
        "Note: Data represents delivered orders only. Nov 2016 is a known data gap; Sep-Oct 2018 had 0 delivered orders due to extraction cutoff.",
        transform=ax.transAxes, fontsize=8, color=MUTED_GRAY, style="italic"
    )
    
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "monthly_gmv.png"), dpi=300)
    plt.close()
    print("Saved charts/monthly_gmv.png")


# 2. Top 10 Categories Bar Chart
def chart_top_categories():
    df = pd.read_csv(os.path.join(CLEAN_DIR, "category.csv"))
    top10 = df.head(10).iloc[::-1] # reverse for horizontal bar chart
    
    fig, ax = plt.subplots(figsize=(11, 7), dpi=300)
    bars = ax.barh(top10["category_en"], top10["gmv"], color=SLATE_BLUE, edgecolor="none", height=0.65, zorder=3)
    
    # Highlight #1 category health_beauty
    bars[-1].set_color(CORAL_ACCENT)
    
    ax.set_title("Top 10 Product Categories by Delivered GMV\nhealth_beauty leads with R$ 1,233,132 (9.3% share)", fontsize=14, fontweight="bold", color=PRIMARY_NAVY, pad=15)
    ax.set_xlabel("Delivered GMV (R$)", fontsize=11, fontweight="600", color=PRIMARY_NAVY, labelpad=10)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_currency_brl))
    
    for bar in bars:
        w = bar.get_width()
        ax.text(w + 15000, bar.get_y() + bar.get_height()/2, f"R$ {w:,.0f}", ha="left", va="center", fontsize=9, fontweight="600", color=PRIMARY_NAVY)
        
    ax.set_xlim(0, top10["gmv"].max() * 1.18)
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "top_categories.png"), dpi=300)
    plt.close()
    print("Saved charts/top_categories.png")


# 3. Top 10 States Bar Chart
def chart_top_states():
    df = pd.read_csv(os.path.join(CLEAN_DIR, "state.csv"))
    top10 = df.head(10).iloc[::-1]
    
    fig, ax = plt.subplots(figsize=(11, 7), dpi=300)
    bars = ax.barh(top10["customer_state"], top10["gmv"], color=SLATE_BLUE, edgecolor="none", height=0.65, zorder=3)
    
    # Highlight SP
    bars[-1].set_color(PRIMARY_NAVY)
    
    ax.set_title("Top 10 Brazilian States by Customer GMV\nSão Paulo (SP) accounts for R$ 5,067,633 (38.3% of national GMV)", fontsize=14, fontweight="bold", color=PRIMARY_NAVY, pad=15)
    ax.set_xlabel("Delivered GMV (R$)", fontsize=11, fontweight="600", color=PRIMARY_NAVY, labelpad=10)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_currency_brl))
    
    for bar, (_, row) in zip(bars, top10.iterrows()):
        w = bar.get_width()
        late = row["late_rate"]
        ax.text(w + 50000, bar.get_y() + bar.get_height()/2, f"R$ {w:,.0f}  (Late: {late:.1f}%)", ha="left", va="center", fontsize=9, fontweight="600", color=PRIMARY_NAVY)
        
    ax.set_xlim(0, top10["gmv"].max() * 1.25)
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "top_states.png"), dpi=300)
    plt.close()
    print("Saved charts/top_states.png")


# 4. Review Distribution Bar Chart
def chart_review_dist():
    df = pd.read_csv(os.path.join(CLEAN_DIR, "review_distribution.csv"))
    
    fig, ax = plt.subplots(figsize=(9, 6), dpi=300)
    colors = ["#EF4444", "#F97316", "#FBBF24", "#34D399", "#10B981"]
    bars = ax.bar(df["review_score"].astype(str) + " Stars", df["count"], color=colors, edgecolor="none", width=0.55, zorder=3)
    
    ax.set_title("Order Review Score Distribution (Delivered Orders)\n58.6% of orders received 5-star reviews (Average: 4.16 / 5.00)", fontsize=13, fontweight="bold", color=PRIMARY_NAVY, pad=15)
    ax.set_ylabel("Delivered Orders Count", fontsize=11, fontweight="600", color=PRIMARY_NAVY, labelpad=10)
    ax.set_xlabel("Review Score", fontsize=11, fontweight="600", color=PRIMARY_NAVY, labelpad=10)
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))
    
    for bar, (_, row) in zip(bars, df.iterrows()):
        h = bar.get_height()
        pct = row["pct_of_delivered_orders"]
        ax.text(bar.get_x() + bar.get_width()/2, h + 1000, f"{h:,}\n({pct:.1f}%)", ha="center", va="bottom", fontsize=9.5, fontweight="bold", color=PRIMARY_NAVY)
        
    ax.set_ylim(0, df["count"].max() * 1.15)
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "review_dist.png"), dpi=300)
    plt.close()
    print("Saved charts/review_dist.png")


# 5. RFM Segment GMV Bar Chart
def chart_rfm_gmv():
    df = pd.read_csv(os.path.join(CLEAN_DIR, "rfm_segments.csv"))
    df = df[df["customers"] > 0].sort_values(by="total_gmv", ascending=True)
    
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    bars = ax.barh(df["segment"], df["total_gmv"], color=SLATE_BLUE, height=0.6, zorder=3)
    
    ax.set_title("RFM Customer Segment Delivered GMV\nNote: Champions segment is 0 (3.0% repeat rate gap; no customer reached 13/15 score)", fontsize=13, fontweight="bold", color=PRIMARY_NAVY, pad=15)
    ax.set_xlabel("Delivered GMV (R$)", fontsize=11, fontweight="600", color=PRIMARY_NAVY, labelpad=10)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_currency_brl))
    
    for bar, (_, row) in zip(bars, df.iterrows()):
        w = bar.get_width()
        cust = int(row["customers"])
        avg_s = row["avg_spend"]
        ax.text(w + 60000, bar.get_y() + bar.get_height()/2, f"R$ {w:,.0f}\n({cust:,} cust | Avg R$ {avg_s:.2f})", ha="left", va="center", fontsize=9, fontweight="bold", color=PRIMARY_NAVY)
        
    ax.set_xlim(0, df["total_gmv"].max() * 1.35)
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "rfm_gmv.png"), dpi=300)
    plt.close()
    print("Saved charts/rfm_gmv.png")


# 6. Delivery Bucket vs Review Score Bar Chart
def chart_delivery_review():
    df = pd.read_csv(os.path.join(CLEAN_DIR, "delivery_vs_review.csv"))
    
    fig, ax1 = plt.subplots(figsize=(10, 6), dpi=300)
    
    x = np.arange(len(df))
    bars = ax1.bar(x, df["avg_review"], color=SLATE_BLUE, width=0.5, label="Average Review Score", zorder=3)
    
    # Color 30d+ bar coral
    bars[-1].set_color(CORAL_ACCENT)
    
    ax1.set_title("Average Customer Review Score by Delivery Duration Bucket\nLate delivery is associated with sharp review decline: 0-5d (4.45 stars) vs 30d+ (2.25 stars)", fontsize=13, fontweight="bold", color=PRIMARY_NAVY, pad=15)
    ax1.set_xlabel("Actual Delivery Duration Bucket", fontsize=11, fontweight="600", color=PRIMARY_NAVY, labelpad=10)
    ax1.set_ylabel("Average Review Score (1.0 - 5.0)", fontsize=11, fontweight="600", color=PRIMARY_NAVY, labelpad=10)
    ax1.set_xticks(x)
    ax1.set_xticklabels(df["delivery_bucket"], fontsize=10, fontweight="600")
    ax1.set_ylim(0, 5.2)
    
    for bar, (_, row) in zip(bars, df.iterrows()):
        h = bar.get_height()
        pct5 = row["pct_5star"]
        orders = int(row["orders"])
        ax1.text(bar.get_x() + bar.get_width()/2, h + 0.12, f"{h:.2f} / 5\n({pct5:.1f}% 5-star)\n{orders:,} ord", ha="center", va="bottom", fontsize=8.5, fontweight="bold", color=PRIMARY_NAVY)
        
    ax1.axhline(4.16, color=AMBER_ACCENT, linestyle="--", linewidth=1.5, label="National Mean: 4.16", zorder=4)
    ax1.legend(loc="upper right", frameon=True, facecolor="white", edgecolor="#CBD5E1")
    
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "delivery_review.png"), dpi=300)
    plt.close()
    print("Saved charts/delivery_review.png")


# 7. Cohort Retention Heatmap
def chart_cohort_heatmap():
    df = pd.read_csv(os.path.join(CLEAN_DIR, "cohort_retention.csv"))
    
    # Filter cohorts from 2017-01 to 2018-03 for readable matrix
    matrix_df = df.copy()
    cohort_months = matrix_df["cohort_month"].astype(str)
    
    # Select index 0 to 12
    cols = [c for c in matrix_df.columns if c not in ["cohort_month", "cohort_size"] and int(c) <= 12]
    retention_vals = matrix_df[cols].values
    cohort_sizes = matrix_df["cohort_size"].values
    
    # Calculate percentage retention
    pct_matrix = (retention_vals / cohort_sizes[:, np.newaxis]) * 100.0
    
    fig, ax = plt.subplots(figsize=(14, 10), dpi=300)
    
    cmap = plt.cm.Blues
    cax = ax.matshow(pct_matrix, cmap=cmap, vmin=0, vmax=1.5)
    
    fig.colorbar(cax, ax=ax, fraction=0.03, pad=0.04, label="Retention Rate (%)")
    
    ax.set_title("Customer Cohort Retention Rate (%) Across Months\nRepeat rate is ~3.0% overall; Sep 2016 (n=1) and Dec 2016 (n=1) are single-customer cohorts", fontsize=13, fontweight="bold", color=PRIMARY_NAVY, pad=20)
    
    ax.set_xticks(range(len(cols)))
    ax.set_xticklabels([f"M+{c}" if c != "0" else "M0" for c in cols], fontsize=9, fontweight="600")
    ax.xaxis.set_ticks_position("bottom")
    
    ax.set_yticks(range(len(cohort_months)))
    y_labels = [f"{m} (n={s:,})" for m, s in zip(cohort_months, cohort_sizes)]
    ax.set_yticklabels(y_labels, fontsize=8.5, color=PRIMARY_NAVY)
    
    # Add text annotations inside cells
    for i in range(len(cohort_months)):
        for j in range(len(cols)):
            val = pct_matrix[i, j]
            if not np.isnan(val) and val > 0:
                text_color = "white" if val > 0.8 else PRIMARY_NAVY
                if j == 0:
                    ax.text(j, i, "100%", ha="center", va="center", color="white", fontsize=7.5, fontweight="bold")
                else:
                    ax.text(j, i, f"{val:.1f}%", ha="center", va="center", color=text_color, fontsize=7)
                    
    plt.tight_layout()
    plt.savefig(os.path.join(CHARTS_DIR, "cohort_heatmap.png"), dpi=300)
    plt.close()
    print("Saved charts/cohort_heatmap.png")


def main():
    print("Generating 7 charts...")
    chart_monthly_gmv()
    chart_top_categories()
    chart_top_states()
    chart_review_dist()
    chart_rfm_gmv()
    chart_delivery_review()
    chart_cohort_heatmap()
    print("All charts generated successfully.")


if __name__ == "__main__":
    main()
