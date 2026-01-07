"""
Kevin AI - Upload & Configure Page
Step 1: Upload SOP and configure context

Version: 4.1 - Fixed CSS
Date: January 7, 2026
"""

import streamlit as st
from pathlib import Path
import time

# Page config
st.set_page_config(
    page_title="Kevin AI - Upload & Configure",
    page_icon="📤",
    layout="wide"
)

# Minimal CSS using st.html()
st.html("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""")

# Progress indicator
st.markdown("### Step 1 of 6: Upload & Configure")
st.progress(0.17)

st.markdown("---")

# Initialize session state
if "sop_uploaded" not in st.session_state:
    st.session_state.sop_uploaded = False
if "process_diagram_uploaded" not in st.session_state:
    st.session_state.process_diagram_uploaded = False

# Split Layout using columns
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("## Transform Your SOPs to Intelligent Automation")
    st.markdown("""
    Kevin AI analyzes your standard operating procedures and identifies 
    automation opportunities with measurable ROI. Minutes, not months.
    """)
    
    st.markdown("**Key Features:**")
    st.markdown("- ✓ AI-Powered Process Analysis")
    st.markdown("- ✓ Automated Opportunity Detection")
    st.markdown("- ✓ Test Case Generation")
    st.markdown("- ✓ Production-Ready Code")
    st.markdown("- ✓ Comprehensive ROI Metrics")
    
    st.info("💡 **Demo Tip:** Use the sample SOP file `sample_sop_cars_commerce.md` to see Kevin AI in action!")

with col2:
    st.markdown("### 📄 Upload SOP Document")
    
    sop_file = st.file_uploader(
        "Upload your Standard Operating Procedure",
        type=["pdf", "docx", "md", "txt"],
        help="Supported formats: PDF, DOCX, Markdown, Text"
    )
    
    if sop_file:
        st.session_state.sop_uploaded = True
        st.session_state.sop_file = sop_file
        file_size = len(sop_file.getvalue()) / 1024
        st.success(f"✓ {sop_file.name} ({file_size:.1f} KB)")
    
    st.markdown("### 🖼️ Process Diagram (Optional)")
    
    diagram_file = st.file_uploader(
        "Upload existing process diagram if available",
        type=["png", "jpg", "jpeg", "mermaid"],
        help="Optional: Existing process flowchart"
    )
    
    if diagram_file:
        st.session_state.process_diagram_uploaded = True
        st.session_state.diagram_file = diagram_file
        st.success(f"✓ {diagram_file.name}")
    
    st.markdown("### ⚙️ Process Configuration")
    
    # Industry selection
    industry = st.selectbox(
        "Industry Vertical",
        [
            "Logistics & Supply Chain",
            "Insurance & Financial Services",
            "Healthcare & Life Sciences",
            "Manufacturing",
            "Retail & E-commerce",
            "Telecommunications",
            "Professional Services"
        ]
    )
    
    # Process type
    process_type = st.selectbox(
        "Process Type",
        [
            "Order Processing",
            "Claims Management",
            "Customer Onboarding",
            "Invoice Processing",
            "Compliance Review",
            "Inventory Management",
            "Quality Control",
            "Service Delivery"
        ]
    )
    
    # ERP System
    erp_system = st.selectbox(
        "ERP/System",
        [
            "SAP",
            "Oracle",
            "Microsoft Dynamics",
            "Workday",
            "NetSuite",
            "Salesforce",
            "Custom/Other",
            "None"
        ]
    )
    
    # Risk sensitivity
    risk_profile = st.selectbox(
        "Risk Sensitivity",
        [
            "Low - Non-critical operations",
            "Medium - Standard business processes",
            "High - Compliance-sensitive",
            "Critical - Mission-critical operations"
        ],
        index=1
    )

# Action Buttons
st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    if st.button("← Back to Home", use_container_width=True):
        st.switch_page("Home.py")

with col3:
    if st.session_state.sop_uploaded:
        if st.button("🚀 Analyze Process →", use_container_width=True, type="primary"):
            # Save configuration
            st.session_state.config = {
                "industry": industry,
                "process_type": process_type,
                "erp_system": erp_system,
                "risk_profile": risk_profile
            }
            
            with st.spinner("🔄 Initializing AI analysis..."):
                time.sleep(1)
            
            st.success("✓ Configuration saved!")
            time.sleep(1)
            st.switch_page("pages/2_Current_State.py")
    else:
        st.button("🚀 Analyze Process →", use_container_width=True, type="primary", disabled=True)
        st.caption("⚠️ Please upload an SOP document to continue")
