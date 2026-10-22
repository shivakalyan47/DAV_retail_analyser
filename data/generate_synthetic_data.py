"""
Synthetic Indian Retail Dataset Generator
==========================================
One-time script to generate a realistic synthetic Indian retail e-commerce
dataset for academic purposes (DAV Lab AAT project).

The generated CSV simulates ~15,000 retail orders placed between 2022-01-01
and 2024-12-31 across Indian states, with intentional data-quality issues
(missing values, duplicates, wrong dates, negative quantities) so that
downstream cleaning and EDA steps have realistic problems to handle.

Usage:
    python data/generate_synthetic_data.py

Output:
    data/raw/indian_retail_orders.csv
"""

import os
import sys

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Reproducibility
# ---------------------------------------------------------------------------
SEED = 42
np.random.seed(SEED)

# ---------------------------------------------------------------------------
# Output path  (works whether script is run from project root or data/)
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
RAW_DIR = os.path.join(SCRIPT_DIR, "raw")
os.makedirs(RAW_DIR, exist_ok=True)
OUTPUT_PATH = os.path.join(RAW_DIR, "indian_retail_orders.csv")

# ---------------------------------------------------------------------------
# Constants & lookup tables
# ---------------------------------------------------------------------------
NUM_ORDERS = 15_000
DATE_START = "2022-01-01"
DATE_END = "2024-12-31"

# Indian names ---------------------------------------------------------------
FIRST_NAMES = [
    "Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Reyansh",
    "Ayaan", "Krishna", "Ishaan", "Ananya", "Diya", "Saanvi", "Aanya",
    "Aadhya", "Isha", "Pari", "Nisha", "Kavya", "Riya", "Priya", "Rahul",
    "Amit", "Raj", "Neha", "Pooja", "Vikram", "Suresh", "Deepa", "Meera",
    "Rohan", "Kiran", "Sanjay", "Preeti", "Anjali", "Manish", "Gaurav",
    "Sunita", "Rekha", "Mohan",
]

LAST_NAMES = [
    "Sharma", "Patel", "Singh", "Kumar", "Gupta", "Verma", "Joshi",
    "Reddy", "Nair", "Pillai", "Iyer", "Mehta", "Shah", "Das", "Bose",
    "Rao", "Menon", "Kulkarni", "Deshmukh", "Patil", "Chauhan", "Yadav",
    "Mishra", "Pandey", "Tiwari", "Agarwal", "Banerjee", "Mukherjee",
    "Chatterjee", "Sen",
]

# State -> cities mapping with population-weighted probabilities -------------
STATE_CITIES = {
    "Maharashtra":      ["Mumbai", "Pune", "Nagpur", "Thane", "Nashik"],
    "Delhi":            ["New Delhi", "Dwarka", "Rohini"],
    "Karnataka":        ["Bengaluru", "Mysuru", "Hubli"],
    "Tamil Nadu":       ["Chennai", "Coimbatore", "Madurai"],
    "Telangana":        ["Hyderabad", "Warangal"],
    "Gujarat":          ["Ahmedabad", "Surat", "Vadodara", "Rajkot"],
    "Uttar Pradesh":    ["Lucknow", "Noida", "Kanpur", "Varanasi", "Agra"],
    "West Bengal":      ["Kolkata", "Howrah", "Durgapur"],
    "Rajasthan":        ["Jaipur", "Jodhpur", "Udaipur"],
    "Kerala":           ["Kochi", "Thiruvananthapuram", "Kozhikode"],
    "Madhya Pradesh":   ["Bhopal", "Indore", "Gwalior"],
    "Punjab":           ["Ludhiana", "Amritsar", "Chandigarh"],
    "Haryana":          ["Gurugram", "Faridabad"],
    "Bihar":            ["Patna", "Gaya"],
    "Odisha":           ["Bhubaneswar", "Cuttack"],
    "Assam":            ["Guwahati"],
    "Jharkhand":        ["Ranchi", "Jamshedpur"],
    "Chhattisgarh":     ["Raipur"],
    "Andhra Pradesh":   ["Visakhapatnam", "Vijayawada", "Tirupati"],
}

# Higher weights for economically dominant states
STATE_WEIGHTS = {
    "Maharashtra": 0.14,
    "Delhi": 0.10,
    "Karnataka": 0.09,
    "Tamil Nadu": 0.09,
    "Telangana": 0.07,
    "Gujarat": 0.07,
    "Uttar Pradesh": 0.08,
    "West Bengal": 0.06,
    "Rajasthan": 0.05,
    "Kerala": 0.05,
    "Madhya Pradesh": 0.04,
    "Punjab": 0.03,
    "Haryana": 0.03,
    "Bihar": 0.03,
    "Odisha": 0.02,
    "Assam": 0.01,
    "Jharkhand": 0.01,
    "Chhattisgarh": 0.01,
    "Andhra Pradesh": 0.02,
}

