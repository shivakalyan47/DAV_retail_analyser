"""
Visualization Module for Indian Retail Analytics.

Creates interactive Plotly charts and static Matplotlib/Seaborn charts.
All functions return Plotly figure objects for dashboard integration.
"""
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# Consistent color scheme
COLORS = {
    "primary": "#1f77b4",
    "secondary": "#ff7f0e",
    "success": "#2ca02c",
    "danger": "#d62728",
    "warning": "#ffbb33",
    "info": "#17a2b8",
    "palette": px.colors.qualitative.Set2,
}

CHART_TEMPLATE = "plotly_white"
CHART_HEIGHT = 450


def _apply_common_layout(fig, title: str = "", height: int = CHART_HEIGHT):
    """Apply consistent layout to all charts."""
    fig.update_layout(
        title=dict(text=title, font=dict(size=16)),
        template=CHART_TEMPLATE,
        height=height,
        margin=dict(l=40, r=40, t=60, b=40),
        font=dict(family="Segoe UI, Arial, sans-serif", size=12),
        hoverlabel=dict(bgcolor="white", font_size=12),
    )
    return fig


def monthly_revenue_chart(df: pd.DataFrame) -> go.Figure:
    """Line chart showing monthly revenue trend."""
    if df.empty or "year_month" not in df.columns:
        fig = go.Figure()
        fig.add_annotation(text="No data available", xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False, font=dict(size=16))
        return _apply_common_layout(fig, "Monthly Revenue Trend")
    
    monthly = df.groupby("year_month").agg(
        revenue=("revenue", "sum"),
        orders=("order_id", "nunique"),
    ).reset_index().sort_values("year_month")
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly["year_month"],
        y=monthly["revenue"],
        mode="lines+markers",
        name="Revenue",
        line=dict(color=COLORS["primary"], width=2),
        marker=dict(size=6),
        hovertemplate="<b>%{x}</b><br>Revenue: ₹%{y:,.0f}<br><extra></extra>",
    ))
    
    fig = _apply_common_layout(fig, "Monthly Revenue Trend")
    fig.update_xaxes(title_text="Month", tickangle=-45)
    fig.update_yaxes(title_text="Revenue (₹)")
    
    return fig


def category_revenue_chart(df: pd.DataFrame) -> go.Figure:
    """Bar chart showing revenue by product category."""
    if df.empty or "category" not in df.columns:
        fig = go.Figure()
        fig.add_annotation(text="No data available", xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False, font=dict(size=16))
        return _apply_common_layout(fig, "Revenue by Category")
    
    cat_data = df.groupby("category")["revenue"].sum().reset_index()
    cat_data = cat_data.sort_values("revenue", ascending=True)
    
    fig = go.Figure(go.Bar(
        x=cat_data["revenue"],
        y=cat_data["category"],
        orientation="h",
        marker_color=COLORS["palette"][:len(cat_data)],
        hovertemplate="<b>%{y}</b><br>Revenue: ₹%{x:,.0f}<extra></extra>",
    ))
    
    fig = _apply_common_layout(fig, "Revenue by Product Category")
    fig.update_xaxes(title_text="Revenue (₹)")
    fig.update_yaxes(title_text="")
    
    return fig


def top_products_revenue_chart(df: pd.DataFrame, top_n: int = 10) -> go.Figure:
    """Horizontal bar chart for top N products by revenue."""
    if df.empty or "product_name" not in df.columns:
        fig = go.Figure()
        fig.add_annotation(text="No data available", xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False, font=dict(size=16))
        return _apply_common_layout(fig, f"Top {top_n} Products by Revenue")
    
    prod_data = df.groupby("product_name")["revenue"].sum().reset_index()
    prod_data = prod_data.sort_values("revenue", ascending=False).head(top_n)
    prod_data = prod_data.sort_values("revenue", ascending=True)  # For horizontal bar
    
    fig = go.Figure(go.Bar(
        x=prod_data["revenue"],
        y=prod_data["product_name"],
        orientation="h",
        marker_color=COLORS["primary"],
        hovertemplate="<b>%{y}</b><br>Revenue: ₹%{x:,.0f}<extra></extra>",
    ))
    
    fig = _apply_common_layout(fig, f"Top {top_n} Products by Revenue", height=max(400, top_n * 35))
    fig.update_xaxes(title_text="Revenue (₹)")
    fig.update_yaxes(title_text="")
    
    return fig


