# Olist Brazilian E-Commerce Analytics — Power BI Desktop Build Guide
**Author:** Ayushi Singh, Data Analyst  
**Data Source:** Kaggle (`olistbr/brazilian-ecommerce`, CC BY-NC-SA 4.0)  
**Scope Rule:** Strictly Delivered Orders Only (96,478 orders | GMV: R$ 13,221,498.11)

---

## IMPORTANT NOTICE ON POWER BI ARTIFACTS
> **⚠️ Power BI Desktop Environment Notice:**  
> Power BI Desktop is a proprietary Windows GUI application. It cannot be generated programmatically as a raw `.pbix` binary file by an automated coding agent.  
> **Power BI Desktop IS installed on this system** as a Microsoft Store application (`Microsoft.MicrosoftPowerBIDesktop`, Version 2.159.883.0). Per project governance rules, the agent will **NOT** attempt to blindly drive the Windows desktop GUI.  
> Instead, this guide provides the exact, production-ready step-by-step instructions, verbatim visual specifications, field mappings, slicers, DAX formulas, and verification totals to build the `.pbix` in Power BI Desktop on Windows.  
> **A failed verification total is an error, not a number to adjust.** If your model does not return the exact figures below, do NOT force or tweak measures — verify your data load and relationships.

---

## 5 MANDATORY VERIFICATION TOTALS (Check Before Building Visuals)
Before adding any visual elements to the report canvas, build a test card or table and verify these five core numbers:
1. **Delivered GMV:** `R$ 13,221,498.11`
2. **Delivered Orders:** `96,478`
3. **Average Order Value (AOV):** `R$ 137.04`
4. **Average Review Score:** `4.16`
5. **Late Delivery Rate:** `8.11%`

---

## DATA MODELING & RELATIONSHIPS (Star Schema)
1. In Power BI Desktop, open **Home > Transform Data (Power Query Editor)**.
2. In Power Query, open **Advanced Editor** and paste the code from `powerbi/Power_Query_M.txt` (or import the clean CSVs from `data/clean/`).
3. Set the `CleanDataPath` parameter to your local `data\clean\` path.
4. Close & Apply.
5. In **Model View**, establish the following 1-to-Many single-directional relationships:
   - `Dim_Customer[customer_unique_id]` 1 ─── * `Fact_Orders[customer_unique_id]`
   - `Dim_Date[Date]` 1 ─── * `Fact_Orders[purchase_date]`
   - `Fact_Orders[order_id]` 1 ─── * `Fact_Order_Items[order_id]`
   - `Dim_Product[product_id]` 1 ─── * `Fact_Order_Items[product_id]`
6. Create a dedicated **Measures** table and paste the DAX formulas from `powerbi/DAX_Measures.dax`.

---

## REPORT PAGE SPECIFICATIONS (4 PAGES)

### PAGE 1: EXECUTIVE OVERVIEW
- **Canvas Size:** 16:9 (1280 × 720 px)
- **Page Title:** Executive Performance Overview
- **Header Banner:** Deep Navy (`#0F2040`) banner with white bold title text: *"Olist Brazilian E-Commerce Analytics — Executive Overview"*.
- **Top Slicers:**
  - **Year Slicer:** Field `Dim_Date[Year]` (Dropdown / Tiles: 2016, 2017, 2018).
  - **State Slicer:** Field `Fact_Orders[customer_state]` (Dropdown multi-select).
- **Top Row KPI Cards (4 Visuals):**
  1. **Delivered GMV Card:** Measure `[Delivered GMV]`, Display Units: None, Currency formatting: `R$ #,##0.00`. Target: `R$ 13,221,498.11`.
  2. **Delivered Orders Card:** Measure `[Delivered Orders]`, Number formatting: `#,##0`. Target: `96,478`.
  3. **Average Order Value Card:** Measure `[Avg Order Value]`, Formatting: `R$ #,##0.00`. Target: `R$ 137.04`.
  4. **Average Review Score Card:** Measure `[Avg Review Score]`, Formatting: `0.00`. Target: `4.16 / 5.00`.
