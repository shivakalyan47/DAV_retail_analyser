# Slide Deck Plan & Live Demonstration Script

## Indian Retail Sales and Revenue Analytics: An Interactive Python Dashboard
**Course:** Data Analytics and Visualization (DAV) Lab AAT  
**Presentation Timing:** 10–12 Minutes Total (Presentation + Live Demonstration)

---

## Part 1: Slide-by-Slide Presentation Structure (10 Slides)

```
┌────────────────────────────────────────────────────────────────────────┐
│ SLIDE 1: Title & Team Information                                      │
├────────────────────────────────────────────────────────────────────────┤
│ • Title: Indian Retail Sales and Revenue Analytics                     │
│ • Subtitle: An Interactive Python Dashboard for DAV Lab AAT            │
│ • Academic Details: Course Code: 21CS54 | Semester: V/VI               │
│ • Student 1: [Name, USN, Section]                                      │
│ • Student 2: [Name, USN, Section]                                      │
│ • Faculty Guide: [Professor Name], Dept. of Computer Science & Engg.  │
│ • Visual: Clean banner with Python, Streamlit, and Plotly logos        │
└────────────────────────────────────────────────────────────────────────┘
```

```
┌────────────────────────────────────────────────────────────────────────┐
│ SLIDE 2: Problem Statement & Motivation                                │
├────────────────────────────────────────────────────────────────────────┤
│ • Context: Indian retail is shifting toward omnichannel e-commerce.   │
│ • Challenge: Unstructured transaction logs suffer from:                │
│   - Dirty records (negative counts, malformed dates, duplicate lines)  │
│   - Double-counting errors between line items and distinct checkouts   │
│   - Static, non-responsive spreadsheet reports                         │
│ • Solution: An automated cleaning pipeline and reactive Streamlit web │
│   dashboard providing multi-dimensional retail intelligence.           │
│ • Academic Disclosure: Evaluated on synthetic data (reproducible seed).│
└────────────────────────────────────────────────────────────────────────┘
```

```
┌────────────────────────────────────────────────────────────────────────┐
│ SLIDE 3: Project Objectives & Scope                                    │
├────────────────────────────────────────────────────────────────────────┤
│ • Objectives:                                                          │
│   1. Implement modular data cleaning with quality audit logging.       │
│   2. Calculate core retail metrics (Revenue, Orders, Units, AOV).      │
│   3. Analyze product, category, regional, and payment breakdowns.      │
│   4. Construct an interactive 5-page dashboard with dynamic filters.   │
│   5. Ensure 100% test coverage using Pytest.                           │
│ • Scope: End-to-end Python stack (Pandas, Plotly, Streamlit, Pytest).  │
│ • Excluded: Complex ML models and paid external cloud APIs.            │
└────────────────────────────────────────────────────────────────────────┘
```

```
┌────────────────────────────────────────────────────────────────────────┐
│ SLIDE 4: Dataset Architecture & Schema                                 │
├────────────────────────────────────────────────────────────────────────┤
│ • Provenance: Generated via NumPy/Pandas (Seed: 42, 15,015 raw rows). │
│ • Features (20 Columns):                                               │
│   - Identifiers: order_id, customer_id, product_id                     │
│   - Customer Profile: customer_name, customer_segment                  │
│   - Catalog: category (7), sub_category, product_name (200 SKUs)       │
│   - Financials: quantity, unit_price, discount_percent, sales_amount   │
│   - Logistics: profit, shipping_cost, payment_method (5), order_status │
│   - Geography: state (19 Indian states), city                          │
│ • Data Integrity: Clean raw/processed directory separation.           │
└────────────────────────────────────────────────────────────────────────┘
```

```
┌────────────────────────────────────────────────────────────────────────┐
│ SLIDE 5: Preprocessing & Data Wrangling Pipeline                       │
├────────────────────────────────────────────────────────────────────────┤
│ • Step 1: Column Standardization (clean snake_case).                   │
│ • Step 2: Exact Duplicate Removal (15 duplicate rows pruned).          │
│ • Step 3: Date Bounds Validation (20 rows outside 2020–2026 removed).  │
│ • Step 4: Numeric Coercion (10 negative-quantity error rows removed).  │
│ • Step 5: Imputation (300 discounts filled with 0; text with 'Unknown')│
│ • Step 6: Recalculate Sales Amount = qty * price * (1 - disc/100).     │
│ • Step 7: Temporal Feature Engineering (year, month, quarter, period). │
│ • Final Cleaned Count: 14,970 verified records (0.3% outlier removal). │
└────────────────────────────────────────────────────────────────────────┘
```

