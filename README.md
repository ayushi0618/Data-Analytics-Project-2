# Olist Brazilian E-Commerce Analytics

An end-to-end data analytics project built on real transaction records from the Brazilian e-commerce marketplace Olist, cleaned and modelled to examine merchandise sales patterns, geographic concentration, the relationship between fulfillment duration and customer satisfaction, and buyer retention dynamics.

> 🌐 **Live Interactive Dashboard:** [streamlit link](https://data-analytics-project-2-euhenhxfrokktgat4nhfhv.streamlit.app/)  
> 📄 **Executive Project Document (PDF):** [Google Drive](https://drive.google.com/file/d/11IBUTnnbd6YbFqTW3roRHBF2nVkDegya/view?usp=drivesdk)  
> 📊 **Excel Analytical Workbook:** [Google Sheets / Drive](https://docs.google.com/spreadsheets/d/1KDrA8lUVef3bM692K-iXKCeDN5y14r9A/edit?usp=drivesdk)  
> ⚖️ **Licence:** [MIT License](LICENSE) (Code) | [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) (Dataset)

---

## Source and Licence
- **Source:** Kaggle [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) (`olistbr/brazilian-ecommerce`)
- **Dataset Licence:** Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International ([CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/))
- **Codebase Licence:** [MIT License](LICENSE)
- **Public Mirror:** `https://github.com/olist/work-at-olist-data`

---

## Headline Numbers (Delivered Orders Only)

All revenue and operational metrics are evaluated strictly on successfully delivered orders. Non-delivered order statuses (shipped, cancelled, unavailable, etc.) are tracked in status tables but excluded from GMV. Freight is reported separately as an operational fee and never conflated with merchandise GMV.

| Metric | Verified Value | Scope / Definition |
|:---|:---:|:---|
| **Delivered Orders** | **96,478** | 96,478 of 99,441 total orders (97.02% fulfillment rate) |
| **Delivered GMV** | **R$ 13,221,498.11** | SUM(item price) for delivered orders |
| **Delivered Freight** | **R$ 2,202,965.54** | SUM(freight_value) for delivered orders |
| **Delivered Payments** | **R$ 15,422,461.77** | SUM(payment_value) across delivered orders |
| **Reconciliation Difference** | **R$ 2,001.88** | GMV + Freight − Payments |
| **Average Order Value (AOV)** | **R$ 137.04** | Delivered GMV / Delivered Orders |
| **Average Review Score** | **4.16 / 5.00** | Order-weighted average (58.6% five-star reviews: 56,521 orders) |
| **Late Delivery Rate** | **8.11%** | Delivered date > Estimated delivery date (7,827 late orders) |
| **Average Delivery Duration** | **12.56 Days** | Mean transit time (purchase to customer delivery) |
| **Median Delivery Duration** | **10.22 Days** | 50th percentile delivery duration |
| **Top Product Category** | **health_beauty** | R$ 1,233,132 GMV (8,836 items sold) |
| **Top Customer State** | **São Paulo (SP)** | R$ 5,067,633 GMV (38.3% of national GMV) |
| **Repeat Customer Rate** | **3.0%** | 2,801 customers with >1 delivered order (out of 93,358) |

---

## The Two Core Findings

### 1. Delivery Lateness and Review Score Association
- **On-Time vs Late:** On-time orders average **4.30 stars** compared to **2.57 stars** for late orders—a difference of **1.73 rating points**.
- **Transit Duration Degradation:** Orders delivered in 0–5 days average **4.45 stars** (69.4% five-star reviews). Review scores decline monotonically as delivery time lengthens: 6–10 days (4.36★), 11–15 days (4.27★), 16–20 days (4.13★), 21–30 days (3.69★), and past 30 days drops to **2.25 stars** (only 15.9% five-star reviews).
- **Geographic Disparities in Lateness:** Destination states in the Southeast and Northeast exhibit substantial variation in fulfillment delay rates:
  - **São Paulo (SP):** 5.9% late rate (8.7 days avg delivery)
  - **Rio de Janeiro (RJ):** 13.5% late rate (15.0 days avg delivery)
  - **Bahia (BA):** 14.0% late rate (15.7 days avg delivery)
  - **Ceará (CE):** 15.3% late rate (20.8 days avg delivery)
- *Analytical note:* This is reported as an **association**, NOT as proof that delivery speed alone caused the rating. Packaging condition, merchant product descriptions, and courier handling co-occur with transit delays.

### 2. Repeat Purchase Deficit and Empty Champions Segment
- **Low Repeat Rate:** Only **3.0% of delivered customers (2,801 out of 93,358)** ever placed a subsequent order on Olist during the dataset window. 97.0% (90,557 buyers) purchased exactly once.
- **Empty Champions Segment:** Because 97.0% of buyers purchased only once, the frequency quintile collapses to 1 for all single-order customers. Under standard RFM scoring (R 1–5, F 1–5, M 1–5; Score = R+F+M, range 3–15), the maximum possible score without repeat transactions is 5 + 1 + 5 = 11. Consequently, **no customer reaches the 13/15 Champion threshold—the Champions segment is 0 (empty)** without invented data.
- **Segment Breakdown:**
  - **Champions (Score >= 13):** 0 customers (R$ 0.00 GMV)
  - **Loyal (Score >= 11):** 3,699 customers (R$ 1,513,441.00 GMV | R$ 409.15 avg spend)
  - **Recent / Potential (R >= 4):** 33,734 customers (R$ 3,896,175.16 GMV | R$ 115.50 avg spend)
  - **Regular (R = 3):** 18,709 customers (R$ 2,508,084.26 GMV | R$ 134.06 avg spend)
  - **Lost / Hibernating (R <= 2):** 37,216 customers (R$ 5,303,797.69 GMV | R$ 142.51 avg spend)

---

## Deliverable Links
- **Live Interactive Dashboard:**  
  [https://data-analytics-project-2-euhenhxfrokktgat4nhfhv.streamlit.app/](https://data-analytics-project-2-euhenhxfrokktgat4nhfhv.streamlit.app/)
- **Project Document (13 pages, PDF):**  
  [https://drive.google.com/file/d/11IBUTnnbd6YbFqTW3roRHBF2nVkDegya/view?usp=drivesdk](https://drive.google.com/file/d/11IBUTnnbd6YbFqTW3roRHBF2nVkDegya/view?usp=drivesdk)
- **Excel Workbook:**  
  [https://docs.google.com/spreadsheets/d/1KDrA8lUVef3bM692K-iXKCeDN5y14r9A/edit?usp=drivesdk](https://docs.google.com/spreadsheets/d/1KDrA8lUVef3bM692K-iXKCeDN5y14r9A/edit?usp=drivesdk)

---

## Project Structure

```
.
├── README.md                              # Executive summary, findings, and project documentation
├── LICENSE                                # MIT License for open source project code
├── requirements.txt                       # Root Python dependencies for cloud deployment
├── .streamlit/
│   └── config.toml                        # Safe UI and server settings (light theme, headless)
├── .gitignore                             # Git exclusion rules for large datasets, binaries, and virtual environments
├── build_olist.py                         # Re-runnable ETL and star-schema modeling script (verifies Gates 1 & 2)
├── generate_charts.py                     # Generates all 7 high-resolution matplotlib charts
├── build_excel.py                         # Builds Excel workbook with live formulas and native charts (verifies Gate 3)
├── build_pdf.py                           # Compiles the 13-page executive project document PDF
├── data/
│   └── clean/                             # Clean analytical tables & summary metadata
│       ├── monthly.csv                    # Full calendar Sep 2016 – Oct 2018 (26 months)
│       ├── category.csv                   # 72 English product categories with GMV and item metrics
│       ├── state.csv                      # 27 Brazilian customer states with GMV and late rates
│       ├── payment_type.csv               # 4 payment methods with installment statistics
│       ├── delivery_vs_review.csv         # 6 delivery duration buckets vs average review ratings
│       ├── rfm_customers.csv              # 93,358 customer RFM scores and segment assignments
│       ├── rfm_segments.csv               # 6 customer segment summaries
│       ├── cohort_retention.csv           # Monthly customer retention matrix (M0 to M20)
│       ├── review_distribution.csv        # Review score counts and percentage shares (1 to 5 stars)
│       ├── top_sellers.csv                # Top seller sales volumes and GMV performance
│       ├── seller_state.csv               # Seller geographic concentration
│       └── summary.json                   # Verified Gate metrics and complete transformation log
├── charts/                                # 7 publication-grade visualizations
│   ├── monthly_gmv.png                    # Monthly delivered GMV line chart
│   ├── top_categories.png                 # Top 10 product categories horizontal bar chart
│   ├── top_states.png                     # Top 10 customer states horizontal bar chart
│   ├── review_dist.png                    # Order review score distribution bar chart
│   ├── rfm_gmv.png                        # Delivered GMV by RFM customer segment bar chart
│   ├── delivery_review.png                # Review score by delivery duration bucket bar chart
│   └── cohort_heatmap.png                 # Customer cohort retention heatmap matrix
├── streamlit_app/
│   ├── app.py                             # 4-page interactive Streamlit web dashboard
│   └── requirements.txt                   # Streamlit environment dependencies
└── powerbi/
    ├── Power_Query_M.txt                  # Complete Power Query M transformation code
    ├── DAX_Measures.dax                   # 16 core DAX measures (using DIVIDE, zero hardcoded totals)
    └── Build_Guide.md                     # Step-by-step 4-page visual implementation specification
```

---

## How to Reproduce

1. **Download Kaggle Data:** Download the 9 CSV files from the Kaggle dataset (`olistbr/brazilian-ecommerce`) or clone the public mirror into `data/raw/`.
2. **Run Pipeline & Verification:**
   ```powershell
   python build_olist.py
   ```
   *Note: This script cleans the raw data, enforces Gate 1 & 2 verification checks, and outputs all clean tables. The full fact tables (`fact_orders.csv` ~33 MB, `fact_order_items.csv` ~17 MB, and `dim_product.csv`) are regenerated by this script and are intentionally excluded from the Git repository to keep the repository lightweight.*
3. **Generate Charts:**
   ```powershell
   python generate_charts.py
   ```
4. **Build Excel Workbook:**
   ```powershell
   python build_excel.py
   ```
5. **Launch Streamlit Dashboard:**
   ```powershell
   pip install -r streamlit_app/requirements.txt
   streamlit run streamlit_app/app.py
   ```

---

## Power BI Status (Honest Assessment)
Power Query M code (`powerbi/Power_Query_M.txt`), 16 core DAX measures (`powerbi/DAX_Measures.dax`), and a 4-page visual implementation specification (`powerbi/Build_Guide.md`) are provided in the repository. No `.pbix` binary is committed directly, as Power BI Desktop is a Windows GUI application that cannot be programmatically generated. The `.pbix` report is built in Power BI Desktop following the provided build pack.

---

## Live Dashboard & Cloud Status (Honest Assessment)
- **Live URL:** [https://data-analytics-project-2-euhenhxfrokktgat4nhfhv.streamlit.app/](https://data-analytics-project-2-euhenhxfrokktgat4nhfhv.streamlit.app/)
- **Hosting Platform:** Deployed 100% FREE on Streamlit Community Cloud directly from this GitHub repository (`ayushi0618/Data-Analytics-Project-2`, branch `main`).
- **Data Source for App:** The app reads verified analytical tables directly from `data/clean/`.
- **Infrastructure Scope:** No Google Cloud project, no BigQuery instance, and no Cloud Run container are used or billed. No credit card or paid service was required.
- **Service Characteristics:** On Streamlit Community Cloud free tier, the application may sleep when idle and take 20–30 seconds to wake on the first visit.
- **Analytical Scope:** This repository does NOT claim live streaming data, customer acquisition cost (CAC), LTV:CAC ratios, profit margins, or predictive sales forecasts. Delivered transactions terminate in August 2018; this is a historical analysis.

---

## Data Cleaning Log Summary
- **Review Deduplication:** 814 duplicate `review_id` rows dropped. For orders with more than one review, the first review per order was retained (243 subsequent reviews dropped).
- **Product Categories:** 623 products categorized as `Unknown` (610 missing Portuguese category in the raw data, 13 untranslated; no category was guessed).
- **Missing Delivery Dates:** 2,965 missing delivery dates and 160 missing approval dates preserved as missing; never imputed or fabricated.
- **Geolocation Excluded:** `olist_geolocation_dataset.csv` (1,000,163 rows, 59 MB) excluded from the relational model as state and city are already present in customer and seller tables.
- **Revenue Scope:** GMV is strictly confined to delivered orders (96,478 orders). Non-delivered statuses (cancelled: 625, unavailable: 609, shipped: 1,107, invoiced: 314, processing: 301, created: 5, approved: 2) are counted in status summaries but never in GMV.

---

## Licence

- **Software / Codebase:** Distributed under the [MIT License](LICENSE).
- **Dataset:** Brazilian E-Commerce Public Dataset by Olist is distributed under the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/) license.
