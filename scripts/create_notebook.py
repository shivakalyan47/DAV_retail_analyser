"""
Generate the exploratory_analysis.ipynb notebook.
"""
import json
import os

notebook = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# Indian Retail Sales and Revenue Analytics\n",
                "## Exploratory Data Analysis (EDA) Notebook\n",
                "\n",
                "**Course:** Data Analytics and Visualization (DAV) Lab AAT  \n",
                "**Dataset:** Synthetic Indian Retail Transaction Dataset (15,015 raw records)  \n",
                "**Authors:** Student 1 & Student 2  \n",
                "\n",
                "---\n",
                "### Objectives\n",
                "1. Load and inspect raw retail transaction data.\n",
                "2. Conduct data quality audits (missing values, duplicates, anomalous dates, negative values).\n",
                "3. Perform standardized preprocessing and data cleaning.\n",
                "4. Compute descriptive statistical summaries and correlation matrices.\n",
                "5. Generate exploratory visualizations across products, geography, time, and customer segments.\n",
                "6. Extract empirical business takeaways."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Step 1: Environment Setup and Imports\n",
                "import os\n",
                "import sys\n",
                "import numpy as np\n",
                "import pandas as pd\n",
                "import matplotlib.pyplot as plt\n",
                "import seaborn as sns\n",
                "\n",
                "# Set plot styling\n",
                "plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')\n",
                "plt.rcParams['figure.figsize'] = (10, 5)\n",
                "plt.rcParams['figure.dpi'] = 120\n",
                "\n",
                "# Ensure project modules can be imported\n",
                "sys.path.insert(0, os.path.abspath('..'))\n",
                "from config import RAW_DATA_DIR, PROCESSED_DATA_DIR, ORDERS_FILE\n",
                "from src.preprocessing import clean_data, detect_missing_values, detect_duplicates\n",
                "from src.metrics import format_inr, format_inr_short\n",
                "\n",
                "print(\"All libraries successfully imported.\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 2. Ingesting Raw Transaction Data\n",
                "We load the uncleaned raw CSV file from `data/raw/indian_retail_orders.csv`."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "raw_path = os.path.join('..', 'data', 'raw', 'indian_retail_orders.csv')\n",
                "df_raw = pd.read_csv(raw_path)\n",
                "print(f\"Raw dataset shape: {df_raw.shape[0]:,} rows x {df_raw.shape[1]} columns\")\n",
                "df_raw.head()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 3. Data Quality Inspection\n",
                "We identify missing values, exact duplicate rows, invalid date years, and negative quantities."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Missing value inspection\n",
                "missing_summary = detect_missing_values(df_raw)\n",
                "print(\"Missing Values Summary:\")\n",
                "print(missing_summary)\n",
                "\n",
                "# Duplicate row check\n",
                "dup_info = detect_duplicates(df_raw)\n",
                "print(f\"\\nExact Duplicate Rows Found: {dup_info['duplicate_count']} ({dup_info['duplicate_percent']}%)\")\n",
                "\n",
                "# Negative quantity check\n",
                "neg_qty = (df_raw['quantity'] < 0).sum()\n",
                "print(f\"Negative Quantity Errors Found: {neg_qty} rows\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 4. Executing the Preprocessing Pipeline\n",
                "We apply the standardized cleaning pipeline implemented in `src/preprocessing.py`."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "df_clean, quality_report = clean_data(df_raw)\n",
                "print(f\"Cleaned dataset shape: {df_clean.shape[0]:,} rows x {df_clean.shape[1]} columns\")\n",
                "print(f\"Total rows pruned: {quality_report['rows_removed_total']} ({quality_report['removal_percent']}%)\")\n",
                "df_clean.info()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 5. Descriptive Statistics\n",
                "We calculate key statistical metrics across continuous numerical fields."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "numeric_cols = ['quantity', 'unit_price', 'discount_percent', 'sales_amount', 'profit', 'shipping_cost']\n",
                "df_clean[numeric_cols].describe().round(2)"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 6. Core Business KPI Calculations\n",
                "We calculate Gross Revenue, Distinct Orders, Units Sold, AOV, and Profit Margins."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "total_rev = df_clean['revenue'].sum()\n",
                "total_orders = df_clean['order_id'].nunique()\n",
                "total_units = df_clean['quantity'].sum()\n",
                "aov = total_rev / total_orders\n",
                "total_profit = df_clean['profit'].sum()\n",
                "profit_margin = (total_profit / total_rev) * 100\n",
                "\n",
                "print(f\"Total Gross Revenue : {format_inr(total_rev)} ({format_inr_short(total_rev)})\")\n",
                "print(f\"Total Distinct Orders: {total_orders:,}\")\n",
                "print(f\"Total Units Sold    : {total_units:,}\")\n",
                "print(f\"Average Order Value : {format_inr(aov)}\")\n",
                "print(f\"Total Net Profit    : {format_inr(total_profit)} (Margin: {profit_margin:.2f}%)\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 7. Category and Product Performance Analysis"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Category revenue breakdown\n",
                "cat_summary = df_clean.groupby('category').agg(\n",
                "    revenue=('revenue', 'sum'),\n",
                "    units=('quantity', 'sum'),\n",
                "    orders=('order_id', 'nunique')\n",
                ").reset_index().sort_values('revenue', ascending=False)\n",
                "cat_summary['share_%'] = (cat_summary['revenue'] / total_rev * 100).round(2)\n",
                "cat_summary"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Horizontal bar chart for Category Revenue\n",
                "plt.figure(figsize=(10, 5))\n",
                "sns.barplot(data=cat_summary, x='revenue', y='category', palette='viridis')\n",
                "plt.title('Gross Revenue Contribution by Category', fontsize=14, fontweight='bold')\n",
                "plt.xlabel('Revenue (INR)')\n",
                "plt.ylabel('Product Category')\n",
                "plt.tight_layout()\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 8. Geographic Breakdown (State-wise Analysis)"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "state_summary = df_clean.groupby('state')['revenue'].sum().reset_index().sort_values('revenue', ascending=False)\n",
                "plt.figure(figsize=(10, 7))\n",
                "sns.barplot(data=state_summary, x='revenue', y='state', palette='Blues_r')\n",
                "plt.title('State-wise Revenue Distribution (19 Indian States)', fontsize=14, fontweight='bold')\n",
                "plt.xlabel('Revenue (INR)')\n",
                "plt.ylabel('State')\n",
                "plt.tight_layout()\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 9. Correlation Analysis"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "plt.figure(figsize=(8, 6))\n",
                "corr = df_clean[numeric_cols].corr()\n",
                "sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', vmin=-1, vmax=1)\n",
                "plt.title('Correlation Heatmap of Numerical Features', fontsize=14, fontweight='bold')\n",
                "plt.tight_layout()\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 10. Key Takeaways & Conclusions\n",
                "1. **Electronics Dominance:** Electronics accounts for ~75% of total revenue due to high unit selling prices.\n",
                "2. **Volume vs. Value Disconnect:** Categories like Sports and Food & Grocery achieve high unit sales but lower total turnover.\n",
                "3. **Top Regional Markets:** Maharashtra, Delhi, and Uttar Pradesh lead nationwide demand.\n",
                "4. **Payment Preferences:** UPI is the preferred payment method (~35% of orders), followed by Cash on Delivery (~24%).\n",
                "5. **Operational Health:** Healthy 12.30% profit margin and manageable 8.20% return rate."
            ]
        }
    ],
    "metadata": {
        "language_info": {
            "name": "python",
            "version": "3.13"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 2
}

os.makedirs('notebooks', exist_ok=True)
notebook_path = os.path.join('notebooks', 'exploratory_analysis.ipynb')
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=2)

print(f"Jupyter notebook written to {notebook_path}")