STATES = list(STATE_WEIGHTS.keys())
STATE_PROBS = np.array(list(STATE_WEIGHTS.values()))
STATE_PROBS = STATE_PROBS / STATE_PROBS.sum()  # normalise

# Categories, sub-categories and price ranges (min, max) in INR -------------
CATEGORY_CONFIG = {
    "Electronics": {
        "sub_categories": {
            "Mobile Phones":  (8000, 80000),
            "Laptops":        (25000, 90000),
            "Headphones":     (500, 8000),
            "Tablets":        (10000, 50000),
            "Cameras":        (15000, 70000),
            "Smartwatches":   (2000, 25000),
        },
        "profit_margin": (0.08, 0.18),
    },
    "Clothing": {
        "sub_categories": {
            "Men's Shirts":   (500, 3000),
            "Women's Kurta":  (400, 2500),
            "Jeans":          (800, 3500),
            "Sarees":         (500, 5000),
            "T-Shirts":       (300, 1500),
            "Jackets":        (1000, 4000),
        },
        "profit_margin": (0.15, 0.25),
    },
    "Home & Kitchen": {
        "sub_categories": {
            "Cookware":       (300, 5000),
            "Appliances":     (1000, 15000),
            "Bedding":        (500, 4000),
            "Storage":        (200, 2000),
            "Decor":          (300, 3000),
        },
        "profit_margin": (0.10, 0.22),
    },
    "Books": {
        "sub_categories": {
            "Fiction":        (150, 600),
            "Non-Fiction":    (200, 800),
            "Academic":       (300, 1500),
            "Children's":     (100, 500),
            "Comics":         (100, 400),
        },
        "profit_margin": (0.12, 0.25),
    },
    "Beauty & Health": {
        "sub_categories": {
            "Skincare":       (200, 3000),
            "Haircare":       (150, 1500),
            "Makeup":         (200, 2500),
            "Supplements":    (300, 2000),
            "Personal Care":  (100, 800),
        },
        "profit_margin": (0.15, 0.25),
    },
    "Sports": {
        "sub_categories": {
            "Fitness Equipment": (500, 15000),
            "Cricket Gear":      (300, 8000),
            "Yoga Accessories":  (200, 2000),
            "Sports Shoes":      (800, 5000),
            "Cycling":           (1000, 20000),
        },
        "profit_margin": (0.10, 0.20),
    },
    "Food & Grocery": {
        "sub_categories": {
            "Snacks":         (50, 500),
            "Beverages":      (50, 400),
            "Spices":         (50, 300),
            "Dry Fruits":     (200, 2000),
            "Organic Food":   (100, 1000),
        },
        "profit_margin": (0.05, 0.15),
    },
}

CATEGORIES = list(CATEGORY_CONFIG.keys())

# Customer segments ----------------------------------------------------------
SEGMENTS = ["Consumer", "Corporate", "Home Office"]
SEGMENT_WEIGHTS = [0.52, 0.30, 0.18]

# Payment methods (UPI most common in India) ---------------------------------
PAYMENT_METHODS = ["Credit Card", "Debit Card", "UPI", "Cash on Delivery", "Net Banking"]
PAYMENT_WEIGHTS = [0.15, 0.15, 0.35, 0.25, 0.10]

# Discount percentages -------------------------------------------------------
DISCOUNTS = [0, 5, 10, 15, 20, 25, 30]
DISCOUNT_WEIGHTS = [0.30, 0.20, 0.18, 0.12, 0.10, 0.06, 0.04]

# Order statuses -------------------------------------------------------------
ORDER_STATUSES = ["Delivered", "Returned", "Cancelled", "Processing"]
STATUS_WEIGHTS = [0.85, 0.08, 0.05, 0.02]

# Return reasons (only for Returned orders) ----------------------------------
RETURN_REASONS = ["Defective", "Wrong Item", "Not as Described", "Changed Mind"]


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _generate_dates(n: int) -> np.ndarray:
    """
    Generate *n* order dates between DATE_START and DATE_END with a
    seasonal boost during Oct-Dec (Diwali / festive season) and January
    (New Year sales).
    """
    all_dates = pd.date_range(DATE_START, DATE_END, freq="D")
    # Build per-day weight: boost months 1, 10, 11, 12
    weights = np.ones(len(all_dates), dtype=float)
    months = all_dates.month
    weights[np.isin(months, [10, 11, 12])] = 1.5   # festive season
    weights[months == 1] = 1.25                      # New Year sales
    weights /= weights.sum()
    chosen_indices = np.random.choice(len(all_dates), size=n, p=weights)
    return all_dates[chosen_indices]