```
┌────────────────────────────────────────────────────────────────────────┐
│ SLIDE 6: Mathematical Formulations & Aggregation Logic                │
├────────────────────────────────────────────────────────────────────────┤
│ • Total Gross Revenue: Σ [ qty * price * (1 - discount/100) ]          │
│ • Distinct Orders: COUNT(DISTINCT order_id) — avoids double-counting   │
│ • Average Order Value (AOV): Total Gross Revenue / Distinct Orders     │
│ • Profit Margin (%): [ Total Profit / Total Revenue ] * 100            │
│ • Return Rate (%): [ Returned Orders / Distinct Orders ] * 100         │
│ • Repeat Customer Rate (%): [ Repeat Customers / Total Customers ] *100│
│ • Safe Math: safe_divide() guards against zero denominators.           │
└────────────────────────────────────────────────────────────────────────┘
```

```
┌────────────────────────────────────────────────────────────────────────┐
│ SLIDE 7: Key Analytical Findings & Business Metrics                    │
├────────────────────────────────────────────────────────────────────────┤
│ • Total Gross Revenue: ₹22.06 Crore (₹22,06,33,094.50) across 14,970   │
│   distinct orders and 50,654 units sold.                               │
│ • Average Order Value: ₹14,738.35 per order.                           │
│ • Net Profit: ₹2.71 Crore (₹2,71,38,823.10) with 12.30% profit margin. │
│ • Category Leader: Electronics represents 74.88% (₹16.52 Cr) of revenue│
│ • Volume Leader: Sports generates highest unit turnover (7,740 units). │
│ • Geographic Leader: Maharashtra ranks #1 with ₹3.21 Cr (14.53% share).│
│ • Payment Leader: UPI dominates with 35.12% share (5,257 orders).      │
│ • Quality Metrics: 8.20% return rate, 4.94% cancellation rate.        │
└────────────────────────────────────────────────────────────────────────┘
```

```
┌────────────────────────────────────────────────────────────────────────┐
│ SLIDE 8: Interactive Dashboard Architecture                            │
├────────────────────────────────────────────────────────────────────────┤
│ • Framework: Streamlit with wide-screen multi-column responsive layout │
│ • Visual Engine: Plotly Express & Plotly Graph Objects (14 chart types)│
│ • Modular Pages:                                                       │
│   1. Executive Overview: KPI cards, monthly trends, category shares    │
│   2. Product Analytics: Top N rankings, volume vs revenue scatter      │
│   3. Regional Analytics: State & city rankings with tabular metrics    │
│   4. Customer & Returns: Repeat rates, return analysis, payment share  │
│   5. Data Quality: Provenance, correlation matrix, schema report       │
│ • Sidebar Controls: Dynamic multi-criteria filters + CSV data export   │
│ • Performance: @st.cache_data for instant sub-second filtering.       │
└────────────────────────────────────────────────────────────────────────┘
```

```
┌────────────────────────────────────────────────────────────────────────┐
│ SLIDE 9: Testing, Quality Assurance & Verification                     │
├────────────────────────────────────────────────────────────────────────┤
│ • Framework: Pytest automated testing suite.                           │
│ • Test Battery: 60 automated unit and integration tests.               │
│ • Results: 60 Passed in 5.62 seconds (100% test passage).              │
│ • Verified Scenarios:                                                  │
│   - Edge cases: Empty DataFrames, zero-denominator divisions           │
│   - Transformations: Column cleaning, datetime bounds, duplicate drops │
│   - Metrics: Correct distinct order counting, INR formatting           │
│   - Integrity: Preservation of legitimate negative operational profits │
└────────────────────────────────────────────────────────────────────────┘
```

```
┌────────────────────────────────────────────────────────────────────────┐
│ SLIDE 10: Conclusion, Limitations & Future Enhancements                │
├────────────────────────────────────────────────────────────────────────┤
│ • Conclusion: Developed a complete, modular, testable retail analytics │
│   platform suitable for academic and operational demonstration.        │
│ • Limitations: Evaluated on synthetic data; lacks GIS shapefiles.      │
│ • Future Scope:                                                        │
│   - Integration of real Kaggle e-commerce datasets                     │
│   - India GeoJSON choropleth map visualizer                            │
│   - Predictive time-series sales forecasting (ARIMA / Prophet)         │
│   - Automated PDF report compilation and export                        │
└────────────────────────────────────────────────────────────────────────┘
```