def top_products_quantity_chart(df: pd.DataFrame, top_n: int = 10) -> go.Figure:
    """Horizontal bar chart for top N products by quantity sold."""
    if df.empty or "product_name" not in df.columns:
        fig = go.Figure()
        fig.add_annotation(text="No data available", xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False, font=dict(size=16))
        return _apply_common_layout(fig, f"Top {top_n} Products by Quantity")
    
    prod_data = df.groupby("product_name")["quantity"].sum().reset_index()
    prod_data = prod_data.sort_values("quantity", ascending=False).head(top_n)
    prod_data = prod_data.sort_values("quantity", ascending=True)
    
    fig = go.Figure(go.Bar(
        x=prod_data["quantity"],
        y=prod_data["product_name"],
        orientation="h",
        marker_color=COLORS["secondary"],
        hovertemplate="<b>%{y}</b><br>Quantity: %{x:,}<extra></extra>",
    ))
    
    fig = _apply_common_layout(fig, f"Top {top_n} Products by Quantity Sold", height=max(400, top_n * 35))
    fig.update_xaxes(title_text="Quantity Sold")
    fig.update_yaxes(title_text="")
    
    return fig


def state_revenue_chart(df: pd.DataFrame) -> go.Figure:
    """Horizontal bar chart for state-wise revenue."""
    if df.empty or "state" not in df.columns:
        fig = go.Figure()
        fig.add_annotation(text="No data available", xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False, font=dict(size=16))
        return _apply_common_layout(fig, "State-wise Revenue")
    
    state_data = df.groupby("state")["revenue"].sum().reset_index()
    state_data = state_data.sort_values("revenue", ascending=True)
    
    fig = go.Figure(go.Bar(
        x=state_data["revenue"],
        y=state_data["state"],
        orientation="h",
        marker_color=COLORS["info"],
        hovertemplate="<b>%{y}</b><br>Revenue: ₹%{x:,.0f}<extra></extra>",
    ))
    
    fig = _apply_common_layout(fig, "State-wise Revenue", height=max(500, len(state_data) * 25))
    fig.update_xaxes(title_text="Revenue (₹)")
    fig.update_yaxes(title_text="")
    
    return fig


def city_revenue_chart(df: pd.DataFrame, top_n: int = 15) -> go.Figure:
    """Horizontal bar chart for top cities by revenue."""
    if df.empty or "city" not in df.columns:
        fig = go.Figure()
        fig.add_annotation(text="No data available", xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False, font=dict(size=16))
        return _apply_common_layout(fig, f"Top {top_n} Cities by Revenue")
    
    city_data = df.groupby("city")["revenue"].sum().reset_index()
    city_data = city_data.sort_values("revenue", ascending=False).head(top_n)
    city_data = city_data.sort_values("revenue", ascending=True)
    
    fig = go.Figure(go.Bar(
        x=city_data["revenue"],
        y=city_data["city"],
        orientation="h",
        marker_color=COLORS["success"],
        hovertemplate="<b>%{y}</b><br>Revenue: ₹%{x:,.0f}<extra></extra>",
    ))
    
    fig = _apply_common_layout(fig, f"Top {top_n} Cities by Revenue", height=max(400, top_n * 30))
    fig.update_xaxes(title_text="Revenue (₹)")
    fig.update_yaxes(title_text="")
    
    return fig


def quantity_vs_revenue_scatter(df: pd.DataFrame) -> go.Figure:
    """Scatter plot of quantity vs revenue, colored by category."""
    if df.empty or not all(c in df.columns for c in ["quantity", "revenue"]):
        fig = go.Figure()
        fig.add_annotation(text="No data available", xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False, font=dict(size=16))
        return _apply_common_layout(fig, "Quantity vs Revenue")
    
    # Aggregate by product to avoid too many points
    agg_col = "product_name" if "product_name" in df.columns else "order_id"
    color_col = "category" if "category" in df.columns else None
    
    prod_data = df.groupby([agg_col] + ([color_col] if color_col else [])).agg(
        quantity=("quantity", "sum"),
        revenue=("revenue", "sum"),
    ).reset_index()
    
    fig = px.scatter(
        prod_data, x="quantity", y="revenue",
        color=color_col,
        hover_name=agg_col,
        color_discrete_sequence=COLORS["palette"],
        labels={"quantity": "Total Quantity Sold", "revenue": "Total Revenue (₹)"},
    )
    
    fig = _apply_common_layout(fig, "Quantity vs Revenue by Product")
    
    return fig


