import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# In practice: df = pd.read_csv('sales_data.csv')
# Simulated dataset for illustration
np.random.seed(42)
# Without the seed, every time you rerun the script
# you'd get a different simulated dataset
#  different revenue numbers, different chart shapes.
dates = pd.date_range('2025-01-01', '2025-12-31', freq='D')
regions = ['North', 'South', 'East', 'West']
categories = ['Electronics', 'Clothing', 'Groceries', 'Home & Garden']

df = pd.DataFrame({
    'date': np.random.choice(dates, 5000),
    'region': np.random.choice(regions, 5000),
    'category': np.random.choice(categories, 5000),
    'units_sold': np.random.poisson(8, 5000),
    'unit_price': np.round(np.random.uniform(5, 200, 5000), 2)
})
# This creates a made-up DataFrame with 5,000
# random rows of dates, regions, categories,
# units sold, and prices
df['revenue'] = df['units_sold'] * df['unit_price']
df['month'] = df['date'].dt.to_period('M').astype(str)

print(df.head())
print(df.describe())

# Step 2 — Find the monthly Revenue Trend (Line Chart)
# monthly_revenue = df.groupby('month')['revenue'].sum().reset_index()
#
# plt.figure(figsize=(10, 5))
# sns.lineplot(data=monthly_revenue, x='month', y='revenue', marker='o', color='#1f77b4')
# plt.xticks(rotation=45)
# plt.title('Monthly Revenue Trend — 2025')
# plt.ylabel('Revenue ($)')
# plt.tight_layout()
# plt.show()
#
# # Step 3 find the Revenue by Region (Bar Chart)
# region_revenue = df.groupby('region')['revenue'].sum().sort_values(ascending=False)
#
# plt.figure(figsize=(7, 5))
# sns.barplot(x=region_revenue.index, y=region_revenue.values, palette='viridis')
# plt.title('Total Revenue by Region')
# plt.ylabel('Revenue ($)')
# plt.show()
#
#
# # Step 4 — Category Performance Across Regions (Heatmap)
# pivot = df.pivot_table(values='revenue', index='category', columns='region', aggfunc='sum')
#
# plt.figure(figsize=(8, 5))
# sns.heatmap(pivot, annot=True, fmt='.0f', cmap='YlOrRd')
# plt.title('Revenue Heatmap: Category vs Region')
# plt.show()

# Step 5 — Distribution and Outliers (Box Plot)
plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x='category', y='revenue', palette='Set2')
plt.title('Revenue Distribution by Category (Outlier Detection)')
plt.xticks(rotation=15)
plt.show()

# Step 6 Build an Interactive Dashboard Chart (Plotly)
# import plotly.express as px
#
# monthly_region = df.groupby(['month', 'region'])['revenue'].sum().reset_index()
#
# fig = px.line(
#     monthly_region, x='month', y='revenue', color='region',
#     title='Interactive Monthly Revenue by Region',
#     markers=True
# )
# fig.update_layout(xaxis_tickangle=-45)
# fig.write_html('sales_dashboard.html')  # can be emailed or embedded in an internal portal
# fig.show()