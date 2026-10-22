"""
Generate and save static analytical charts for reports and presentation.
Uses Matplotlib and Seaborn to produce publication-quality figures.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

from config import CHARTS_DIR
from src.data_loader import load_cleaned_data

# Set styling
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['figure.autolayout'] = True
plt.rcParams['figure.dpi'] = 150

df = load_cleaned_data()
os.makedirs(CHARTS_DIR, exist_ok=True)

# 1. Monthly Revenue Trend
plt.figure(figsize=(12, 5))
monthly = df.groupby('year_month')['revenue'].sum().reset_index()
monthly['revenue_cr'] = monthly['revenue'] / 1e7
plt.plot(monthly['year_month'], monthly['revenue_cr'], marker='o', color='#1f77b4', linewidth=2, markersize=5)
plt.title('Monthly Revenue Trend (2022 - 2024)', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Year-Month', fontsize=11)
plt.ylabel('Revenue (₹ Crores)', fontsize=11)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_DIR, '01_monthly_revenue_trend.png'))
plt.close()

# 2. Category Revenue
plt.figure(figsize=(10, 5))
cat = df.groupby('category')['revenue'].sum().reset_index().sort_values('revenue', ascending=True)
cat['revenue_cr'] = cat['revenue'] / 1e7
bars = plt.barh(cat['category'], cat['revenue_cr'], color='#2ca02c')
plt.title('Revenue by Product Category', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Revenue (₹ Crores)', fontsize=11)
plt.ylabel('Category', fontsize=11)
for bar in bars:
    w = bar.get_width()
    plt.text(w + 0.2, bar.get_y() + bar.get_height()/2, f'₹{w:.2f} Cr', va='center', fontsize=9)
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_DIR, '02_revenue_by_category.png'))
plt.close()

# 3. Top 10 Products by Revenue
plt.figure(figsize=(10, 6))
top_p = df.groupby('product_name')['revenue'].sum().reset_index().sort_values('revenue', ascending=False).head(10)
top_p = top_p.sort_values('revenue', ascending=True)
top_p['revenue_cr'] = top_p['revenue'] / 1e7
bars = plt.barh(top_p['product_name'], top_p['revenue_cr'], color='#1f77b4')
plt.title('Top 10 Products by Revenue', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Revenue (₹ Crores)', fontsize=11)
plt.ylabel('Product Name', fontsize=11)
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_DIR, '03_top_products_revenue.png'))
plt.close()

# 4. Top 10 Products by Quantity
plt.figure(figsize=(10, 6))
top_q = df.groupby('product_name')['quantity'].sum().reset_index().sort_values('quantity', ascending=False).head(10)
top_q = top_q.sort_values('quantity', ascending=True)
bars = plt.barh(top_q['product_name'], top_q['quantity'], color='#ff7f0e')
plt.title('Top 10 Products by Units Sold', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Units Sold', fontsize=11)
plt.ylabel('Product Name', fontsize=11)
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_DIR, '04_top_products_quantity.png'))
plt.close()

# 5. State-wise Revenue
plt.figure(figsize=(10, 7))
st_rev = df.groupby('state')['revenue'].sum().reset_index().sort_values('revenue', ascending=True)
st_rev['revenue_cr'] = st_rev['revenue'] / 1e7
plt.barh(st_rev['state'], st_rev['revenue_cr'], color='#17becf')
plt.title('State-wise Revenue Distribution (19 States)', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Revenue (₹ Crores)', fontsize=11)
plt.ylabel('Indian State', fontsize=11)
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_DIR, '05_state_wise_revenue.png'))
plt.close()

# 6. Quantity vs Revenue Scatter
plt.figure(figsize=(10, 6))
prod_agg = df.groupby(['product_name', 'category']).agg({'quantity': 'sum', 'revenue': 'sum'}).reset_index()
prod_agg['revenue_lakhs'] = prod_agg['revenue'] / 1e5
sns.scatterplot(data=prod_agg, x='quantity', y='revenue_lakhs', hue='category', s=90, alpha=0.85)
plt.title('Product Performance: Quantity Sold vs. Revenue Generated', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Total Units Sold', fontsize=11)
plt.ylabel('Total Revenue (₹ Lakhs)', fontsize=11)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_DIR, '06_quantity_vs_revenue_scatter.png'))
plt.close()

# 7. Revenue vs Profit by Category
plt.figure(figsize=(11, 5))
cat_perf = df.groupby('category').agg({'revenue': 'sum', 'profit': 'sum'}).reset_index()
cat_perf['revenue_cr'] = cat_perf['revenue'] / 1e7
cat_perf['profit_cr'] = cat_perf['profit'] / 1e7
x = np.arange(len(cat_perf))
width = 0.35
plt.bar(x - width/2, cat_perf['revenue_cr'], width, label='Revenue', color='#1f77b4')
plt.bar(x + width/2, cat_perf['profit_cr'], width, label='Profit', color='#2ca02c')
plt.xticks(x, cat_perf['category'], rotation=30, ha='right')
plt.title('Revenue vs Profit by Product Category', fontsize=14, fontweight='bold', pad=15)
plt.ylabel('Amount (₹ Crores)', fontsize=11)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_DIR, '07_revenue_vs_profit.png'))
plt.close()

# 8. Sales Amount Distribution
plt.figure(figsize=(10, 5))
sns.histplot(df['revenue'], bins=40, kde=True, color='#4c72b0')
plt.title('Transaction Value Distribution', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Transaction Sales Amount (₹)', fontsize=11)
plt.ylabel('Frequency', fontsize=11)
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_DIR, '08_sales_distribution_histogram.png'))
plt.close()

# 9. Correlation Heatmap
plt.figure(figsize=(8, 6))
num_cols = ['quantity', 'unit_price', 'discount_percent', 'sales_amount', 'profit', 'shipping_cost']
corr = df[num_cols].corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', vmin=-1, vmax=1, linewidths=0.5)
plt.title('Correlation Matrix of Numeric Attributes', fontsize=14, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_DIR, '09_correlation_heatmap.png'))
plt.close()

# 10. Payment Method Distribution
plt.figure(figsize=(7, 7))
pay = df['payment_method'].value_counts()
plt.pie(pay, labels=pay.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('Set2'))
plt.title('Order Distribution by Payment Method', fontsize=14, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_DIR, '10_payment_method_distribution.png'))
plt.close()

# 11. Order Status Distribution
plt.figure(figsize=(7, 7))
status = df['order_status'].value_counts()
colors = {'Delivered': '#2ca02c', 'Returned': '#d62728', 'Cancelled': '#ff7f0e', 'Processing': '#17becf'}
pie_colors = [colors.get(s, '#7f7f7f') for s in status.index]
plt.pie(status, labels=status.index, autopct='%1.1f%%', startangle=140, colors=pie_colors)
plt.title('Order Fulfillment Status Breakdown', fontsize=14, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_DIR, '11_order_status_distribution.png'))
plt.close()

print(f"Generated 11 static charts in {CHARTS_DIR}")