- **Main Chart 1 (Left 60%): Line Chart — Monthly Delivered GMV**
  - **X-Axis:** `Dim_Date[YearMonth]` (sorted ascending).
  - **Y-Axis:** `[Delivered GMV]`.
  - **Line Color:** Slate Blue (`#1E40AF`), Line width: 3, Data markers: On.
  - **Annotation/Callout Text Box:** *"Black Friday 2017 peak: R$ 987,765 across 7,289 orders. Nov 2016 is a raw data gap (0 orders); Sep-Oct 2018 is extraction cutoff."*
- **Main Chart 2 (Right 40%): Donut / Bar Chart — Payment Methods Share**
  - **Legend / Axis:** `Summary_Payment[payment_type]`.
  - **Values:** `Summary_Payment[total_value]`.
  - **Data Labels:** Percentage of Total & Value in BRL.
- **Verbatim Text Box (Bottom):**
  > *"Scope Rule: Confined strictly to delivered orders (96,478 orders). Shipped, cancelled, and unavailable orders are excluded from GMV calculations. Reconciliation discrepancy between GMV + Freight and customer payment receipts is exactly R$ 2,001.88 across the dataset."*

---

### PAGE 2: CATEGORY & GEOGRAPHY
- **Page Title:** Category Demand & Geographic Logistics
- **Top Slicers:**
  - Category search dropdown: `Fact_Order_Items[category_en]`.
  - Destination State multi-select: `Fact_Orders[customer_state]`.
- **Visual 1 (Top Left): Horizontal Clustered Bar Chart — Top 10 Product Categories by GMV**
  - **Y-Axis:** `Fact_Order_Items[category_en]`.
  - **X-Axis:** `[Delivered GMV]`.
  - **Top N Filter:** Top 10 by `[Delivered GMV]`.
  - **Bar Color:** Slate Blue (`#1E40AF`), with top bar `health_beauty` colored Coral (`#E11D48`).
  - **Data Labels:** On, Formatted as `R$ #,##0`.
- **Visual 2 (Top Right): Horizontal Clustered Bar Chart — Top 10 Customer States by GMV**
  - **Y-Axis:** `Fact_Orders[customer_state]`.
  - **X-Axis:** `[Delivered GMV]`.
  - **Top N Filter:** Top 10 by `[Delivered GMV]`.
  - **Bar Color:** Navy (`#0F2040`).
  - **Data Labels:** On, Formatted as `R$ #,##0`.
- **Visual 3 (Bottom Table): State Delivery Health Matrix**
  - **Columns:** `Fact_Orders[customer_state]`, `[Delivered Orders]`, `[Delivered GMV]`, `[Avg Delivery Days]`, `[Late Rate]`, `[Avg Review Score]`.
  - **Conditional Formatting:** Color scale on `[Late Rate]` (Green for 5.9% SP to Red for 15.3% CE).
- **Verbatim Text Box:**
  > *"São Paulo (SP) dominates demand with R$ 5,067,633 (38.3% of national GMV) and the lowest major state late rate (5.9%). In contrast, destination states in the Northeast and Southeast suffer acute logistics delays: Rio de Janeiro (13.5% late), Bahia (14.0% late), and Ceará (15.3% late), resulting in lower review satisfaction."*

---

### PAGE 3: DELIVERY & SATISFACTION
- **Page Title:** Logistics SLAs & Customer Satisfaction Impact
- **Headline Alert Card (Full Width):**
  - **Background:** Soft Coral (`#FFE4E6`), Border: Crimson (`#E11D48`).
  - **Text:** *"🚨 ON-TIME ORDERS AVERAGE 4.30 STARS VS LATE ORDERS 2.57 STARS — LATENESS DRIVES A 1.73-STAR REPUTATIONAL COLLAPSE."*
- **Visual 1 (Left 50%): Column Chart — Average Review Score by Actual Delivery Bucket**
  - **X-Axis:** `Summary_Delivery_Review[delivery_bucket]` (sorted: `0-5d`, `6-10d`, `11-15d`, `16-20d`, `21-30d`, `30d+`).
  - **Y-Axis:** `Summary_Delivery_Review[avg_review]`.
  - **Reference Line:** Constant line at `4.16` (National Mean), Color: Amber (`#D97706`).
  - **Data Labels:** On (`4.45`, `4.36`, `4.27`, `4.13`, `3.69`, `2.25`).
