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

# Custom CSS using st.html() - Fix for Streamlit 1.42+ 
st.html("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Hero section styling */
    [data-testid="stMarkdownContainer"] h1 {
        font-size: 48px !important;
        font-weight: 700 !important;
        margin-bottom: 20px !important;
        line-height: 1.2 !important;
    }
</style>
""")

# Hero Section using native Streamlit
st.title("🚀 Transform SOPs to Intelligent Automation")
st.subheader("The AI-native platform for enterprise process optimization")
st.markdown("""
Kevin AI analyzes your standard operating procedures and identifies automation 
opportunities with measurable ROI. From manual processes to intelligent workflows 
in minutes, not months.
""")

st.markdown("<br>", unsafe_allow_html=True)

# CTA Button - Navigate to Upload page
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🚀 Start Your Analysis", use_container_width=True, type="primary"):
        st.switch_page("pages/1_Upload_Configure.py")

st.markdown("<br>", unsafe_allow_html=True)

# Value Propositions using columns
st.markdown("### Key Benefits")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### 🔍 AI-Powered Analysis")
    st.markdown("""
    Advanced NLP and process mining to extract every step, decision point, 
    and automation opportunity from your SOPs
    """)

with col2:
    st.markdown("#### 💰 Measurable ROI")
    st.markdown("""
    Precise cost savings calculations with payback periods, 3-year NPV, 
    and implementation roadmaps
    """)

with col3:
    st.markdown("#### 🚀 Production-Ready")
    st.markdown("""
    Generate test cases, production code, and deployment guides—not just 
    recommendations
    """)

st.markdown("<br>", unsafe_allow_html=True)

# Process Steps using columns
st.markdown("### How It Works")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### 1️⃣ Upload & Configure")
    st.markdown("Upload your SOP document and configure process context")

with col2:
    st.markdown("#### 2️⃣ AI Analysis")
    st.markdown("Identify steps, bottlenecks, and automation opportunities")

with col3:
    st.markdown("#### 3️⃣ Generate Deliverables")
    st.markdown("Receive process maps, test cases, code, and ROI analysis")

st.markdown("<br>", unsafe_allow_html=True)

# Stats Section using metrics
st.markdown("### Why Kevin AI?")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Avg Cycle Time Reduction", "45%")
with col2:
    st.metric("Avg Annual Savings", "$524K")
with col3:
    st.metric("Months Payback Period", "8.7")
with col4:
    st.metric("Test Coverage Achieved", "92%")

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
st.markdown("---")
st.caption("Kevin AI - Enterprise SOP Automation Platform | Version 4.0")
st.caption("© 2026 XYZ Consulting. Powered by GPT-4o and LangGraph")
