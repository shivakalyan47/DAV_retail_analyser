"""
Data Loading Module for Indian Retail Analytics.

Provides configurable data loading functions that handle CSV files
from the raw data directory. Supports caching for Streamlit performance.
"""
import os
import pandas as pd
import streamlit as st
from config import RAW_DATA_DIR, PROCESSED_DATA_DIR, ORDERS_FILE, CLEANED_FILE


def load_raw_data(filename: str = None) -> pd.DataFrame:
    """
    Load raw CSV data from the raw data directory.
    
    Args:
        filename: Name of the CSV file. Defaults to ORDERS_FILE from config.
    
    Returns:
        pd.DataFrame with raw data.
    
    Raises:
        FileNotFoundError: If the CSV file doesn't exist.
    """
    if filename is None:
        filename = ORDERS_FILE
    filepath = os.path.join(RAW_DATA_DIR, filename)
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(
            f"Dataset file not found: {filepath}\n"
            f"Please place your CSV file in: {RAW_DATA_DIR}\n"
            f"Expected filename: {filename}\n"
            f"You can change the filename in config.py (ORDERS_FILE setting)."
        )
    
    encodings_to_try = ["utf-8", "latin1", "cp1252", "iso-8859-1", "utf-8-sig"]
    for enc in encodings_to_try:
        try:
            return pd.read_csv(filepath, encoding=enc)
        except (UnicodeDecodeError, UnicodeError):
            continue
        except Exception:
            continue
    return pd.read_csv(filepath, encoding="utf-8", encoding_errors="replace")


def load_cleaned_data(filename: str = None) -> pd.DataFrame:
    """
    Load cleaned/processed CSV data.
    
    Args:
        filename: Name of the cleaned CSV file. Defaults to CLEANED_FILE from config.
    
    Returns:
        pd.DataFrame with cleaned data.
    
    Raises:
        FileNotFoundError: If cleaned data doesn't exist.
    """
    if filename is None:
        filename = CLEANED_FILE
    filepath = os.path.join(PROCESSED_DATA_DIR, filename)
    
    if not os.path.exists(filepath):
        raw_path = os.path.join(RAW_DATA_DIR, ORDERS_FILE)
        if os.path.exists(raw_path):
            from src.preprocessing import run_preprocessing
            df_clean, _ = run_preprocessing()
            return df_clean
        raise FileNotFoundError(
            f"Cleaned data not found: {filepath}\n"
            "Please run preprocessing first:\n"
            "  python -m src.preprocessing"
        )
    
    df = pd.read_csv(filepath, parse_dates=["order_date"])
    return df


@st.cache_data(ttl=3600, show_spinner="Loading data...")
def load_data_cached() -> pd.DataFrame:
    """
    Load cleaned data with Streamlit caching.
    Cached for 1 hour to avoid reloading on every interaction.
    
    Returns:
        pd.DataFrame with cleaned data.
    """
    return load_cleaned_data()


def get_available_datasets() -> list:
    """
    List all CSV files available in the raw data directory.
    
    Returns:
        List of CSV filenames.
    """
    if not os.path.exists(RAW_DATA_DIR):
        return []
    return [f for f in os.listdir(RAW_DATA_DIR) if f.endswith(".csv")]


def validate_required_columns(df: pd.DataFrame, required: list) -> dict:
    """
    Check which required columns exist in the DataFrame.
    
    Args:
        df: Input DataFrame.
        required: List of required column names.
    
    Returns:
        Dict with 'present' and 'missing' column lists.
    """
    present = [col for col in required if col in df.columns]
    missing = [col for col in required if col not in df.columns]
    return {"present": present, "missing": missing}
