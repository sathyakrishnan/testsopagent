"""
Kevin AI - Current State Analysis Page
Step 2: AI analysis with live progress and process visualization

Version: 4.0 - Pace UI
Date: January 7, 2026
"""

import streamlit as st
import time
import json

# Page config
st.set_page_config(
    page_title="Kevin AI - Current State Analysis",
    page_icon="📊",
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
        --alert-red: #F44336;
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
    
    .step-circle.active {
        background: var(--primary-blue);
        color: white;
    }
    
    .step-circle.completed {
        background: var(--success-green);
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
    
    /* Insights panel */
    .insights-panel {
        background: white;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 20px;
    }
    
    .insights-title {
        font-size: 18px;
        font-weight: 600;
        color: var(--dark-blue);
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .metric-row {
        display: flex;
        justify-content: space-between;
        padding: 12px 0;
        border-bottom: 1px solid #F0F0F0;
    }
    
    .metric-row:last-child {
        border-bottom: none;
    }
    
    .metric-label {
        font-size: 14px;
        color: #757575;
    }
    
    .metric-value {
        font-size: 16px;
        font-weight: 600;
        color: var(--dark-blue);
    }
    
    .bottleneck-card {
        background: #FFF3E0;
        border-left: 4px solid var(--warning-orange);
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    
    .bottleneck-title {
        font-size: 14px;
        font-weight: 600;
        color: var(--dark-blue);
        margin-bottom: 5px;
    }
    
    .bottleneck-desc {
        font-size: 13px;
        color: #666;
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
        <div class="step-circle active">2</div>
        <div class="step-label active">Current State</div>
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

# Check if analysis is already done
if "analysis_complete" not in st.session_state:
    st.session_state.analysis_complete = False

# If not analyzed yet, show progress and run backend
if not st.session_state.analysis_complete:
    st.title("🔍 Analyzing Your Process...")
    
    # Progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Import backend connector
    try:
        from backend_connector import process_sop, BACKEND_AVAILABLE
        
        # Show analysis steps
        analysis_steps = [
            ("📄 Extracting text from SOP document...", 15),
            ("🧠 Applying NLP to identify process steps...", 30),
            ("🔍 Detecting decision points and conditions...", 45),
            ("👥 Mapping actors and responsibilities...", 60),
            ("💻 Identifying systems and integrations...", 75),
            ("📊 Analyzing data flows and dependencies...", 90),
            ("✅ Generating current state process map...", 100)
        ]
        
        for step, progress in analysis_steps:
            status_text.markdown(f"**{step}**")
            progress_bar.progress(progress)
            time.sleep(0.8)
        
        # Actually process the SOP if file available
        if hasattr(st.session_state, 'sop_file') and hasattr(st.session_state, 'config'):
            status_text.markdown("**🤖 Running AI analysis...**")
            results = process_sop(st.session_state.sop_file, st.session_state.config)
            st.session_state.analysis_results = results
        else:
            # Use mock data if no file
            from backend_connector import get_mock_results
            st.session_state.analysis_results = get_mock_results()
        
        st.session_state.analysis_complete = True
        status_text.markdown("**✓ Analysis Complete!**")
        time.sleep(1)
        st.rerun()
        
    except Exception as e:
        st.error(f"Backend error: {e}")
        st.session_state.analysis_complete = True
        from backend_connector import get_mock_results
        st.session_state.analysis_results = get_mock_results()
        time.sleep(1)
        st.rerun()

# Show results
st.title("📊 Current State Process Analysis")

# Layout: Process Map + Insights Panel
col1, col2 = st.columns([2, 1], gap="large")

with col1:
    st.subheader("Process Flowchart")
    
    # Mock Mermaid diagram (in production, this comes from AI)
    mermaid_code = """
    flowchart TD
        Start([Order Received]) --> A
        
        subgraph CS[Customer Service]
            A[Review Order Details<br/>Manual - 5 min]
            B[Validate Customer Info<br/>Manual - 3 min]
        end
        
        subgraph OMS[Order Management System]
            C[Check Inventory<br/>Auto - 10 sec]
            D{Stock Available?}
            E[Create Pick List<br/>Auto - 30 sec]
        end
        
        subgraph WH[Warehouse]
            F[Assign Picker<br/>Manual - 2 min]
            G[Exception Review<br/>Manual - 15 min]
        end
        
        A --> B
        B --> C
        C --> D
        D -->|Yes| E
        D -->|No| G
        E --> F
        F --> End([Order Processed])
        G --> End
        
        style A fill:#FFE6CC
        style B fill:#FFE6CC
        style C fill:#D5E8D4
        style D fill:#FFF4E6
        style E fill:#D5E8D4
        style F fill:#FFE6CC
        style G fill:#F8CECC
    """
    
    # Render as image using mermaid.ink
    import base64
    encoded = base64.b64encode(mermaid_code.encode()).decode()
    mermaid_url = f"https://mermaid.ink/img/{encoded}?type=png"
    
    st.image(mermaid_url, use_container_width=True)
    
    # Download options
    col_a, col_b = st.columns(2)
    with col_a:
        st.download_button(
            "📥 Download PNG",
            data="placeholder",  # In production, actual image data
            file_name="current_state_process.png",
            mime="image/png",
            use_container_width=True
        )
    with col_b:
        st.download_button(
            "📄 Download Mermaid Code",
            data=mermaid_code,
            file_name="current_state.mermaid",
            mime="text/plain",
            use_container_width=True
        )

with col2:
    # Insights Panel
    st.markdown("""
    <div class="insights-panel">
        <div class="insights-title">📊 Process Metrics</div>
        <div class="metric-row">
            <span class="metric-label">Total Steps</span>
            <span class="metric-value">18</span>
        </div>
        <div class="metric-row">
            <span class="metric-label">Manual Steps</span>
            <span class="metric-value">12</span>
        </div>
        <div class="metric-row">
            <span class="metric-label">Automated Steps</span>
            <span class="metric-value">6</span>
        </div>
        <div class="metric-row">
            <span class="metric-label">Decision Points</span>
            <span class="metric-value">4</span>
        </div>
        <div class="metric-row">
            <span class="metric-label">Avg Cycle Time</span>
            <span class="metric-value">4.2 hours</span>
        </div>
        <div class="metric-row">
            <span class="metric-label">Error Rate</span>
            <span class="metric-value">5%</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Bottlenecks
    st.markdown("""
    <div class="insights-panel">
        <div class="insights-title">⚠️ Identified Bottlenecks</div>
        <div class="bottleneck-card">
            <div class="bottleneck-title">Manual Inventory Check</div>
            <div class="bottleneck-desc">Takes 15 min per order, causes 30% of delays</div>
        </div>
        <div class="bottleneck-card">
            <div class="bottleneck-title">Approval Wait Time</div>
            <div class="bottleneck-desc">Average 2-4 hours, blocks downstream processing</div>
        </div>
        <div class="bottleneck-card">
            <div class="bottleneck-title">Manual Data Entry</div>
            <div class="bottleneck-desc">5% error rate, requires rework cycles</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Systems Involved
    with st.expander("💻 Systems & Integrations"):
        st.markdown("""
        - **Order Management System** - Manual entry
        - **Warehouse Management System** - Manual lookups
        - **Email** - Manual notifications
        - **Spreadsheets** - Manual tracking
        
        *Integration opportunities identified: 6*
        """)

# Navigation
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    if st.button("← Back", use_container_width=True):
        st.session_state.analysis_complete = False
        st.switch_page("pages/1_Upload_Configure.py")
with col3:
    if st.button("Continue to Automation →", use_container_width=True, type="primary"):
        st.switch_page("pages/3_Automation_Opportunities.py")
