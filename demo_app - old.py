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
# ASK AI FEATURE (REAL CLAUDE API - FREE-FORM QUESTIONS)
# ================================================================
st.sidebar.markdown("---")
st.sidebar.markdown("### 💬 Ask AI About Your Data")
st.sidebar.markdown("Ask ANY question about your data:")
st.sidebar.markdown("""
Examples:
- *Who are my top 10 customers by revenue?*
- *Which customers stopped ordering?*
- *What was the best sales day and why?*
- *Compare mobile vs desktop revenue*
- *Show me trends over time*
- *How can I increase revenue?*
""")

# Initialize Claude client (with error handling)
try:
    import anthropic
    ANTHROPIC_API_KEY = st.secrets.get("ANTHROPIC_API_KEY", "")
    if ANTHROPIC_API_KEY:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        api_available = True
    else:
        api_available = False
except Exception as e:
    api_available = False
    st.sidebar.warning("⚠️ Configure Claude API in .streamlit/secrets.toml for AI features")

user_question = st.sidebar.text_input("Your question:", placeholder="Ask anything about your data...")

# Initialize session state for storing response
if 'last_response' not in st.session_state:
    st.session_state.last_response = ""

if user_question:
    with st.sidebar:
        with st.spinner('🤖 Claude is analyzing your data...'):
            
            if api_available:
                try:
                    # Get current dataset
                    if "E-commerce" in demo_company:
                        df = data['ecommerce']
                        customers = data['customers']
                        
                        # Create data summary
                        data_summary = f"""
                        E-COMMERCE DATA SUMMARY:
                        
                        Overall Metrics:
                        - Total Revenue: {df['revenue_sek'].sum():,.0f} SEK
                        - Total Transactions: {df['transactions'].sum():,.0f}
                        - Unique Customers: {df['customer_id'].nunique():,.0f}
                        - Average Order Value: {df['revenue_sek'].sum() / df['transactions'].sum():,.0f} SEK
                        
                        Traffic Sources (by revenue):
                        {df.groupby('traffic_source')['revenue_sek'].sum().sort_values(ascending=False).to_dict()}
                        
                        Device Types:
                        {df['device_type'].value_counts().to_dict()}
                        
                        Top Countries:
                        {df['country'].value_counts().head(5).to_dict()}
                        
                        Customer Summary (Top 10 by revenue):
                        {customers.nlargest(10, 'total_revenue_sek')[['customer_id', 'total_revenue_sek', 'total_transactions', 'total_sessions', 'country']].to_string()}
                        """
                        
                    elif "Retail" in demo_company:
                        df = data['retail']
                        df['date'] = pd.to_datetime(df['date'])
                        
                        data_summary = f"""
                        RETAIL SALES DATA SUMMARY:
                        
                        Overall Metrics:
                        - Total Sales: {df['order_amount_sek'].sum():,.0f} SEK
                        - Total Orders: {len(df):,.0f}
                        - Average Order: {df['order_amount_sek'].mean():,.0f} SEK
                        - Unique Stores: {df['customer_id'].nunique():,.0f}
                        
                        Top Product Categories:
                        {df.groupby('product_category')['order_amount_sek'].sum().sort_values(ascending=False).head(10).to_dict()}
                        
                        Top Cities:
                        {df['city'].value_counts().head(10).to_dict()}
                        
                        Daily Sales (Top 5 days):
                        {df.groupby('date')['order_amount_sek'].sum().sort_values(ascending=False).head(5).to_dict()}
                        """
                        
                    elif "Service" in demo_company:
                        df = data['services']
                        
                        data_summary = f"""
                        SERVICE BUSINESS DATA SUMMARY:
                        
                        Overall Metrics:
                        - Total Revenue: {df['total_amount_sek'].sum():,.0f} SEK
                        - Total Trips: {len(df):,.0f}
                        - Average Fare: {df['fare_amount_sek'].mean():,.0f} SEK
                        - Average Distance: {df['trip_distance'].mean():.2f} km
                        
                        Payment Types:
                        {df['payment_type'].value_counts().to_dict()}
                        
                        Trip Distance Distribution:
                        - Short (<5 km): {len(df[df['trip_distance'] < 5])}
                        - Medium (5-15 km): {len(df[(df['trip_distance'] >= 5) & (df['trip_distance'] < 15)])}
                        - Long (15+ km): {len(df[df['trip_distance'] >= 15])}
                        """
                        
                    else:  # Tech/SaaS
                        df = data['tech']
                        
                        data_summary = f"""
                        TECH COMPANY DATA SUMMARY:
                        
                        Overall Metrics:
                        - Total Events: {len(df):,.0f}
                        - Active Developers: {df['user_id'].nunique():,.0f}
                        - Active Projects: {df['project_name'].nunique():,.0f}
                        - Total Commits: {df[df['commits_count'].notna()]['commits_count'].sum():,.0f}
                        
                        Event Types:
                        {df['event_type'].value_counts().to_dict()}
                        
                        Top Organizations:
                        {df['organization'].value_counts().head(10).to_dict()}
                        
                        Programming Languages:
                        {df['language'].value_counts().to_dict()}
                        """
                    
                    # Call Claude API
                    message = client.messages.create(
                        model="claude-sonnet-4-20250514",
                        max_tokens=1500,
                        messages=[{
                            "role": "user",
                            "content": f"""
You are an expert business analyst analyzing data for a Swedish company. 

DATA AVAILABLE:
{data_summary}

USER QUESTION: {user_question}

Provide a detailed, actionable answer with:
1. Direct answer to their question with specific numbers from the data
2. Key insights (2-3 bullet points)
3. One concrete recommendation

Use Swedish Kronor (SEK) for all currency values.
Be concise but thorough. Format with markdown for readability.
If asking about specific customers, reference the data provided.
If asking about trends, analyze the patterns in the data.
Always provide actionable insights, not just data summaries.
"""
                        }]
                    )
                    
                    response_text = message.content[0].text
                    
                    # Store response in session state for export
                    st.session_state.last_response = response_text
                    
                    st.markdown("**Claude's Analysis:**")
                    st.info(response_text)
                    
                except Exception as e:
                    st.error(f"❌ API Error: {str(e)}")
                    st.info("💡 Make sure your API key is configured in .streamlit/secrets.toml")
            
            else:
                # Fallback to simulated response
                import time
                time.sleep(1.5)
                
                st.markdown("**AI Response (Demo Mode):**")
                
                question_lower = user_question.lower()
                
                # Quick keyword matching for demo mode
                if any(word in question_lower for word in ['top', 'highest', 'best', 'biggest']):
                    response = """
**Top Customers by Revenue:**

Based on the data, here are your highest-value customers:

1. **Customer 345892** - 487,000 SEK (23 orders)
2. **Customer 892341** - 423,000 SEK (18 orders)
3. **Customer 123456** - 389,000 SEK (31 orders)

💡 **Insight:** Top 10 customers represent 34% of total revenue. Focus retention efforts here.
"""
                
                elif any(word in question_lower for word in ['stop', 'inactive', '90', 'churn']):
                    response = """
**Inactive Customers Analysis:**

23 customers haven't ordered in 90+ days, representing 186,000 SEK at-risk revenue.

**Priority Actions:**
- 5 Enterprise customers (127K SEK) - Personal calls
- 18 Pro customers (59K SEK) - Email campaign

💡 **Expected Recovery:** 65% success rate = 120,000 SEK
"""
                
                elif any(word in question_lower for word in ['sale', 'day', 'date', 'when']):
                    response = """
**Peak Sales Day: November 24, 2023 (Black Friday)**

**Performance:**
- Revenue: 487,000 SEK (+312% vs average)
- Orders: 156
- Conversion: 89%

**Success Factors:**
- 25% discount + free shipping
- LinkedIn ads (best ROI)
- Mobile optimized (78% traffic)

💡 **Recommendation:** Replicate this strategy for next major campaign
"""
                
                else:
                    response = f"""
**Analysis for: "{user_question}"**

Key insights from your data:
- Revenue opportunities: 186,000 SEK identified
- Upsell potential: 216,000 SEK annually
- Cost savings: 186,000 SEK possible

💡 **Configure Claude API** in `.streamlit/secrets.toml` for real AI analysis of any question.

Try asking:
- "Who are my top 10 customers?"
- "Which day had the highest sales?"
- "Compare mobile vs desktop revenue"
"""
                
                st.session_state.last_response = response
                st.info(response)

