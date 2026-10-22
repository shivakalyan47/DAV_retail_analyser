"""
Calculate and print project metrics from cleaned dataset.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.stdout.reconfigure(encoding='utf-8')

import pandas as pd
from src.data_loader import load_cleaned_data
from src.metrics import (
    total_revenue, total_orders, total_units_sold, average_order_value,
    monthly_revenue, revenue_by_category, revenue_by_product, quantity_by_product,
    revenue_by_state, revenue_by_city, repeat_customer_rate, return_analysis,
    profit_analysis, discount_analysis, payment_method_analysis, segment_analysis,
    generate_insights, format_inr, format_inr_short
)

df = load_cleaned_data()
print("=" * 60)
print("INDIAN RETAIL ANALYTICS - EXACT CALCULATED METRICS")
print("=" * 60)

rev = total_revenue(df)
orders = total_orders(df)
units = total_units_sold(df)
aov = average_order_value(df)

print(f"Total Transactions (Rows): {len(df):,}")
print(f"Total Columns: {len(df.columns)}")
print(f"Total Revenue: {format_inr(rev)} ({format_inr_short(rev)}) [Exact: {rev:,.2f}]")
print(f"Total Distinct Orders: {orders:,}")
print(f"Total Units Sold: {units:,}")
print(f"Average Order Value: {format_inr(aov)} [Exact: {aov:,.2f}]")

prof = profit_analysis(df)
print(f"\nTotal Profit: {format_inr(prof['total_profit'])} ({format_inr_short(prof['total_profit'])})")
print(f"Profit Margin: {prof['profit_margin']}%")
print(f"Profitable Transactions: {prof['profitable_transactions']:,}")
print(f"Loss-Making Transactions: {prof['loss_making_transactions']:,}")

ret = return_analysis(df)
print(f"\nOrder Status Breakdown:")
for k, v in ret['status_counts'].items():
    print(f"  {k}: {v:,} ({v/orders*100:.2f}%)")
print(f"Return Rate: {ret['return_rate']}%")
print(f"Cancellation Rate: {ret['cancellation_rate']}%")

rep = repeat_customer_rate(df)
print(f"\nCustomer Dynamics:")
print(f"  Total Unique Customers: {rep['total_customers']:,}")
print(f"  Repeat Customers: {rep['repeat_customers']:,}")
print(f"  Single Purchase Customers: {rep['single_purchase']:,}")
print(f"  Repeat Customer Rate: {rep['repeat_rate']}%")

print(f"\nCategory-wise Revenue Breakdown:")
cat_df = revenue_by_category(df)
cat_df["share_%"] = (cat_df["revenue"] / rev * 100).round(2)
for _, r in cat_df.iterrows():
    print(f"  {r['category']:<20} | Revenue: {format_inr(r['revenue']):<15} | Share: {r['share_%']}% | Units: {r['quantity']:,} | Orders: {r['order_count']:,}")

print(f"\nTop 5 States by Revenue:")
st_df = revenue_by_state(df).head(5)
st_df["share_%"] = (st_df["revenue"] / rev * 100).round(2)
for _, r in st_df.iterrows():
    print(f"  {r['state']:<20} | Revenue: {format_inr(r['revenue']):<15} | Share: {r['share_%']}% | Orders: {r['order_count']:,}")

print(f"\nTop 5 Cities by Revenue:")
city_df = revenue_by_city(df, top_n=5)
for _, r in city_df.iterrows():
    print(f"  {r['city']} ({r['state']}): {format_inr(r['revenue'])} | Orders: {r['order_count']:,}")

print(f"\nPayment Method Distribution:")
pay_df = payment_method_analysis(df)
pay_df["order_share_%"] = (pay_df["order_count"] / orders * 100).round(2)
for _, r in pay_df.iterrows():
    print(f"  {r['payment_method']:<20} | Orders: {r['order_count']:,} ({r['order_share_%']}%) | Revenue: {format_inr(r['revenue']):<15} | AOV: {format_inr(r['avg_order_value'])}")

m_df = monthly_revenue(df)
best_m = m_df.loc[m_df['revenue'].idxmax()]
worst_m = m_df.loc[m_df['revenue'].idxmin()]
print(f"\nTemporal Performance:")
print(f"  Strongest Month: {best_m['year_month']} with {format_inr(best_m['revenue'])} ({best_m['order_count']:,} orders)")
print(f"  Lowest Month:    {worst_m['year_month']} with {format_inr(worst_m['revenue'])} ({worst_m['order_count']:,} orders)")

print(f"\nTop 5 Products by Revenue:")
p_rev = revenue_by_product(df, top_n=5)
for _, r in p_rev.iterrows():
    print(f"  {r['product_name']} ({r['category']}): {format_inr(r['revenue'])} | Units: {r['quantity']:,}")

print(f"\nTop 5 Products by Quantity Sold:")
p_qty = quantity_by_product(df, top_n=5)
for _, r in p_qty.iterrows():
    print(f"  {r['product_name']} ({r['category']}): {r['quantity']:,} units | Revenue: {format_inr(r['revenue'])}")

print(f"\nAutomated Insights Generated:")
for ins in generate_insights(df):
    print(f"  * {ins['title']}: {ins['description']}")
