"""
Indian Retail Analytics Dashboard
==================================
An interactive Streamlit dashboard for analyzing retail sales and revenue data.
Supports built-in datasets and custom CSV file uploads.

Course: Data Analytics and Visualization (DAV) Lab AAT
"""
import os
import sys
import streamlit as st
import pandas as pd
import numpy as np

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import APP_TITLE, APP_ICON, DATASET_INFO, DEFAULT_TOP_N, CURRENCY_SYMBOL
from src.data_loader import load_data_cached, validate_required_columns
from src.preprocessing import clean_data, detect_missing_values
from src.metrics import (
    total_revenue, total_orders, total_units_sold, average_order_value,
    monthly_revenue, revenue_by_category, revenue_by_product, quantity_by_product,
    revenue_by_state, revenue_by_city, payment_method_analysis, customer_summary,
    repeat_customer_rate, return_analysis, profit_analysis, discount_analysis,
    segment_analysis, generate_insights, format_inr, format_inr_short,
)
from src.visualizations import (
    monthly_revenue_chart, category_revenue_chart, top_products_revenue_chart,
    top_products_quantity_chart, state_revenue_chart, city_revenue_chart,
    quantity_vs_revenue_scatter, revenue_profit_chart, sales_distribution_histogram,
    correlation_heatmap, payment_method_chart, order_status_chart,
    discount_impact_chart, segment_revenue_chart,
)

