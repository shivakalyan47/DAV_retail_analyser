# Indian Retail Sales and Revenue Analytics: An Interactive Python Dashboard

## Mini-Project Report

**Course:** Data Analytics and Visualization (DAV) Lab AAT  
**Academic Year:** 2026-27  
**Course Code:** 21CS54 / DAV Lab  
**Semester:** V / VI  

---

### Team Details

| Role | Student Name | USN | Section | Email |
| :--- | :--- | :--- | :--- | :--- |
| **Student 1 (Lead)** | _[Student 1 Name]_ | _[USN 1]_ | _[Sec]_ | _[email1@college.edu]_ |
| **Student 2 (Co-Lead)** | _[Student 2 Name]_ | _[USN 2]_ | _[Sec]_ | _[email2@college.edu]_ |

**Faculty Guide:** _[Prof. Faculty Name]_  
**Department:** Department of Computer Science & Engineering / Information Science  
**Institution:** _[Engineering College / University Name, City, State]_  

---

## 1. Abstract

Modern retail businesses generate extensive multi-dimensional transaction records that encapsulate customer purchase behaviors, geographic demand patterns, and operational margins. This project presents an end-to-end, reproducible Data Analytics and Visualization (DAV) pipeline and an interactive web dashboard developed in Python for Indian retail sales analytics. The system ingests raw transaction data, executes standardized data cleaning and validation routines, calculates core retail Key Performance Indicators (KPIs), conducts descriptive statistical modeling, and visualizes dynamic insights across executive, product, regional, and customer dimensions. The accompanying interactive dashboard is implemented using Streamlit and Plotly, supported by automated Pytest suites. The dataset utilized comprises 15,015 initial synthetic transaction records across 19 Indian states and 7 product categories, specifically designed to model Indian commerce while maintaining academic integrity through explicit synthetic data disclosures.

---

## 2. Introduction

The Indian retail ecosystem is one of the most vibrant and rapidly evolving sectors globally, experiencing a structural shift driven by digital payments (notably Unified Payments Interface - UPI), smartphone penetration, and tier-2/tier-3 city consumer expansion. Retail analytics enables enterprises to transition from reactive reporting to evidence-based decision-making. 

In this Data Analytics and Visualization (DAV) Lab Alternative Assessment Task (AAT), we design and implement a modular Python software suite and interactive analytics dashboard that addresses end-to-end analytical tasks: from raw schema ingestion and anomalous data handling to multi-variate statistical aggregation and reactive front-end dashboard presentation.

### Academic Context and Justification
- **Hands-on Analytics Pipeline:** Combines standard Python data structures (Pandas, NumPy) with web-based visualization frameworks (Plotly, Streamlit).
- **Practical Domain:** Demonstrates business-critical retail metrics including Average Order Value (AOV), category contribution margins, regional revenue shares, and return rates.
- **Scientific Integrity:** Models real-world data quality issues (missing values, malformed timestamps, anomalous negative quantities, and duplicate order entries) while explicitly disclosing data provenance.

---

## 3. Problem Statement

Retail management and operations teams face substantial hurdles when attempting to derive actionable intelligence from large, unstructured, or dirty transaction logs. Specific challenges include:
1. **Data Inconsistency:** Raw transaction dumps often suffer from human entry errors, negative order counts, duplicate rows, and unstandardized column formats.
2. **Double-Counting and Granularity Errors:** Mistaking order-line items for unique orders inflates order frequency metrics and distorts Average Order Value (AOV).
3. **Regional and Categorical Blindspots:** Inability to isolate underperforming regional markets, evaluate shipping cost impacts, or assess return rates.
4. **Static Reporting Bottlenecks:** Traditional spreadsheet summaries cannot provide dynamic filtering across dates, states, payment mechanisms, or customer segments.

**Objective:** Develop a robust, testable, and interactive Python dashboard that processes India-focused retail transaction data, enforces automated data cleaning rules, calculates precise retail KPIs, visualizes trends, and offers intuitive user exploration with dynamic filtering.