def revenue_profit_chart(df: pd.DataFrame) -> go.Figure:
    """Bar chart comparing revenue and profit by category."""
    if df.empty or "profit" not in df.columns or "category" not in df.columns:
        fig = go.Figure()
        fig.add_annotation(text="Profit data not available", xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False, font=dict(size=16))
        return _apply_common_layout(fig, "Revenue vs Profit by Category")
    
    cat_data = df.groupby("category").agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum"),
    ).reset_index().sort_values("revenue", ascending=False)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=cat_data["category"], y=cat_data["revenue"],
        name="Revenue", marker_color=COLORS["primary"],
        hovertemplate="<b>%{x}</b><br>Revenue: ₹%{y:,.0f}<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        x=cat_data["category"], y=cat_data["profit"],
        name="Profit", marker_color=COLORS["success"],
        hovertemplate="<b>%{x}</b><br>Profit: ₹%{y:,.0f}<extra></extra>",
    ))
    
    fig.update_layout(barmode="group")
    fig = _apply_common_layout(fig, "Revenue vs Profit by Category")
    fig.update_xaxes(title_text="Category")
    fig.update_yaxes(title_text="Amount (₹)")
    
    return fig


def sales_distribution_histogram(df: pd.DataFrame) -> go.Figure:
    """Histogram of sales amount distribution."""
    if df.empty or "revenue" not in df.columns:
        fig = go.Figure()
        fig.add_annotation(text="No data available", xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False, font=dict(size=16))
        return _apply_common_layout(fig, "Sales Amount Distribution")
    
    fig = px.histogram(
        df, x="revenue", nbins=50,
        color_discrete_sequence=[COLORS["primary"]],
        labels={"revenue": "Sales Amount (₹)", "count": "Number of Transactions"},
    )
    
    fig = _apply_common_layout(fig, "Sales Amount Distribution")
    fig.update_xaxes(title_text="Sales Amount (₹)")
    fig.update_yaxes(title_text="Number of Transactions")
    
    return fig


def correlation_heatmap(df: pd.DataFrame) -> go.Figure:
    """Correlation heatmap for numeric columns."""
    numeric_cols = ["quantity", "unit_price", "discount_percent", "sales_amount",
                    "revenue", "profit", "shipping_cost"]
    available = [c for c in numeric_cols if c in df.columns]
    
    if len(available) < 2:
        fig = go.Figure()
        fig.add_annotation(text="Insufficient numeric data", xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False, font=dict(size=16))
        return _apply_common_layout(fig, "Correlation Heatmap")
    
    corr = df[available].corr()
    
    fig = go.Figure(go.Heatmap(
        z=corr.values,
        x=corr.columns,
        y=corr.columns,
        colorscale="RdBu_r",
        zmin=-1, zmax=1,
        text=corr.values.round(2),
        texttemplate="%{text}",
        hovertemplate="<b>%{x} × %{y}</b><br>Correlation: %{z:.3f}<extra></extra>",
    ))
    
    fig = _apply_common_layout(fig, "Correlation Heatmap (Numeric Fields)", height=500)
    
    return fig


def payment_method_chart(df: pd.DataFrame) -> go.Figure:
    """Pie chart for payment method distribution."""
    if df.empty or "payment_method" not in df.columns:
        fig = go.Figure()
        fig.add_annotation(text="Payment data not available", xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False, font=dict(size=16))
        return _apply_common_layout(fig, "Payment Method Distribution")
    
    pay_data = df.groupby("payment_method")["order_id"].nunique().reset_index()
    pay_data.columns = ["payment_method", "order_count"]
    
    fig = px.pie(
        pay_data, values="order_count", names="payment_method",
        color_discrete_sequence=COLORS["palette"],
        hole=0.4,
    )
    
    fig.update_traces(
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>Orders: %{value:,}<br>Share: %{percent}<extra></extra>",
    )
    
    fig = _apply_common_layout(fig, "Payment Method Distribution (by Order Count)")
    
    return fig


def order_status_chart(df: pd.DataFrame) -> go.Figure:
    """Donut chart for order status distribution."""
    if df.empty or "order_status" not in df.columns:
        fig = go.Figure()
        fig.add_annotation(text="Order status data not available", xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False, font=dict(size=16))
        return _apply_common_layout(fig, "Order Status Distribution")
    
    status_data = df.groupby("order_status")["order_id"].nunique().reset_index()
    status_data.columns = ["order_status", "order_count"]
    
    color_map = {
        "Delivered": COLORS["success"],
        "Returned": COLORS["danger"],
        "Cancelled": COLORS["warning"],
        "Processing": COLORS["info"],
    }
    colors = [color_map.get(s, COLORS["primary"]) for s in status_data["order_status"]]
    
    fig = go.Figure(go.Pie(
        labels=status_data["order_status"],
        values=status_data["order_count"],
        hole=0.4,
        marker_colors=colors,
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>Orders: %{value:,}<br>Share: %{percent}<extra></extra>",
    ))
    
    fig = _apply_common_layout(fig, "Order Status Distribution")
    
    return fig


