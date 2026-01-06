"""
Download Google BigQuery Public Data
Requires: gcloud auth application-default login
"""

from google.cloud import bigquery
import pandas as pd

print("Connecting to BigQuery...")

# Initialize client (uses your Google account credentials)
client = bigquery.Client(project='ai-analytics-demo')

print("✓ Connected!")
print()

# ================================================================
# DATASET 1: Google Analytics E-commerce
# ================================================================
print("📊 Downloading Google Analytics data...")

ga_query = """
SELECT 
    fullVisitorId as customer_id,
    visitId as session_id,
    date,
    totals.transactions as transactions,
    totals.totalTransactionRevenue / 1000000 as revenue_usd,
    (totals.totalTransactionRevenue / 1000000) * 10 as revenue_sek,
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
LIMIT 5000
"""

try:
    ga_df = client.query(ga_query).to_dataframe()
    ga_df.to_csv('google_analytics_ecommerce.csv', index=False)
    print(f"✓ Saved: google_analytics_ecommerce.csv ({len(ga_df)} rows)")
    print(f"  Revenue range: {ga_df['revenue_sek'].min():.0f} - {ga_df['revenue_sek'].max():.0f} SEK")
    print()
except Exception as e:
    print(f"❌ Error downloading Google Analytics data: {e}")
    print()
    ga_df = None

# ================================================================
# DATASET 2: Iowa Liquor Sales
# ================================================================
print("📊 Downloading Iowa Retail Sales data...")

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
    sale_dollars * 10 as order_amount_sek,
    volume_sold_liters,
    volume_sold_gallons
FROM `bigquery-public-data.iowa_liquor_sales.sales`
WHERE date BETWEEN '2023-01-01' AND '2023-03-31'
    AND sale_dollars > 0
ORDER BY date DESC
LIMIT 5000
"""

try:
    iowa_df = client.query(iowa_query).to_dataframe()
    iowa_df.to_csv('iowa_retail_sales.csv', index=False)
    print(f"✓ Saved: iowa_retail_sales.csv ({len(iowa_df)} rows)")
    print()
except Exception as e:
    print(f"❌ Error downloading Iowa data: {e}")
    print()
    iowa_df = None

# ================================================================
# DATASET 3: NYC Taxi
# ================================================================
print("📊 Downloading NYC Taxi data...")

taxi_query = """
SELECT 
    CAST(pickup_datetime AS DATE) as service_date,
    pickup_location_id,
    dropoff_location_id,
    trip_distance,
    fare_amount,
    fare_amount * 10 as fare_amount_sek,
    tip_amount,
    total_amount,
    total_amount * 10 as total_amount_sek,
    payment_type,
    passenger_count
FROM `bigquery-public-data.new_york_taxi_trips.tlc_yellow_trips_2022`
WHERE pickup_datetime BETWEEN '2022-06-01' AND '2022-06-30'
    AND fare_amount > 0
    AND trip_distance > 0
ORDER BY RAND()
LIMIT 5000
"""

try:
    taxi_df = client.query(taxi_query).to_dataframe()
    taxi_df.to_csv('nyc_taxi_services.csv', index=False)
    print(f"✓ Saved: nyc_taxi_services.csv ({len(taxi_df)} rows)")
    print()
except Exception as e:
    print(f"❌ Error downloading Taxi data: {e}")
    print()
    taxi_df = None

# ================================================================
# DATASET 4: GitHub Activity (FIXED QUERY)
# ================================================================
print("📊 Downloading GitHub activity data...")

# Using actual available table: sample_commits
github_query = """
SELECT 
    'CommitEvent' as event_type,
    CAST(committer.date AS DATE) as event_date,
    committer.name as user_id,
    repo_name as project_name,
    SPLIT(repo_name, '/')[OFFSET(0)] as organization,
    subject as commit_message
FROM `bigquery-public-data.github_repos.sample_commits`
WHERE committer.date BETWEEN '2016-01-01' AND '2016-12-31'
    AND repo_name IS NOT NULL
    AND committer.name IS NOT NULL
    AND SPLIT(repo_name, '/')[OFFSET(0)] IN ('tensorflow', 'kubernetes', 'microsoft', 'google', 'facebook', 'apache', 'golang')
LIMIT 5000
"""

try:
    github_df = client.query(github_query).to_dataframe()
    github_df.to_csv('github_tech_activity.csv', index=False)
    print(f"✓ Saved: github_tech_activity.csv ({len(github_df)} rows)")
    print()
except Exception as e:
    print(f"❌ Error downloading GitHub data: {e}")
    print()
    github_df = None

# ================================================================
# DATASET 5: Customer Summary (from Google Analytics)
# ================================================================
print("📊 Creating customer summary...")

if ga_df is not None and len(ga_df) > 0:
    try:
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
    except Exception as e:
        print(f"❌ Error creating customer summary: {e}")
        print()
else:
    print("⚠️  Skipping customer_summary.csv (no Google Analytics data)")
    print()

# ================================================================
# SUMMARY
# ================================================================
print("=" * 70)
print("✅ DOWNLOAD COMPLETE!")
print("=" * 70)
print()
print("Files created:")

import os
files_created = []
if os.path.exists('google_analytics_ecommerce.csv'):
    files_created.append("  ✓ google_analytics_ecommerce.csv")
if os.path.exists('iowa_retail_sales.csv'):
    files_created.append("  ✓ iowa_retail_sales.csv")
if os.path.exists('nyc_taxi_services.csv'):
    files_created.append("  ✓ nyc_taxi_services.csv")
if os.path.exists('github_tech_activity.csv'):
    files_created.append("  ✓ github_tech_activity.csv")
if os.path.exists('customer_summary.csv'):
    files_created.append("  ✓ customer_summary.csv")

for f in files_created:
    print(f)

print()
print(f"Total files: {len(files_created)}/5")
print()

if len(files_created) < 5:
    print("⚠️  Some files were not created due to query errors.")
    print("   This is normal - some BigQuery datasets have restrictions.")
    print("   The files you have are sufficient for demo purposes!")
print()