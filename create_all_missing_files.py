"""
Create missing CSV files for AI Analytics Demo
This creates customer_summary.csv and github_tech_activity.csv
"""

import pandas as pd
import random
from datetime import datetime, timedelta
import os

print("=" * 70)
print("CREATING MISSING DEMO FILES")
print("=" * 70)
print()

# ================================================================
# FILE 1: Customer Summary (from existing Google Analytics data)
# ================================================================
print("📊 Creating customer_summary.csv...")

if os.path.exists('google_analytics_ecommerce.csv'):
    ga_df = pd.read_csv('google_analytics_ecommerce.csv')
    
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
    print(f"✓ customer_summary.csv created ({len(customer_summary):,} customers)")
    print(f"  Total revenue: {customer_summary['total_revenue_sek'].sum():,.0f} SEK")
    print()
else:
    print("❌ google_analytics_ecommerce.csv not found. Run download_bigquery_data.py first.")
    print()

# ================================================================
# FILE 2: GitHub Tech Activity (Simulated but Realistic)
# ================================================================
print("📊 Creating github_tech_activity.csv...")
print("   (Simulated data based on real tech company patterns)")
print()

# Realistic tech organizations and their projects
orgs_projects = {
    'microsoft': ['vscode', 'TypeScript', 'PowerToys', 'terminal', 'playwright', 'dotnet'],
    'google': ['tensorflow', 'flutter', 'go', 'kubernetes', 'chromium', 'angular'],
    'facebook': ['react', 'react-native', 'jest', 'yoga', 'docusaurus', 'relay'],
    'apache': ['kafka', 'spark', 'airflow', 'flink', 'beam', 'cassandra'],
    'hashicorp': ['terraform', 'vault', 'consul', 'nomad', 'packer', 'vagrant'],
    'elastic': ['elasticsearch', 'kibana', 'logstash', 'beats', 'apm-server'],
    'vercel': ['next.js', 'turbo', 'swr', 'hyper', 'pkg', 'micro'],
    'netflix': ['hystrix', 'eureka', 'zuul', 'ribbon', 'archaius', 'conductor'],
    'uber': ['cadence', 'jaeger', 'pyro', 'kraken', 'react-map-gl'],
    'airbnb': ['lottie', 'visx', 'enzyme', 'javascript', 'mavericks']
}

# Realistic developer names
developers = [
    'sarah_chen', 'mike_johnson', 'emma_garcia', 'james_smith', 
    'lisa_anderson', 'david_martinez', 'anna_wilson', 'john_taylor',
    'maria_rodriguez', 'robert_brown', 'jen_liu', 'alex_kumar',
    'sophie_duval', 'tom_nelson', 'nina_patel', 'chris_lee',
    'rachel_kim', 'dan_murphy', 'olivia_zhang', 'mark_davis'
]

# Event types and actions
event_types = ['PushEvent', 'PullRequestEvent', 'IssuesEvent', 'CommitEvent', 'MergeEvent', 'CreateEvent']
actions = ['opened', 'closed', 'merged', 'created', 'updated', 'commented', 'reviewed', 'approved']

github_data = []
base_date = datetime(2023, 1, 1)

print("   Generating 5,000 realistic events...")

for i in range(5000):
    org = random.choice(list(orgs_projects.keys()))
    project = random.choice(orgs_projects[org])
    event = random.choice(event_types)
    
    # Create realistic patterns
    commits = None
    files = None
    if event in ['PushEvent', 'CommitEvent']:
        commits = random.randint(1, 15)
        files = random.randint(1, 25)
    elif event == 'PullRequestEvent':
        commits = random.randint(1, 50)
        files = random.randint(1, 100)
    
    github_data.append({
        'event_type': event,
        'event_date': (base_date + timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d'),
        'user_id': random.choice(developers),
        'project_name': f'{org}/{project}',
        'organization': org,
        'action': random.choice(actions),
        'commits_count': commits,
        'files_changed': files,
        'is_public': random.choice([True, True, True, False]),  # Mostly public
        'language': random.choice(['Python', 'JavaScript', 'TypeScript', 'Go', 'Java', 'Rust', 'C++'])
    })

github_df = pd.DataFrame(github_data)
github_df.to_csv('github_tech_activity.csv', index=False)

print(f"✓ github_tech_activity.csv created ({len(github_df):,} events)")
print()

# Show statistics
print("   Event distribution:")
for event, count in github_df['event_type'].value_counts().items():
    print(f"      {event}: {count:,}")
print()

print("   Top 5 organizations:")
for org, count in github_df['organization'].value_counts().head(5).items():
    print(f"      {org}: {count:,} events")
print()

print("   Programming languages:")
for lang, count in github_df['language'].value_counts().head(5).items():
    print(f"      {lang}: {count:,}")
print()

# ================================================================
# VERIFY ALL FILES
# ================================================================
print("=" * 70)
print("✅ FILE CREATION COMPLETE!")
print("=" * 70)
print()
print("Checking all required files:")
print()

required_files = [
    'google_analytics_ecommerce.csv',
    'iowa_retail_sales.csv',
    'nyc_taxi_services.csv',
    'github_tech_activity.csv',
    'customer_summary.csv'
]

files_found = 0
for filename in required_files:
    if os.path.exists(filename):
        df = pd.read_csv(filename)
        print(f"   ✓ {filename:<35} {len(df):>6,} rows")
        files_found += 1
    else:
        print(f"   ✗ {filename:<35} MISSING")

print()
print(f"Files ready: {files_found}/5")
print()

if files_found == 5:
    print("🎉 ALL FILES READY FOR STREAMLIT DEMO!")
    print()
    print("Next step: Build Streamlit demo application")
else:
    print("⚠️  Some files are missing.")
    if not os.path.exists('google_analytics_ecommerce.csv'):
        print("   Run: python download_bigquery_data.py")
    print()