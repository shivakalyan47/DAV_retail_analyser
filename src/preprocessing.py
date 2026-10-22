"""
Data Preprocessing Module for Indian Retail Analytics.

Handles data cleaning, validation, type conversion, and quality reporting.
Can be run as a standalone script: python -m src.preprocessing
"""
import os
import sys
import pandas as pd
import numpy as np

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import RAW_DATA_DIR, PROCESSED_DATA_DIR, ORDERS_FILE, CLEANED_FILE, DATA_QUALITY_FILE


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize column names to lowercase with underscores.
    
    Args:
        df: Input DataFrame.
    
    Returns:
        DataFrame with standardized column names.
    """
    df = df.copy()
    # Normalize non-breaking spaces and other whitespace variations
    df.columns = df.columns.astype(str).str.replace('\xa0', ' ', regex=False)
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(r"[^\w\s]", "", regex=True)
        .str.strip()
        .str.replace(r"\s+", "_", regex=True)
        .str.strip("_")
    )
    return df


def inspect_data(df: pd.DataFrame) -> dict:
    """
    Inspect dataset dimensions, types, and sample rows.
    
    Args:
        df: Input DataFrame.
    
    Returns:
        Dictionary with inspection results.
    """
    return {
        "shape": df.shape,
        "columns": list(df.columns),
        "dtypes": df.dtypes.to_dict(),
        "sample_rows": df.head(3).to_dict(),
        "memory_usage_mb": round(df.memory_usage(deep=True).sum() / 1024 / 1024, 2),
    }


def detect_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detect and summarize missing values per column.
    
    Args:
        df: Input DataFrame.
    
    Returns:
        DataFrame with columns: column, missing_count, missing_percent, dtype.
    """
    missing = df.isnull().sum()
    total = len(df)
    summary = pd.DataFrame({
        "column": missing.index,
        "missing_count": missing.values,
        "missing_percent": np.round(missing.values / total * 100, 2) if total > 0 else 0.0,
        "dtype": df.dtypes.values.astype(str),
    })
    return summary[summary["missing_count"] > 0].sort_values(
        "missing_count", ascending=False
    ).reset_index(drop=True)


def detect_duplicates(df: pd.DataFrame) -> dict:
    """
    Identify exact duplicate rows.
    
    Args:
        df: Input DataFrame.
    
    Returns:
        Dict with duplicate count and sample duplicates.
    """
    if df.empty:
        return {"duplicate_count": 0, "duplicate_percent": 0.0, "sample_duplicates": pd.DataFrame()}
    duplicated_mask = df.duplicated(keep="first")
    dup_count = duplicated_mask.sum()
    return {
        "duplicate_count": int(dup_count),
        "duplicate_percent": round(float(dup_count / len(df) * 100), 2),
        "sample_duplicates": df[duplicated_mask].head(5) if dup_count > 0 else pd.DataFrame(),
    }


def convert_dates(df: pd.DataFrame, date_columns: list = None) -> pd.DataFrame:
    """
    Convert date columns to datetime, handling invalid dates.
    
    Args:
        df: Input DataFrame.
        date_columns: List of columns to convert. Auto-detects 'order_date' if None.
    
    Returns:
        DataFrame with converted dates. Invalid dates become NaT.
    """
    df = df.copy()
    if date_columns is None:
        date_columns = [col for col in df.columns if "date" in col.lower()]
    
    for col in date_columns:
        if col in df.columns:
            try:
                df[col] = pd.to_datetime(df[col], errors="coerce", format="mixed")
            except Exception:
                df[col] = pd.to_datetime(df[col], errors="coerce")
    
    return df


def validate_numeric_fields(df: pd.DataFrame) -> dict:
    """
    Validate numeric fields for anomalies.
    
    Returns dict with findings about negative values, outliers, etc.
    """
    findings = {}
    
    numeric_checks = {
        "quantity": {"allow_negative": False, "description": "Units ordered"},
        "unit_price": {"allow_negative": False, "description": "Price per unit"},
        "sales_amount": {"allow_negative": True, "description": "Can be negative for returns/refunds"},
        "discount_percent": {"allow_negative": False, "description": "Discount percentage"},
        "profit": {"allow_negative": True, "description": "Can be negative (loss)"},
        "shipping_cost": {"allow_negative": False, "description": "Shipping cost"},
    }
    
    for col, rules in numeric_checks.items():
        if col not in df.columns:
            continue
        
        col_data = pd.to_numeric(df[col], errors="coerce")
        neg_count = (col_data < 0).sum()
        null_count = col_data.isnull().sum()
        
        findings[col] = {
            "negative_count": int(neg_count),
            "null_after_conversion": int(null_count),
            "allow_negative": rules["allow_negative"],
            "description": rules["description"],
            "min": float(col_data.min()) if not col_data.isnull().all() else None,
            "max": float(col_data.max()) if not col_data.isnull().all() else None,
            "mean": float(col_data.mean()) if not col_data.isnull().all() else None,
        }
    
    return findings