---

## Part 2: Step-by-Step Live Demonstration Script

**Target Duration:** 5–6 Minutes  
**Prerequisites:** 
- Open terminal in `c:\Users\shiva\Downloads\DAV AAT`
- Execute: `streamlit run app.py`
- Browser opens at `http://localhost:8501`

---

### Step 1: Opening & Executive Overview (1.5 Minutes)
- **Speaker:** "Good morning, respected faculty and evaluators. Today we present our DAV Lab AAT project: *Indian Retail Sales and Revenue Analytics: An Interactive Python Dashboard*."
- **Action:** Point to the title banner, synthetic data disclaimer, and top KPI cards.
- **Explain:**
  - "Notice the four prominent KPI cards at the top: Total Gross Revenue is **₹22.06 Cr**, Total Distinct Orders is **14,970**, Units Sold is **50,654**, and Average Order Value is **₹14,738.35**."
  - "Below, the Monthly Revenue Trend line chart shows peak sales occurring in Q4 (specifically December 2022 with **₹94.83 L**), capturing festive shopping seasonality."
  - "The Category Bar chart clearly demonstrates that Electronics drives **74.88%** of total business turnover."
  - "At the bottom of Page 1, our analytics engine automatically outputs data-derived key insight cards summarizing top performers."

---

### Step 2: Dynamic Sidebar Filtering Demonstration (1 Minute)
- **Speaker:** "Now let's demonstrate the interactive filtering capabilities that update all charts and metrics in real time."
- **Action 1:** In the sidebar, select **State** $\rightarrow$ choose `Maharashtra` and `Karnataka`.
- **Explain:** "Observe how the KPI cards instantly update to reflect only the combined revenue of Maharashtra and Karnataka. The Monthly Trend and Category charts adjust automatically."
- **Action 2:** Select **Category** $\rightarrow$ choose `Electronics`.
- **Explain:** "The product list filter now dynamically scopes down to only electronics SKUs."
- **Action 3:** Click **🔄 Reset All Filters**.
- **Explain:** "A single click resets all parameters back to the full dataset of 14,970 records."

---

### Step 3: Product & Regional Analytics (1 Minute)
- **Action:** Navigate to **🏷️ Product Analytics** in the sidebar.
- **Explain:**
  - "Here we have an interactive Top N slider. If we adjust it from 10 to 15, both the revenue and unit volume charts update dynamically."
  - "Notice the Scatter Plot: It contrasts total units sold against total revenue. Products like Sports Shoes sell over 1,500 units but generate lower turnover, whereas Laptops sell 1,134 units and generate over **₹5.51 Cr**."
- **Action:** Navigate to **🗺️ Regional Analytics**.
- **Explain:** "Here we display ranked revenue across all 19 states. Maharashtra leads at **₹3.21 Cr**, followed by Delhi at **₹2.29 Cr**."

---

### Step 4: Customer & Returns Analytics (1 Minute)
- **Action:** Navigate to **👥 Customer & Returns**.
- **Explain:**
  - "Our Customer Overview card indicates that out of 2,975 unique buyers, 2,863 are repeat purchasers, giving a repeat rate of **96.24%**."
  - "The Order Status Donut chart reveals an **8.20% return rate** and a **4.94% cancellation rate**."
  - "The Payment Method chart highlights Indian consumer preferences: **UPI is the #1 payment rail at 35.12%**, followed by Cash on Delivery at **24.24%**."
  - "The Profit Analysis section confirms an overall profit margin of **12.30%** with 668 loss-making promotion transactions accurately captured."

---

### Step 5: Data Quality, Tests & Data Export (1 Minute)
- **Action:** Navigate to **🔍 Data Quality & Methodology**.
- **Explain:**
  - "Academic projects must maintain data transparency. This page documents our dataset provenance, explicit synthetic disclosures, and preprocessing steps."
  - "The Correlation Heatmap shows a 0.85 correlation between sales amount and profit."
  - "We also show the full descriptive statistics table with quartiles, standard deviations, and memory footprints."
- **Action:** Scroll to the bottom and click **📥 Download Filtered Data (CSV)**.
- **Explain:** "Users can export the exact filtered dataset to CSV at any time for downstream reporting."
- **Closing:** "To ensure production-grade reliability, our test suite has **60 automated Pytest test cases with 100% pass rate**. Thank you, and we welcome your questions!"
