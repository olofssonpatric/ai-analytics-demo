"""
AI Analytics Demo Platform
Professional demo for sales presentations
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import io

# ================================================================
# PAGE CONFIG
# ================================================================
st.set_page_config(
    page_title="AI Analytics Platform Demo",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================================================================
# CUSTOM CSS
# ================================================================
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-top: 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    .insight-box {
        background-color: #fff3cd;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #ffc107;
        margin: 10px 0;
    }
    .action-box {
        background-color: #d4edda;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #28a745;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ================================================================
# LOAD DATA (with caching for performance)
# ================================================================
@st.cache_data
def load_data():
    """Load all demo datasets"""
    data = {}
    
    try:
        data['ecommerce'] = pd.read_csv('google_analytics_ecommerce.csv')
        data['customers'] = pd.read_csv('customer_summary.csv')
        data['retail'] = pd.read_csv('iowa_retail_sales.csv')
        data['services'] = pd.read_csv('nyc_taxi_services.csv')
        data['tech'] = pd.read_csv('github_tech_activity.csv')
    except FileNotFoundError as e:
        st.error(f"❌ Missing data file: {e}")
        st.stop()
    
    return data

data = load_data()

# ================================================================
# SIDEBAR - Company Selector
# ================================================================
st.sidebar.markdown("### 🏢 Demo Company Selector")
st.sidebar.markdown("---")

demo_company = st.sidebar.selectbox(
    "Choose Industry:",
    ["E-commerce (Google Analytics)", 
     "Retail (Iowa Liquor Sales)", 
     "Service Business (NYC Taxi)",
     "Tech/SaaS (GitHub Activity)"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Demo Features")
st.sidebar.markdown("""
- **Real-time Insights**: AI-powered analytics
- **Revenue Opportunities**: Upsell detection
- **Churn Prevention**: At-risk customers
- **Cost Optimization**: Hidden savings
- **Team Performance**: Productivity metrics
""")

# ================================================================
# INITIALIZE CLAUDE API
# ================================================================
try:
    import anthropic
    ANTHROPIC_API_KEY = st.secrets.get("ANTHROPIC_API_KEY", "")
    
    if ANTHROPIC_API_KEY and ANTHROPIC_API_KEY.startswith("sk-ant"):
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        api_available = True
        st.sidebar.success("✅ Claude API Active")
    else:
        api_available = False
        st.sidebar.warning("⚠️ Demo Mode (Configure API key in Settings → Secrets)")
except Exception as e:
    api_available = False
    st.sidebar.error(f"❌ API Error: {str(e)}")

# ================================================================
# ASK AI FEATURE (REAL CLAUDE API)
# ================================================================
st.sidebar.markdown("---")
st.sidebar.markdown("### 💬 Ask AI About Your Data")
st.sidebar.markdown("Try asking:")
st.sidebar.markdown("""
- *Who are my top 5 customers?*
- *Which customers stopped ordering?*
- *What was my best sales day?*
- *Compare mobile vs desktop revenue*
- *How can I increase revenue?*
""")

# Initialize session state for storing response
if 'last_response' not in st.session_state:
    st.session_state.last_response = ""
if 'last_question' not in st.session_state:
    st.session_state.last_question = ""

user_question = st.sidebar.text_input("Your question:", placeholder="Ask anything about your data...")

if user_question:
    with st.sidebar:
        with st.spinner('🤖 Claude is analyzing your data...'):
            
            if api_available:
                try:
                    # Get current dataset and create rich context
                    if "E-commerce" in demo_company:
                        df = data['ecommerce']
                        customers = data['customers']
                        
                        # Create comprehensive data summary
                        top_customers = customers.nlargest(10, 'total_revenue_sek')
                        traffic_sources = df.groupby('traffic_source')['revenue_sek'].sum().sort_values(ascending=False)
                        device_breakdown = df['device_type'].value_counts()
                        
                        context = f"""
E-COMMERCE DATA ANALYSIS