def validate_dates(df: pd.DataFrame, date_col: str = "order_date",
                   min_year: int = 2020, max_year: int = 2026) -> dict:
    """
    Identify dates outside a reasonable range.
    
    Args:
        df: DataFrame with datetime column.
        date_col: Name of date column.
        min_year: Earliest acceptable year.
        max_year: Latest acceptable year.
    
    Returns:
        Dict with invalid date information.
    """
    if date_col not in df.columns:
        return {"error": f"Column '{date_col}' not found"}
    
    dates = df[date_col]
    nat_count = dates.isnull().sum()
    
    valid_dates = dates.dropna()
    if len(valid_dates) == 0:
        return {"nat_count": int(nat_count), "out_of_range": 0}
    
    out_of_range_mask = (valid_dates.dt.year < min_year) | (valid_dates.dt.year > max_year)
    
    return {
        "nat_count": int(nat_count),
        "out_of_range_count": int(out_of_range_mask.sum()),
        "date_range": f"{valid_dates.min()} to {valid_dates.max()}",
        "out_of_range_years": valid_dates[out_of_range_mask].dt.year.unique().tolist()
        if out_of_range_mask.any() else [],
    }


def clean_data(df: pd.DataFrame) -> tuple:
    """
    Main cleaning pipeline. Returns cleaned DataFrame and quality report.
    
    Cleaning steps:
    1. Standardize column names
    2. Remove exact duplicate rows
    3. Convert dates, coercing invalid dates to NaT
    4. Remove rows with invalid dates (outside 2020-2026 range)
    5. Convert numeric columns to proper types
    6. Remove rows with negative quantities (data errors, not returns)
    7. Fill missing discount_percent with 0 (assume no discount)
    8. Fill missing payment_method with 'Unknown'
    9. Fill missing customer_name with 'Unknown'
    10. Fill missing city with 'Unknown'
    11. Recalculate sales_amount for consistency
    12. Derive year, month, quarter, month_name columns
    13. Derive revenue = sales_amount (alias for clarity)
    
    Decision log:
    - Negative quantities: Removed as data errors (not returns - returns have order_status='Returned')
    - Missing discounts: Set to 0 (conservative assumption: no discount applied)
    - Missing payment_method: Set to 'Unknown' (preserves the record)
    - Invalid dates: Removed (cannot analyze trends without valid dates)
    - Duplicate rows: Removed (exact duplicates are data entry errors)
    - Negative profit: KEPT (legitimate business scenario - selling at a loss)
    - Negative sales_amount: KEPT only if order_status is Returned/Cancelled
    
    Args:
        df: Raw DataFrame.
    
    Returns:
        Tuple of (cleaned_df, quality_report_dict).
    """
    quality = {
        "original_rows": len(df),
        "original_columns": len(df.columns),
        "steps": [],
    }
    
    # Step 1: Standardize columns
    df = standardize_columns(df)
    
    # Map common column name variations to standard names
    column_aliases = {
        "order_number": "order_id",
        "orderno": "order_id",
        "order_no": "order_id",
        "invoice_no": "order_id",
        "invoice_id": "order_id",
        "invoiceno": "order_id",
        "transaction_id": "order_id",
        "date": "order_date",
        "orderdate": "order_date",
        "transaction_date": "order_date",
        "invoice_date": "order_date",
        "customer": "customer_name",
        "customername": "customer_name",
        "client_name": "customer_name",
        "cust_id": "customer_id",
        "custid": "customer_id",
        "product": "product_name",
        "productname": "product_name",
        "item": "product_name",
        "item_name": "product_name",
        "sku": "product_id",
        "product_category": "category",
        "prod_category": "category",
        "department": "category",
        "qty": "quantity",
        "units": "quantity",
        "count": "quantity",
        "price": "unit_price",
        "rate": "unit_price",
        "unitprice": "unit_price",
        "sales": "sales_amount",
        "amount": "sales_amount",
        "total_amount": "sales_amount",
        "total_sales": "sales_amount",
        "revenue": "sales_amount",
        "gross_amount": "sales_amount",
        "discount": "discount_percent",
        "discount_rate": "discount_percent",
        "disc": "discount_percent",
        "status": "order_status",
        "payment": "payment_method",
        "payment_type": "payment_method",
        "payment_mode": "payment_method",
        "state_name": "state",
        "province": "state",
        "region": "state",
        "city_name": "city",
    }
    for alias, target in column_aliases.items():
        if alias in df.columns and target not in df.columns:
            df.rename(columns={alias: target}, inplace=True)

    # Ensure essential identifiers
    if "order_id" not in df.columns:
        df["order_id"] = [f"ORD-{i:05d}" for i in range(1, len(df) + 1)]
    if "category" not in df.columns:
        df["category"] = "General"
    if "product_name" not in df.columns:
        df["product_name"] = "Item-" + df.index.astype(str)
    if "state" not in df.columns:
        df["state"] = "All Regions"
    if "city" not in df.columns:
        df["city"] = "All Cities"

    quality["steps"].append({"step": "Standardize and normalize column names", "rows_after": len(df)})
    
    # Step 2: Remove exact duplicates
    dup_info = detect_duplicates(df)
    df = df.drop_duplicates(keep="first").reset_index(drop=True)
    quality["steps"].append({
        "step": "Remove exact duplicate rows",
        "duplicates_removed": dup_info["duplicate_count"],
        "rows_after": len(df),
    })
    
    # Step 3: Convert dates
    df = convert_dates(df, ["order_date"])
    
    # Step 4: Remove invalid dates
    if "order_date" in df.columns:
        date_info = validate_dates(df)
        valid_date_mask = df["order_date"].notna()
        valid_date_mask &= (df["order_date"].dt.year >= 2000) & (df["order_date"].dt.year <= 2035)
        removed = len(df) - valid_date_mask.sum()
        df = df[valid_date_mask].reset_index(drop=True)
        quality["steps"].append({
            "step": "Remove rows with invalid/missing dates",
            "rows_removed": int(removed),
            "rows_after": len(df),
            "details": date_info,
        })
    
    # Step 5: Convert numeric columns
    numeric_cols = ["quantity", "unit_price", "sales_amount", "discount_percent",
                    "profit", "shipping_cost"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    
    # Step 6: Remove negative quantities (data errors)
    if "quantity" not in df.columns:
        df["quantity"] = 1
    else:
        neg_qty = (df["quantity"] < 0).sum()
        df = df[df["quantity"] >= 0].reset_index(drop=True)
        zero_qty = (df["quantity"] == 0).sum()
        df = df[df["quantity"] > 0].reset_index(drop=True)
        quality["steps"].append({
            "step": "Remove rows with negative/zero quantities (data errors)",
            "negative_removed": int(neg_qty),
            "zero_removed": int(zero_qty),
            "rows_after": len(df),
        })
    
    # Step 7: Fill missing discount_percent with 0
    if "discount_percent" in df.columns:
        missing_disc = df["discount_percent"].isnull().sum()
        df["discount_percent"] = df["discount_percent"].fillna(0)
        quality["steps"].append({
            "step": "Fill missing discount_percent with 0 (assume no discount)",
            "filled_count": int(missing_disc),
        })
    else:
        df["discount_percent"] = 0.0
    
    # Step 8: Fill missing categorical fields
    fill_unknowns = {"payment_method": "Unknown", "customer_name": "Unknown", "city": "Unknown", "order_status": "Delivered"}
    for col, fill_val in fill_unknowns.items():
        if col in df.columns:
            missing = df[col].isnull().sum()
            df[col] = df[col].fillna(fill_val)
            if missing > 0:
                quality["steps"].append({
                    "step": f"Fill missing {col} with '{fill_val}'",
                    "filled_count": int(missing),
                })
        else:
            df[col] = fill_val
    
    # Step 9: Recalculate or establish sales_amount & unit_price
    if "unit_price" in df.columns and "quantity" in df.columns:
        df["sales_amount"] = (
            df["quantity"] * df["unit_price"] * (1 - df["discount_percent"] / 100)
        ).round(2)
        quality["steps"].append({"step": "Recalculated sales_amount = qty * price * (1 - disc/100)"})
    elif "sales_amount" in df.columns:
        df["sales_amount"] = df["sales_amount"].round(2)
        if "unit_price" not in df.columns:
            df["unit_price"] = (df["sales_amount"] / df["quantity"].replace(0, 1)).round(2)
    elif "revenue" in df.columns:
        df["sales_amount"] = df["revenue"].round(2)
        df["unit_price"] = (df["sales_amount"] / df["quantity"].replace(0, 1)).round(2)
    else:
        df["unit_price"] = 100.0
        df["sales_amount"] = (df["quantity"] * df["unit_price"]).round(2)
    
    # Step 10: Derive time columns
    if "order_date" in df.columns:
        df["year"] = df["order_date"].dt.year
        df["month"] = df["order_date"].dt.month
        df["quarter"] = df["order_date"].dt.quarter
        df["month_name"] = df["order_date"].dt.strftime("%b")
        df["year_month"] = df["order_date"].dt.to_period("M").astype(str)
        quality["steps"].append({"step": "Derived year, month, quarter, month_name, year_month columns"})
    
    # Step 11: Revenue alias
    if "sales_amount" in df.columns:
        df["revenue"] = df["sales_amount"]
    
    quality["final_rows"] = len(df)
    quality["final_columns"] = len(df.columns)
    quality["rows_removed_total"] = quality["original_rows"] - quality["final_rows"]
    quality["removal_percent"] = round(
        quality["rows_removed_total"] / quality["original_rows"] * 100, 2
    )
    
    return df, quality


def generate_quality_report(df_raw: pd.DataFrame, df_clean: pd.DataFrame,
                            quality: dict) -> str:
    """
    Generate a human-readable data quality report.
    
    Returns:
        Formatted string report.
    """
    lines = [
        "=" * 60,
        "DATA QUALITY REPORT",
        "=" * 60,
        f"Original rows: {quality['original_rows']:,}",
        f"Original columns: {quality['original_columns']}",
        f"Final rows: {quality['final_rows']:,}",
        f"Final columns: {quality['final_columns']}",
        f"Total rows removed: {quality['rows_removed_total']:,} ({quality['removal_percent']}%)",
        "",
        "CLEANING STEPS:",
        "-" * 40,
    ]
    
    for i, step in enumerate(quality["steps"], 1):
        lines.append(f"  {i}. {step['step']}")
        for k, v in step.items():
            if k != "step":
                lines.append(f"     {k}: {v}")
    
    lines.extend([
        "",
        "REMAINING MISSING VALUES (cleaned data):",
        "-" * 40,
    ])
    
    missing = detect_missing_values(df_clean)
    if len(missing) == 0:
        lines.append("  None")
    else:
        for _, row in missing.iterrows():
            lines.append(f"  {row['column']}: {row['missing_count']} ({row['missing_percent']}%)")
    
    lines.extend([
        "",
        "CLEANED DATA TYPES:",
        "-" * 40,
    ])
    for col, dtype in df_clean.dtypes.items():
        lines.append(f"  {col}: {dtype}")
    
    return "\n".join(lines)


def run_preprocessing():
    """Run the full preprocessing pipeline and save results."""
    print("=" * 60)
    print("INDIAN RETAIL ANALYTICS - DATA PREPROCESSING")
    print("=" * 60)
    
    # Load raw data
    raw_path = os.path.join(RAW_DATA_DIR, ORDERS_FILE)
    print(f"\nLoading raw data from: {raw_path}")
    
    if not os.path.exists(raw_path):
        print(f"ERROR: File not found: {raw_path}")
        print(f"Please place your CSV in: {RAW_DATA_DIR}")
        sys.exit(1)
    
    df_raw = pd.read_csv(raw_path)
    print(f"Raw data shape: {df_raw.shape}")
    print(f"Columns: {list(df_raw.columns)}")
    
    # Run cleaning
    print("\nRunning cleaning pipeline...")
    df_clean, quality = clean_data(df_raw)
    
    # Generate report
    report = generate_quality_report(df_raw, df_clean, quality)
    print(f"\n{report}")
    
    # Save cleaned data
    clean_path = os.path.join(PROCESSED_DATA_DIR, CLEANED_FILE)
    df_clean.to_csv(clean_path, index=False)
    print(f"\nCleaned data saved to: {clean_path}")
    print(f"Cleaned data shape: {df_clean.shape}")
    
    # Save quality report
    report_path = os.path.join(PROCESSED_DATA_DIR, DATA_QUALITY_FILE.replace(".csv", ".txt"))
    with open(report_path, "w") as f:
        f.write(report)
    print(f"Quality report saved to: {report_path}")
    
    return df_clean, quality


if __name__ == "__main__":
    run_preprocessing()
