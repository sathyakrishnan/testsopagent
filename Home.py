"""
Kevin AI - Home Page
Pace-inspired landing page with hero section

Version: 4.0 - Pace UI
Date: January 7, 2026
"""

import streamlit as st
from pathlib import Path

# Page config
st.set_page_config(
    page_title="Kevin AI - Transform SOPs to Automation",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS - Pace-inspired design
st.markdown("""
<style>
    /* Pace color scheme */
    :root {
        --primary-blue: #0066FF;
        --dark-blue: #001F3F;
        --success-green: #00C853;
        --warning-orange: #FF9800;
        --alert-red: #F44336;
        --neutral-gray: #F5F7FA;
        --text-dark: #1A1A1A;
        --text-gray: #757575;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Hero section */
    .hero-container {
        background: linear-gradient(135deg, #001F3F 0%, #0066FF 100%);
        padding: 80px 40px;
        border-radius: 12px;
        margin-bottom: 40px;
        color: white;
        text-align: center;
    }
    
    .hero-title {
        font-size: 48px;
        font-weight: 700;
        margin-bottom: 20px;
        line-height: 1.2;
    }
    
    .hero-subtitle {
        font-size: 24px;
        font-weight: 400;
        margin-bottom: 30px;
        opacity: 0.9;
    }
    
    .hero-description {
        font-size: 18px;
        max-width: 700px;
        margin: 0 auto 40px auto;
        line-height: 1.6;
        opacity: 0.8;
    }
    
    /* Value props */
    .value-prop-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 30px;
        margin: 50px 0;
    }
    
    .value-prop-card {
        background: white;
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        text-align: center;
        transition: transform 0.2s;
    }
    
    .value-prop-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 16px rgba(0,0,0,0.15);
    }
    
    .value-prop-icon {
        font-size: 48px;
        margin-bottom: 20px;
    }
    
    .value-prop-title {
        font-size: 20px;
        font-weight: 600;
        margin-bottom: 10px;
        color: var(--dark-blue);
    }
    
    .value-prop-desc {
        font-size: 16px;
        color: var(--text-gray);
        line-height: 1.5;
    }
    
    /* Process steps */
    .process-steps {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 60px 0;
        padding: 40px;
        background: var(--neutral-gray);
        border-radius: 12px;
    }
    
    .process-step {
        flex: 1;
        text-align: center;
        padding: 20px;
    }
    
    .step-number {
        display: inline-block;
        width: 50px;
        height: 50px;
        background: var(--primary-blue);
        color: white;
        border-radius: 50%;
        line-height: 50px;
        font-size: 24px;
        font-weight: 700;
        margin-bottom: 15px;
    }
    
    .step-title {
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 8px;
        color: var(--dark-blue);
    }
    
    .step-desc {
        font-size: 14px;
        color: var(--text-gray);
    }
    
    .step-arrow {
        font-size: 32px;
        color: var(--primary-blue);
        opacity: 0.5;
    }
    
    /* CTA Button */
    .cta-button {
        background: var(--primary-blue);
        color: white;
        padding: 16px 48px;
        border-radius: 8px;
        font-size: 18px;
        font-weight: 600;
        border: none;
        cursor: pointer;
        transition: all 0.3s;
        text-decoration: none;
        display: inline-block;
    }
    
    .cta-button:hover {
        background: #0052CC;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,102,255,0.4);
    }
    
    /* Stats section */
    .stats-container {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 20px;
        margin: 40px 0;
    }
    
    .stat-card {
        background: white;
        padding: 25px;
        border-radius: 8px;
        border-left: 4px solid var(--primary-blue);
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .stat-value {
        font-size: 36px;
        font-weight: 700;
        color: var(--primary-blue);
        margin-bottom: 5px;
    }
    
    .stat-label {
        font-size: 14px;
        color: var(--text-gray);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-container">
    <div class="hero-title">Transform SOPs to Intelligent Automation</div>
    <div class="hero-subtitle">The AI-native platform for enterprise process optimization</div>
    <div class="hero-description">
        Kevin AI analyzes your standard operating procedures and identifies automation 
        opportunities with measurable ROI. From manual processes to intelligent workflows 
        in minutes, not months.
    </div>
</div>
""", unsafe_allow_html=True)

# CTA Button - Navigate to Upload page
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🚀 Start Your Analysis", use_container_width=True, type="primary"):
        st.switch_page("pages/1_Upload_Configure.py")

# Value Propositions
st.markdown("""
<div class="value-prop-container">
    <div class="value-prop-card">
        <div class="value-prop-icon">🔍</div>
        <div class="value-prop-title">AI-Powered Analysis</div>
        <div class="value-prop-desc">
            Advanced NLP and process mining to extract every step, decision point, 
            and automation opportunity from your SOPs
        </div>
    </div>
    
    <div class="value-prop-card">
        <div class="value-prop-icon">💰</div>
        <div class="value-prop-title">Measurable ROI</div>
        <div class="value-prop-desc">
            Precise cost savings calculations with payback periods, 3-year NPV, 
            and implementation roadmaps
        </div>
    </div>
    
    <div class="value-prop-card">
        <div class="value-prop-icon">🚀</div>
        <div class="value-prop-title">Production-Ready</div>
        <div class="value-prop-desc">
            Generate test cases, production code, and deployment guides—not just 
            recommendations
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Process Steps (Pace-style: Intake → Reason → Act)
st.markdown("""
<div class="process-steps">
    <div class="process-step">
        <div class="step-number">1</div>
        <div class="step-title">Upload & Configure</div>
        <div class="step-desc">Upload your SOP document and configure process context</div>
    </div>
    
    <div class="step-arrow">→</div>
    
    <div class="process-step">
        <div class="step-number">2</div>
        <div class="step-title">AI Analysis</div>
        <div class="step-desc">Identify steps, bottlenecks, and automation opportunities</div>
    </div>
    
    <div class="step-arrow">→</div>
    
    <div class="process-step">
        <div class="step-number">3</div>
        <div class="step-title">Generate Deliverables</div>
        <div class="step-desc">Receive process maps, test cases, code, and ROI analysis</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Stats Section
st.markdown("### Why Kevin AI?")
st.markdown("""
<div class="stats-container">
    <div class="stat-card">
        <div class="stat-value">45%</div>
        <div class="stat-label">Avg Cycle Time Reduction</div>
    </div>
    
    <div class="stat-card">
        <div class="stat-value">$524K</div>
        <div class="stat-label">Avg Annual Savings</div>
    </div>
    
    <div class="stat-card">
        <div class="stat-value">8.7</div>
        <div class="stat-label">Months Payback Period</div>
    </div>
    
    <div class="stat-card">
        <div class="stat-value">92%</div>
        <div class="stat-label">Test Coverage Achieved</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Trusted By Section
st.markdown("---")
st.markdown("### Trusted By Industry Leaders")
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.markdown("🏢 **Logistics**")
with col2:
    st.markdown("🏥 **Healthcare**")
with col3:
    st.markdown("🏦 **Finance**")
with col4:
    st.markdown("📞 **Telecom**")
with col5:
    st.markdown("🏭 **Manufacturing**")

# Footer CTA
st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("Get Started Now →", use_container_width=True, type="primary"):
        st.switch_page("pages/1_Upload_Configure.py")

# Footer
st.markdown("""
<div style="text-align: center; padding: 40px 0 20px 0; color: var(--text-gray); font-size: 14px;">
    <p>Kevin AI - Enterprise SOP Automation Platform | Version 4.0</p>
    <p>© 2026 XYZ Consulting. Powered by GPT-4o and LangGraph</p>
</div>
""", unsafe_allow_html=True)