OVERALL METRICS:
- Total Revenue: {df['revenue_sek'].sum():,.0f} SEK
- Total Transactions: {df['transactions'].sum():,.0f}
- Unique Customers: {df['customer_id'].nunique():,.0f}
- Average Order Value: {df['revenue_sek'].sum() / df['transactions'].sum():,.0f} SEK

TOP 10 CUSTOMERS BY REVENUE:
{top_customers[['customer_id', 'total_revenue_sek', 'total_transactions', 'total_sessions', 'country']].to_string(index=False)}

TRAFFIC SOURCE PERFORMANCE (by revenue):
{traffic_sources.to_dict()}

DEVICE TYPE BREAKDOWN:
{device_breakdown.to_dict()}

TOP COUNTRIES:
{df['country'].value_counts().head(5).to_dict()}
"""
                        
                    elif "Retail" in demo_company:
                        df = data['retail']
                        df['date'] = pd.to_datetime(df['date'])
                        
                        top_categories = df.groupby('product_category')['order_amount_sek'].sum().sort_values(ascending=False).head(10)
                        daily_sales = df.groupby('date')['order_amount_sek'].sum().sort_values(ascending=False).head(10)
                        
                        context = f"""
RETAIL SALES DATA ANALYSIS

OVERALL METRICS:
- Total Sales: {df['order_amount_sek'].sum():,.0f} SEK
- Total Orders: {len(df):,.0f}
- Average Order Size: {df['order_amount_sek'].mean():,.0f} SEK
- Unique Stores: {df['customer_id'].nunique():,.0f}

TOP 10 PRODUCT CATEGORIES BY SALES:
{top_categories.to_dict()}

TOP 10 CITIES BY NUMBER OF ORDERS:
{df['city'].value_counts().head(10).to_dict()}

BEST PERFORMING DAYS (Top 10):
{daily_sales.to_dict()}
"""
                        
                    elif "Service" in demo_company:
                        df = data['services']
                        
                        payment_breakdown = df.groupby('payment_type')['total_amount_sek'].sum().sort_values(ascending=False)
                        
                        context = f"""
SERVICE BUSINESS DATA ANALYSIS

OVERALL METRICS:
- Total Revenue: {df['total_amount_sek'].sum():,.0f} SEK
- Total Trips/Services: {len(df):,.0f}
- Average Fare: {df['fare_amount_sek'].mean():,.0f} SEK
- Average Distance: {df['trip_distance'].mean():.2f} km

PAYMENT TYPE BREAKDOWN (by revenue):
{payment_breakdown.to_dict()}

TRIP DISTANCE ANALYSIS:
- Short trips (<5 km): {len(df[df['trip_distance'] < 5]):,} trips
- Medium trips (5-15 km): {len(df[(df['trip_distance'] >= 5) & (df['trip_distance'] < 15)]):,} trips
- Long trips (15+ km): {len(df[df['trip_distance'] >= 15]):,} trips

AVERAGE METRICS:
- Avg fare per km: {df['fare_amount_sek'].sum() / df['trip_distance'].sum():.0f} SEK/km
- Avg trip duration estimate: {df['trip_distance'].mean() * 3:.0f} minutes
"""
                        
                    else:  # Tech/SaaS
                        df = data['tech']
                        
                        event_breakdown = df['event_type'].value_counts()
                        top_orgs = df['organization'].value_counts().head(10)
                        language_breakdown = df['language'].value_counts()
                        
                        context = f"""
TECH COMPANY DATA ANALYSIS

OVERALL METRICS:
- Total Events: {len(df):,.0f}
- Active Developers: {df['user_id'].nunique():,.0f}
- Active Projects: {df['project_name'].nunique():,.0f}
- Active Organizations: {df['organization'].nunique():,.0f}
- Total Commits: {df[df['commits_count'].notna()]['commits_count'].sum():,.0f}

EVENT TYPE BREAKDOWN:
{event_breakdown.to_dict()}

TOP 10 ORGANIZATIONS BY ACTIVITY:
{top_orgs.to_dict()}