---

## 4. Objectives

The specific measurable objectives of this project are:
1. **Dataset Selection and Architecture:** Ingest a 20-field retail dataset simulating Indian market dynamics and define a clean separation between raw and processed data.
2. **Data Preprocessing & Validation:** Detect and clean missing values, eliminate exact duplicates, filter anomalous dates and negative quantities, and derive temporal features (`year`, `month`, `quarter`, `year_month`).
3. **Descriptive & Aggregative Analysis:** Calculate foundational retail KPIs:
   - Total Gross Revenue
   - Distinct Order Count
   - Cumulative Units Sold
   - Average Order Value (AOV)
   - Category and Product-level Contribution
   - State and City-level Distribution
   - Repeat Customer Rates and Order Fulfillment Statuses
4. **Interactive Dashboard Development:** Construct a 5-page Streamlit web application with interactive Plotly visualizations and comprehensive sidebar filters.
5. **Quality Assurance & Testing:** Implement automated unit tests via Pytest covering edge cases, division-by-zero safeguards, and data transformations.
6. **Academic Documentation & Viva Preparation:** Compile a comprehensive technical report, presentation plan, and viva question bank.

---

## 5. Scope of the Project

### In-Scope
- Automated data loading and caching architecture.
- Full cleaning pipeline handling missing categorical entries, duplicate lines, and negative quantities.
- Multi-dimensional descriptive statistics, correlation matrices, and distribution histograms.
- 5 dedicated dashboard modules: Executive Overview, Product Analytics, Regional Analytics, Customer & Returns Analytics, and Data Quality & Provenance.
- Multi-criteria filtering (Date Range, State, Category, Product, Customer Segment, Payment Method, Order Status) and filtered CSV dataset export.
- 60 comprehensive Pytest test cases.

### Out-of-Scope
- Complex machine learning or neural predictive modeling (prioritizing clear data analytics and visualization per course syllabus).
- Live real-time streaming connections to external cloud APIs or paid database subscriptions.
- Payment gateway integrations or real-world consumer financial processing.

---

## 6. Dataset Description and Provenance

### Provenance Metadata

| Property | Description |
| :--- | :--- |
| **Dataset Title** | Indian Retail Sales and Revenue Dataset |
| **Data Modality** | Tabular Transactional Record (CSV) |
| **Data Nature** | **Synthetic / Academic Simulation** (Generated via NumPy/Pandas) |
| **Generator Script** | `data/generate_synthetic_data.py` (Fixed seed: 42) |
| **Licensing** | Creative Commons Zero (CC0 - Public Domain) |
| **Generation Date** | October 2026 |
| **Raw Dimension** | 15,015 rows × 20 columns (2.53 MB) |
| **Cleaned Dimension**| 14,970 rows × 26 columns (2.61 MB) |
| **Temporal Span** | January 1, 2022 to December 31, 2024 (excluding injected bad dates) |

### ⚠️ Explicit Synthetic Data Disclosure
The dataset utilized in this project is entirely synthetic, formulated using controlled stochastic distributions to reflect authentic Indian retail attributes (e.g., Diwali shopping seasonality, UPI payment dominance, tier-1 state economic weights). It does **not** reflect real financial data of any commercial entity, real citizen names, or official government census data. All findings herein serve as a practical demonstration of analytics methodology.

### Schema and Field Descriptions

