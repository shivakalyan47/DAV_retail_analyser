"""
Tests for the metrics module.
Tests use small fixtures with known expected outputs.
"""
import os
import sys
import pytest
import pandas as pd
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.metrics import (
    safe_divide,
    format_inr,
    format_inr_short,
    total_revenue,
    total_orders,
    total_units_sold,
    average_order_value,
    monthly_revenue,
    revenue_by_category,
    revenue_by_product,
    revenue_by_state,
    repeat_customer_rate,
    return_analysis,
    profit_analysis,
    generate_insights,
)


@pytest.fixture
def sample_data():
    """Clean test data with known expected values."""
    return pd.DataFrame({
        "order_id": ["ORD-001", "ORD-001", "ORD-002", "ORD-003", "ORD-004"],
        "order_date": pd.to_datetime(["2023-01-15", "2023-01-15", "2023-02-20", "2023-02-25", "2023-03-10"]),
        "customer_id": ["C001", "C001", "C002", "C001", "C003"],
        "customer_name": ["Aarav", "Aarav", "Vivaan", "Aarav", "Diya"],
        "product_name": ["Laptop", "Mouse", "Phone", "Shirt", "Book"],
        "category": ["Electronics", "Electronics", "Electronics", "Clothing", "Books"],
        "quantity": [1, 2, 1, 3, 5],
        "unit_price": [50000.0, 500.0, 25000.0, 1000.0, 300.0],
        "discount_percent": [10.0, 0.0, 5.0, 0.0, 0.0],
        "revenue": [45000.0, 1000.0, 23750.0, 3000.0, 1500.0],
        "sales_amount": [45000.0, 1000.0, 23750.0, 3000.0, 1500.0],
        "profit": [4500.0, 100.0, 2375.0, 300.0, -150.0],
        "state": ["Maharashtra", "Maharashtra", "Delhi", "Karnataka", "Tamil Nadu"],
        "city": ["Mumbai", "Mumbai", "New Delhi", "Bengaluru", "Chennai"],
        "order_status": ["Delivered", "Delivered", "Delivered", "Returned", "Delivered"],
        "payment_method": ["UPI", "UPI", "Credit Card", "Debit Card", "UPI"],
        "customer_segment": ["Consumer", "Consumer", "Corporate", "Consumer", "Home Office"],
        "year_month": ["2023-01", "2023-01", "2023-02", "2023-02", "2023-03"],
    })


@pytest.fixture
def empty_data():
    """Empty DataFrame for edge case testing."""
    return pd.DataFrame()


class TestSafeDivide:
    """Tests for safe division."""
    
    def test_normal_division(self):
        assert safe_divide(10, 2) == 5.0
    
    def test_zero_denominator(self):
        assert safe_divide(10, 0) == 0.0
    
    def test_none_denominator(self):
        assert safe_divide(10, None) == 0.0
    
    def test_nan_denominator(self):
        assert safe_divide(10, float("nan")) == 0.0
    
    def test_custom_default(self):
        assert safe_divide(10, 0, default=-1.0) == -1.0


class TestFormatINR:
    """Tests for Indian Rupee formatting."""
    
    def test_small_number(self):
        assert format_inr(500) == "₹500"
    
    def test_thousands(self):
        result = format_inr(12345)
        assert "₹12,345" in result
    
    def test_lakhs(self):
        result = format_inr(123456)
        assert "₹1,23,456" in result
    
    def test_crores(self):
        result = format_inr(12345678)
        assert "₹1,23,45,678" in result
    
    def test_negative(self):
        result = format_inr(-5000)
        assert result.startswith("-₹")
    
    def test_nan(self):
        assert format_inr(float("nan")) == "₹0"


class TestFormatINRShort:
    """Tests for short INR formatting."""
    
    def test_crore(self):
        result = format_inr_short(1_50_00_000)
        assert "Cr" in result
    
    def test_lakh(self):
        result = format_inr_short(5_00_000)
        assert "L" in result
    
    def test_thousand(self):
        result = format_inr_short(5000)
        assert "K" in result


class TestTotalRevenue:
    """Tests for total revenue calculation."""
    
    def test_normal(self, sample_data):
        # 45000 + 1000 + 23750 + 3000 + 1500 = 74250
        assert total_revenue(sample_data) == 74250.0
    
    def test_empty(self, empty_data):
        assert total_revenue(empty_data) == 0.0
    
    def test_missing_column(self):
        df = pd.DataFrame({"other": [1, 2, 3]})
        assert total_revenue(df) == 0.0


