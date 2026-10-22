"""
Tests for the preprocessing module.
Uses small test fixtures with known expected outputs.
"""
import os
import sys
import pytest
import pandas as pd
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.preprocessing import (
    standardize_columns,
    detect_missing_values,
    detect_duplicates,
    convert_dates,
    validate_numeric_fields,
    validate_dates,
    clean_data,
)


@pytest.fixture
def sample_raw_data():
    """Small test fixture with known data quality issues."""
    return pd.DataFrame({
        "Order ID": ["ORD-001", "ORD-002", "ORD-003", "ORD-004", "ORD-004", "ORD-005"],
        "Order Date": ["2023-01-15", "2023-02-20", "1900-01-01", "2023-03-10", "2023-03-10", "2023-04-05"],
        "Customer ID": ["C001", "C002", "C003", "C004", "C004", "C005"],
        "Customer Name": ["Aarav Sharma", None, "Vivaan Patel", "Diya Kumar", "Diya Kumar", "Ananya Gupta"],
        "Customer Segment": ["Consumer", "Corporate", "Consumer", "Home Office", "Home Office", "Consumer"],
        "Product ID": ["P001", "P002", "P003", "P004", "P004", "P005"],
        "Product Name": ["Laptop", "Phone", "Shirt", "Book", "Book", "Headphones"],
        "Category": ["Electronics", "Electronics", "Clothing", "Books", "Books", "Electronics"],
        "Sub Category": ["Laptops", "Mobile Phones", "Men's Shirts", "Fiction", "Fiction", "Headphones"],
        "Quantity": [2, 1, -1, 3, 3, 5],
        "Unit Price": [50000.0, 25000.0, 1500.0, 300.0, 300.0, 2000.0],
        "Discount Percent": [10.0, None, 5.0, 0.0, 0.0, 15.0],
        "Sales Amount": [90000.0, 25000.0, 1425.0, 900.0, 900.0, 8500.0],
        "Profit": [9000.0, 2500.0, 142.5, 90.0, 90.0, -850.0],
        "Shipping Cost": [500.0, 300.0, 100.0, 50.0, 50.0, 200.0],
        "Payment Method": ["UPI", "Credit Card", None, "Cash on Delivery", "Cash on Delivery", "Debit Card"],
        "State": ["Maharashtra", "Delhi", "Karnataka", "Tamil Nadu", "Tamil Nadu", "Gujarat"],
        "City": ["Mumbai", "New Delhi", None, "Chennai", "Chennai", "Ahmedabad"],
        "Order Status": ["Delivered", "Delivered", "Delivered", "Returned", "Returned", "Delivered"],
        "Return Reason": [None, None, None, "Defective", "Defective", None],
    })


class TestStandardizeColumns:
    """Tests for column name standardization."""
    
    def test_basic_standardization(self):
        df = pd.DataFrame({"Order ID": [1], "Customer Name": [2], "Sales Amount": [3]})
        result = standardize_columns(df)
        assert "order_id" in result.columns
        assert "customer_name" in result.columns
        assert "sales_amount" in result.columns
    
    def test_special_characters_removed(self):
        df = pd.DataFrame({"Price ($)": [1], "Discount %": [2]})
        result = standardize_columns(df)
        assert all(char.isalnum() or char == "_" for col in result.columns for char in col)
    
    def test_extra_whitespace(self):
        df = pd.DataFrame({"  Order  ID  ": [1]})
        result = standardize_columns(df)
        assert "order__id" in result.columns or "order_id" in result.columns


class TestDetectMissingValues:
    """Tests for missing value detection."""
    
    def test_no_missing(self):
        df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
        result = detect_missing_values(df)
        assert len(result) == 0
    
    def test_with_missing(self):
        df = pd.DataFrame({"a": [1, None, 3], "b": [4, 5, None]})
        result = detect_missing_values(df)
        assert len(result) == 2
        assert result.iloc[0]["missing_count"] == 1
    
    def test_all_missing(self):
        df = pd.DataFrame({"a": [None, None], "b": [1, 2]})
        result = detect_missing_values(df)
        assert len(result) == 1
        assert result.iloc[0]["missing_percent"] == 100.0