| # | Attribute | Type | Example Value | Description |
|---|:---|:---|:---|:---|
| 1 | `order_id` | String | `ORD-00142` | Unique transaction identifier |
| 2 | `order_date` | Date | `2023-10-18` | Date of order placement |
| 3 | `customer_id` | String | `CUST-0842` | Unique customer alphanumeric code |
| 4 | `customer_name` | String | `Aarav Sharma` | Synthetic Indian customer name |
| 5 | `customer_segment` | Category | `Consumer` | Segment: Consumer, Corporate, Home Office |
| 6 | `product_id` | String | `PROD-045` | Unique product stock keeping unit (SKU) |
| 7 | `product_name` | String | `Smartwatches` | Product title within retail catalog |
| 8 | `category` | Category | `Electronics` | 1 of 7 broad retail departments |
| 9 | `sub_category` | Category | `Wearables` | Granular product sub-classification |
| 10 | `quantity` | Integer | `3` | Units purchased in order line (1 to 10) |
| 11 | `unit_price` | Float | `4500.00` | Base selling price per unit in INR (₹) |
| 12 | `discount_percent`| Float | `10.0` | Discount applied (0% to 30%) |
| 13 | `sales_amount` | Float | `12150.00` | Net revenue: `qty × price × (1 - disc/100)` |
| 14 | `profit` | Float | `1822.50` | Net operational profit or loss |
| 15 | `shipping_cost` | Float | `350.00` | Logistics handling expense in INR |
| 16 | `payment_method` | Category | `UPI` | UPI, Debit Card, Credit Card, COD, Net Banking |
| 17 | `state` | Category | `Maharashtra` | Indian state of delivery (19 distinct states) |
| 18 | `city` | Category | `Mumbai` | Urban delivery destination |
| 19 | `order_status` | Category | `Delivered` | Delivered, Returned, Cancelled, Processing |
| 20 | `return_reason` | String | `Defective` | Reason code populated if status is Returned |

---

## 7. Data Preprocessing Methodology

The preprocessing subsystem (`src/preprocessing.py`) executes a sequential, reproducible transformation pipeline:

```
[Raw CSV: 15,015 Rows]
       │
       ▼
 1. Standardize Column Names (strip whitespace, lower, replace non-alphanumeric with '_')
       │
       ▼
 2. Drop Exact Duplicates (15 duplicate rows removed -> 15,000 Rows)
       │
       ▼
 3. Datetime Parsing & Outlier Range Validation (20 rows with years 1900/2099 removed -> 14,980 Rows)
       │
       ▼
 4. Numeric Type Coercion & Quality Validation (10 rows with negative quantity removed -> 14,970 Rows)
       │
       ▼
 5. Imputation & Missing Value Treatment (Impute missing discounts with 0.0; categoricals with 'Unknown')
       │
       ▼
 6. Mathematical Sales Recalculation (Enforce: sales_amount = qty * unit_price * (1 - disc/100))
       │
       ▼
 7. Temporal & Semantic Feature Engineering (Derive year, month, quarter, month_name, year_month, revenue)
       │
       ▼
[Cleaned CSV: 14,970 Rows × 26 Columns Saved]
```

### Cleaning Decisions Log
1. **Duplicate Row Elimination:** 15 exact duplicate records were excised. Records sharing `order_id` with distinct product lines were strictly preserved as multi-item cart purchases.
2. **Date Boundaries:** Valid date window established between `2020-01-01` and `2026-12-31`. 20 artificial records containing years 1900 or 2099 were eliminated.
3. **Negative Quantities vs. Negative Profit:** Rows exhibiting negative quantities (10 rows) were purged as data entry errors, since product returns are systematically tracked via `order_status == 'Returned'`. Conversely, negative profit rows (668 rows) were intentionally retained to accurately capture legitimate loss-making promotions.
4. **Missing Values Imputation:** 
   - `discount_percent`: 300 missing values filled with `0.0` (conservative business assumption of zero discount).
   - `payment_method`, `customer_name`, `city`: ~300 missing values filled with `'Unknown'` to retain revenue aggregation integrity.

---

## 8. Statistical Analysis and Mathematical Formulations

### Mathematical Metric Definitions

1. **Total Gross Revenue ($R$):**
   $$R = \sum_{i=1}^{N} \text{sales\_amount}_i = \sum_{i=1}^{N} \left[ q_i \times p_i \times \left(1 - \frac{d_i}{100}\right) \right]$$