PROGRAMMING LANGUAGES USED:
{language_breakdown.to_dict()}

DEVELOPER PRODUCTIVITY:
- Avg events per developer: {len(df) / df['user_id'].nunique():.1f}
- Avg commits per developer: {df[df['commits_count'].notna()]['commits_count'].sum() / df['user_id'].nunique():.1f}
"""
                    
                    # Call Claude API with comprehensive prompt
                    message = client.messages.create(
                        model="claude-sonnet-4-20250514",
                        max_tokens=2000,
                        messages=[{
                            "role": "user",
                            "content": f"""You are an expert business analyst helping a Swedish company analyze their data.

DATA CONTEXT:
{context}

USER QUESTION: {user_question}

Provide a comprehensive, actionable answer that includes:

1. **Direct Answer**: Answer the specific question with concrete numbers from the data above
2. **Key Insights**: Provide 2-3 data-driven insights related to the question
3. **Actionable Recommendation**: Give one specific, implementable recommendation

Format your response in clear sections using markdown. Use Swedish Kronor (SEK) for all currency. Be specific with numbers and percentages. Make recommendations concrete and actionable.

If the question asks about specific customers, use the customer data provided. If asking about trends, analyze patterns in the data. Always ground your analysis in the actual data provided."""
                        }]
                    )
                    
                    response_text = message.content[0].text
                    
                    # Store response in session state
                    st.session_state.last_response = response_text
                    st.session_state.last_question = user_question
                    
                    st.markdown("**Claude's Analysis:**")
                    st.success(response_text)
                    
                except Exception as e:
                    st.error(f"❌ API Error: {str(e)}")
                    st.info("💡 Make sure your API key is configured correctly in Settings → Secrets")
            
            else:
                # Demo mode with better keyword matching
                import time
                time.sleep(1.5)
                
                st.markdown("**AI Analysis (Demo Mode):**")
                
                q = user_question.lower()
                
                # Smart keyword-based responses
                if any(word in q for word in ['top', 'highest', 'best', 'biggest', 'most revenue']):
                    if "E-commerce" in demo_company:
                        top_5 = data['customers'].nlargest(5, 'total_revenue_sek')
                        response = "**Top 5 Customers by Revenue:**\n\n"
                        for i, row in top_5.iterrows():
                            response += f"**{i+1}. Customer {row['customer_id'][-8:]}**\n"
                            response += f"- Total Revenue: {row['total_revenue_sek']:,.0f} SEK\n"
                            response += f"- Orders: {int(row['total_transactions'])}\n"
                            response += f"- Sessions: {int(row['total_sessions'])}\n"
                            response += f"- Country: {row['country']}\n\n"
                        
                        response += f"\n**Insight:** Top 5 customers represent {top_5['total_revenue_sek'].sum():,.0f} SEK ({top_5['total_revenue_sek'].sum()/data['customers']['total_revenue_sek'].sum()*100:.1f}% of total revenue)\n\n"
                        response += "**Recommendation:** Implement VIP program for these customers with dedicated account manager."
                    else:
                        response = "Switch to E-commerce dataset for detailed customer analysis."
                
                elif any(word in q for word in ['stop', 'inactive', 'churn', 'left']):
                    response = """**Inactive Customer Analysis:**

23 customers haven't ordered in 90+ days, representing **186,000 SEK** at-risk revenue.

**Breakdown:**
- **5 Enterprise customers:** 127,000 SEK annually
- **18 Pro customers:** 59,000 SEK annually

**Recommended Actions:**
1. Personal outreach to Enterprise tier (phone calls this week)
2. Automated email campaign to Pro tier (15% discount offer)
3. Survey to identify reasons for inactivity

**Expected Recovery:** 65% success rate = 120,000 SEK saved

💡 **Configure Claude API for real-time analysis of your actual data.**"""
                
                elif any(word in q for word in ['sale', 'day', 'date', 'best', 'highest']):
                    response = """**Peak Sales Day Analysis:**

**Best Day:** November 24, 2023 (Black Friday)

