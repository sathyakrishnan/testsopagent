"""Kevin AI - ROI Summary Page - Version 4.0"""
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Kevin AI - ROI Summary", page_icon="💰", layout="wide")
st.markdown("### Step 6 of 6: Executive ROI Summary")
st.progress(1.0)

st.title("💰 Executive ROI Summary")
st.markdown("**SOP Automation Business Case**")

# Before/After Comparison
st.subheader("📊 Before vs After")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("##### BEFORE")
    st.metric("Avg Cycle Time", "4.2 hrs")
    st.metric("Cost/Transaction", "$35")
    st.metric("Error Rate", "5%")
    st.metric("Manual Steps", "12")
with col2:
    st.markdown("##### AFTER")
    st.metric("Avg Cycle Time", "2.3 hrs", "-45%")
    st.metric("Cost/Transaction", "$12", "-66%")
    st.metric("Error Rate", "0.5%", "-90%")
    st.metric("Manual Steps", "2", "-83%")
with col3:
    st.markdown("##### IMPROVEMENT")
    st.metric("Time Saved", "1.9 hrs", "+82%")
    st.metric("Cost Reduced", "$23", "+66%")
    st.metric("Quality Up", "4.5%", "+90%")
    st.metric("Automation", "10 steps", "+83%")

# Financial Summary
st.markdown("---")
st.subheader("💵 Financial Impact")
col1, col2 = st.columns([2,1])
with col1:
    st.markdown("""
    | Metric | Value |
    |--------|-------|
    | **Annual Cost Savings** | $524,000 |
    | **Implementation Cost** | $380,000 |
    | **Payback Period** | 8.7 months |
    | **3-Year ROI** | 313% |
    | **3-Year NPV** | $1,195,000 |
    """)
with col2:
    st.info("""
    **Quick Wins (P0):**
    - 4 opportunities
    - $234K savings
    - 6.4 month payback
    """)

# Automation Breakdown
st.markdown("---")
st.subheader("🤖 Automation Breakdown")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Agentic AI", "3 opportunities", "$234K/year")
with col2:
    st.metric("API Integration", "3 opportunities", "$212K/year")
with col3:
    st.metric("RPA", "2 opportunities", "$78K/year")

# Implementation Roadmap
st.markdown("---")
st.subheader("📅 Next Steps")
st.markdown("""
**Phase 1 (Weeks 1-8):** API Integration - $47K quick win  
**Phase 2 (Weeks 9-16):** Workflow Automation - $156K impact  
**Phase 3 (Weeks 17-24):** Agentic AI - $321K impact  
""")

# Export Options
st.markdown("---")
st.subheader("📤 Export & Share")
col1, col2, col3 = st.columns(3)
with col1:
    # Mock PDF content
    pdf_content = f"""
KEVIN AI - SOP AUTOMATION BUSINESS CASE
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

EXECUTIVE SUMMARY
- Annual Savings: $524,000
- Payback Period: 8.7 months
- 3-Year ROI: 313%

PROCESS IMPROVEMENTS
- Cycle Time: 4.2hrs → 2.3hrs (-45%)
- Cost/Transaction: $35 → $12 (-66%)
- Error Rate: 5% → 0.5% (-90%)

AUTOMATION OPPORTUNITIES
1. Inventory API Integration - $47K/year
2. AI Order Routing - $89K/year
3. Email Automation - $28K/year
[... 5 more opportunities]

IMPLEMENTATION ROADMAP
Phase 1 (Q1): Quick Wins - $47K
Phase 2 (Q2): Workflows - $156K
Phase 3 (Q3): AI Agents - $321K
    """
    
    st.download_button(
        "📄 Download PDF Report",
        data=pdf_content,
        file_name=f"Kevin_AI_ROI_Summary_{datetime.now().strftime('%Y%m%d')}.txt",
        mime="text/plain",
        use_container_width=True
    )
with col2:
    st.download_button(
        "📧 Email to Stakeholders",
        data="mailto:?subject=Kevin AI ROI Summary&body=See attached report",
        file_name="share.html",
        use_container_width=True
    )
with col3:
    st.button("🔗 Generate Share Link", use_container_width=True)

# Call to Action
st.markdown("---")
st.success("""
### 🎯 Ready to Transform Your Operations?

**This analysis shows $524K in annual savings with 8.7 month payback.**

Next Steps:
1. Review this report with your CFO
2. Schedule implementation kickoff
3. Start with Phase 1 quick wins
""")

col1, col2, col3 = st.columns([1,2,1])
with col1:
    st.button("← Back", use_container_width=True, on_click=lambda: st.switch_page("pages/5_Test_Cases.py"))
with col2:
    st.button("📞 Schedule Implementation Call", use_container_width=True, type="primary")
with col3:
    st.button("🏠 New Analysis", use_container_width=True, on_click=lambda: st.switch_page("Home.py"))