2. **Distinct Orders ($O$):**
   $$O = |\{ \text{order\_id}_i : i \in \{1, \dots, N\} \}| = \text{count\_distinct}(\text{order\_id})$$

3. **Average Order Value ($\text{AOV}$):**
   $$\text{AOV} = \frac{R}{O}$$

4. **Profit Margin ($M_{\text{profit}}$):**
   $$M_{\text{profit}} = \left( \frac{\sum_{i=1}^{N} \text{profit}_i}{R} \right) \times 100$$

5. **Return Rate ($r_{\text{return}}$):**
   $$r_{\text{return}} = \left( \frac{|\{ \text{order\_id} : \text{status} = \text{'Returned'} \}|}{O} \right) \times 100$$

6. **Repeat Customer Rate ($r_{\text{repeat}}$):**
   $$r_{\text{repeat}} = \left( \frac{|\{ c \in \text{Customers} : \text{orders}(c) > 1 \}|}{|\text{Customers}|} \right) \times 100$$

---

## 9. Actual Calculated Results and Findings

Based on execution against the cleaned dataset of **14,970 verified records**, the empirical analytical findings are:

### Key Performance Summary

| Metric Indicator | Exact Calculated Value | Formatted Display |
| :--- | :--- | :--- |
| **Total Processed Transactions** | 14,970 records | 14,970 |
| **Total Gross Revenue** | ₹220,633,094.50 | **₹22.06 Cr** |
| **Total Distinct Orders** | 14,970 orders | 14,970 |
| **Total Units Sold** | 50,654 units | 50,654 |
| **Average Order Value (AOV)** | ₹14,738.35 | **₹14,738.35** |
| **Total Net Profit** | ₹27,138,823.10 | **₹2.71 Cr** |
| **Overall Profit Margin** | 12.30% | 12.30% |
| **Profitable Transactions** | 14,302 lines (95.54%) | 14,302 |
| **Loss-Making Transactions** | 668 lines (4.46%) | 668 |
| **Distinct Customers** | 2,975 customers | 2,975 |
| **Repeat Customer Rate** | 96.24% (2,863 customers) | 96.24% |
| **Return Rate** | 8.20% (1,227 orders) | 8.20% |
| **Cancellation Rate** | 4.94% (739 orders) | 4.94% |

### Category Performance Breakdown

| Category | Gross Revenue (₹) | Share (%) | Units Sold | Order Lines | Revenue per Unit (₹) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Electronics** | ₹16,52,03,683.50 | **74.88%** | 7,153 | 2,107 | ₹23,095.72 |
| **Sports** | ₹2,21,98,671.00 | **10.06%** | 7,740 | 2,171 | ₹2,868.05 |
| **Home & Kitchen** | ₹1,37,70,115.50 | **6.24%** | 7,229 | 2,094 | ₹1,904.84 |
| **Clothing** | ₹99,14,921.00 | **4.49%** | 7,155 | 2,193 | ₹1,385.73 |
| **Beauty & Health** | ₹48,77,865.50 | **2.21%** | 7,067 | 2,133 | ₹690.23 |
| **Books** | ₹25,39,820.00 | **1.15%** | 7,100 | 2,142 | ₹357.72 |
| **Food & Grocery** | ₹21,28,018.00 | **0.96%** | 7,210 | 2,130 | ₹295.15 |

### Geographic Performance (Top 5 States)

| State | Revenue (₹) | National Share (%) | Order Count | AOV (₹) |
| :--- | :--- | :--- | :--- | :--- |
| **Maharashtra** | ₹3,20,50,833.00 | **14.53%** | 2,033 | ₹15,765.29 |
| **Delhi** | ₹2,29,25,278.00 | **10.39%** | 1,483 | ₹15,458.72 |
| **Uttar Pradesh** | ₹1,96,69,671.00 | **8.92%** | 1,246 | ₹15,786.25 |
| **Karnataka** | ₹1,87,19,960.00 | **8.48%** | 1,351 | ₹13,856.37 |
| **Tamil Nadu** | ₹1,75,63,216.50 | **7.96%** | 1,382 | ₹12,708.55 |

