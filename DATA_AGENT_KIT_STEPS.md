> **SUPERSEDED — I chose the free Streamlit Cloud route instead of Google Cloud, so the BigQuery/Cloud Run steps in this file are NOT to be followed.**

# Google Cloud Data Agent Kit & BigQuery Deployment Guide
**Project:** Olist Brazilian E-Commerce Analytics  
**Author:** Ayushi Singh, Data Analyst  
**Active Project ID:** `dataanalytics-512912` (Configured in Data Agent Kit)  
**BigQuery Location:** `us` (or `southamerica-east1` for Brazil data residency)  

---

## TELEMETRY OPT-OUT NOTICE FOR USER
> **📌 Google Cloud Data Agent Kit Telemetry Notice:**  
> The Data Agent Kit plugin collects anonymous feature usage statistics and telemetry by default to help improve Google Cloud developer experiences.  
> You can opt out at any time in Antigravity IDE settings:  
> Navigate to **Settings > Extensions > Google > Datacloud: Enable Telemetry** and uncheck the box.

---

## OVERVIEW & CURRENT AUTHENTICATION STATUS
- **Local Analytics & Deliverables:** 100% verified and complete locally.
- **Google Cloud Status:** `gcloud` CLI is not installed on this workstation, and Google Cloud Application Default Credentials (ADC) are not authenticated.
- **Action Required by User:** To execute Step 8a (BigQuery upload) and Step 8b (Cloud Run deployment), complete the Google Cloud sign-in and project authentication steps detailed below. **Do NOT invent BigQuery query outputs or synthetic Cloud Run URLs until these steps are run.**

---

## STEP 1: AUTHENTICATION & ENVIRONMENT SETUP
1. Install the Google Cloud SDK (if not already installed):
   Download and install from: `https://cloud.google.com/sdk/docs/install`
2. Open PowerShell and authenticate your Google account:
   ```powershell
   gcloud auth login
   gcloud auth application-default login
   ```
3. Set your target project:
   ```powershell
   gcloud config set project dataanalytics-512912
   ```
4. Verify authentication:
   ```powershell
   gcloud auth list
   ```

---

## STEP 2: BIGQUERY DATASET CREATION & SUMMARY TABLES UPLOAD
Create the BigQuery dataset `olist` and upload the 8 clean summary CSV tables from `data/clean/`.  
*(Notice: Do NOT upload `olist_geolocation_dataset.csv`, `fact_orders.csv`, or `fact_order_items.csv` to keep storage and querying lightweight and cost-free).*

### 2.1 Create BigQuery Dataset:
```powershell
bq --location=US mk --dataset dataanalytics-512912:olist
```

### 2.2 Upload the 8 Clean Summary Tables:
```powershell
# 1. Monthly Summary Table
bq load --source_format=CSV --autodetect --skip_leading_rows=1 dataanalytics-512912:olist.monthly data/clean/monthly.csv

# 2. Category Summary Table
bq load --source_format=CSV --autodetect --skip_leading_rows=1 dataanalytics-512912:olist.category data/clean/category.csv

# 3. State Summary Table
bq load --source_format=CSV --autodetect --skip_leading_rows=1 dataanalytics-512912:olist.state data/clean/state.csv

# 4. Payment Type Table
bq load --source_format=CSV --autodetect --skip_leading_rows=1 dataanalytics-512912:olist.payment_type data/clean/payment_type.csv

# 5. Delivery vs Review Table
bq load --source_format=CSV --autodetect --skip_leading_rows=1 dataanalytics-512912:olist.delivery_vs_review data/clean/delivery_vs_review.csv

# 6. RFM Segments Summary Table
bq load --source_format=CSV --autodetect --skip_leading_rows=1 dataanalytics-512912:olist.rfm_segments data/clean/rfm_segments.csv

# 7. Review Distribution Table
bq load --source_format=CSV --autodetect --skip_leading_rows=1 dataanalytics-512912:olist.review_distribution data/clean/review_distribution.csv

# 8. Cohort Retention Table
bq load --source_format=CSV --autodetect --skip_leading_rows=1 dataanalytics-512912:olist.cohort_retention data/clean/cohort_retention.csv
```

---

