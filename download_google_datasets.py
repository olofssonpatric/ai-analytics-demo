"""
Download Google BigQuery Public Datasets for AI Analytics Demo
No authentication required - uses public datasets
"""

import pandas as pd
from google.cloud import bigquery
import os

print("=" * 60)
print("DOWNLOADING GOOGLE BIGQUERY PUBLIC DATASETS")
print("=" * 60)
print()

# Initialize BigQuery client (no auth needed for public data)
client = bigquery.Client()

# ================================================================
# DATASET 1: GOOGLE ANALYTICS E-COMMERCE DATA
# ================================================================
print("📊 Dataset 1: Google Analytics E-commerce Sample")
print("Source: Google Merchandise Store")
print("Use case: E-commerce business analytics")
print()

ga_query = """
SELECT 
    fullVisitorId as customer_id,
    visitId as session_id,
    date,
    totals.transactions as transactions,
    totals.totalTransactionRevenue as revenue,
    totals.pageviews as pageviews,
    totals.timeOnSite as time_on_site,
    trafficSource.source as traffic_source,
    trafficSource.medium as traffic_medium,
    device.deviceCategory as device_type,
    geoNetwork.country as country,
    geoNetwork.city as city
FROM `bigquery-public-data.google_analytics_sample.ga_sessions_*`
WHERE _TABLE_SUFFIX BETWEEN '20170701' AND '20170731'
    AND totals.transactions IS NOT NULL
LIMIT 20000
"""

print("Querying BigQuery...")
ga_df = client.query(ga_query).to_dataframe()

# Convert revenue from micros to actual currency
ga_df['revenue'] = ga_df['revenue'] / 1000000
ga_df['revenue_sek'] = ga_df['revenue'] * 10  # Approximate USD to SEK

ga_df.to_csv('google_analytics_ecommerce.csv', index=False)
print(f"✓ Saved: google_analytics_ecommerce.csv ({len(ga_df)} rows)")
print(f"  Revenue range: {ga_df['revenue_sek'].min():.0f} - {ga_df['revenue_sek'].max():.0f} SEK")
print()

# ================================================================
# DATASET 2: IOWA LIQUOR SALES (RETAIL TRANSACTIONS)
# ================================================================
print("📊 Dataset 2: Iowa Liquor Sales (Retail)")
print("Source: Iowa Department of Commerce")
print("Use case: Retail/Distribution business")
print()

iowa_query = """
SELECT 
    invoice_and_item_number as order_id,
    date,
    store_number as customer_id,
    store_name as customer_name,
    city,
    zip_code,
    county,
    category_name as product_category,
    item_description as product_name,
    bottles_sold,
    sale_dollars as order_amount,
    volume_sold_liters,
    volume_sold_gallons
FROM `bigquery-public-data.iowa_liquor_sales.sales`
WHERE date BETWEEN '2023-01-01' AND '2023-03-31'
    AND sale_dollars > 0
ORDER BY date DESC
LIMIT 20000
"""

print("Querying BigQuery...")
iowa_df = client.query(iowa_query).to_dataframe()

# Convert to SEK
iowa_df['order_amount_sek'] = iowa_df['order_amount'] * 10

iowa_df.to_csv('iowa_retail_sales.csv', index=False)
print(f"✓ Saved: iowa_retail_sales.csv ({len(iowa_df)} rows)")
print(f"  Order range: {iowa_df['order_amount_sek'].min():.0f} - {iowa_df['order_amount_sek'].max():.0f} SEK")
print()

# ================================================================
# DATASET 3: NYC TAXI TRIPS (SERVICE BUSINESS)
# ================================================================
print("📊 Dataset 3: NYC Taxi Trips (Service Business)")
print("Source: NYC Taxi & Limousine Commission")
print("Use case: Service/Transportation business")
print()

taxi_query = """
SELECT 
    CAST(pickup_datetime AS DATE) as service_date,
    pickup_location_id,
    dropoff_location_id,
    trip_distance,
    fare_amount,
    tip_amount,
    total_amount,
    payment_type,
    passenger_count
FROM `bigquery-public-data.new_york_taxi_trips.tlc_yellow_trips_2023`
WHERE pickup_datetime BETWEEN '2023-06-01' AND '2023-06-30'
    AND fare_amount > 0
    AND trip_distance > 0
ORDER BY RAND()
LIMIT 20000
"""

print("Querying BigQuery...")
taxi_df = client.query(taxi_query).to_dataframe()

# Convert to SEK
taxi_df['fare_amount_sek'] = taxi_df['fare_amount'] * 10
taxi_df['total_amount_sek'] = taxi_df['total_amount'] * 10

taxi_df.to_csv('nyc_taxi_services.csv', index=False)
print(f"✓ Saved: nyc_taxi_services.csv ({len(taxi_df)} rows)")
print(f"  Fare range: {taxi_df['fare_amount_sek'].min():.0f} - {taxi_df['total_amount_sek'].max():.0f} SEK")
print()

# ================================================================
# DATASET 4: GITHUB ACTIVITY (TECH COMPANY)
# ================================================================
print("📊 Dataset 4: GitHub Activity (Tech Company Simulation)")
print("Source: GitHub Archive")
print("Use case: Software/SaaS company metrics")
print()

