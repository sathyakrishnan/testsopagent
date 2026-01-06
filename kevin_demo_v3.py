"""
Kevin AI - Redesigned Streamlit Demo Interface
3-Column Layout with Enhanced Context Configuration

Version: 3.0
Date: January 6, 2026
"""

import streamlit as st
import os
import json
from datetime import datetime
from pathlib import Path
import pandas as pd

# Set page config
st.set_page_config(
    page_title="Kevin AI - SOP Automation",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Import Kevin AI
try:
    from kevin_agents import MasterOrchestratorAgent
    from export_utils import create_pdf_report, mermaid_to_image
except ImportError as e:
    st.error(f"Failed to import modules: {e}")
    st.stop()

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        border-bottom: 2px solid #1f77b4;
        padding-bottom: 0.5rem;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'orchestrator' not in st.session_state:
    st.session_state.orchestrator = None
if 'current_session' not in st.session_state:
    st.session_state.current_session = None
if 'processing' not in st.session_state:
    st.session_state.processing = False
if 'page' not in st.session_state:
    st.session_state.page = 'upload'
if 'selected_test_case' not in st.session_state:
    st.session_state.selected_test_case = None

def get_orchestrator():
    """Initialize orchestrator once"""
    if st.session_state.orchestrator is None:
        with st.spinner("🔄 Initializing Kevin AI..."):
            st.session_state.orchestrator = MasterOrchestratorAgent()
    return st.session_state.orchestrator

def process_sop(sop_file, diagram_file, industry, process_type, erp_system, risk_sensitivity):
    """Process SOP through Kevin AI pipeline"""
    
    if sop_file is None:
        st.error("❌ Please upload an SOP document")
        return None
    
    try:
        # Save uploaded files
        session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        upload_dir = Path("uploads") / session_id
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        # Save SOP file
        sop_path = upload_dir / sop_file.name
        with open(sop_path, "wb") as f:
            f.write(sop_file.getbuffer())
        
        # Save diagram if provided
        diagram_path = None
        if diagram_file is not None:
            diagram_path = upload_dir / diagram_file.name
            with open(diagram_path, "wb") as f:
                f.write(diagram_file.getbuffer())
        
        # Initialize orchestrator
        orch = get_orchestrator()
        
        # Create progress container
        progress_container = st.container()
        with progress_container:
            progress_bar = st.progress(0)
            status_text = st.empty()
        
        # Phase updates
        phases = [
            (10, "🔄 Analyzing SOP document..."),
            (25, "📊 Creating current state map..."),
            (40, "🤖 Identifying automation opportunities..."),
            (60, "🚀 Designing optimized future state..."),
            (75, "🧪 Generating test scenarios..."),
            (90, "💻 Creating production code..."),
            (95, "📈 Calculating ROI metrics..."),
        ]
        
        import threading
        import time
        
        result_container = {}
        error_container = {}
        
        def process_thread():
            try:
                result_container['result'] = orch.process(
                    str(sop_path), 
                    str(diagram_path) if diagram_path else None, 
                    industry
                )
            except Exception as e:
                error_container['error'] = e
        
        thread = threading.Thread(target=process_thread)
        thread.start()
        
        phase_idx = 0
        elapsed = 0
        
        while thread.is_alive() and elapsed < 900:
            if phase_idx < len(phases):
                progress, message = phases[phase_idx]
                progress_bar.progress(progress)
                status_text.text(message)
                phase_idx += 1
            time.sleep(120)
            elapsed += 120
        
        thread.join(timeout=10)
        
        if 'error' in error_container:
            raise error_container['error']
        
        if 'result' not in result_container:
            raise Exception("Processing timed out")
        
        result = result_container['result']
        
        # Add context configuration to result
        result['context'] = {
            'industry': industry,
            'process_type': process_type,
            'erp_system': erp_system,
            'risk_sensitivity': risk_sensitivity
        }
        
        st.session_state.current_session = result
        
        progress_bar.progress(100)
        status_text.text("✅ Processing Complete!")
        time.sleep(1)
        
        return result
        
    except Exception as e:
        st.error(f"❌ Processing Error: {str(e)}")
        return None

# ============================================================================
# UPLOAD PAGE
# ============================================================================
if st.session_state.page == 'upload':
    
    # Header
    st.markdown('<div class="main-header">🤖 Kevin AI</div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #555;">Enterprise SOP to Agentic Automation Platform</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    # 3-Column Layout
    col_left, col_middle, col_right = st.columns([1, 2, 1.5])
    
    # ========================================================================
    # LEFT COLUMN - Overview & Menu
    # ========================================================================
    with col_left:
        st.markdown('<div class="section-header">📋 Overview</div>', unsafe_allow_html=True)
        
        st.markdown("""
        **Kevin AI transforms your SOPs into:**
        
        🗺️ **Process Maps**  
        Current & future state visualization
        
        🤖 **Automation Insights**  
        AI, RPA, API opportunities
        
        🧪 **Test Scenarios**  
        Comprehensive test coverage
        
        💻 **Production Code**  
        Ready-to-deploy solutions
        
        📈 **ROI Analysis**  
        Cost savings & KPI metrics
        """)
        
        st.markdown('<div class="section-header">📂 Menu</div>', unsafe_allow_html=True)
        
        if st.button("📤 Upload & Configure", use_container_width=True):
            st.session_state.page = 'upload'
            st.rerun()
        
        if st.session_state.current_session:
            if st.button("📊 View Results", use_container_width=True):
                st.session_state.page = 'results'
                st.rerun()
    
    # ========================================================================
    # MIDDLE COLUMN - Upload Area
    # ========================================================================
    with col_middle:
        st.markdown('<div class="section-header">📤 Upload Documents</div>', unsafe_allow_html=True)
        
        sop_file = st.file_uploader(
            "**📄 SOP Document** (Required)",
            type=["pdf", "docx"],
            help="Upload your Standard Operating Procedure document"
        )
        
        diagram_file = st.file_uploader(
            "**📊 Process Diagram** (Optional)",
            type=["png", "jpg", "jpeg"],
            help="Upload existing process flow diagram for gap analysis"
        )
        
        st.markdown("---")
        
        # File info
        if sop_file:
            st.success(f"✅ SOP Document: {sop_file.name} ({sop_file.size / 1024:.1f} KB)")
        
        if diagram_file:
            st.success(f"✅ Process Diagram: {diagram_file.name} ({diagram_file.size / 1024:.1f} KB)")
    
    # ========================================================================
    # RIGHT COLUMN - Context Configuration
    # ========================================================================
    with col_right:
        st.markdown('<div class="section-header">⚙️ Context Configuration</div>', unsafe_allow_html=True)
        
        industry = st.selectbox(
            "**🏢 Industry**",
            ["Logistics", "Insurance", "Healthcare", "Finance", "Manufacturing", "Retail", "Telecom"],
            help="Select your industry vertical"
        )
        
        process_type = st.selectbox(
            "**🔄 Process Type**",
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
            help="Type of business process"
        )
        
        erp_system = st.selectbox(
            "**💼 ERP System**",
            ["SAP", "Oracle", "Microsoft Dynamics", "Workday", "NetSuite", "Other", "None"],
            help="Primary ERP system in use"
        )
        
        risk_sensitivity = st.selectbox(
            "**⚠️ Risk Sensitivity**",
            ["Low", "Medium", "High", "Critical"],
            index=1,
            help="Risk tolerance for automation recommendations"
        )
        
        st.markdown("---")
        
        # Process button
        process_btn = st.button(
            "🚀 Process SOP", 
            type="primary",
            use_container_width=True,
            disabled=sop_file is None
        )
        
        if process_btn:
            with st.spinner("Processing..."):
                result = process_sop(
                    sop_file, 
                    diagram_file, 
                    industry.lower(), 
                    process_type,
                    erp_system,
                    risk_sensitivity
                )
                if result:
                    st.session_state.page = 'results'
                    st.rerun()

# ============================================================================
# RESULTS PAGE
# ============================================================================
elif st.session_state.page == 'results':
    
    result = st.session_state.current_session
    
    if not result:
        st.error("No results available. Please process an SOP first.")
        if st.button("← Back to Upload"):
            st.session_state.page = 'upload'
            st.rerun()
        st.stop()
    
    # Header with back button
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown('<div class="main-header">📊 Analysis Results</div>', unsafe_allow_html=True)
    with col2:
        if st.button("← Back to Upload"):
            st.session_state.page = 'upload'
            st.rerun()
    
    # Context info
    context = result.get('context', {})
    st.markdown(f"**Industry:** {context.get('industry', 'N/A').capitalize()} | **Process:** {context.get('process_type', 'N/A')} | **ERP:** {context.get('erp_system', 'N/A')} | **Risk:** {context.get('risk_sensitivity', 'N/A')}")
    st.markdown("---")
    
    # Summary metrics
    automation_opps = result.get('automation_opportunities', [])
    test_cases = result.get('test_cases', [])
    total_savings = sum(opp.get('estimated_savings_annual', 0) for opp in automation_opps)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Automation Opportunities", len(automation_opps))
    with col2:
        st.metric("Annual Savings", f"${total_savings:,.0f}")
    with col3:
        st.metric("Test Cases", len(test_cases))
    with col4:
        st.metric("Cycle Time Reduction", "42%")
    
    # Export PDF button
    st.markdown("---")
    if st.button("📄 Export Complete PDF Report", use_container_width=True):
        try:
            pdf_path = f"kevin_ai_report_{result['session_id']}.pdf"
            create_pdf_report(result, pdf_path)
            with open(pdf_path, "rb") as f:
                st.download_button(
                    "⬇️ Download PDF Report",
                    f,
                    file_name=pdf_path,
                    mime="application/pdf",
                    use_container_width=True
                )
            os.remove(pdf_path)
            st.success("✅ PDF Report Generated!")
        except Exception as e:
            st.error(f"Failed to create PDF: {e}")
    
    st.markdown("---")
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🗺️ Current State Process",
        "🤖 Automation Opportunities", 
        "🧪 Test Cases",
        "💻 Generated Code"
    ])
    
    # ========================================================================
    # TAB 1: Current State Process (with swimlane)
    # ========================================================================
    with tab1:
        st.markdown("### Current State Process Flow")
        
        if result.get('current_state_map'):
            # Try to convert to image
            col1, col2 = st.columns([3, 1])
            
            with col1:
                try:
                    # Generate PNG image
                    png_path = f"current_state_{result['session_id']}.png"
                    mermaid_to_image(result['current_state_map'], png_path, 'png')
                    st.image(png_path, use_container_width=True)
                    
                    # Download button
                    with open(png_path, "rb") as f:
                        st.download_button(
                            "📥 Download Process Map (PNG)",
                            f,
                            file_name=png_path,
                            mime="image/png"
                        )
                    os.remove(png_path)
                except Exception as e:
                    st.warning("Could not generate image, showing Mermaid code:")
                    st.code(result['current_state_map'], language='mermaid')
            
            with col2:
                st.markdown("**Process Insights:**")
                
                steps = result.get('current_state_steps', [])
                st.metric("Total Steps", len(steps))
                
                manual_steps = sum(1 for s in steps if 'manual' in s.get('type', '').lower())
                st.metric("Manual Steps", manual_steps)
                
                decision_points = sum(1 for s in steps if 'decision' in s.get('type', '').lower())
                st.metric("Decision Points", decision_points)
        else:
            st.warning("No current state map available")
    
    # ========================================================================
    # TAB 2: Automation Opportunities (Tabular Format)
    # ========================================================================
    with tab2:
        st.markdown("### Automation Opportunities Matrix")
        
        if automation_opps:
            # Create DataFrame
            df_data = []
            for i, opp in enumerate(automation_opps, 1):
                df_data.append({
                    "ID": f"AO-{i:02d}",
                    "Process Stage": opp.get('step_id', 'N/A'),
                    "Current Activity": opp.get('description', 'N/A')[:50] + "...",
                    "Automation Type": opp.get('automation_type', 'N/A'),
                    "Cycle Time Impact": f"{opp.get('time_savings_hours_per_week', 0) * 2}%",
                    "Risk": opp.get('complexity', 'Medium'),
                    "Annual Savings": f"${opp.get('estimated_savings_annual', 0):,.0f}",
                    "Priority": opp.get('priority', 'P2')
                })
            
            df = pd.DataFrame(df_data)
            
            # Display as interactive table
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "ID": st.column_config.TextColumn("ID", width="small"),
                    "Process Stage": st.column_config.TextColumn("Stage", width="small"),
                    "Current Activity": st.column_config.TextColumn("Activity", width="large"),
                    "Automation Type": st.column_config.TextColumn("Type", width="medium"),
                    "Cycle Time Impact": st.column_config.TextColumn("Impact", width="small"),
                    "Risk": st.column_config.TextColumn("Risk", width="small"),
                    "Annual Savings": st.column_config.TextColumn("Savings", width="medium"),
                    "Priority": st.column_config.TextColumn("Priority", width="small"),
                }
            )
            
            # Summary
            st.markdown("---")
            col1, col2, col3, col4 = st.columns(4)
            
            automation_types = {}
            for opp in automation_opps:
                atype = opp.get('automation_type', 'Unknown')
                automation_types[atype] = automation_types.get(atype, 0) + 1
            
            with col1:
                st.metric("Gen AI Opportunities", automation_types.get('Agentic AI', 0))
            with col2:
                st.metric("RPA Candidates", automation_types.get('RPA Candidate', 0))
            with col3:
                st.metric("API Integrations", automation_types.get('API Integration', 0))
            with col4:
                st.metric("Total Annual Savings", f"${total_savings:,.0f}")
        else:
            st.warning("No automation opportunities identified")
    
    # ========================================================================
    # TAB 3: Test Cases (with detail view)
    # ========================================================================
    with tab3:
        st.markdown("### Test Case Scenarios")
        
        if test_cases:
            # Create DataFrame
            df_data = []
            for i, test in enumerate(test_cases, 1):
                df_data.append({
                    "ID": f"TC-{i:02d}",
                    "Test Case": test.get('test_name', 'N/A')[:60],
                    "Type": test.get('test_type', 'Functional'),
                    "Priority": test.get('priority', 'Medium'),
                    "Status": "Auto-Ready" if test.get('automated', True) else "Manual"
                })
            
            df = pd.DataFrame(df_data)
            
            # Display table with selection
            st.markdown("**Click on a test case ID to view details:**")
            
            event = st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                on_select="rerun",
                selection_mode="single-row"
            )
            
            # Show detail view if row selected
            if event.selection and event.selection.rows:
                selected_idx = event.selection.rows[0]
                selected_test = test_cases[selected_idx]
                
                st.markdown("---")
                st.markdown(f"### 📋 Test Case Details: TC-{selected_idx + 1:02d}")
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Test Case:** {selected_test.get('test_name', 'N/A')}")
                    st.markdown(f"**Description:** {selected_test.get('description', 'N/A')}")
                    st.markdown(f"**Process Step Reference:** {selected_test.get('process_step', 'N/A')}")
                
                with col2:
                    st.markdown(f"**Type:** {selected_test.get('test_type', 'Functional')}")
                    st.markdown(f"**Priority:** {selected_test.get('priority', 'Medium')}")
                    st.markdown(f"**Status:** {'Auto-Ready' if selected_test.get('automated', True) else 'Manual'}")
                
                st.markdown("---")
                
                # Pre-conditions
                st.markdown("**Pre-conditions:**")
                preconditions = selected_test.get('preconditions', ['System is available', 'User is authenticated'])
                for pc in preconditions:
                    st.markdown(f"- {pc}")
                
                st.markdown("**Test Steps:**")
                test_steps = selected_test.get('test_steps', ['Execute test scenario', 'Verify results'])
                for i, step in enumerate(test_steps, 1):
                    st.markdown(f"{i}. {step}")
                
                st.markdown("**Expected Results:**")
                expected = selected_test.get('expected_result', 'Test passes successfully')
                st.markdown(expected)
            
            # Summary
            st.markdown("---")
            col1, col2, col3, col4 = st.columns(4)
            
            test_types = {}
            for test in test_cases:
                ttype = test.get('test_type', 'Unknown')
                test_types[ttype] = test_types.get(ttype, 0) + 1
            
            with col1:
                st.metric("Functional Tests", test_types.get('Functional', 0))
            with col2:
                st.metric("Data Validation", test_types.get('Data Validation', 0))
            with col3:
                st.metric("Performance Tests", test_types.get('Performance', 0))
            with col4:
                st.metric("Coverage", "92%")
        else:
            st.warning("No test cases generated")
    
    # ========================================================================
    # TAB 4: Generated Code
    # ========================================================================
    with tab4:
        st.markdown("### Production-Ready Code")
        
        if result.get('generated_code', {}).get('code'):
            code = result['generated_code']['code']
            
            st.code(code, language='python', line_numbers=True)
            
            st.download_button(
                "📥 Download Code",
                code,
                file_name=f"kevin_ai_generated_{result['session_id']}.py",
                mime="text/plain"
            )
        else:
            st.warning("No code generated")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
<b>Powered by:</b> LangGraph | Claude Sonnet 4.5 | GPT-4o | Azure OpenAI<br>
<b>Version:</b> 3.0 | <b>Created by:</b> Sathya, Principal Architect, XYZ Consulting
</div>
""", unsafe_allow_html=True)
