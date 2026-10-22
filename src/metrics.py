"""
Metrics Module for Indian Retail Analytics.

Provides reusable functions for computing business metrics.
All functions handle edge cases: empty DataFrames, missing columns, division by zero.

Metric formulas and assumptions:
- Revenue: Sum of sales_amount (quantity * unit_price * (1 - discount/100))
- Distinct orders: Count of unique order_id values
- Units sold: Sum of quantity
- Average order value (AOV): Total revenue / distinct orders
- Profit margin: (profit / revenue) * 100
- Return rate: Returned orders / total orders * 100

Currency: Indian Rupees (INR / ₹) - the dataset uses INR values.
"""
import pandas as pd
import numpy as np


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safe division handling zero and NaN denominators."""
    if denominator is None or denominator == 0 or pd.isna(denominator):
        return default
    return numerator / denominator


def format_inr(value: float) -> str:
    """
    Format a number as Indian Rupee string with Indian numbering system.
    Example: 1234567.89 -> ₹12,34,567.89
    """
    if pd.isna(value):
        return "₹0"
    
    is_negative = value < 0
    value = abs(value)
    
    # Split integer and decimal parts
    int_part = int(value)
    dec_part = round(value - int_part, 2)
    
    # Indian numbering: first group of 3, then groups of 2
    s = str(int_part)
    if len(s) <= 3:
        formatted = s
    else:
        last3 = s[-3:]
        remaining = s[:-3]
        groups = []
        while remaining:
            groups.append(remaining[-2:])
            remaining = remaining[:-2]
        groups.reverse()
        formatted = ",".join(groups) + "," + last3
    
    if dec_part > 0:
        dec_str = f"{dec_part:.2f}"[1:]  # ".XX"
        formatted += dec_str
    
    prefix = "-" if is_negative else ""
    return f"{prefix}₹{formatted}"


def format_inr_short(value: float) -> str:
    """Format large INR values in lakhs/crores for dashboard display."""
    if pd.isna(value):
        return "₹0"
    
    is_negative = value < 0
    value = abs(value)
    prefix = "-" if is_negative else ""
    
    if value >= 1_00_00_000:  # 1 crore
        return f"{prefix}₹{value / 1_00_00_000:.2f} Cr"
    elif value >= 1_00_000:  # 1 lakh
        return f"{prefix}₹{value / 1_00_000:.2f} L"
    elif value >= 1000:
        return f"{prefix}₹{value / 1000:.1f}K"
    else:
        return f"{prefix}₹{value:,.0f}"


def total_revenue(df: pd.DataFrame, col: str = "revenue") -> float:
    """Calculate total revenue. Returns 0 for empty DataFrame."""
    if df.empty or col not in df.columns:
        return 0.0
    return float(df[col].sum())


def total_orders(df: pd.DataFrame, col: str = "order_id") -> int:
    """Count distinct orders. Returns 0 for empty DataFrame."""
    if df.empty or col not in df.columns:
        return 0
    return int(df[col].nunique())


def total_units_sold(df: pd.DataFrame, col: str = "quantity") -> int:
    """Sum of quantities sold. Returns 0 for empty DataFrame."""
    if df.empty or col not in df.columns:
        return 0
    return int(df[col].sum())


def average_order_value(df: pd.DataFrame) -> float:
    """
    Average Order Value = Total Revenue / Distinct Orders.
    Returns 0 if no orders.
    """
    rev = total_revenue(df)
    orders = total_orders(df)
    return safe_divide(rev, orders)


def monthly_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate monthly revenue aggregation.
    
    Returns DataFrame with columns: year_month, revenue, order_count.
    Sorted by year_month.
    """
    if df.empty or "year_month" not in df.columns:
        return pd.DataFrame(columns=["year_month", "revenue", "order_count"])
    
    result = df.groupby("year_month").agg(
        revenue=("revenue", "sum"),
        order_count=("order_id", "nunique"),
    ).reset_index().sort_values("year_month")
    
    return result


def revenue_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """Revenue aggregated by product category."""
    if df.empty or "category" not in df.columns:
        return pd.DataFrame(columns=["category", "revenue", "quantity", "order_count"])
    
    result = df.groupby("category").agg(
        revenue=("revenue", "sum"),
        quantity=("quantity", "sum"),
        order_count=("order_id", "nunique"),
    ).reset_index().sort_values("revenue", ascending=False)
    
    return result


