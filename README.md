# Indian Retail Sales and Revenue Analytics: An Interactive Python Dashboard

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Streamlit-1.28%2B-red.svg)](https://streamlit.io/)
[![Visualization](https://img.shields.io/badge/Plotly-5.15%2B-orange.svg)](https://plotly.com/)
[![Tests](https://img.shields.io/badge/Pytest-60%20Passed-brightgreen.svg)](https://pytest.org/)
[![License](https://img.shields.io/badge/License-CC0--1.0-lightgrey.svg)](LICENSE)

An interactive, college-level Data Analytics and Visualization (DAV) Lab Alternative Assessment Task (AAT) project. This repository delivers an end-to-end analytics pipeline and an interactive web dashboard for analyzing Indian retail transaction records, product performance, geographic distribution, and customer purchasing patterns.

---

## 📋 Table of Contents
- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [Dataset Architecture & Provenance](#dataset-architecture--provenance)
- [Project Directory Structure](#project-directory-structure)
- [Installation & Virtual Environment Setup (Windows)](#installation--virtual-environment-setup-windows)
- [How to Run Data Preprocessing](#how-to-run-data-preprocessing)
- [How to Execute the Automated Test Suite](#how-to-execute-the-automated-test-suite)
- [How to Launch the Interactive Dashboard](#how-to-launch-the-interactive-dashboard)
- [Dashboard Navigation & User Guide](#dashboard-navigation--user-guide)
- [Key Empirical Findings & Business Metrics](#key-empirical-findings--business-metrics)
- [How to Integrate a New or Custom Dataset](#how-to-integrate-a-new-or-custom-dataset)
- [Limitations & Disclaimers](#limitations--disclaimers)
- [Academic Information & Team](#academic-information--team)

---

## 🛒 Project Overview

The Indian retail market is characterized by rapid digital payment adoption (UPI), complex product catalogs, and diverse regional consumption patterns. This project addresses the challenge of transforming raw, messy transaction records into actionable visual intelligence without relying on opaque machine learning black-boxes.

The software performs:
1. **Automated Cleaning:** Pruning duplicate rows, invalid date years, negative unit errors, and standardizing schemas.
2. **Mathematical Aggregation:** Calculating exact retail KPIs (Total Gross Revenue, Order Frequencies, Units Sold, Average Order Value, Profit Margins, Return Rates) while strictly preventing double-counting between order-line items and distinct orders.
3. **Interactive Visualization:** Rendering dynamic Plotly charts across 5 dedicated web pages in a responsive Streamlit dashboard.
4. **Reproducible Quality Assurance:** Ensuring 100% test coverage through 60 automated Pytest unit tests.

---

## ✨ Key Features

- **5 Dedicated Interactive Dashboard Views:**
  - 📊 **Executive Overview:** High-level KPI cards, monthly revenue trend lines, category turnover, top products, and data-derived insights.
  - 🏷️ **Product Analytics:** Interactive Top $N$ sliders, volume-versus-revenue scatter plots, category summary tables, and discount bracket analyses.
  - 🗺️ **Regional Analytics:** 19-state ranked performance bars, city-level comparisons, and regional revenue share percentages.
  - 👥 **Customer & Returns:** Unique customer loyalty metrics (repeat rate), order fulfillment donut charts (returns vs. cancellations), payment rail distributions, and net profit analyses.
  - 🔍 **Data Quality & Methodology:** Real-time data profiling, schema validation, missing value summaries, correlation heatmaps, and dataset provenance.
- **Dynamic Cross-Filtering:** Filter simultaneously by Date Range, State, Category, Product SKU, Customer Segment, Payment Method, and Order Status.
- **Indian Number System Formatting:** Custom formatting for Indian Rupees (`₹`), Lakhs (`L`), and Crores (`Cr`).
- **Data Export:** Filter records dynamically and download the scoped dataset as a CSV file with a single click.
- **Defensive Engineering:** Graceful fallbacks for missing columns or zero-denominator divisions (`safe_divide()`).

---

## 📊 Dataset Architecture & Provenance

### Dataset Overview
| Property | Specification |
| :--- | :--- |
| **Dataset Title** | Indian Retail Sales and Revenue Dataset |
| **Data Nature** | **Synthetic / Academic Simulation** (Generated via NumPy & Pandas) |
| **Random Seed** | Fixed Seed: `42` for 100% deterministic reproducibility |
| **File Location** | `data/raw/indian_retail_orders.csv` |
| **Raw Dimension** | 15,015 rows × 20 columns (2.53 MB) |
| **Cleaned Dimension**| 14,970 rows × 26 columns (2.61 MB) |
| **Time Horizon** | January 1, 2022 to December 31, 2024 |
| **Geography** | 19 Indian States & Major Urban Centers |
| **Licensing** | CC0: Public Domain |

### Injected Data Quality Challenges (For Academic Preprocessing)
- ~300 missing values (~2%) across `customer_name`, `city`, `discount_percent`, and `payment_method`.
- 15 exact duplicate transaction rows.
- 20 rows with out-of-bounds date years (`1900` and `2099`).
- 10 rows with negative quantities (simulating human entry errors).

> ⚠️ **Academic Disclosure:** This dataset is entirely synthetic. Findings demonstrate data analytics and visualization methodologies and should not be cited as real-world market statistics.

---

## 📁 Project Directory Structure

```
DAV AAT/
├── app.py                      # Main Streamlit interactive web application
├── config.py                   # Centralized configuration, paths, and constants
├── requirements.txt            # Locked project dependencies
├── README.md                   # Comprehensive documentation and setup instructions
├── .gitignore                  # Git version control exclusions
│
├── data/
│   ├── raw/
│   │   └── indian_retail_orders.csv     # Raw ingested transactional dataset
│   ├── processed/
│   │   ├── cleaned_retail_data.csv      # Cleaned and feature-engineered dataset
│   │   └── data_quality_report.txt      # Text-based data quality audit log
│   └── generate_synthetic_data.py       # Script used to generate synthetic dataset
│
├── src/
│   ├── __init__.py             # Python package identifier
│   ├── data_loader.py          # Cached data loading and schema validation
│   ├── preprocessing.py        # Automated cleaning and transformation pipeline
│   ├── metrics.py              # Retail KPI calculation formulas and insights
│   └── visualizations.py       # Reusable Plotly chart rendering functions
│
├── tests/
│   ├── test_preprocessing.py   # 22 automated tests for data cleaning & validation
│   └── test_metrics.py         # 38 automated tests for mathematical KPI logic
│
├── notebooks/
│   └── exploratory_analysis.ipynb # Jupyter notebook for step-by-step EDA
│
├── outputs/
│   ├── charts/                 # 11 publication-quality static chart renders (PNG)
│   └── reports/                # Output analysis artifacts
│
├── report/
│   ├── mini_project_report.md  # Complete academic mini-project report
│   ├── viva_questions.md       # 35 comprehensive viva questions and answers
│   └── presentation_outline.md # 10-slide deck plan and demonstration script
│
└── scripts/
    ├── calculate_metrics.py    # CLI script to print exact verified dataset KPIs
    ├── generate_charts.py      # Script to render static charts into outputs/charts/
    └── create_notebook.py      # Generator script for exploratory_analysis.ipynb
```

---

## 💻 Installation & Virtual Environment Setup (Windows)

Follow these exact commands in Windows PowerShell:

### Step 1: Open Terminal in Project Directory
```powershell
cd "c:\Users\shiva\Downloads\DAV AAT"
```

### Step 2: Create a Python Virtual Environment
```powershell
python -m venv venv
```

### Step 3: Activate the Virtual Environment
```powershell
.\venv\Scripts\Activate.ps1
```
*(If PowerShell displays an Execution Policy restriction, run: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` then activate again).*

### Step 4: Upgrade Pip & Install Dependencies
```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

---

## 🔄 How to Run Data Preprocessing

The preprocessing module cleans raw data, drops duplicates and outliers, imputes missing values, recalculates sales amounts, and exports the cleaned dataset:

```powershell
python -m src.preprocessing
```

**Expected Console Output:**
```
============================================================
DATA QUALITY REPORT
============================================================
Original rows: 15,015
Original columns: 20
Final rows: 14,970
Final columns: 26
Total rows removed: 45 (0.3%)
...
Cleaned data saved to: data/processed/cleaned_retail_data.csv
```

---

## 🧪 How to Execute the Automated Test Suite

Verify calculation accuracy and edge-case handling using Pytest:

```powershell
python -m pytest tests/ -v
```

**Expected Result:**
```
============================= 60 passed in 5.62s ==============================
```

All 60 tests cover:
- Column standardization and special character sanitization
- Missing value detection and duplicate elimination
- Date boundary filtering and negative quantity removal
- Non-negative profit preservation
- Division-by-zero safeguards (`safe_divide`)
- Distinct order vs. order-line item counting accuracy
- Indian currency formatting (`₹`, Lakhs, Crores)

---

## 🚀 How to Launch the Interactive Dashboard

Launch the Streamlit web application locally:

```powershell
streamlit run app.py
```

The application will start and open automatically in your browser at:
`http://localhost:8501`

---

## 🧭 Dashboard Navigation & User Guide

1. **Sidebar Navigation:** Use the radio buttons in the left sidebar to switch between the 5 dashboard pages.
2. **Sidebar Filters:**
   - **Date Range:** Adjust start and end dates to focus on specific quarters or festive periods.
   - **State / City:** Select one or multiple Indian states/cities.
   - **Category / Product:** Drill down into specific merchandise lines.
   - **Customer Segment & Payment Method:** Filter by Consumer, Corporate, UPI, COD, etc.
   - **🔄 Reset All Filters:** Click to restore the full dataset view.
3. **Interactive Charts:**
   - **Hover:** Move your mouse over any bar or line point to inspect exact values in ₹.
   - **Zoom & Pan:** Click and drag on any chart to zoom into specific regions; double-click to reset.
   - **Legend Toggle:** Click category names in the chart legend to show/hide specific lines.
4. **Export Filtered Data:** At the bottom of any page, click **📥 Download Filtered Data (CSV)** to download the currently filtered dataset.

---

## 📈 Key Empirical Findings & Business Metrics

*Calculated from the verified cleaned dataset of 14,970 transactions:*

- **Total Turnover:** **₹22.06 Crore** (`₹22,06,33,094.50`) across **14,970 distinct orders** and **50,654 units**.
- **Average Order Value (AOV):** **₹14,738.35**.
- **Operational Profit:** **₹2.71 Crore** (`₹2,71,38,823.10`) with an overall **12.30% profit margin**.
- **Top Product Category:** **Electronics** accounts for **74.88%** (₹16.52 Cr) of total revenue, led by Laptops (₹5.51 Cr) and Cameras (₹3.80 Cr).
- **Top Volume Category:** **Sports** accounts for highest physical inventory turnover with **7,740 units sold** (led by Sports Shoes and Fitness Equipment).
- **Leading State:** **Maharashtra** ranks #1, generating **₹3.21 Cr** (14.53% of national revenue) across 2,033 orders, followed by Delhi (₹2.29 Cr) and Uttar Pradesh (₹1.97 Cr).
- **Payment Method Preference:** **UPI** is the dominant payment rail, used in **35.12%** of orders (5,257 orders, ₹7.33 Cr), followed by Cash on Delivery (**24.24%**).
- **Order Fulfillment Quality:** **8.20% return rate** (1,227 orders) and **4.94% cancellation rate** (739 orders).
- **Customer Loyalty:** **96.24% repeat customer rate** (2,863 of 2,975 unique customers placed $>1$ order).

---

## 🔌 Uploading & Analyzing a Custom CSV Dataset

You can upload and analyze your own custom CSV dataset directly in the application or place it in the data folder:

### Method 1: Instant In-App Upload (Recommended)
1. Launch the dashboard: `streamlit run app.py`
2. In the left sidebar under **📁 Data Source**, select **Upload Custom CSV**.
3. Drag & drop or browse your CSV file.
4. The system automatically:
   - Maps column name variations (`sales` / `amount` → `sales_amount`, `date` → `order_date`, etc.)
   - Validates and standardizes data types
   - Generates derived temporal fields (`year`, `month`, `quarter`)
   - Recalculates all KPIs, charts, and tables instantly across all 5 pages!
5. To switch back at any time, click **↩️ Switch to Built-in Data**.

### Method 2: Offline Configuration
1. Place your CSV file in `data/raw/` (e.g., `data/raw/my_retail_data.csv`).
2. Update `config.py`:
   ```python
   ORDERS_FILE = "my_retail_data.csv"
   ```
3. Run the preprocessing pipeline:
   ```powershell
   python -m src.preprocessing
   ```
4. Run `streamlit run app.py`.

---

## ⚠️ Limitations & Disclaimers

1. **Synthetic Data Disclosure:** All transactions were synthetically generated for academic demonstration. Patterns reflect injected statistical distributions rather than actual commercial audit data.
2. **Geographic Coordinates:** The dataset contains state and city names, but lacks latitude/longitude coordinates; choropleth mapping is therefore omitted to avoid fabricating geographic coordinates.
3. **In-Memory Architecture:** Designed for single-machine local execution using Pandas DataFrames (ideal for datasets up to ~1 million rows).
4. **Descriptive Scope:** The project focuses on descriptive and diagnostic analytics. It does not perform black-box predictive modeling.

---

## 👥 Academic Information & Team

- **Course:** Data Analytics and Visualization (DAV) Lab AAT
- **Course Code:** 21CS54 / DAV Lab
- **Semester:** V / VI
- **Academic Year:** 2026-27
- **Team Size:** 2 Students

| Role | Student Name | USN | Section |
| :--- | :--- | :--- | :--- |
| **Student 1** | _[Student 1 Name]_ | _[USN 1]_ | _[Sec]_ |
| **Student 2** | _[Student 2 Name]_ | _[USN 2]_ | _[Sec]_ |

**Faculty Guide:** _[Prof. Faculty Name]_, Department of Computer Science & Engineering.