def _generate_product_details(n: int):
    """
    Return arrays: category, sub_category, unit_price, profit_margin_range
    for *n* products.
    """
    cats = np.random.choice(CATEGORIES, size=n)
    sub_cats = np.empty(n, dtype=object)
    prices = np.empty(n, dtype=float)
    margin_low = np.empty(n, dtype=float)
    margin_high = np.empty(n, dtype=float)

    for i, cat in enumerate(cats):
        cfg = CATEGORY_CONFIG[cat]
        sc_names = list(cfg["sub_categories"].keys())
        sc = np.random.choice(sc_names)
        lo, hi = cfg["sub_categories"][sc]
        sub_cats[i] = sc
        # Log-uniform gives a more realistic price spread
        prices[i] = np.round(np.exp(np.random.uniform(np.log(lo), np.log(hi))), -1)
        margin_low[i], margin_high[i] = cfg["profit_margin"]

    return cats, sub_cats, prices, margin_low, margin_high


def _assign_state_city(n: int):
    """Return arrays of states and matching cities for *n* rows."""
    states = np.random.choice(STATES, size=n, p=STATE_PROBS)
    cities = np.array([np.random.choice(STATE_CITIES[s]) for s in states])
    return states, cities


# ---------------------------------------------------------------------------
# Main generation routine
# ---------------------------------------------------------------------------

