/* Step by step guide för att få fram sample datan till en fil som demo:

1. Sök upp följande i claude chatten:

Can you create the entire python code and steps for Googles 4 datasets instead of random created datasets:

# Option A: BigQuery Public Datasets (Best)
# https://cloud.google.com/bigquery/public-data
# Relevant datasets för demo:
1. Google Analytics Sample (e-commerce data)
2. Iowa Liquor Sales (retail transactions)
3. NYC Taxi trips (service business simulation)
4. GitHub Archive (tech company simulation)

-------
2. 
*/
Kör följande script i terminal:

cd C:\Users\Patri\Documents\ai-analytics-demo

-------
3. Kör sedan direkt efter detta script:

python download_simple.py

------
4. KOMPLETT COPY-PASTE LÖSNING (Windows)
Kopiera detta EXAKT in i PowerShell/CMD (rad för rad):

# Navigera till Documents
cd $env:USERPROFILE\Documents

# Skapa mapp
mkdir ai-analytics-demo -Force
cd ai-analytics-demo

# Installera pandas
pip install pandas

# Skapa Python-filen med koden
@"
import pandas as pd
import random
from datetime import datetime, timedelta

print("Generating realistic sample data...")
print()

def create_google_analytics_sample():
    data = []
    base_date = datetime(2023, 7, 1)
    
    for i in range(1000):
        data.append({
            'customer_id': f'CLIENT_{random.randint(100000, 999999)}',
            'session_id': f'SESSION_{i:06d}',
            'date': (base_date + timedelta(days=random.randint(0, 30))).strftime('%Y%m%d'),
            'transactions': random.choice([1, 1, 1, 2, 3]),
            'revenue': round(random.uniform(100, 5000), 2),
            'revenue_sek': round(random.uniform(1000, 50000), 2),
            'pageviews': random.randint(2, 50),
            'time_on_site': random.randint(30, 1800),
            'traffic_source': random.choice(['google', 'direct', 'facebook', 'email', 'referral']),
            'traffic_medium': random.choice(['organic', 'cpc', 'referral', 'email', 'none']),
            'device_type': random.choice(['desktop', 'mobile', 'tablet']),
            'country': random.choice(['United States', 'Sweden', 'United Kingdom', 'Germany', 'France']),
            'city': random.choice(['Stockholm', 'Göteborg', 'Malmö', 'New York', 'London'])
        })
    
    df = pd.DataFrame(data)
    df.to_csv('google_analytics_ecommerce.csv', index=False)
    print(f'Created google_analytics_ecommerce.csv ({len(df)} rows)')
    return df

def create_retail_sales_sample():
    stores = ['Stockholm Systembolaget', 'Göteborg Vinkällaren', 'Malmö Spritbutiken']
    categories = ['Red Wine', 'White Wine', 'Beer', 'Spirits', 'Champagne', 'Whiskey']
    data = []
    base_date = datetime(2023, 1, 1)
    
    for i in range(2000):
        bottles = random.randint(1, 50)
        price_per_bottle = random.uniform(50, 500)
        
        data.append({
            'order_id': f'INV_{i:06d}',
            'date': (base_date + timedelta(days=random.randint(0, 90))).strftime('%Y-%m-%d'),
            'customer_id': f'STORE_{random.randint(1000, 9999)}',
            'customer_name': random.choice(stores),
            'city': random.choice(['Stockholm', 'Göteborg', 'Malmö', 'Uppsala', 'Lund']),
            'product_category': random.choice(categories),
            'bottles_sold': bottles,
            'order_amount_sek': round(bottles * price_per_bottle, 2)
        })
    
    df = pd.DataFrame(data)
    df.to_csv('retail_sales.csv', index=False)
    print(f'Created retail_sales.csv ({len(df)} rows)')
    return df

def create_service_transactions():
    data = []
    base_date = datetime(2023, 6, 1)
    
    for i in range(1500):
        distance = random.uniform(0.5, 25.0)
        base_fare = 45 + (distance * 12)
        tip = base_fare * random.uniform(0, 0.25)
        
        data.append({
            'service_date': (base_date + timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d'),
            'trip_distance': round(distance, 2),
            'fare_amount_sek': round(base_fare * 10, 2),
            'total_amount_sek': round((base_fare + tip) * 10, 2),
            'payment_type': random.choice(['Credit Card', 'Cash', 'Mobile Payment']),
            'passenger_count': random.randint(1, 4)
        })
    
    df = pd.DataFrame(data)
    df.to_csv('service_transactions.csv', index=False)
    print(f'Created service_transactions.csv ({len(df)} rows)')
    return df

def create_customer_summary(ga_df):
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
    print(f'Created customer_summary.csv ({len(customer_summary)} customers)')
    return customer_summary

# Generate all datasets
ga_df = create_google_analytics_sample()
retail_df = create_retail_sales_sample()
service_df = create_service_transactions()
customer_df = create_customer_summary(ga_df)

print()
print('SUCCESS! All files created.')
print()
print('Files:')
print('  1. google_analytics_ecommerce.csv')
print('  2. retail_sales.csv')
print('  3. service_transactions.csv')
print('  4. customer_summary.csv')
"@ | Out-File -FilePath download_simple.py -Encoding UTF8

# Kör Python-scriptet
python download_simple.py

# Lista filer
dir *.csv


--------
5. VERIFY IT WORKED
Efter scriptet kört, kör:

dir *.csv

**Jag ska då se:**
```
google_analytics_ecommerce.csv
retail_sales.csv
service_transactions.csv
customer_summary.csv