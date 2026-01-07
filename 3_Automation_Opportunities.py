"""
Kevin AI - Automation Opportunities Page
Step 3: Display opportunities with Pace-style before/after cards

Version: 4.0 - Pace UI
Date: January 7, 2026
"""

import streamlit as st

# Page config
st.set_page_config(
    page_title="Kevin AI - Automation Opportunities",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    :root {
        --primary-blue: #0066FF;
        --dark-blue: #001F3F;
        --success-green: #00C853;
        --warning-orange: #FF9800;
    }
    
    .progress-stepper {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 30px 0 50px 0;
        padding: 20px;
        background: white;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .step-item {
        flex: 1;
        text-align: center;
    }
    
    .step-circle {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        margin: 0 auto 8px auto;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
    }
    
    .step-circle.completed {
        background: var(--success-green);
        color: white;
    }
    
    .step-circle.active {
        background: var(--primary-blue);
        color: white;
    }
    
    .step-circle.inactive {
        background: #E0E0E0;
        color: #9E9E9E;
    }
    
    /* Opportunity cards */
    .opportunity-card {
        background: white;
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        padding: 30px;
        margin-bottom: 25px;
        transition: transform 0.2s;
    }
    
    .opportunity-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.12);
    }
    
    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }
    
    .opp-id {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .priority-badge {
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }
    
    .priority-p0 {
        background: #FFEBEE;
        color: #C62828;
    }
    
    .priority-p1 {
        background: #FFF3E0;
        color: #E65100;
    }
    
    .opp-title {
        font-size: 20px;
        font-weight: 600;
        color: var(--dark-blue);
        margin: 10px 0 20px 0;
    }
    
    .savings-badge {
        font-size: 24px;
        font-weight: 700;
        color: var(--success-green);
    }
    
    /* Before/After comparison */
    .comparison-container {
        display: grid;
        grid-template-columns: 1fr auto 1fr;
        gap: 20px;
        margin: 25px 0;
        align-items: center;
    }
    
    .state-box {
        background: #F8F9FA;
        border-radius: 8px;
        padding: 20px;
    }
    
    .state-label {
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #757575;
        margin-bottom: 10px;
    }
    
    .state-method {
        font-size: 16px;
        font-weight: 600;
        color: var(--dark-blue);
        margin-bottom: 15px;
    }
    
    .state-metric {
        display: flex;
        align-items: center;
        gap: 8px;
        margin: 8px 0;
        font-size: 14px;
        color: #424242;
    }
    
    .arrow-icon {
        font-size: 32px;
        color: var(--primary-blue);
    }
    
    .metrics-row {
        display: flex;
        gap: 30px;
        margin: 20px 0;
        padding: 15px 0;
        border-top: 1px solid #E0E0E0;
        border-bottom: 1px solid #E0E0E0;
    }
    
    .metric-item {
        display: flex;
        flex-direction: column;
    }
    
    .metric-label-small {
        font-size: 12px;
        color: #757575;
        margin-bottom: 4px;
    }
    
    .metric-value-small {
        font-size: 16px;
        font-weight: 600;
        color: var(--dark-blue);
    }
    
    /* Summary box */
    .summary-box {
        background: linear-gradient(135deg, #001F3F 0%, #0066FF 100%);
        color: white;
        padding: 30px;
        border-radius: 12px;
        margin: 30px 0;
    }
    
    .summary-title {
        font-size: 24px;
        font-weight: 700;
        margin-bottom: 20px;
    }
    
    .summary-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
    }
    
    .summary-metric {
        text-align: center;
    }
    
    .summary-value {
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 5px;
    }
    
    .summary-label {
        font-size: 14px;
        opacity: 0.9;
    }
</style>
""", unsafe_allow_html=True)

# Progress Stepper
st.markdown("""
<div class="progress-stepper">
    <div class="step-item">
        <div class="step-circle completed">✓</div>
        <div class="step-label">Upload & Configure</div>
    </div>
    <div class="step-item">
        <div class="step-circle completed">✓</div>
        <div class="step-label">Current State</div>
    </div>
    <div class="step-item">
        <div class="step-circle active">3</div>
        <div class="step-label active">Automation</div>
    </div>
    <div class="step-item">
        <div class="step-circle inactive">4</div>
        <div class="step-label">Future State</div>
    </div>
    <div class="step-item">
        <div class="step-circle inactive">5</div>
        <div class="step-label">Test & Code</div>
    </div>
    <div class="step-item">
        <div class="step-circle inactive">6</div>
        <div class="step-label">ROI Summary</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Header
st.title("🤖 Automation Opportunities")
st.markdown("**8 opportunities identified** | Potential savings: **$524,000/year** | Avg payback: **8.7 months**")

# Filters
col1, col2, col3, col4 = st.columns(4)
with col1:
    filter_priority = st.selectbox("Priority", ["All", "P0 - Quick Wins", "P1", "P2"])
with col2:
    filter_type = st.selectbox("Type", ["All", "API Integration", "RPA", "Agentic AI", "Workflow"])
with col3:
    filter_complexity = st.selectbox("Complexity", ["All", "Low", "Medium", "High"])
with col4:
    st.write("")  # Spacer
    st.write("")
    show_details = st.checkbox("Show Technical Details", value=True)

st.markdown("<br>", unsafe_allow_html=True)

# Opportunity Cards (Mock data - in production comes from AI)
opportunities = [
    {
        "id": "AUTO-001",
        "priority": "P0",
        "title": "Automate Inventory Availability Check",
        "current_method": "Warehouse Manager",
        "current_desc": "Manual WMS Lookup",
        "current_time": "60 sec/order",
        "current_error": "5% error rate",
        "future_method": "Real-time API Call",
        "future_desc": "Automated Response",
        "future_time": "2 sec/order",
        "future_error": "0.1% error rate",
        "type": "API Integration",
        "complexity": "Medium",
        "payback": "6.4 months",
        "savings": "$47,112",
        "impact": "42% cycle time reduction"
    },
    {
        "id": "AUTO-002",
        "priority": "P0",
        "title": "Intelligent Order Routing with Agentic AI",
        "current_method": "Customer Service Rep",
        "current_desc": "Manual Classification",
        "current_time": "8 min/order",
        "current_error": "12% misrouting",
        "future_method": "AI Agent Analysis",
        "future_desc": "Automated Routing",
        "future_time": "15 sec/order",
        "future_error": "1% misrouting",
        "type": "Agentic AI",
        "complexity": "High",
        "payback": "9.2 months",
        "savings": "$89,340",
        "impact": "68% faster routing, 92% accuracy improvement"
    },
    {
        "id": "AUTO-003",
        "priority": "P1",
        "title": "Automated Order Confirmation Emails",
        "current_method": "Customer Service",
        "current_desc": "Manual Email Composition",
        "current_time": "3 min/order",
        "current_error": "2% errors",
        "future_method": "Template Engine",
        "future_desc": "Auto-generated Emails",
        "future_time": "5 sec/order",
        "future_error": "0.1% errors",
        "type": "Workflow Automation",
        "complexity": "Low",
        "payback": "4.1 months",
        "savings": "$28,600",
        "impact": "95% time reduction"
    }
]

for opp in opportunities:
    st.markdown(f"""
    <div class="opportunity-card">
        <div class="card-header">
            <div class="opp-id">
                <span class="priority-badge priority-{opp['priority'].lower()}">{opp['priority']} - QUICK WIN</span>
                <span style="color: #757575; font-size: 14px;">{opp['id']}</span>
            </div>
            <div class="savings-badge">{opp['savings']}/year</div>
        </div>
        
        <div class="opp-title">{opp['title']}</div>
        
        <div class="comparison-container">
            <div class="state-box">
                <div class="state-label">Current State</div>
                <div class="state-method">{opp['current_method']}</div>
                <div class="state-metric">⏱️ {opp['current_time']}</div>
                <div class="state-metric">⚠️ {opp['current_error']}</div>
                <div class="state-metric">👤 {opp['current_desc']}</div>
            </div>
            
            <div class="arrow-icon">→</div>
            
            <div class="state-box" style="background: #E8F5E9;">
                <div class="state-label">Future State</div>
                <div class="state-method">{opp['future_method']}</div>
                <div class="state-metric">⚡ {opp['future_time']}</div>
                <div class="state-metric">✅ {opp['future_error']}</div>
                <div class="state-metric">🤖 {opp['future_desc']}</div>
            </div>
        </div>
        
        <div class="metrics-row">
            <div class="metric-item">
                <span class="metric-label-small">TYPE</span>
                <span class="metric-value-small">{opp['type']}</span>
            </div>
            <div class="metric-item">
                <span class="metric-label-small">COMPLEXITY</span>
                <span class="metric-value-small">{opp['complexity']}</span>
            </div>
            <div class="metric-item">
                <span class="metric-label-small">PAYBACK</span>
                <span class="metric-value-small">{opp['payback']}</span>
            </div>
            <div class="metric-item">
                <span class="metric-label-small">IMPACT</span>
                <span class="metric-value-small">{opp['impact']}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if show_details:
        with st.expander(f"📋 Technical Details - {opp['id']}"):
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("**Implementation Approach:**")
                st.markdown("- Develop REST API connector to WMS")
                st.markdown("- Implement real-time inventory query")
                st.markdown("- Add caching layer for performance")
                st.markdown("- Build error handling & retry logic")
            with col_b:
                st.markdown("**Resources Required:**")
                st.markdown("- Backend Developer (4 weeks)")
                st.markdown("- QA Engineer (2 weeks)")
                st.markdown("- Business Analyst (1 week)")
                st.markdown("- Implementation cost: $25,000")

# Summary Section
st.markdown("""
<div class="summary-box">
    <div class="summary-title">💰 Total Automation Impact</div>
    <div class="summary-grid">
        <div class="summary-metric">
            <div class="summary-value">$524K</div>
            <div class="summary-label">Annual Savings</div>
        </div>
        <div class="summary-metric">
            <div class="summary-value">8</div>
            <div class="summary-label">Opportunities</div>
        </div>
        <div class="summary-metric">
            <div class="summary-value">8.7 mo</div>
            <div class="summary-label">Avg Payback</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Breakdown by type
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("🤖 Agentic AI", "3 opportunities", "$234K savings")
with col2:
    st.metric("🔌 API Integration", "3 opportunities", "$212K savings")
with col3:
    st.metric("🔄 RPA", "2 opportunities", "$78K savings")

# Navigation
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    if st.button("← Back", use_container_width=True):
        st.switch_page("pages/2_Current_State.py")
with col3:
    if st.button("Continue to Future State →", use_container_width=True, type="primary"):
        st.switch_page("pages/4_Future_State.py")