class TestTotalOrders:
    """Tests for distinct order counting."""
    
    def test_distinct_count(self, sample_data):
        # ORD-001 appears twice (2 line items), ORD-002, ORD-003, ORD-004 = 4 distinct
        assert total_orders(sample_data) == 4
    
    def test_empty(self, empty_data):
        assert total_orders(empty_data) == 0
    
    def test_all_same_order(self):
        df = pd.DataFrame({"order_id": ["ORD-001", "ORD-001", "ORD-001"]})
        assert total_orders(df) == 1


class TestTotalUnitsSold:
    """Tests for units sold."""
    
    def test_sum(self, sample_data):
        # 1 + 2 + 1 + 3 + 5 = 12
        assert total_units_sold(sample_data) == 12
    
    def test_empty(self, empty_data):
        assert total_units_sold(empty_data) == 0


class TestAverageOrderValue:
    """Tests for average order value."""
    
    def test_calculation(self, sample_data):
        # Revenue: 74250, Orders: 4 -> AOV = 18562.50
        aov = average_order_value(sample_data)
        assert abs(aov - 18562.50) < 0.01
    
    def test_empty(self, empty_data):
        assert average_order_value(empty_data) == 0.0
    
    def test_single_order(self):
        df = pd.DataFrame({
            "order_id": ["ORD-001", "ORD-001"],
            "revenue": [1000.0, 500.0],
            "quantity": [1, 1],
        })
        # Total revenue: 1500, Orders: 1 -> AOV = 1500
        assert average_order_value(df) == 1500.0


class TestMonthlyRevenue:
    """Tests for monthly revenue aggregation."""
    
    def test_grouping(self, sample_data):
        result = monthly_revenue(sample_data)
        assert len(result) == 3  # 3 months
        assert "revenue" in result.columns
        assert "order_count" in result.columns
    
    def test_empty(self, empty_data):
        result = monthly_revenue(empty_data)
        assert len(result) == 0


class TestRevenueByCategory:
    """Tests for category revenue."""
    
    def test_grouping(self, sample_data):
        result = revenue_by_category(sample_data)
        assert len(result) == 3  # Electronics, Clothing, Books
        electronics = result[result["category"] == "Electronics"]["revenue"].iloc[0]
        assert electronics == 69750.0  # 45000 + 1000 + 23750
    
    def test_empty(self, empty_data):
        result = revenue_by_category(empty_data)
        assert len(result) == 0


class TestRevenueByState:
    """Tests for state-wise revenue."""
    
    def test_grouping(self, sample_data):
        result = revenue_by_state(sample_data)
        assert len(result) == 4  # 4 states
        mh = result[result["state"] == "Maharashtra"]["revenue"].iloc[0]
        assert mh == 46000.0  # 45000 + 1000


class TestRepeatCustomerRate:
    """Tests for repeat customer analysis."""
    
    def test_with_repeats(self, sample_data):
        result = repeat_customer_rate(sample_data)
        # C001 has 3 orders (ORD-001, ORD-003 -> 2 distinct), C002 has 1, C003 has 1
        assert result["total_customers"] == 3
        assert result["repeat_customers"] == 1  # Only C001
    
    def test_empty(self, empty_data):
        result = repeat_customer_rate(empty_data)
        assert result["total_customers"] == 0


class TestReturnAnalysis:
    """Tests for return analysis."""
    
    def test_with_returns(self, sample_data):
        result = return_analysis(sample_data)
        assert result["available"] is True
        assert result["returned"] == 1  # ORD-003
        assert result["delivered"] == 3  # ORD-001, ORD-002, ORD-004
    
    def test_missing_column(self):
        df = pd.DataFrame({"order_id": ["ORD-001"]})
        result = return_analysis(df)
        assert result["available"] is False


class TestProfitAnalysis:
    """Tests for profit analysis."""
    
    def test_with_profit(self, sample_data):
        result = profit_analysis(sample_data)
        assert result["available"] is True
        total = 4500 + 100 + 2375 + 300 + (-150)
        assert abs(result["total_profit"] - total) < 0.01
        assert result["loss_making_transactions"] == 1  # Book has -150
    
    def test_missing_column(self, empty_data):
        result = profit_analysis(empty_data)
        assert result["available"] is False


class TestGenerateInsights:
    """Tests for insight generation."""
    
    def test_returns_insights(self, sample_data):
        insights = generate_insights(sample_data)
        assert len(insights) > 0
        assert all("title" in i and "description" in i for i in insights)
    
    def test_empty_data(self, empty_data):
        insights = generate_insights(empty_data)
        assert len(insights) == 1
        assert "No Data" in insights[0]["title"]