def discount_impact_chart(df: pd.DataFrame) -> go.Figure:
    """Bar chart showing revenue by discount bracket."""
    if df.empty or "discount_percent" not in df.columns:
        fig = go.Figure()
        fig.add_annotation(text="Discount data not available", xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False, font=dict(size=16))
        return _apply_common_layout(fig, "Discount Impact on Revenue")
    
    df_copy = df.copy()
    bins = [0, 0.01, 5, 10, 15, 20, 25, 100]
    labels = ["No Discount", "1-5%", "6-10%", "11-15%", "16-20%", "21-25%", "26%+"]
    df_copy["discount_bracket"] = pd.cut(
        df_copy["discount_percent"], bins=bins, labels=labels, include_lowest=True
    )
    
    disc_data = df_copy.groupby("discount_bracket", observed=True).agg(
        revenue=("revenue", "sum"),
        order_count=("order_id", "nunique"),
    ).reset_index()
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=disc_data["discount_bracket"].astype(str),
        y=disc_data["revenue"],
        name="Revenue",
        marker_color=COLORS["primary"],
        hovertemplate="<b>%{x}</b><br>Revenue: ₹%{y:,.0f}<extra></extra>",
    ))
    
    fig = _apply_common_layout(fig, "Discount Impact on Revenue")
    fig.update_xaxes(title_text="Discount Bracket")
    fig.update_yaxes(title_text="Revenue (₹)")
    
    return fig


def segment_revenue_chart(df: pd.DataFrame) -> go.Figure:
    """Bar chart for revenue by customer segment."""
    if df.empty or "customer_segment" not in df.columns:
        fig = go.Figure()
        fig.add_annotation(text="Segment data not available", xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False, font=dict(size=16))
        return _apply_common_layout(fig, "Revenue by Customer Segment")
    
    seg_data = df.groupby("customer_segment")["revenue"].sum().reset_index()
    seg_data = seg_data.sort_values("revenue", ascending=True)
    
    fig = go.Figure(go.Bar(
        x=seg_data["revenue"],
        y=seg_data["customer_segment"],
        orientation="h",
        marker_color=COLORS["palette"][:len(seg_data)],
        hovertemplate="<b>%{y}</b><br>Revenue: ₹%{x:,.0f}<extra></extra>",
    ))
    
    fig = _apply_common_layout(fig, "Revenue by Customer Segment")
    fig.update_xaxes(title_text="Revenue (₹)")
    fig.update_yaxes(title_text="")
    
    return fig


def monthly_orders_chart(df: pd.DataFrame) -> go.Figure:
    """Bar chart showing monthly order counts."""
    if df.empty or "year_month" not in df.columns:
        fig = go.Figure()
        fig.add_annotation(text="No data available", xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False, font=dict(size=16))
        return _apply_common_layout(fig, "Monthly Order Count")
    
    monthly = df.groupby("year_month")["order_id"].nunique().reset_index()
    monthly.columns = ["year_month", "order_count"]
    monthly = monthly.sort_values("year_month")
    
    fig = go.Figure(go.Bar(
        x=monthly["year_month"],
        y=monthly["order_count"],
        marker_color=COLORS["secondary"],
        hovertemplate="<b>%{x}</b><br>Orders: %{y:,}<extra></extra>",
    ))
    
    fig = _apply_common_layout(fig, "Monthly Order Count")
    fig.update_xaxes(title_text="Month", tickangle=-45)
    fig.update_yaxes(title_text="Number of Orders")
    
    return fig


def quarterly_revenue_chart(df: pd.DataFrame) -> go.Figure:
    """Grouped bar chart for quarterly revenue by year."""
    if df.empty or "quarter" not in df.columns or "year" not in df.columns:
        fig = go.Figure()
        fig.add_annotation(text="No data available", xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False, font=dict(size=16))
        return _apply_common_layout(fig, "Quarterly Revenue")
    
    quarterly = df.groupby(["year", "quarter"])["revenue"].sum().reset_index()
    quarterly["quarter_label"] = "Q" + quarterly["quarter"].astype(str)
    
    fig = px.bar(
        quarterly, x="quarter_label", y="revenue",
        color="year", barmode="group",
        color_discrete_sequence=COLORS["palette"],
        labels={"quarter_label": "Quarter", "revenue": "Revenue (₹)", "year": "Year"},
    )
    
    fig = _apply_common_layout(fig, "Quarterly Revenue Comparison")
    fig.update_xaxes(title_text="Quarter")
    fig.update_yaxes(title_text="Revenue (₹)")
    
    return fig