**Performance:**
- Revenue: **487,000 SEK** (+312% vs daily average)
- Orders: 156
- Conversion Rate: 89%

**Success Factors:**
1. **Promotion:** 25% discount + free shipping
2. **Marketing:** LinkedIn ads performed best (156K SEK revenue)
3. **Timing:** Peak hours 08:00-10:00 and 20:00-22:00
4. **Device:** 78% mobile traffic (optimized UX paid off)

**Recommendation:** Replicate this strategy for next major campaign. Focus budget on LinkedIn, optimize for mobile, and target morning/evening time slots."""
                
                else:
                    response = f"""**Analysis for: "{user_question}"**

Based on the available data:
- **Revenue Opportunities:** 186,000 SEK at-risk customers identified
- **Upsell Potential:** 216,000 SEK annually from Basic → Pro upgrades
- **Cost Savings:** 186,000 SEK in unused subscriptions

💡 **For detailed analysis of this specific question, configure Claude API in Settings → Secrets**

**Try asking:**
- "Who are my top 5 customers?"
- "Which customers stopped ordering?"
- "What was my best sales day?"
"""
                
                st.session_state.last_response = response
                st.session_state.last_question = user_question
                st.info(response)

# ================================================================
# EXPORT OPTIONS (IMPROVED)
# ================================================================
if st.session_state.last_response:
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📥 Export Analysis")
    
    col1, col2 = st.sidebar.columns(2)
    
    # Excel Export
    with col1:
        # Create structured data for Excel
        export_data = {
            'Timestamp': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            'Industry': [demo_company],
            'Question': [st.session_state.last_question],
            'AI Analysis': [st.session_state.last_response],
            'Mode': ['Claude API' if api_available else 'Demo Mode']
        }
        
        df_export = pd.DataFrame(export_data)
        
        # Create Excel file in memory
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            df_export.to_excel(writer, index=False, sheet_name='AI Analysis')
            
            # Add some formatting
            worksheet = writer.sheets['AI Analysis']
            worksheet.column_dimensions['A'].width = 20
            worksheet.column_dimensions['B'].width = 30
            worksheet.column_dimensions['C'].width = 40
            worksheet.column_dimensions['D'].width = 60
            worksheet.column_dimensions['E'].width = 15
        
        st.download_button(
            label="📊 Excel",
            data=excel_buffer.getvalue(),
            file_name=f"ai_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            help="Download as Excel spreadsheet"
        )
    
    # Text Export
    with col2:
        report_text = f"""AI ANALYTICS REPORT
{'=' * 60}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Industry: {demo_company}
Analysis Mode: {'Claude API' if api_available else 'Demo Mode'}

QUESTION:
{st.session_state.last_question}

{'=' * 60}

ANALYSIS:
{st.session_state.last_response}

{'=' * 60}

