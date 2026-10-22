"""
Configuration module for Indian Retail Analytics Dashboard.
All project-wide settings and paths are defined here.
"""
import os

# Project root directory
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Data directories
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")

# Output directories
OUTPUTS_DIR = os.path.join(PROJECT_ROOT, "outputs")
CHARTS_DIR = os.path.join(OUTPUTS_DIR, "charts")
REPORTS_DIR = os.path.join(OUTPUTS_DIR, "reports")

# Dataset file configuration
# Place your CSV file(s) in data/raw/ and update these names if different
ORDERS_FILE = "indian_retail_orders.csv"
CLEANED_FILE = "cleaned_retail_data.csv"
DATA_QUALITY_FILE = "data_quality_report.csv"

# Dashboard settings
APP_TITLE = "Indian Retail Analytics"
APP_ICON = "🛒"
DEFAULT_TOP_N = 10
CURRENCY_SYMBOL = "₹"
CURRENCY_CODE = "INR"

# Date format expected in dataset
DATE_FORMAT = "%Y-%m-%d"

# Dataset metadata
DATASET_INFO = {
    "name": "Indian Retail Sales and Revenue Dataset",
    "type": "Retail Analytics Dataset",
    "description": (
        "Comprehensive retail dataset simulating Indian e-commerce transactions across "
        "multiple product categories, payment channels, geographic regions, and customer segments."
    ),
    "source": "DAV Retail Analytics Repository",
    "licence": "Educational / Open Access",
    "access_date": "2026-10-22",
    "limitations": [
        "Product catalog and pricing reflect standard Indian retail e-commerce categories.",
        "Geographic representations cover major Indian state and city retail hubs.",
        "Transactions record online and digital payment orders.",
    ],
}

# Ensure directories exist
for d in [RAW_DATA_DIR, PROCESSED_DATA_DIR, CHARTS_DIR, REPORTS_DIR]:
    os.makedirs(d, exist_ok=True)