## STEP 3: BIGQUERY GATE VERIFICATION QUERY
Run the mandatory verification query against BigQuery:
```sql
SELECT 
    ROUND(SUM(gmv), 2) AS total_gmv, 
    SUM(orders) AS total_orders 
FROM `dataanalytics-512912.olist.monthly`;
```

### Expected Output:
| Row | total_gmv | total_orders | Status |
|:---:|:---:|:---:|:---:|
| 1 | `13221498.11` | `96478` | **PASS (Exact Match)** |

If the query returns anything other than `13221498.11` and `96478`, STOP immediately — do not proceed to Cloud Run deployment until the data upload is corrected.

---

## STEP 4: SWITCHING STREAMLIT TO BIGQUERY (OPTIONAL CLOUD RUN MODE)
To query BigQuery directly in production, add `google-cloud-bigquery` and `db-dtypes` to `streamlit_app/requirements.txt`:
```txt
streamlit>=1.38.0
pandas>=2.2.0
matplotlib>=3.9.0
google-cloud-bigquery>=3.25.0
db-dtypes>=1.3.0
```

And update `streamlit_app/app.py` data loader function:
```python
from google.cloud import bigquery

@st.cache_data(ttl=3600)
def load_data_from_bigquery():
    client = bigquery.Client(project="dataanalytics-512912")
    monthly = client.query("SELECT * FROM `dataanalytics-512912.olist.monthly` ORDER BY purchase_month").to_dataframe()
    category = client.query("SELECT * FROM `dataanalytics-512912.olist.category` ORDER BY gmv DESC").to_dataframe()
    state = client.query("SELECT * FROM `dataanalytics-512912.olist.state` ORDER BY gmv DESC").to_dataframe()
    payment = client.query("SELECT * FROM `dataanalytics-512912.olist.payment_type` ORDER BY total_value DESC").to_dataframe()
    deliv_rev = client.query("SELECT * FROM `dataanalytics-512912.olist.delivery_vs_review`").to_dataframe()
    rfm_segments = client.query("SELECT * FROM `dataanalytics-512912.olist.rfm_segments`").to_dataframe()
    cohort = client.query("SELECT * FROM `dataanalytics-512912.olist.cohort_retention`").to_dataframe()
    rev_dist = client.query("SELECT * FROM `dataanalytics-512912.olist.review_distribution` ORDER BY review_score").to_dataframe()
    return monthly, category, state, payment, deliv_rev, rfm_segments, cohort, rev_dist
```

---

## STEP 5: CLOUD RUN DEPLOYMENT
Once Step 8a succeeds, deploy the Streamlit application to Google Cloud Run:
```powershell
gcloud run deploy olist-analytics `
    --source streamlit_app `
    --region southamerica-east1 `
    --allow-unauthenticated `
    --port 8501 `
    --memory 512Mi `
    --cpu 1
```

### Post-Deployment Verification Checklist:
1. Open the URL provided by Cloud Run (e.g. `https://olist-analytics-xxxx-xx.a.run.app`).
2. Verify Executive GMV reads **R$ 13,221,498.11** and orders read **96,478**.
3. Verify all 4 pages render with zero errors.
4. Record the live verified URL in `README.md`.

---

## COST ESTIMATION & ARCHITECTURAL EFFICIENCY
- **BigQuery Storage:** The 8 summary tables occupy less than 200 KB in total. Storage falls well within BigQuery's 10 GB free monthly tier ($0.00 cost).
- **BigQuery Compute:** Querying summary tables scans negligible bytes (< 1 MB per query), well within the 1 TB free monthly query tier ($0.00 cost).
- **Cloud Run Compute:** Cloud Run scales to zero instances when idle. With 512 MB memory and 1 vCPU, normal testing consumes fractions of a cent ($0.00 to $0.05).

---

## WHAT NOT TO CLAIM
- **Do NOT claim this is a "real-time" streaming pipeline:** The dataset ends in August 2018. It is a historical analysis.
- **Do NOT claim CAC, LTV:CAC, or Net Profit:** Advertising spend, overhead, and product costs do not exist in the Kaggle dataset.
- **Do NOT report a non-empty Champions segment:** With 97.0% one-time buyers, Champions (>=13 score) is legitimately 0.