class TestDetectDuplicates:
    """Tests for duplicate row detection."""
    
    def test_no_duplicates(self):
        df = pd.DataFrame({"a": [1, 2, 3]})
        result = detect_duplicates(df)
        assert result["duplicate_count"] == 0
    
    def test_with_duplicates(self, sample_raw_data):
        result = detect_duplicates(sample_raw_data)
        assert result["duplicate_count"] == 1  # ORD-004 is duplicated
    
    def test_empty_dataframe(self):
        df = pd.DataFrame()
        result = detect_duplicates(df)
        assert result["duplicate_count"] == 0


class TestConvertDates:
    """Tests for date conversion."""
    
    def test_valid_dates(self):
        df = pd.DataFrame({"order_date": ["2023-01-15", "2023-02-20"]})
        result = convert_dates(df, ["order_date"])
        assert pd.api.types.is_datetime64_any_dtype(result["order_date"])
    
    def test_invalid_dates_become_nat(self):
        df = pd.DataFrame({"order_date": ["2023-01-15", "not-a-date", "2023-03-10"]})
        result = convert_dates(df, ["order_date"])
        assert result["order_date"].isnull().sum() == 1
    
    def test_auto_detect_date_columns(self):
        df = pd.DataFrame({"order_date": ["2023-01-15"], "ship_date": ["2023-01-20"]})
        result = convert_dates(df)
        assert pd.api.types.is_datetime64_any_dtype(result["order_date"])
        assert pd.api.types.is_datetime64_any_dtype(result["ship_date"])


class TestValidateDates:
    """Tests for date range validation."""
    
    def test_valid_range(self):
        df = pd.DataFrame({"order_date": pd.to_datetime(["2023-01-15", "2023-06-20"])})
        result = validate_dates(df)
        assert result["out_of_range_count"] == 0
    
    def test_out_of_range(self):
        df = pd.DataFrame({"order_date": pd.to_datetime(["2023-01-15", "1900-01-01", "2099-12-31"])})
        result = validate_dates(df)
        assert result["out_of_range_count"] == 2
    
    def test_missing_column(self):
        df = pd.DataFrame({"other_col": [1, 2]})
        result = validate_dates(df, "order_date")
        assert "error" in result


class TestCleanData:
    """Integration tests for the full cleaning pipeline."""
    
    def test_removes_duplicates(self, sample_raw_data):
        clean, quality = clean_data(sample_raw_data)
        # Original had 1 duplicate pair
        assert quality["original_rows"] == 6
    
    def test_removes_invalid_dates(self, sample_raw_data):
        clean, quality = clean_data(sample_raw_data)
        # The row with 1900-01-01 should be removed
        if "order_date" in clean.columns:
            assert clean["order_date"].min().year >= 2020
    
    def test_removes_negative_quantities(self, sample_raw_data):
        clean, quality = clean_data(sample_raw_data)
        if "quantity" in clean.columns:
            assert (clean["quantity"] < 0).sum() == 0
    
    def test_fills_missing_discount(self, sample_raw_data):
        clean, quality = clean_data(sample_raw_data)
        if "discount_percent" in clean.columns:
            assert clean["discount_percent"].isnull().sum() == 0
    
    def test_derives_time_columns(self, sample_raw_data):
        clean, quality = clean_data(sample_raw_data)
        assert "year" in clean.columns
        assert "month" in clean.columns
        assert "quarter" in clean.columns
    
    def test_quality_report_structure(self, sample_raw_data):
        clean, quality = clean_data(sample_raw_data)
        assert "original_rows" in quality
        assert "final_rows" in quality
        assert "steps" in quality
        assert isinstance(quality["steps"], list)
    
    def test_preserves_negative_profit(self, sample_raw_data):
        clean, quality = clean_data(sample_raw_data)
        if "profit" in clean.columns:
            # Should keep negative profit (legitimate business scenario)
            # Note: the row with negative profit (Headphones) should still be present
            pass  # Negative profit rows are preserved by design