Generated by AI Analytics Platform
Powered by Claude & BigQuery
Contact: your-email@company.com
"""
        
        st.download_button(
            label="📄 Text",
            data=report_text,
            file_name=f"ai_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            help="Download as text file"
        )

st.sidebar.markdown("---")
st.sidebar.info("💡 **Demo Mode**: This uses sample data. Your actual data would show here in production.")

# ================================================================
# HEADER
# ================================================================
st.markdown('<p class="main-header">📊 AI-Driven Data Analytics Platform</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Automated insights from your business data • Updated in real-time</p>', unsafe_allow_html=True)
st.markdown("---")

# ================================================================
# MAIN CONTENT - Based on Selected Company
# ================================================================

if "E-commerce" in demo_company:
    # [Keep all your existing E-commerce demo code - don't change]
    st.markdown("## 🛒 E-commerce Business Analytics")
    st.markdown("**Data source:** Google Analytics (Google Merchandise Store)")
    st.markdown("")
    
    df = data['ecommerce']
    customers = data['customers']
    
    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Revenue",
            value=f"{df['revenue_sek'].sum():,.0f} SEK",
            delta="+12.5% vs last month"
        )
    
    with col2:
        st.metric(
            label="Total Transactions",
            value=f"{df['transactions'].sum():,.0f}",
            delta="+8.2%"
        )
    
    with col3:
        avg_order = df['revenue_sek'].sum() / df['transactions'].sum()
        st.metric(
            label="Avg Order Value",
            value=f"{avg_order:,.0f} SEK",
            delta="+3.7%"
        )
    
    with col4:
        st.metric(
            label="Unique Customers",
            value=f"{df['customer_id'].nunique():,.0f}",
            delta="+15.3%"
        )
    
    st.markdown("---")
    
    # AI INSIGHTS SECTION
    st.markdown("### 🤖 AI-Powered Insights (Updated Daily)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="insight-box">
        <h4>⚠️ Revenue Leakage Detected</h4>
        <p><strong>23 customers</strong> who ordered monthly in Q1-Q3 haven't ordered in 90+ days.</p>
        <p><strong>At-risk revenue:</strong> 186,000 SEK annually</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="action-box">
        <h4>💡 Recommended Action</h4>
        <p>• Send re-engagement email with 15% discount<br>
        • Prioritize 5 Enterprise-tier customers this week<br>
        • Expected recovery: 120,000 SEK (65%)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="insight-box">
        <h4>💰 Upsell Opportunity</h4>
        <p><strong>12 customers</strong> on Basic plan show Pro usage patterns (10+ users, 500+ API calls/day).</p>
        <p><strong>Upsell potential:</strong> 220,000 SEK annually</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="action-box">
        <h4>💡 Recommended Action</h4>
        <p>• Schedule "optimization review" calls<br>
        • Highlight Pro features they need<br>
        • Offer 2-month trial at current price</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # CHARTS
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Revenue by Traffic Source")
        
        source_revenue = df.groupby('traffic_source')['revenue_sek'].sum().sort_values(ascending=False)
        
        fig = px.bar(
            x=source_revenue.index,
            y=source_revenue.values,
            labels={'x': 'Traffic Source', 'y': 'Revenue (SEK)'},
            color=source_revenue.values,
            color_continuous_scale='Blues'
        )
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("💡 **LinkedIn generates 3× higher LTV** than Google Ads. Consider shifting 30% of ad budget to LinkedIn.")
    
    with col2:
        st.markdown("#### Device Type Distribution")
        
        device_counts = df['device_type'].value_counts()
        
        fig = px.pie(
            values=device_counts.values,
            names=device_counts.index,
            hole=0.4,
            color_discrete_sequence=['#1f77b4', '#ff7f0e', '#2ca02c']
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("💡 **Mobile users have 40% lower conversion** rate. Mobile UX optimization could add 80K SEK/month.")
    
    # Customer Insights Table
    st.markdown("---")
    st.markdown("#### 🎯 High-Value Customer Insights")
    
    top_customers = customers.nlargest(10, 'total_revenue_sek')[
        ['customer_id', 'total_revenue_sek', 'total_sessions', 'total_transactions', 'first_traffic_source', 'country']
    ]
    top_customers.columns = ['Customer ID', 'Total Revenue (SEK)', 'Sessions', 'Orders', 'Source', 'Country']
    
    st.dataframe(top_customers, use_container_width=True, hide_index=True)

# [Keep all your other industry sections - Retail, Service, Tech - exactly as they are]

elif "Retail" in demo_company:
    st.markdown("## 🏪 Retail Business Analytics")
    # ... rest of retail code stays the same

elif "Service" in demo_company:
    st.markdown("## 🚕 Service Business Analytics")
    # ... rest of service code stays the same

else:  # Tech/SaaS
    st.markdown("## 💻 Tech Company Analytics")
    # ... rest of tech code stays the same

# ================================================================
# FOOTER
# ================================================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p><strong>AI Analytics Platform Demo</strong> • Powered by Claude & BigQuery</p>
    <p>📧 Contact: your-email@company.com • 📱 +46 XXX XXX XXX</p>
</div>
""", unsafe_allow_html=True)