- **Visual 2 (Right 50%): Column Chart — Order Review Score Distribution**
  - **X-Axis:** `Summary_Review_Dist[review_score]` (1 to 5 Stars).
  - **Y-Axis:** `Summary_Review_Dist[count]`.
  - **Bar Colors:** 1 Star (`#EF4444`), 2 Stars (`#F97316`), 3 Stars (`#FBBF24`), 4 Stars (`#34D399`), 5 Stars (`#10B981`).
  - **Data Labels:** Value & % of Delivered Orders (`58.6% for 5-star`).
- **Visual 3 (Bottom): Detailed Delivery Bucket Table**
  - **Columns:** Delivery Bucket, Delivered Orders, Share of Orders (%), Avg Review Score, 5-Star Share (%).
- **Verbatim Text Box:**
  > *"Customer reviews exhibit a sharp cliff beyond 15 days of transit. While 0–5 day deliveries achieve 69.4% five-star ratings, orders delayed past 30 days plummet to 15.9% five-star ratings and an average score of 2.25 / 5.00. Expedited delivery and proactive SLA management are the single largest levers for customer satisfaction."*

---

### PAGE 4: CUSTOMERS: RFM & COHORTS
- **Page Title:** Customer Segmentation & Retention Dynamics
- **Headline Alert Card:**
  - **Background:** Soft Amber (`#FEF3C7`), Border: Amber (`#D97706`).
  - **Text:** *"⚠️ CUSTOMER LOYALTY GAP: ONLY 3.0% OF DELIVERED CUSTOMERS MADE A REPEAT PURCHASE (2,801 OUT OF 93,358). NO CUSTOMER REACHES THE 13/15 CHAMPION SCORE — CHAMPIONS SEGMENT IS 0 (EMPTY)."*
- **Visual 1 (Left 50%): Horizontal Clustered Bar Chart — GMV by RFM Segment**
  - **Y-Axis:** `Summary_RFM[segment]` (`Loyal`, `Recent/Potential`, `Regular`, `Lost/Hibernating`).
  - **X-Axis:** `Summary_RFM[total_gmv]`.
  - **Bar Color:** Slate Blue (`#1E40AF`).
  - **Data Labels:** Value in BRL.
- **Visual 2 (Right 50%): Matrix Table — RFM Segments Summary**
  - **Rows:** `Summary_RFM[segment]`.
  - **Values:** `Summary_RFM[customers]`, `Summary_RFM[total_gmv]`, `Summary_RFM[avg_spend]`, `Summary_RFM[share_of_customers]`, `Summary_RFM[share_of_gmv]`.
  - **Highlight:** Loyal segment has 3,699 customers with average spend R$ 409.15.
- **Visual 3 (Bottom): Customer Cohort Retention Heatmap Matrix**
  - **Rows:** `Summary_Cohort[cohort_month]` (Jan 2017 to Aug 2018).
  - **Columns:** M0, M+1, M+2, M+3 ... M+12.
  - **Values:** Cohort customer count and retention rate (%).
  - **Conditional Formatting:** Gradient fill from light blue to deep navy.
- **Verbatim Text Box:**
  > *"Cohort Statistical Note: September 2016 (n=1) and December 2016 (n=1) are single-customer beta cohorts and must NOT be interpreted as standard cohort retention rates. Across all commercial cohorts, Month 1+ retention remains below 0.5%, proving that Olist functioned almost entirely as a one-time acquisition funnel rather than a repeat-purchase ecosystem."*

---

## FINAL VALIDATION CHECKLIST
- [ ] Delivered GMV equals `R$ 13,221,498.11`.
- [ ] Delivered Orders equals `96,478`.
- [ ] Average Review equals `4.16`.
- [ ] Late Delivery Rate equals `8.11%`.
- [ ] Champions count is `0` (not forced or imputed).
- [ ] Loyal customers count is `3,699` with average spend `R$ 409.15`.
- [ ] No CAC, profit, or margin measures created (unsupported by dataset).
- [ ] Save the workbook as `Olist_Ecommerce_Analytics.pbix` in Power BI Desktop.