# --- Page Configuration ---
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Custom CSS for KPI cards and styling ---
st.markdown("""
<style>
    /* KPI Card Styling */
    .kpi-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 12px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 10px;
    }
    .kpi-card h3 {
        font-size: 14px;
        font-weight: 400;
        margin: 0 0 8px 0;
        opacity: 0.9;
    }
    .kpi-card h2 {
        font-size: 28px;
        font-weight: 700;
        margin: 0;
    }
    .kpi-card-green {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    }
    .kpi-card-blue {
        background: linear-gradient(135deg, #2193b0 0%, #6dd5ed 100%);
    }
    .kpi-card-orange {
        background: linear-gradient(135deg, #f7971e 0%, #ffd200 100%);
    }
    .kpi-card-red {
        background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
    }
    
    /* Insight card */
    .insight-card {
        background: rgba(102, 126, 234, 0.12);
        border: 1px solid rgba(102, 126, 234, 0.28);
        border-left: 5px solid #667eea;
        padding: 16px 20px;
        margin-bottom: 14px;
        border-radius: 10px;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .insight-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.12);
    }
    .insight-title {
        font-size: 15px;
        font-weight: 700;
        margin-bottom: 8px;
        display: block;
    }
    .insight-body {
        font-size: 14px;
        line-height: 1.55;
        opacity: 0.95;
    }
    
    /* Upload banner */
    .upload-banner {
        background-color: #e8f4fd;
        border: 1px solid #b6e0fe;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 15px;
        font-size: 14px;
        color: #0c5460;
    }
    
    /* Section headers */
    .section-header {
        border-bottom: 2px solid #667eea;
        padding-bottom: 8px;
        margin-bottom: 16px;
    }
    
    /* Hide Streamlit footer */
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


def render_kpi_card(title: str, value: str, css_class: str = ""):
    """Render a styled KPI metric card."""
    st.markdown(f"""
    <div class="kpi-card {css_class}">
        <h3>{title}</h3>
        <h2>{value}</h2>
    </div>
    """, unsafe_allow_html=True)


# --- Load Data ---
@st.cache_data(show_spinner="Loading dataset...")
def get_data():
    """Load and cache the default cleaned dataset."""
    try:
        df = load_data_cached()
        return df, None
    except FileNotFoundError as e:
        return None, str(e)
    except Exception as e:
        return None, f"Error loading data: {str(e)}"


def read_csv_robust(uploaded_file):
    """
    Read CSV file with automatic fallback for multiple encodings.
    Handles UTF-8, Latin-1, Windows-1252, UTF-8-SIG, and non-breaking spaces (0xa0).
    """
    encodings_to_try = ["utf-8", "latin1", "cp1252", "iso-8859-1", "utf-8-sig"]
    
    # 1. Try standard encodings
    for enc in encodings_to_try:
        try:
            uploaded_file.seek(0)
            df = pd.read_csv(uploaded_file, encoding=enc)
            # If comma wasn't the delimiter (only 1 column found), try auto-detecting separator
            if len(df.columns) == 1 and len(df) > 0:
                try:
                    uploaded_file.seek(0)
                    df_auto = pd.read_csv(uploaded_file, encoding=enc, sep=None, engine="python")
                    if len(df_auto.columns) > 1:
                        df = df_auto
                except Exception:
                    pass
            return df
        except (UnicodeDecodeError, UnicodeError):
            continue
        except Exception:
            continue
            
    # 2. Fallback: latin-1 always decodes any byte stream (0x00 to 0xFF)
    try:
        uploaded_file.seek(0)
        return pd.read_csv(uploaded_file, encoding="latin1")
    except Exception:
        # 3. Ultimate fallback: utf-8 with error replacement
        uploaded_file.seek(0)
        return pd.read_csv(uploaded_file, encoding="utf-8", encoding_errors="replace")


def process_uploaded_file(uploaded_file):
    """Read and automatically clean an uploaded custom CSV file."""
    try:
        raw_df = read_csv_robust(uploaded_file)
        if raw_df is None or raw_df.empty:
            return None, None, "Uploaded CSV file is empty."
        cleaned_df, quality_report = clean_data(raw_df)
        return cleaned_df, quality_report, None
    except Exception as e:
        return None, None, f"Failed to process CSV: {str(e)}"


def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    """Apply sidebar filters to the dataframe."""
    st.sidebar.markdown("---")
    st.sidebar.header("🔍 Filters")
    
    filtered = df.copy()
    
    # Date range filter
    if "order_date" in df.columns:
        valid_dates = pd.to_datetime(df["order_date"], errors="coerce").dropna()
        if not valid_dates.empty:
            min_date = valid_dates.min().date()
            max_date = valid_dates.max().date()
            if min_date <= max_date:
                date_range = st.sidebar.date_input(
                    "📅 Date Range",
                    value=(min_date, max_date),
                    min_value=min_date,
                    max_value=max_date,
                )
                if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
                    start_date, end_date = date_range
                    order_dates = pd.to_datetime(filtered["order_date"], errors="coerce").dt.date
                    filtered = filtered[(order_dates >= start_date) & (order_dates <= end_date)]
    
    # State filter
    if "state" in df.columns:
        states = sorted(df["state"].dropna().unique().tolist())
        selected_states = st.sidebar.multiselect("🗺️ State", states, default=[])
        if selected_states:
            filtered = filtered[filtered["state"].isin(selected_states)]
    
    # Category filter
    if "category" in df.columns:
        categories = sorted(df["category"].dropna().unique().tolist())
        selected_cats = st.sidebar.multiselect("📦 Category", categories, default=[])
        if selected_cats:
            filtered = filtered[filtered["category"].isin(selected_cats)]
    
    # Product filter (only show if category is filtered to keep list manageable)
    if "product_name" in df.columns:
        available_products = sorted(filtered["product_name"].dropna().unique().tolist())
        selected_products = st.sidebar.multiselect("🏷️ Product", available_products, default=[])
        if selected_products:
            filtered = filtered[filtered["product_name"].isin(selected_products)]
    
    # Customer segment filter
    if "customer_segment" in df.columns:
        segments = sorted(df["customer_segment"].dropna().unique().tolist())
        selected_segs = st.sidebar.multiselect("👥 Customer Segment", segments, default=[])
        if selected_segs:
            filtered = filtered[filtered["customer_segment"].isin(selected_segs)]
    
    # Payment method filter
    if "payment_method" in df.columns:
        methods = sorted(df["payment_method"].dropna().unique().tolist())
        selected_methods = st.sidebar.multiselect("💳 Payment Method", methods, default=[])
        if selected_methods:
            filtered = filtered[filtered["payment_method"].isin(selected_methods)]
    
    # Order status filter
    if "order_status" in df.columns:
        statuses = sorted(df["order_status"].dropna().unique().tolist())
        selected_statuses = st.sidebar.multiselect("📋 Order Status", statuses, default=[])
        if selected_statuses:
            filtered = filtered[filtered["order_status"].isin(selected_statuses)]
    
    # Reset filters button
    st.sidebar.markdown("---")
    if st.sidebar.button("🔄 Reset All Filters"):
        st.rerun()
    
    # Show filter summary
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Showing:** {len(filtered):,} of {len(df):,} records")
    
    return filtered


def page_overview(df: pd.DataFrame):
    """Page 1: Executive Overview"""
    st.markdown('<h2 class="section-header">📊 Executive Overview</h2>', unsafe_allow_html=True)
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi_card("Total Revenue", format_inr_short(total_revenue(df)), "")
    with col2:
        render_kpi_card("Distinct Orders", f"{total_orders(df):,}", "kpi-card-green")
    with col3:
        render_kpi_card("Units Sold", f"{total_units_sold(df):,}", "kpi-card-blue")
    with col4:
        render_kpi_card("Avg Order Value", format_inr(average_order_value(df)), "kpi-card-orange")
    
    st.markdown("")
    
    # Charts Row 1
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(monthly_revenue_chart(df), use_container_width=True)
    with col2:
        st.plotly_chart(category_revenue_chart(df), use_container_width=True)
    
    # Charts Row 2
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(top_products_revenue_chart(df, DEFAULT_TOP_N), use_container_width=True)
    with col2:
        if "profit" in df.columns and df["profit"].notna().any():
            st.plotly_chart(revenue_profit_chart(df), use_container_width=True)
        else:
            st.plotly_chart(sales_distribution_histogram(df), use_container_width=True)
    
    # Data-derived insights
    st.markdown('<h3 class="section-header">💡 Key Insights</h3>', unsafe_allow_html=True)
    insights = generate_insights(df)
    
    cols = st.columns(2)
    for i, insight in enumerate(insights):
        with cols[i % 2]:
            desc = insight['description']
            while '**' in desc:
                desc = desc.replace('**', '<b>', 1).replace('**', '</b>', 1)
            st.markdown(f"""
            <div class="insight-card">
                <span class="insight-title">{insight['title']}</span>
                <span class="insight-body">{desc}</span>
            </div>
            """, unsafe_allow_html=True)


def page_products(df: pd.DataFrame):
    """Page 2: Product Analytics"""
    st.markdown('<h2 class="section-header">🏷️ Product Analytics</h2>', unsafe_allow_html=True)
    
    # Top N selector
    top_n = st.slider("Select Top N Products", min_value=5, max_value=30, value=DEFAULT_TOP_N, step=5)
    
    # Charts Row 1
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(top_products_revenue_chart(df, top_n), use_container_width=True)
    with col2:
        st.plotly_chart(top_products_quantity_chart(df, top_n), use_container_width=True)
    
    # Category comparison
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(category_revenue_chart(df), use_container_width=True)
    with col2:
        st.plotly_chart(quantity_vs_revenue_scatter(df), use_container_width=True)
    
    # Revenue contribution by category (table)
    st.markdown("### 📋 Category-wise Summary")
    cat_data = revenue_by_category(df)
    if not cat_data.empty:
        total_rev = cat_data["revenue"].sum()
        cat_data["revenue_share_%"] = (cat_data["revenue"] / total_rev * 100).round(2) if total_rev > 0 else 0.0
        cat_data["avg_revenue_per_order"] = (cat_data["revenue"] / cat_data["order_count"].replace(0, 1)).round(2)
        st.dataframe(
            cat_data.style.format({
                "revenue": "₹{:,.0f}",
                "avg_revenue_per_order": "₹{:,.0f}",
                "revenue_share_%": "{:.1f}%",
            }),
            use_container_width=True,
            hide_index=True,
        )
    
    # Product-level summary table
    st.markdown("### 📋 Product-level Summary")
    prod_data = revenue_by_product(df, top_n=None)
    if not prod_data.empty:
        st.dataframe(
            prod_data.head(50).style.format({
                "revenue": "₹{:,.0f}",
            }),
            use_container_width=True,
            hide_index=True,
        )
    
    # Discount analysis
    if "discount_percent" in df.columns:
        st.markdown("### 🏷️ Discount Impact Analysis")
        st.plotly_chart(discount_impact_chart(df), use_container_width=True)


def page_regional(df: pd.DataFrame):
    """Page 3: Regional Analytics"""
    st.markdown('<h2 class="section-header">🗺️ Regional Analytics</h2>', unsafe_allow_html=True)
    
    # State-wise revenue
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(state_revenue_chart(df), use_container_width=True)
    with col2:
        st.plotly_chart(city_revenue_chart(df, 15), use_container_width=True)
    
    # State summary table
    st.markdown("### 📋 State-wise Summary")
    state_data = revenue_by_state(df)
    if not state_data.empty:
        total_rev = state_data["revenue"].sum()
        state_data["revenue_share_%"] = (state_data["revenue"] / total_rev * 100).round(2) if total_rev > 0 else 0.0
        state_data["avg_revenue_per_order"] = (state_data["revenue"] / state_data["order_count"].replace(0, 1)).round(2)
        st.dataframe(
            state_data.style.format({
                "revenue": "₹{:,.0f}",
                "avg_revenue_per_order": "₹{:,.0f}",
                "revenue_share_%": "{:.1f}%",
            }),
            use_container_width=True,
            hide_index=True,
        )
    
    # City summary table
    st.markdown("### 📋 City-wise Summary (Top 20)")
    city_data = revenue_by_city(df, top_n=20)
    if not city_data.empty:
        st.dataframe(
            city_data.style.format({
                "revenue": "₹{:,.0f}",
            }),
            use_container_width=True,
            hide_index=True,
        )


def page_customers(df: pd.DataFrame):
    """Page 4: Customer & Returns Analytics"""
    st.markdown('<h2 class="section-header">👥 Customer & Returns Analytics</h2>', unsafe_allow_html=True)
    
    # Customer metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 👥 Customer Overview")
        repeat_info = repeat_customer_rate(df)
        if repeat_info["total_customers"] > 0:
            c1, c2 = st.columns(2)
            with c1:
                render_kpi_card("Total Customers", f"{repeat_info['total_customers']:,}", "kpi-card-blue")
            with c2:
                render_kpi_card("Repeat Rate", f"{repeat_info['repeat_rate']}%", "kpi-card-green")
            
            st.markdown(f"""
            - **Repeat Customers:** {repeat_info['repeat_customers']:,}
            - **Single-Purchase Customers:** {repeat_info['single_purchase']:,}
            - *Repeat customer = placed more than 1 distinct order*
            """)
        else:
            st.info("Customer identifier not available in this dataset.")
    
    with col2:
        st.markdown("### 📦 Order Status & Returns")
        ret_info = return_analysis(df)
        if ret_info.get("available"):
            c1, c2 = st.columns(2)
            with c1:
                render_kpi_card("Return Rate", f"{ret_info['return_rate']}%", "kpi-card-red")
            with c2:
                render_kpi_card("Cancel Rate", f"{ret_info['cancellation_rate']}%", "kpi-card-orange")
            
            st.markdown(f"""
            - **Delivered:** {ret_info['delivered']:,} orders
            - **Returned:** {ret_info['returned']:,} orders
            - **Cancelled:** {ret_info['cancelled']:,} orders
            - **Processing:** {ret_info['processing']:,} orders
            - *Rates calculated as: count / total distinct orders × 100*
            """)
        else:
            st.info("Order status field not available in this dataset.")
    
    # Charts
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(order_status_chart(df), use_container_width=True)
    with col2:
        st.plotly_chart(payment_method_chart(df), use_container_width=True)
    
    # Customer segment analysis
    if "customer_segment" in df.columns:
        st.markdown("### 🎯 Customer Segment Analysis")
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(segment_revenue_chart(df), use_container_width=True)
        with col2:
            seg_data = segment_analysis(df)
            if not seg_data.empty:
                st.dataframe(
                    seg_data.style.format({"revenue": "₹{:,.0f}"}),
                    use_container_width=True,
                    hide_index=True,
                )
    
    # Top customers table (aggregated)
    st.markdown("### 🏆 Top Customers by Revenue (Aggregated)")
    st.caption("Customer transactions aggregated by Customer ID.")
    cust_data = customer_summary(df, top_n=20)
    if not cust_data.empty:
        display_cols = [c for c in ["customer_id", "total_revenue", "total_orders", 
                                     "total_quantity", "avg_order_value"] if c in cust_data.columns]
        st.dataframe(
            cust_data[display_cols].style.format({
                "total_revenue": "₹{:,.0f}",
                "avg_order_value": "₹{:,.0f}",
            }),
            use_container_width=True,
            hide_index=True,
        )
    
    # Profit analysis
    if "profit" in df.columns:
        st.markdown("### 💰 Profit Analysis")
        profit_info = profit_analysis(df)
        if profit_info.get("available"):
            col1, col2, col3 = st.columns(3)
            with col1:
                render_kpi_card("Total Profit", format_inr_short(profit_info["total_profit"]), "kpi-card-green")
            with col2:
                render_kpi_card("Profit Margin", f"{profit_info['profit_margin']}%", "kpi-card-blue")
            with col3:
                render_kpi_card("Loss Transactions", f"{profit_info['loss_making_transactions']:,}", "kpi-card-red")
            
            st.plotly_chart(revenue_profit_chart(df), use_container_width=True)


def page_data_quality(df: pd.DataFrame, active_name: str = "", is_custom: bool = False, quality_report: dict = None):
    """Page 5: Data Quality & Methodology"""
    st.markdown('<h2 class="section-header">🔍 Data Quality & Methodology</h2>', unsafe_allow_html=True)
    
    # Active Dataset Provenance
    st.markdown("### 📋 Active Dataset Details")
    if is_custom:
        st.markdown(f"""
        | Property | Value |
        |----------|-------|
        | **Active Dataset** | **{active_name}** |
        | **Dataset Mode** | User-Uploaded Custom CSV |
        | **Cleaning Status** | Standardized, Cleansed & Imputed In-Memory |
        """)
    else:
        st.markdown(f"""
        | Property | Value |
        |----------|-------|
        | **Dataset Name** | {DATASET_INFO.get('name', 'N/A')} |
        | **Data Type** | {DATASET_INFO.get('type', 'N/A')} |
        | **Source** | {DATASET_INFO.get('source', 'N/A')} |
        | **License** | {DATASET_INFO.get('licence', 'N/A')} |
        | **Access Date** | {DATASET_INFO.get('access_date', 'N/A')} |
        """)
        st.info(DATASET_INFO.get("description", "Indian retail transaction dataset."))
    
    # Upload Custom CSV section right on this page
    st.markdown("---")
    st.markdown("### 📤 Upload Another Custom CSV Dataset")
    st.markdown("You can upload any Indian retail or e-commerce transaction CSV. The system automatically standardizes column headers, prunes corrupt dates/negative quantities, and recalculates KPIs.")
    
    inpage_file = st.file_uploader(
        "Upload a retail CSV file to replace current data:",
        type=["csv"],
        key="data_quality_uploader",
        help="Upload any compatible CSV containing sales, products, and prices."
    )
    if inpage_file is not None:
        if st.session_state.get("uploaded_filename") != inpage_file.name:
            with st.spinner("Processing & standardizing custom CSV..."):
                clean_custom, quality, err = process_uploaded_file(inpage_file)
                if not err:
                    st.session_state["custom_df"] = clean_custom
                    st.session_state["uploaded_filename"] = inpage_file.name
                    st.session_state["custom_quality"] = quality
                    st.success(f"Successfully loaded and cleaned {inpage_file.name} ({len(clean_custom):,} rows)!")
                    st.rerun()
                else:
                    st.error(f"Error loading file: {err}")
    
    st.markdown("---")
    
    # Data shape
    st.markdown("### 📊 Dataset Dimensions (Active Data)")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Rows", f"{len(df):,}")
    with col2:
        st.metric("Columns", f"{len(df.columns)}")
    with col3:
        mem = round(df.memory_usage(deep=True).sum() / 1024 / 1024, 2)
        st.metric("Memory Footprint", f"{mem} MB")
    
    # Data types
    st.markdown("### 🔧 Column Data Types & Profiling")
    dtype_df = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str).values,
        "Non-Null Count": df.notnull().sum().values,
        "Null Count": df.isnull().sum().values,
        "Sample Value": [str(df[col].dropna().iloc[0]) if df[col].notnull().any() else "N/A" for col in df.columns],
    })
    st.dataframe(dtype_df, use_container_width=True, hide_index=True)
    
    # Missing values summary (in cleaned data)
    st.markdown("### ❓ Missing Values Audit")
    missing = detect_missing_values(df)
    if missing.empty:
        st.success("No missing values in core analytical columns! ✅")
    else:
        st.dataframe(missing, use_container_width=True, hide_index=True)
    
    # Preprocessing methodology
    st.markdown("### 🔄 Preprocessing Pipeline Steps")
    if quality_report and "steps" in quality_report:
        for idx, s in enumerate(quality_report["steps"], 1):
            st.markdown(f"**Step {idx}:** {s.get('step')}")
    else:
        st.markdown("""
        1. **Column Standardization** — Converted all column names to lowercase snake_case and mapped aliases.
        2. **Duplicate Removal** — Removed exact duplicate records while preserving multi-item checkout order lines.
        3. **Date Conversion** — Parsed order timestamps and validated date boundaries.
        4. **Numeric Conversion** — Converted quantity, unit_price, sales_amount, discount, profit to float/integer.
        5. **Negative Quantity Filtering** — Pruned negative values representing clerical entry errors.
        6. **Imputation** — Filled missing discounts with 0.0, and missing categorical fields with 'Unknown'.
        7. **Sales Amount Verification** — Enforced mathematical consistency: `sales_amount = qty × price × (1 - disc/100)`.
        8. **Feature Engineering** — Derived temporal dimensions: `year`, `month`, `quarter`, `year_month`, and `revenue`.
        """)
    
    # Correlation heatmap
    st.markdown("### 📈 Numeric Correlations")
    st.plotly_chart(correlation_heatmap(df), use_container_width=True)
    
    # Descriptive statistics
    st.markdown("### 📊 Descriptive Statistics")
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if numeric_cols:
        desc = df[numeric_cols].describe().T
        desc = desc.round(2)
        st.dataframe(desc, use_container_width=True)


# --- Main Application ---
def main():
    """Main application entry point."""
    # Sidebar header
    st.sidebar.markdown(f"# {APP_ICON} {APP_TITLE}")
    st.sidebar.markdown("*Sales & Revenue Analytics Dashboard*")
    
    # --- Data Source Selector in Sidebar ---
    st.sidebar.markdown("---")
    st.sidebar.subheader("📁 Data Source")
    
    has_custom = "custom_df" in st.session_state
    
    data_source_mode = st.sidebar.radio(
        "Choose Dataset:",
        ["Built-in Dataset", "Upload Custom CSV"],
        index=1 if has_custom else 0,
        help="Analyze the built-in Indian retail dataset or upload your own CSV file."
    )
    
    active_dataset_name = DATASET_INFO.get("name", "Indian Retail Sales and Revenue Dataset")
    is_custom = False
    custom_quality = None
    df = None
    error = None

    if data_source_mode == "Upload Custom CSV":
        st.sidebar.markdown("**Upload Custom File:**")
        uploaded_file = st.sidebar.file_uploader(
            "Select CSV file",
            type=["csv"],
            key="sidebar_csv_uploader",
            help="Upload an Indian retail or e-commerce transaction CSV."
        )
        
        if uploaded_file is not None:
            if st.session_state.get("uploaded_filename") != uploaded_file.name:
                with st.spinner("Standardizing and processing uploaded CSV..."):
                    clean_custom, quality, err = process_uploaded_file(uploaded_file)
                    if err:
                        st.sidebar.error(f"❌ {err}")
                    else:
                        st.session_state["custom_df"] = clean_custom
                        st.session_state["uploaded_filename"] = uploaded_file.name
                        st.session_state["custom_quality"] = quality
                        st.sidebar.success(f"✅ Loaded: {uploaded_file.name}")
        
        if "custom_df" in st.session_state:
            df = st.session_state["custom_df"]
            active_dataset_name = f"Custom: {st.session_state.get('uploaded_filename', 'Uploaded File')}"
            is_custom = True
            custom_quality = st.session_state.get("custom_quality")
            st.sidebar.info(f"📊 Active: {st.session_state.get('uploaded_filename')} ({len(df):,} records)")
            if st.sidebar.button("↩️ Switch to Built-in Data"):
                for k in ["custom_df", "uploaded_filename", "custom_quality"]:
                    if k in st.session_state:
                        del st.session_state[k]
                st.rerun()
        else:
            st.sidebar.info("👆 Please upload a CSV file above to begin.")
            st.markdown("### 📂 Upload Custom CSV Dataset")
            st.markdown("Please choose a retail CSV file using the sidebar uploader or drag & drop below to analyze your data:")
            inpage_file = st.file_uploader("Upload CSV file here:", type=["csv"], key="empty_state_uploader")
            if inpage_file is not None:
                clean_custom, quality, err = process_uploaded_file(inpage_file)
                if not err:
                    st.session_state["custom_df"] = clean_custom
                    st.session_state["uploaded_filename"] = inpage_file.name
                    st.session_state["custom_quality"] = quality
                    st.rerun()
                else:
                    st.error(err)
            return
    else:
        # Built-in dataset
        if "custom_df" in st.session_state:
            del st.session_state["custom_df"]
        if "uploaded_filename" in st.session_state:
            del st.session_state["uploaded_filename"]
        if "custom_quality" in st.session_state:
            del st.session_state["custom_quality"]
        df, error = get_data()

    if error:
        st.error(f"❌ Failed to load data: {error}")
        st.markdown("""
        ### Setup Instructions
        1. Run preprocessing: `python -m src.preprocessing`
        2. Restart dashboard: `streamlit run app.py`
        """)
        return
    
    if df is None or df.empty:
        st.warning("⚠️ No data available in the selected dataset.")
        return

    # Navigation in sidebar
    st.sidebar.markdown("---")
    page = st.sidebar.radio(
        "📑 Navigation",
        [
            "📊 Executive Overview",
            "🏷️ Product Analytics",
            "🗺️ Regional Analytics",
            "👥 Customer & Returns",
            "🔍 Data Quality",
        ],
    )
    
    # Apply filters
    filtered_df = apply_filters(df)
    
    if filtered_df.empty:
        st.warning("⚠️ No data matches the selected filters. Try adjusting the filter criteria in the sidebar.")
        return
    
    # Render selected page
    if page == "📊 Executive Overview":
        page_overview(filtered_df)
    elif page == "🏷️ Product Analytics":
        page_products(filtered_df)
    elif page == "🗺️ Regional Analytics":
        page_regional(filtered_df)
    elif page == "👥 Customer & Returns":
        page_customers(filtered_df)
    elif page == "🔍 Data Quality":
        page_data_quality(filtered_df, active_name=active_dataset_name, is_custom=is_custom, quality_report=custom_quality)
    
    # Footer with download option
    st.markdown("---")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.caption(
            f"📊 {APP_TITLE} | Dataset: {active_dataset_name} | "
            f"Showing {len(filtered_df):,} of {len(df):,} records"
        )
    with col2:
        csv_data = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Filtered Data (CSV)",
            data=csv_data,
            file_name="filtered_retail_data.csv",
            mime="text/csv",
        )


if __name__ == "__main__":
    main()
