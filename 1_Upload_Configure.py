"""
Kevin AI - Upload & Configure Page
Step 1: Upload SOP and configure context

Version: 4.0 - Pace UI
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

# Import custom CSS
st.markdown("""
<style>
    :root {
        --primary-blue: #0066FF;
        --dark-blue: #001F3F;
        --success-green: #00C853;
        --neutral-gray: #F5F7FA;
    }
    
    /* Progress stepper */
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
        position: relative;
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
        font-size: 16px;
    }
    
    .step-circle.active {
        background: var(--primary-blue);
        color: white;
    }
    
    .step-circle.inactive {
        background: #E0E0E0;
        color: #9E9E9E;
    }
    
    .step-label {
        font-size: 12px;
        color: #757575;
    }
    
    .step-label.active {
        color: var(--primary-blue);
        font-weight: 600;
    }
    
    /* Split layout */
    .split-container {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 40px;
        margin-top: 30px;
    }
    
    .left-panel {
        padding: 40px;
    }
    
    .right-panel {
        background: white;
        padding: 40px;
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    }
    
    .section-title {
        font-size: 32px;
        font-weight: 700;
        color: var(--dark-blue);
        margin-bottom: 20px;
    }
    
    .section-subtitle {
        font-size: 18px;
        color: #757575;
        line-height: 1.6;
        margin-bottom: 30px;
    }
    
    .feature-list {
        list-style: none;
        padding: 0;
    }
    
    .feature-item {
        font-size: 16px;
        color: #424242;
        margin-bottom: 12px;
        padding-left: 30px;
        position: relative;
    }
    
    .feature-item:before {
        content: "✓";
        position: absolute;
        left: 0;
        color: var(--success-green);
        font-weight: 700;
        font-size: 18px;
    }
    
    /* Upload zone */
    .upload-section {
        margin-bottom: 30px;
    }
    
    .upload-title {
        font-size: 16px;
        font-weight: 600;
        color: var(--dark-blue);
        margin-bottom: 10px;
    }
    
    .file-uploaded {
        background: #E8F5E9;
        border: 2px solid var(--success-green);
        border-radius: 8px;
        padding: 12px 16px;
        margin-top: 10px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .file-info {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .file-size {
        font-size: 12px;
        color: #666;
    }
    
    /* Configuration section */
    .config-section {
        background: var(--neutral-gray);
        padding: 20px;
        border-radius: 8px;
        margin-top: 30px;
    }
    
    .config-title {
        font-size: 18px;
        font-weight: 600;
        color: var(--dark-blue);
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Progress Stepper
st.markdown("""
<div class="progress-stepper">
    <div class="step-item">
        <div class="step-circle active">1</div>
        <div class="step-label active">Upload & Configure</div>
    </div>
    <div class="step-item">
        <div class="step-circle inactive">2</div>
        <div class="step-label">Current State</div>
    </div>
    <div class="step-item">
        <div class="step-circle inactive">3</div>
        <div class="step-label">Automation</div>
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

# Initialize session state
if "sop_uploaded" not in st.session_state:
    st.session_state.sop_uploaded = False
if "process_diagram_uploaded" not in st.session_state:
    st.session_state.process_diagram_uploaded = False

# Split Layout
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("""
    <div class="left-panel">
        <div class="section-title">Transform Your SOPs to Intelligent Automation</div>
        <div class="section-subtitle">
            Kevin AI analyzes your standard operating procedures and identifies 
            automation opportunities with measurable ROI. Minutes, not months.
        </div>
        <ul class="feature-list">
            <li class="feature-item">AI-Powered Process Analysis</li>
            <li class="feature-item">Automated Opportunity Detection</li>
            <li class="feature-item">Test Case Generation</li>
            <li class="feature-item">Production-Ready Code</li>
            <li class="feature-item">Comprehensive ROI Metrics</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Demo instructions
    st.info("💡 **Demo Tip:** Use the sample SOP file `sample_sop_cars_commerce.md` to see Kevin AI in action!")

with col2:
    st.markdown('<div class="right-panel">', unsafe_allow_html=True)
    
    # SOP Document Upload
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    st.markdown('<div class="upload-title">📄 Upload SOP Document *</div>', unsafe_allow_html=True)
    
    sop_file = st.file_uploader(
        "Upload your Standard Operating Procedure",
        type=["pdf", "docx", "md", "txt"],
        help="Supported formats: PDF, DOCX, Markdown, Text",
        label_visibility="collapsed"
    )
    
    if sop_file:
        st.session_state.sop_uploaded = True
        st.session_state.sop_file = sop_file
        file_size = len(sop_file.getvalue()) / 1024  # KB
        st.markdown(f"""
        <div class="file-uploaded">
            <div class="file-info">
                <span>✓</span>
                <div>
                    <div><strong>{sop_file.name}</strong></div>
                    <div class="file-size">{file_size:.1f} KB</div>
                </div>
            </div>
            <div>📄</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Process Diagram Upload (Optional)
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    st.markdown('<div class="upload-title">🖼️ Process Diagram (Optional)</div>', unsafe_allow_html=True)
    
    diagram_file = st.file_uploader(
        "Upload existing process diagram if available",
        type=["png", "jpg", "jpeg", "mermaid"],
        help="Optional: Existing process flowchart or diagram",
        label_visibility="collapsed"
    )
    
    if diagram_file:
        st.session_state.process_diagram_uploaded = True
        st.session_state.diagram_file = diagram_file
        st.markdown(f"""
        <div class="file-uploaded">
            <div class="file-info">
                <span>✓</span>
                <div><strong>{diagram_file.name}</strong></div>
            </div>
            <div>🖼️</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Configuration Section
    st.markdown('<div class="config-section">', unsafe_allow_html=True)
    st.markdown('<div class="config-title">⚙️ Process Configuration</div>', unsafe_allow_html=True)
    
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
        ],
        help="Select the industry for context-aware analysis"
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
        ],
        help="Type of business process being analyzed"
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
        ],
        help="Primary ERP or system used in this process"
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
        index=1,
        help="Risk profile affects automation recommendations"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Action Button
st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.session_state.sop_uploaded:
        if st.button("🚀 Analyze Process →", use_container_width=True, type="primary"):
            # Save configuration to session state
            st.session_state.config = {
                "industry": industry,
                "process_type": process_type,
                "erp_system": erp_system,
                "risk_profile": risk_profile
            }
            
            # Show loading animation
            with st.spinner("🔄 Initializing AI analysis..."):
                time.sleep(1)
            
            st.success("✓ Configuration saved! Redirecting to analysis...")
            time.sleep(1)
            st.switch_page("pages/2_Current_State.py")
    else:
        st.button("🚀 Analyze Process →", use_container_width=True, type="primary", disabled=True)
        st.caption("⚠️ Please upload an SOP document to continue")

# Back to Home
st.markdown("<br><br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    if st.button("← Back to Home", use_container_width=True):
        st.switch_page("Home.py")