### Payment Method Distribution

| Payment Method | Orders Count | Order Share (%) | Total Revenue (₹) | Mean AOV (₹) |
| :--- | :--- | :--- | :--- | :--- |
| **UPI** | 5,257 | **35.12%** | ₹7,33,46,316.00 | ₹13,952.12 |
| **Cash on Delivery (COD)**| 3,629 | **24.24%** | ₹5,22,10,661.00 | ₹14,387.07 |
| **Credit Card** | 2,190 | **14.63%** | ₹3,64,04,192.00 | ₹16,622.92 |
| **Debit Card** | 2,127 | **14.21%** | ₹3,00,06,408.50 | ₹14,107.39 |
| **Net Banking** | 1,468 | **9.81%** | ₹2,34,36,440.50 | ₹15,964.88 |
| **Unknown (Imputed)** | 299 | **2.00%** | ₹52,29,076.50 | ₹17,488.55 |

---

## 10. Dashboard Design and Visualizations

The interactive Streamlit application (`app.py`) features 5 modular views:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        INDIAN RETAIL ANALYTICS                         │
│  [ Executive Overview | Product | Regional | Customers | Data Quality ]│
├───────────────┬────────────────────────────────────────────────────────┤
│ SIDEBAR       │ MAIN CONTENT AREA                                      │
│ • Date Range  │ • KPI Summary Cards (Gradient Styling)                 │
│ • State       │ • Dynamic Plotly Line / Bar / Scatter Charts           │
│ • Category    │ • Automated Insight Callouts                           │
│ • Product     │ • Tabular Aggregations with INR Formatting             │
│ • Segment     │ • Direct Filtered CSV Export                           │
│ • Payment     │                                                        │
│ • Reset All   │                                                        │
└───────────────┴────────────────────────────────────────────────────────┘
```

### Visualizations Implemented

| # | Visualization Title | Analytical Question Addressed | Chart Mechanism |
|---|:---|:---|:---|
| 1 | **Monthly Revenue Trend** | How has gross turnover evolved across 2022–2024? | Time-series line chart with marker hovers |
| 2 | **Revenue by Category** | Which merchandise lines generate bulk revenue? | Ranked horizontal bar chart |
| 3 | **Top 10 Products by Revenue** | What specific SKUs dominate corporate receipts? | Sorted horizontal bar chart |
| 4 | **Top 10 Products by Quantity** | Which SKUs represent highest inventory turnover? | Sorted horizontal bar chart |
| 5 | **State-wise Revenue** | How does revenue distribute across Indian states? | 19-state ranked bar chart |
| 6 | **City-wise Revenue** | Which urban clusters contribute most to demand? | Top 15 cities comparative bar chart |
| 7 | **Quantity vs Revenue Scatter** | Are high-volume products also high-revenue? | Multi-category scatter plot |
| 8 | **Revenue vs Profit by Category**| Are revenue-dominant sectors equally profitable?| Paired dual bar chart |
| 9 | **Sales Amount Distribution** | What is the frequency distribution of basket sizes?| 50-bin histogram with density curve |
| 10| **Correlation Heatmap** | Which numeric transaction variables correlate? | Pearson correlation matrix heatmap |
| 11| **Payment Method Distribution** | What payment rails do consumers prefer? | Donut chart with order shares |
| 12| **Order Status Distribution** | What proportion of orders result in returns/cancels?| 4-segment fulfillment donut chart |
| 13| **Discount Impact Analysis** | How do steep markdowns affect gross turnover? | Discount bracket bar chart |
| 14| **Customer Segment Revenue** | How do Consumers vs Corporate accounts compare?| Horizontal contribution bar chart |

*All 11 static publication-quality chart renders are preserved in `outputs/charts/`.*

---

## 11. Testing and Verification Strategy

Quality assurance is verified via a 60-test automated suite executed through Pytest:

```
============================= test session starts =============================
platform win32 -- Python 3.13.11, pytest-9.1.1, pluggy-1.7.0
rootdir: C:\Users\shiva\Downloads\DAV AAT
collected 60 items