# EXPORT BUTTON (WORKING VERSION)
if st.session_state.last_response:
    st.sidebar.markdown("---")
    
    # Create downloadable report
    report_content = f"""
AI ANALYTICS REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Industry: {demo_company}

QUESTION:
{user_question}

ANALYSIS:
{st.session_state.last_response}

---
Generated by AI Analytics Platform
Powered by Claude & BigQuery
"""
    
    st.sidebar.download_button(
        label="📥 Download Analysis Report",
        data=report_content,
        file_name=f"ai_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
        mime="text/plain",
        type="primary"
    )

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
    # ============================================================
    # E-COMMERCE DEMO
    # ============================================================
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

elif "Retail" in demo_company:
    # ============================================================
    # RETAIL DEMO
    # ============================================================
    st.markdown("## 🏪 Retail Business Analytics")
    st.markdown("**Data source:** Iowa Liquor Sales (Retail Transactions)")
    st.markdown("")
    
    df = data['retail']
    df['date'] = pd.to_datetime(df['date'])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Sales",
            value=f"{df['order_amount_sek'].sum():,.0f} SEK",
            delta="+7.8%"
        )
    
    with col2:
        st.metric(
            label="Total Orders",
            value=f"{len(df):,.0f}",
            delta="+5.2%"
        )
    
    with col3:
        st.metric(
            label="Avg Order Size",
            value=f"{df['order_amount_sek'].mean():,.0f} SEK",
            delta="+2.1%"
        )
    
    with col4:
        st.metric(
            label="Unique Stores",
            value=f"{df['customer_id'].nunique():,.0f}",
            delta="+12 new"
        )
    
    st.markdown("---")
    st.markdown("### 🤖 AI-Powered Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="insight-box">
        <h4>📦 Inventory Optimization</h4>
        <p><strong>12 products</strong> have 180+ days inventory with <2 units/month sales.</p>
        <p><strong>Capital tied up:</strong> 340,000 SEK</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="action-box">
        <h4>💡 Recommended Action</h4>
        <p>• Discount slow-movers 25-40%<br>
        • Free up 250K SEK capital in 60 days<br>
        • Reinvest in fast-moving categories</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="insight-box">
        <h4>📍 Regional Performance Gap</h4>
        <p><strong>Stockholm region:</strong> 35% higher revenue per store than Göteborg.</p>
        <p><strong>Opportunity:</strong> Apply Stockholm playbook to Göteborg = +180K SEK/month</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="action-box">
        <h4>💡 Recommended Action</h4>
        <p>• Analyze Stockholm product mix<br>
        • Train Göteborg staff on upselling<br>
        • Adjust inventory for regional preferences</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Sales by Product Category")
        category_sales = df.groupby('product_category')['order_amount_sek'].sum().sort_values(ascending=False).head(10)
        fig = px.bar(
            x=category_sales.values,
            y=category_sales.index,
            orientation='h',
            labels={'x': 'Sales (SEK)', 'y': 'Category'},
            color=category_sales.values,
            color_continuous_scale='Greens'
        )
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Sales Trend Over Time")
        daily_sales = df.groupby('date')['order_amount_sek'].sum().reset_index()
        fig = px.line(
            daily_sales,
            x='date',
            y='order_amount_sek',
            labels={'date': 'Date', 'order_amount_sek': 'Daily Sales (SEK)'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

elif "Service" in demo_company:
    # ============================================================
    # SERVICE BUSINESS DEMO
    # ============================================================
    st.markdown("## 🚕 Service Business Analytics")
    st.markdown("**Data source:** NYC Taxi Trips (Service Operations)")
    st.markdown("")
    
    df = data['services']
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Revenue",
            value=f"{df['total_amount_sek'].sum():,.0f} SEK",
            delta="+9.2%"
        )
    
    with col2:
        st.metric(
            label="Total Trips",
            value=f"{len(df):,.0f}",
            delta="+6.7%"
        )
    
    with col3:
        st.metric(
            label="Avg Fare",
            value=f"{df['fare_amount_sek'].mean():,.0f} SEK",
            delta="+1.8%"
        )
    
    with col4:
        st.metric(
            label="Avg Trip Distance",
            value=f"{df['trip_distance'].mean():.1f} km",
            delta="-0.3 km"
        )
    
    st.markdown("---")
    st.markdown("### 🤖 AI-Powered Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="insight-box">
        <h4>⚡ Route Optimization</h4>
        <p><strong>3 vehicles</strong> drive 48% of distance but only 22% of trips (inefficient routes).</p>
        <p><strong>Waste:</strong> 89,000 SEK/month in fuel</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="action-box">
        <h4>💡 Recommended Action</h4>
        <p>• Implement route planning software (24K/year)<br>
        • Reduce distance 15-20%<br>
        • Save 80-107K SEK/year in fuel</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="insight-box">
        <h4>💳 Payment Method Insight</h4>
        <p><strong>Cash payments:</strong> 12% of trips but 40% longer processing time.</p>
        <p><strong>Cost:</strong> 45K SEK/month in lost productivity</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="action-box">
        <h4>💡 Recommended Action</h4>
        <p>• Incentivize card/mobile payments (2% discount)<br>
        • Reduce cash handling by 60%<br>
        • Save 27K SEK/month in admin costs</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Revenue by Payment Type")
        payment_revenue = df.groupby('payment_type')['total_amount_sek'].sum().sort_values(ascending=False)
        fig = px.bar(
            x=payment_revenue.index,
            y=payment_revenue.values,
            labels={'x': 'Payment Type', 'y': 'Revenue (SEK)'},
            color=payment_revenue.values,
            color_continuous_scale='Oranges'
        )
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Trip Distance Distribution")
        fig = px.histogram(
            df,
            x='trip_distance',
            nbins=50,
            labels={'trip_distance': 'Trip Distance (km)', 'count': 'Number of Trips'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

else:  # Tech/SaaS
    # ============================================================
    # TECH/SAAS DEMO
    # ============================================================
    st.markdown("## 💻 Tech Company Analytics")
    st.markdown("**Data source:** GitHub Activity (Developer Productivity)")
    st.markdown("")
    
    df = data['tech']
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Events",
            value=f"{len(df):,.0f}",
            delta="+18.3%"
        )
    
    with col2:
        st.metric(
            label="Active Developers",
            value=f"{df['user_id'].nunique():,.0f}",
            delta="+3 new"
        )
    
    with col3:
        st.metric(
            label="Active Projects",
            value=f"{df['project_name'].nunique():,.0f}",
            delta="+7 new"
        )
    
    with col4:
        commits = df[df['commits_count'].notna()]['commits_count'].sum()
        st.metric(
            label="Total Commits",
            value=f"{commits:,.0f}",
            delta="+12.1%"
        )
    
    st.markdown("---")
    st.markdown("### 🤖 AI-Powered Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="insight-box">
        <h4>👥 Team Productivity Gap</h4>
        <p><strong>Top 20% developers</strong> complete 3× more PRs than average.</p>
        <p><strong>Opportunity:</strong> Share best practices = +40% team output</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="action-box">
        <h4>💡 Recommended Action</h4>
        <p>• Analyze top performer workflows<br>
        • Create internal training program<br>
        • Expected productivity gain: 35-45%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="insight-box">
        <h4>🔧 Tech Debt Accumulation</h4>
        <p><strong>23% of PRs</strong> are bug fixes vs 11% industry average.</p>
        <p><strong>Cost:</strong> 180K SEK/month in rework</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="action-box">
        <h4>💡 Recommended Action</h4>
        <p>• Implement code review checklist<br>
        • Increase test coverage to 80%<br>
        • Reduce bug rate by 40% = 72K SEK/month saved</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Activity by Event Type")
        event_counts = df['event_type'].value_counts()
        fig = px.pie(
            values=event_counts.values,
            names=event_counts.index,
            hole=0.3,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Top Organizations by Activity")
        org_activity = df['organization'].value_counts().head(10)
        fig = px.bar(
            x=org_activity.values,
            y=org_activity.index,
            orientation='h',
            labels={'x': 'Number of Events', 'y': 'Organization'},
            color=org_activity.values,
            color_continuous_scale='Purples'
        )
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)

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