github_query = """
SELECT 
    type as event_type,
    CAST(created_at AS DATE) as event_date,
    actor.login as user_id,
    repo.name as project_name,
    JSON_EXTRACT_SCALAR(payload, '$.action') as action,
    org.login as organization
FROM `bigquery-public-data.github_repos.sample_events`
WHERE type IN ('PushEvent', 'PullRequestEvent', 'IssuesEvent', 'WatchEvent')
    AND created_at BETWEEN '2023-01-01' AND '2023-01-31'
    AND org.login IS NOT NULL
ORDER BY RAND()
LIMIT 20000
"""

print("Querying BigQuery...")
github_df = client.query(github_query).to_dataframe()

github_df.to_csv('github_tech_activity.csv', index=False)
print(f"✓ Saved: github_tech_activity.csv ({len(github_df)} rows)")
print(f"  Event types: {github_df['event_type'].unique().tolist()}")
print()

# ================================================================
# BONUS: CREATE CUSTOMER SUMMARY DATA
# ================================================================
print("📊 Bonus: Creating Customer Summary Dataset")
print("Aggregating e-commerce data for customer insights")
print()

customer_summary = ga_df.groupby('customer_id').agg({
    'session_id': 'count',
    'transactions': 'sum',
    'revenue_sek': 'sum',
    'pageviews': 'sum',
    'time_on_site': 'mean',
    'traffic_source': 'first',
    'device_type': 'first',
    'country': 'first'
}).reset_index()

customer_summary.columns = [
    'customer_id', 'total_sessions', 'total_transactions', 
    'total_revenue_sek', 'total_pageviews', 'avg_time_on_site',
    'first_traffic_source', 'primary_device', 'country'
]

customer_summary.to_csv('customer_summary.csv', index=False)
print(f"✓ Saved: customer_summary.csv ({len(customer_summary)} customers)")
print()

# ================================================================
# CREATE DATA DICTIONARY
# ================================================================
print("📝 Creating Data Dictionary...")

data_dict = """
# AI ANALYTICS DEMO - DATA DICTIONARY

## Files Created:

### 1. google_analytics_ecommerce.csv
Real Google Analytics data from Google Merchandise Store
- customer_id: Unique visitor identifier
- session_id: Individual session/visit ID
- date: Visit date (YYYYMMDD format)
- transactions: Number of transactions in session
- revenue_sek: Transaction revenue in SEK
- pageviews: Pages viewed in session
- time_on_site: Time spent on site (seconds)
- traffic_source: Where visitor came from
- traffic_medium: Marketing medium
- device_type: desktop/mobile/tablet
- country: Visitor country
- city: Visitor city

### 2. iowa_retail_sales.csv
Real retail transaction data from Iowa liquor sales
- order_id: Unique order identifier
- date: Sale date
- customer_id: Store number
- customer_name: Store name
- city: Store location
- product_category: Liquor category
- product_name: Specific product
- bottles_sold: Quantity
- order_amount_sek: Sale amount in SEK

### 3. nyc_taxi_services.csv
Real service transaction data from NYC taxis
- service_date: Trip date
- trip_distance: Distance traveled
- fare_amount_sek: Base fare in SEK
- total_amount_sek: Total including tips in SEK
- payment_type: Payment method
- passenger_count: Number of passengers

### 4. github_tech_activity.csv
Real developer activity from GitHub
- event_type: Type of event (Push, PR, Issues, etc.)
- event_date: When event occurred
- user_id: Developer username
- project_name: Repository name
- action: Specific action taken
- organization: Company/org name

### 5. customer_summary.csv
Aggregated customer analytics
- customer_id: Unique customer
- total_sessions: Number of visits
- total_transactions: Total purchases
- total_revenue_sek: Lifetime value
- total_pageviews: Engagement metric
- avg_time_on_site: Average session duration
- first_traffic_source: Acquisition channel
- primary_device: Most-used device
- country: Customer location

## Use Cases by Industry:

### E-commerce (Files 1, 5):
- Customer churn prediction
- Upsell opportunities
- Traffic source ROI
- Device optimization

### Retail/Distribution (File 2):
- Inventory optimization
- Customer purchase patterns
- Regional performance
- Product mix analysis

### Service Business (File 3):
- Service efficiency
- Pricing optimization
- Geographic demand patterns
- Customer satisfaction proxies

### Tech/SaaS (File 4):
- Developer productivity
- Project activity patterns
- Team collaboration metrics
- Open source engagement
"""

with open('DATA_DICTIONARY.md', 'w') as f:
    f.write(data_dict)

print("✓ Saved: DATA_DICTIONARY.md")
print()

# ================================================================
# SUMMARY
# ================================================================
print("=" * 60)
print("✅ DOWNLOAD COMPLETE!")
print("=" * 60)
print()
print("Files created:")
print("  1. google_analytics_ecommerce.csv (E-commerce)")
print("  2. iowa_retail_sales.csv (Retail)")
print("  3. nyc_taxi_services.csv (Services)")
print("  4. github_tech_activity.csv (Tech/SaaS)")
print("  5. customer_summary.csv (Aggregated)")
print("  6. DATA_DICTIONARY.md (Documentation)")
print()
print("Next steps:")
print("  1. Review the CSV files")
print("  2. Use these in your Streamlit demo")
print("  3. Reference 'real Google data' in sales pitches")
print()
print("Total data points:", 
      len(ga_df) + len(iowa_df) + len(taxi_df) + len(github_df))
print()