tests/test_metrics.py ......................................             [ 63%]
tests/test_preprocessing.py ..........................                   [100%]

============================= 60 passed in 5.62s ==============================
```

### Test Coverage Highlights
- **Column Normalization:** Ensures non-alphanumeric characters and awkward spacing are cleanly converted to snake_case.
- **Date Boundary Enforcement:** Verifies dates outside 2020–2026 are excised and invalid strings become `NaT`.
- **Negative Value Isolation:** Confirms negative quantities are discarded while legitimate negative profits are preserved.
- **Safe Math & Zero Denominators:** Asserts that `safe_divide()`, `average_order_value()`, and `repeat_customer_rate()` return clean defaults when encountering empty DataFrames or zero denominator orders.
- **Distinct Order Aggregation:** Verifies that multi-item order lines sharing the same `order_id` do not artificially inflate distinct order tallies.

---

## 12. Limitations

1. **Synthetic Nature of Data:** The transaction history was algorithmically generated. Observed seasonalities (e.g., Q4 Diwali sales surge) and UPI payment adoption rates reflect injected parameters rather than actual commercial audit data.
2. **Absence of Geographic Coordinate Polygons:** The dataset includes state and city names, but lacks latitude/longitude coordinates or GeoJSON shapefiles, precluding interactive choropleth map plotting.
3. **Absence of Promotional Spend & Ad Attribution:** While discounts and net profits are tracked, customer acquisition costs (CAC) and marketing campaign spends are not present, preventing Return on Ad Spend (ROAS) analysis.
4. **Desktop Memory Architecture:** The pipeline utilizes in-memory Pandas DataFrames, optimized for moderate datasets (~100k rows) on standard PCs, rather than distributed Spark clusters.

---

## 13. Conclusion and Future Work

This DAV Lab AAT project demonstrates a complete, disciplined data analytics and visualization lifecycle. By transforming 15,015 raw records into a validated 14,970-record analytics repository and coupling it with an interactive 5-page Streamlit dashboard, we have created an academic tool that demonstrates:
- Defensive data wrangling and quality reporting.
- Mathematical rigor in retail metric aggregation.
- Responsive, interactive visual UX with Plotly.
- Automated test verification with 100% test passage.

### Proposed Future Enhancements
1. **Real-world Kaggle Integration:** Connect the loader module to public e-commerce datasets (e.g., Indian E-Commerce or Olist-equivalent platforms).
2. **Geospatial Mapping:** Integrate Indian state GeoJSON shapefiles via `plotly.express.choropleth` for choropleth mapping.
3. **Time-Series Forecasting:** Implement an ARIMA or Holt-Winters forecasting module for 30-day inventory demand predictions.
4. **PDF Automated Reporting:** Add a server-side report generator that compiles current filtered KPI states into downloadable PDF executive summaries.

---

## 14. References and Tool Acknowledgements

1. **Python Software Foundation:** Python 3.13 Language Reference (PSF License).
2. **Wes McKinney & Pandas Development Team:** *Data Structures for Statistical Computing in Python*, Proceedings of the 9th Python in Science Conference, 2010.
3. **Plotly Technologies Inc.:** *Collaborative Data Science with Plotly and Dash*, Montreal, QC, 2024.
4. **Streamlit Inc.:** *Streamlit Open-Source Framework Documentation*, 2024.
5. **Hunter, J. D.:** *Matplotlib: A 2D Graphics Environment*, Computing in Science & Engineering, 2007.
6. **Waskom, M. L.:** *Seaborn: Statistical Data Visualization*, Journal of Open Source Software, 2021.
7. **Pytest Development Community:** *pytest: simple powerful testing with Python*, 2024.