def revenue_by_product(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """Top N products by revenue."""
    if df.empty or "product_name" not in df.columns:
        return pd.DataFrame(columns=["product_name", "category", "revenue", "quantity"])
    
    result = df.groupby(["product_name", "category"]).agg(
        revenue=("revenue", "sum"),
        quantity=("quantity", "sum"),
        order_count=("order_id", "nunique"),
    ).reset_index().sort_values("revenue", ascending=False)
    
    if top_n:
        result = result.head(top_n)
    
    return result


def quantity_by_product(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """Top N products by quantity sold."""
    if df.empty or "product_name" not in df.columns:
        return pd.DataFrame(columns=["product_name", "category", "quantity", "revenue"])
    
    result = df.groupby(["product_name", "category"]).agg(
        quantity=("quantity", "sum"),
        revenue=("revenue", "sum"),
        order_count=("order_id", "nunique"),
    ).reset_index().sort_values("quantity", ascending=False)
    
    if top_n:
        result = result.head(top_n)
    
    return result


def revenue_by_state(df: pd.DataFrame) -> pd.DataFrame:
    """Revenue aggregated by state."""
    if df.empty or "state" not in df.columns:
        return pd.DataFrame(columns=["state", "revenue", "order_count", "quantity"])
    
    result = df.groupby("state").agg(
        revenue=("revenue", "sum"),
        order_count=("order_id", "nunique"),
        quantity=("quantity", "sum"),
    ).reset_index().sort_values("revenue", ascending=False)
    
    return result


def revenue_by_city(df: pd.DataFrame, top_n: int = 15) -> pd.DataFrame:
    """Revenue aggregated by city."""
    if df.empty or "city" not in df.columns:
        return pd.DataFrame(columns=["city", "state", "revenue", "order_count"])
    
    result = df.groupby(["city", "state"]).agg(
        revenue=("revenue", "sum"),
        order_count=("order_id", "nunique"),
        quantity=("quantity", "sum"),
    ).reset_index().sort_values("revenue", ascending=False)
    
    if top_n:
        result = result.head(top_n)
    
    return result


def payment_method_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Revenue and order count by payment method."""
    if df.empty or "payment_method" not in df.columns:
        return pd.DataFrame(columns=["payment_method", "revenue", "order_count", "avg_order_value"])
    
    result = df.groupby("payment_method").agg(
        revenue=("revenue", "sum"),
        order_count=("order_id", "nunique"),
    ).reset_index()
    
    result["avg_order_value"] = result.apply(
        lambda r: safe_divide(r["revenue"], r["order_count"]), axis=1
    )
    
    return result.sort_values("revenue", ascending=False)


def customer_summary(df: pd.DataFrame, top_n: int = 20) -> pd.DataFrame:
    """Customer-level purchase summaries."""
    if df.empty or "customer_id" not in df.columns:
        return pd.DataFrame()
    
    result = df.groupby(["customer_id", "customer_name"]).agg(
        total_revenue=("revenue", "sum"),
        total_orders=("order_id", "nunique"),
        total_quantity=("quantity", "sum"),
        avg_order_value=("revenue", "mean"),
        first_order=("order_date", "min"),
        last_order=("order_date", "max"),
    ).reset_index().sort_values("total_revenue", ascending=False)
    
    if top_n:
        result = result.head(top_n)
    
    return result


def repeat_customer_rate(df: pd.DataFrame) -> dict:
    """
    Calculate repeat customer metrics.
    A repeat customer has more than 1 distinct order.
    """
    if df.empty or "customer_id" not in df.columns:
        return {"total_customers": 0, "repeat_customers": 0, "repeat_rate": 0.0}
    
    orders_per_customer = df.groupby("customer_id")["order_id"].nunique()
    total = len(orders_per_customer)
    repeat = (orders_per_customer > 1).sum()
    
    return {
        "total_customers": int(total),
        "repeat_customers": int(repeat),
        "repeat_rate": round(safe_divide(repeat, total) * 100, 2),
        "single_purchase": int(total - repeat),
    }


def return_analysis(df: pd.DataFrame) -> dict:
    """
    Analyze returns and cancellations.
    Return rate = Returned orders / Total distinct orders * 100
    """
    if df.empty or "order_status" not in df.columns:
        return {"available": False, "reason": "order_status column not found"}
    
    total = df["order_id"].nunique()
    status_counts = df.groupby("order_status")["order_id"].nunique()
    
    returned = int(status_counts.get("Returned", 0))
    cancelled = int(status_counts.get("Cancelled", 0))
    delivered = int(status_counts.get("Delivered", 0))
    processing = int(status_counts.get("Processing", 0))
    
    return {
        "available": True,
        "total_orders": int(total),
        "delivered": delivered,
        "returned": returned,
        "cancelled": cancelled,
        "processing": processing,
        "return_rate": round(safe_divide(returned, total) * 100, 2),
        "cancellation_rate": round(safe_divide(cancelled, total) * 100, 2),
        "status_counts": status_counts.to_dict(),
    }


def profit_analysis(df: pd.DataFrame) -> dict:
    """Analyze profit metrics if profit column exists."""
    if df.empty or "profit" not in df.columns:
        return {"available": False, "reason": "profit column not found"}
    
    total_profit = float(df["profit"].sum())
    total_rev = total_revenue(df)
    profit_margin = safe_divide(total_profit, total_rev) * 100
    
    profitable = (df["profit"] > 0).sum()
    loss_making = (df["profit"] < 0).sum()
    
    return {
        "available": True,
        "total_profit": total_profit,
        "profit_margin": round(profit_margin, 2),
        "profitable_transactions": int(profitable),
        "loss_making_transactions": int(loss_making),
        "avg_profit_per_order": float(df.groupby("order_id")["profit"].sum().mean()),
    }


def discount_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Analyze impact of discounts on revenue."""
    if df.empty or "discount_percent" not in df.columns:
        return pd.DataFrame()
    
    # Create discount brackets
    df_copy = df.copy()
    bins = [0, 0.01, 5, 10, 15, 20, 25, 100]
    labels = ["No Discount", "1-5%", "6-10%", "11-15%", "16-20%", "21-25%", "26%+"]
    df_copy["discount_bracket"] = pd.cut(
        df_copy["discount_percent"], bins=bins, labels=labels, include_lowest=True
    )
    
    result = df_copy.groupby("discount_bracket", observed=True).agg(
        revenue=("revenue", "sum"),
        order_count=("order_id", "nunique"),
        avg_discount=("discount_percent", "mean"),
        quantity=("quantity", "sum"),
    ).reset_index()
    
    if "profit" in df_copy.columns:
        profit_by_disc = df_copy.groupby("discount_bracket", observed=True)["profit"].sum().reset_index()
        result = result.merge(profit_by_disc, on="discount_bracket", how="left")
    
    return result


def segment_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Revenue by customer segment."""
    if df.empty or "customer_segment" not in df.columns:
        return pd.DataFrame()
    
    result = df.groupby("customer_segment").agg(
        revenue=("revenue", "sum"),
        order_count=("order_id", "nunique"),
        customers=("customer_id", "nunique"),
        quantity=("quantity", "sum"),
    ).reset_index().sort_values("revenue", ascending=False)
    
    return result


def generate_insights(df: pd.DataFrame) -> list:
    """
    Generate data-derived insight statements from actual calculations.
    Each insight is a dict with 'title' and 'description'.
    """
    insights = []
    
    if df.empty:
        return [{"title": "No Data", "description": "No data available to generate insights."}]
    
    # 1. Top category by revenue
    if "category" in df.columns:
        cat_rev = df.groupby("category")["revenue"].sum()
        top_cat = cat_rev.idxmax()
        top_cat_val = cat_rev.max()
        total_rev = cat_rev.sum()
        share = safe_divide(top_cat_val, total_rev) * 100
        insights.append({
            "title": "📊 Top Revenue Category",
            "description": (
                f"**{top_cat}** leads with {format_inr_short(top_cat_val)} "
                f"({share:.1f}% of total revenue)."
            ),
        })
    
    # 2. Best month
    if "year_month" in df.columns:
        monthly = df.groupby("year_month")["revenue"].sum()
        best_month = monthly.idxmax()
        best_month_val = monthly.max()
        insights.append({
            "title": "📈 Strongest Month",
            "description": (
                f"**{best_month}** recorded the highest monthly revenue "
                f"at {format_inr_short(best_month_val)}."
            ),
        })
    
    # 3. Top state
    if "state" in df.columns:
        state_rev = df.groupby("state")["revenue"].sum()
        top_state = state_rev.idxmax()
        top_state_val = state_rev.max()
        insights.append({
            "title": "🗺️ Leading State",
            "description": (
                f"**{top_state}** is the top-performing state with "
                f"{format_inr_short(top_state_val)} in revenue."
            ),
        })
    
    # 4. High quantity, low revenue categories
    if "category" in df.columns:
        cat_data = df.groupby("category").agg(
            revenue=("revenue", "sum"), quantity=("quantity", "sum")
        )
        cat_data["revenue_per_unit"] = cat_data["revenue"] / cat_data["quantity"]
        lowest_rpu = cat_data["revenue_per_unit"].idxmin()
        highest_rpu = cat_data["revenue_per_unit"].idxmax()
        insights.append({
            "title": "💡 Revenue per Unit Variation",
            "description": (
                f"**{lowest_rpu}** has the lowest revenue per unit "
                f"({format_inr(cat_data.loc[lowest_rpu, 'revenue_per_unit'])}), "
                f"while **{highest_rpu}** has the highest "
                f"({format_inr(cat_data.loc[highest_rpu, 'revenue_per_unit'])})."
            ),
        })
    
    # 5. Return rate insight
    if "order_status" in df.columns:
        ret_info = return_analysis(df)
        if ret_info["available"]:
            insights.append({
                "title": "🔄 Return & Cancellation Rates",
                "description": (
                    f"Return rate: **{ret_info['return_rate']}%** | "
                    f"Cancellation rate: **{ret_info['cancellation_rate']}%** "
                    f"(out of {ret_info['total_orders']:,} distinct orders)."
                ),
            })
    
    # 6. Payment method
    if "payment_method" in df.columns:
        pay_counts = df.groupby("payment_method")["order_id"].nunique()
        top_pay = pay_counts.idxmax()
        top_pay_share = safe_divide(pay_counts.max(), pay_counts.sum()) * 100
        insights.append({
            "title": "💳 Preferred Payment Method",
            "description": (
                f"**{top_pay}** is the most popular payment method, "
                f"used in {top_pay_share:.1f}% of orders."
            ),
        })
    
    # 7. Average order value
    aov = average_order_value(df)
    insights.append({
        "title": "🛒 Average Order Value",
        "description": f"The average order value is **{format_inr(aov)}**.",
    })
    
    return insights