def generate_dataset() -> pd.DataFrame:
    """Build the complete synthetic retail dataset and return a DataFrame."""

    print("=" * 60)
    print("  Generating Synthetic Indian Retail Dataset")
    print("=" * 60)

    # ------------------------------------------------------------------
    # 1.  Core order data
    # ------------------------------------------------------------------
    order_ids = [f"ORD-{i:05d}" for i in range(1, NUM_ORDERS + 1)]
    order_dates = _generate_dates(NUM_ORDERS)

    # Customers (3 000 unique, reused across orders)
    num_customers = 3000
    customer_pool_ids = [f"CUST-{i:04d}" for i in range(1, num_customers + 1)]
    customer_pool_names = [
        f"{np.random.choice(FIRST_NAMES)} {np.random.choice(LAST_NAMES)}"
        for _ in range(num_customers)
    ]
    # Map customer_id -> customer_name for consistency
    cust_name_map = dict(zip(customer_pool_ids, customer_pool_names))

    cust_indices = np.random.choice(num_customers, size=NUM_ORDERS)
    customer_ids = [customer_pool_ids[i] for i in cust_indices]
    customer_names = [cust_name_map[cid] for cid in customer_ids]

    segments = np.random.choice(SEGMENTS, size=NUM_ORDERS, p=SEGMENT_WEIGHTS)

    # Product IDs (200 unique, reused)
    product_pool_ids = [f"PROD-{i:03d}" for i in range(1, 201)]
    product_ids = np.random.choice(product_pool_ids, size=NUM_ORDERS)

    # Category / sub-category / price
    categories, sub_categories, unit_prices, m_low, m_high = (
        _generate_product_details(NUM_ORDERS)
    )

    # Product names = sub-category (acts as a realistic product name)
    product_names = sub_categories.copy()

    # Quantity (weighted toward lower values: geometric-ish distribution)
    qty_choices = np.arange(1, 11)
    qty_weights = 1.0 / qty_choices  # inverse weighting
    qty_weights /= qty_weights.sum()
    quantities = np.random.choice(qty_choices, size=NUM_ORDERS, p=qty_weights)

    # Discounts
    discounts = np.random.choice(DISCOUNTS, size=NUM_ORDERS, p=DISCOUNT_WEIGHTS)

    # Derived financials
    sales_amounts = np.round(
        quantities * unit_prices * (1 - discounts / 100.0), 2
    )

    # Profit margins (per row, within category range; ~5 % negative)
    margins = np.array([
        np.random.uniform(lo, hi) for lo, hi in zip(m_low, m_high)
    ])
    negative_mask = np.random.rand(NUM_ORDERS) < 0.05
    margins[negative_mask] *= -1
    profits = np.round(sales_amounts * margins, 2)

    # Shipping cost (2-8 % of sales)
    shipping_pcts = np.random.uniform(0.02, 0.08, size=NUM_ORDERS)
    shipping_costs = np.round(sales_amounts * shipping_pcts, 2)

    # Payment method
    payments = np.random.choice(
        PAYMENT_METHODS, size=NUM_ORDERS, p=PAYMENT_WEIGHTS
    )

    # Geography
    states, cities = _assign_state_city(NUM_ORDERS)

    # Order status
    statuses = np.random.choice(
        ORDER_STATUSES, size=NUM_ORDERS, p=STATUS_WEIGHTS
    )

    # Return reason (only for Returned orders)
    return_reason_candidates = np.random.choice(RETURN_REASONS, size=NUM_ORDERS)
    return_reasons = np.where(
        statuses == "Returned",
        return_reason_candidates,
        None,
    )

    # ------------------------------------------------------------------
    # 2.  Assemble DataFrame
    # ------------------------------------------------------------------
    df = pd.DataFrame({
        "order_id":         order_ids,
        "order_date":       order_dates,
        "customer_id":      customer_ids,
        "customer_name":    customer_names,
        "customer_segment": segments,
        "product_id":       product_ids,
        "product_name":     product_names,
        "category":         categories,
        "sub_category":     sub_categories,
        "quantity":         quantities,
        "unit_price":       unit_prices,
        "discount_percent": discounts.astype(float),
        "sales_amount":     sales_amounts,
        "profit":           profits,
        "shipping_cost":    shipping_costs,
        "payment_method":   payments,
        "state":            states,
        "city":             cities,
        "order_status":     statuses,
        "return_reason":    return_reasons,
    })

    print(f"  Base orders generated: {len(df):,}")

    # ------------------------------------------------------------------
    # 3.  Introduce data-quality issues
    # ------------------------------------------------------------------

    # 3a. ~2 % missing values in selected columns
    missing_cols = ["customer_name", "city", "discount_percent", "payment_method"]
    num_missing_per_col = int(0.02 * NUM_ORDERS)  # ~300 per column
    for col in missing_cols:
        missing_idx = np.random.choice(df.index, size=num_missing_per_col, replace=False)
        df.loc[missing_idx, col] = np.nan
    print(f"  Missing values injected: ~{num_missing_per_col} per column "
          f"in {missing_cols}")

    # 3b. ~15 exact duplicate rows
    dup_idx = np.random.choice(df.index, size=15, replace=False)
    duplicates = df.loc[dup_idx].copy()
    df = pd.concat([df, duplicates], ignore_index=True)
    print(f"  Duplicate rows added: {len(duplicates)}")

    # 3c. ~20 rows with obviously wrong dates (year 1900 or 2099)
    wrong_date_idx = np.random.choice(df.index, size=20, replace=False)
    wrong_dates = []
    for i, idx in enumerate(wrong_date_idx):
        if i % 2 == 0:
            wrong_dates.append(pd.Timestamp("1900-01-15"))
        else:
            wrong_dates.append(pd.Timestamp("2099-07-20"))
    df.loc[wrong_date_idx, "order_date"] = wrong_dates
    print(f"  Wrong-date rows injected: {len(wrong_date_idx)}")

    # 3d. ~10 rows with negative quantities (data errors)
    neg_qty_idx = np.random.choice(df.index, size=10, replace=False)
    df.loc[neg_qty_idx, "quantity"] = np.random.choice(
        [-1, -2, -3, -5], size=10
    )
    print(f"  Negative-quantity rows injected: {len(neg_qty_idx)}")

    # Shuffle rows so issues aren't clustered at the end
    df = df.sample(frac=1, random_state=SEED).reset_index(drop=True)

    print(f"  Final dataset shape: {df.shape}")
    return df


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    df = generate_dataset()

    # Save to CSV
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"\n  [OK] Dataset saved to: {OUTPUT_PATH}")
    print(f"     File size: {os.path.getsize(OUTPUT_PATH) / (1024 * 1024):.2f} MB")

    # Summary statistics
    print("\n" + "=" * 60)
    print("  Dataset Summary")
    print("=" * 60)
    print(f"  Rows          : {len(df):,}")
    print(f"  Columns       : {len(df.columns)}")
    print(f"  Date range    : {df['order_date'].min()} -> {df['order_date'].max()}")
    print(f"  Categories    : {df['category'].nunique()}")
    print(f"  States        : {df['state'].nunique()}")
    print(f"  Customers     : {df['customer_id'].nunique()}")
    print(f"  Products      : {df['product_id'].nunique()}")
    print(f"  Missing values:\n{df.isnull().sum()[df.isnull().sum() > 0].to_string()}")
    print(f"  Duplicates    : {df.duplicated().sum()}")
    print(f"  Neg quantities: {(df['quantity'] < 0).sum()}")

    # Print column dtypes
    print(f"\n  Column dtypes:")
    for col in df.columns:
        print(f"    {col:<20s} {str(df[col].dtype)}")

    # Print first 5 rows
    print("\n" + "=" * 60)
    print("  First 5 rows")
    print("=" * 60)
    print(df.head().to_string())

    return df


if __name__ == "__main__":
    main()
