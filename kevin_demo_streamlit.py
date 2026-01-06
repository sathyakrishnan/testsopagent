"""
Kevin AI - Streamlit Demo Interface
Interactive UI for SOP to Agentic Automation

Version: 2.0
Date: January 6, 2026
Demo Date: January 8, 2026
"""

import streamlit as st
import os
import json
from datetime import datetime
from pathlib import Path

# Set page config
st.set_page_config(
    page_title="Kevin AI - SOP Automation",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import Kevin AI
try:
    from kevin_agents import MasterOrchestratorAgent
    from export_utils import create_pdf_report, create_pptx_report
except ImportError as e:
    st.error(f"Failed to import modules: {e}")
    st.stop()

# Initialize session state
if 'orchestrator' not in st.session_state:
    st.session_state.orchestrator = None
if 'current_session' not in st.session_state:
    st.session_state.current_session = None
if 'processing' not in st.session_state:
    st.session_state.processing = False

def get_orchestrator():
    """Initialize orchestrator once"""
    if st.session_state.orchestrator is None:
        with st.spinner("🔄 Initializing Kevin AI Orchestrator..."):
            st.session_state.orchestrator = MasterOrchestratorAgent()
    return st.session_state.orchestrator

def process_sop(sop_file, diagram_file, domain):
    """Process SOP through Kevin AI pipeline"""
    
    if sop_file is None:
        st.error("❌ Please upload an SOP document (PDF or DOCX)")
        return
    
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
        
        # Create progress indicators
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("🔄 Phase 1: Analyzing SOP document...")
        progress_bar.progress(10)
        
        # Process
        result = orch.process(str(sop_path), str(diagram_path) if diagram_path else None, domain)
        st.session_state.current_session = result
        
        progress_bar.progress(100)
        status_text.text("✅ Processing Complete!")
        
        return result
        
    except Exception as e:
        st.error(f"❌ Processing Error: {str(e)}")
        return None

# Header
st.title("🤖 Kevin AI - SOP to Agentic Automation Platform")
st.markdown("### Enterprise-Grade Process Transformation Engine")
st.markdown("**Version:** 2.0 | **Demo Ready:** January 8, 2026 | **Go-Live:** January 16, 2026")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("📥 Input")
    
    sop_file = st.file_uploader(
        "📄 SOP Document",
        type=["pdf", "docx"],
        help="Upload your Standard Operating Procedure document"
    )
    
    diagram_file = st.file_uploader(
        "📊 Process Diagram (Optional)",
        type=["png", "jpg", "jpeg"],
        help="Upload process flow diagram if available"
    )
    
    domain = st.selectbox(
        "🏢 Business Domain",
        ["logistics", "insurance", "finance", "healthcare", "retail", "manufacturing"],
        help="Select the business domain for context"
    )
    
    st.markdown("---")
    
    process_btn = st.button("🚀 Process SOP", type="primary", use_container_width=True)
    
    st.markdown("---")
    st.markdown("### 📖 Supported Formats")
    st.markdown("- **SOP:** PDF, DOCX")
    st.markdown("- **Diagrams:** PNG, JPG, JPEG")
    
    st.markdown("### ⏱️ Processing Time")
    st.markdown("- **Complete:** ~14 minutes")
    
    st.markdown("### 🔐 Security")
    st.markdown("- Encrypted at rest/transit")
    st.markdown("- GDPR & SOC 2 compliant")

# Main content
if not process_btn and st.session_state.current_session is None:
    # Welcome screen
    st.info("💡 **Ready to process** - Upload an SOP document and click 'Process SOP' to begin.")
    
    st.markdown("### What Kevin AI will do:")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        1. 🔍 Analyze SOP structure
        2. 📊 Generate current state process map
        3. 🔎 Identify gaps (if diagram provided)
        4. 🤖 Discover automation opportunities
        """)
    with col2:
        st.markdown("""
        5. 🚀 Design optimized future state
        6. 🧪 Generate test scenarios
        7. 💻 Produce production-ready code
        8. 📈 Calculate KPI improvements
        """)

# Process button clicked
if process_btn:
    if sop_file is None:
        st.error("❌ Please upload an SOP document")
    else:
        st.session_state.processing = True
        result = process_sop(sop_file, diagram_file, domain)
        st.session_state.processing = False
        
        if result:
            st.success("✅ Processing Complete!")
            st.rerun()

# Display results if available
if st.session_state.current_session is not None:
    result = st.session_state.current_session
    
    # Summary metrics
    st.markdown("## 📊 Results Summary")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Session ID", result['session_id'])
    with col2:
        st.metric("Automation Opportunities", len(result.get('automation_opportunities', [])))
    with col3:
        st.metric("Test Cases", len(result.get('test_cases', [])))
    with col4:
        total_savings = sum(opp.get("estimated_savings_annual", 0) for opp in result.get("automation_opportunities", []))
        st.metric("Annual Savings", f"${total_savings:,.0f}")
    
    # Export buttons
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Export PDF Report", use_container_width=True):
            try:
                pdf_path = f"kevin_ai_report_{result['session_id']}.pdf"
                create_pdf_report(result, pdf_path)
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        "⬇️ Download PDF",
                        f,
                        file_name=pdf_path,
                        mime="application/pdf",
                        use_container_width=True
                    )
                os.remove(pdf_path)
            except Exception as e:
                st.error(f"Failed to create PDF: {e}")
    
    with col2:
        if st.button("📊 Export PPTX Report", use_container_width=True):
            try:
                pptx_path = f"kevin_ai_report_{result['session_id']}.pptx"
                create_pptx_report(result, pptx_path)
                with open(pptx_path, "rb") as f:
                    st.download_button(
                        "⬇️ Download PPTX",
                        f,
                        file_name=pptx_path,
                        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                        use_container_width=True
                    )
                os.remove(pptx_path)
            except Exception as e:
                st.error(f"Failed to create PPTX: {e}")
    
    with col3:
        # Export all as JSON
        json_data = json.dumps(result, indent=2, default=str)
        st.download_button(
            "📦 Export JSON",
            json_data,
            file_name=f"kevin_ai_results_{result['session_id']}.json",
            mime="application/json",
            use_container_width=True
        )
    
    st.markdown("---")
    
    # Tabs for outputs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🗺️ Current State",
        "🚀 Future State", 
        "🤖 Automation",
        "🧪 Test Cases",
        "💻 Generated Code",
        "📈 KPI Analysis"
    ])
    
    with tab1:
        st.markdown("### Current State Process Map")
        if result.get('current_state_map'):
            st.code(result['current_state_map'], language='mermaid')
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.download_button(
                    "📥 Download Mermaid (.mermaid)",
                    result['current_state_map'],
                    file_name=f"current_state_{result['session_id']}.mermaid",
                    mime="text/plain"
                )
            with col2:
                if st.button("🖼️ Export as PNG", key="current_png"):
                    try:
                        from export_utils import mermaid_to_image
                        png_path = f"current_state_{result['session_id']}.png"
                        mermaid_to_image(result['current_state_map'], png_path, 'png')
                        with open(png_path, "rb") as f:
                            st.download_button(
                                "⬇️ Download PNG",
                                f,
                                file_name=png_path,
                                mime="image/png"
                            )
                        os.remove(png_path)
                    except Exception as e:
                        st.error(f"Error: {e}")
            with col3:
                if st.button("🖼️ Export as JPG", key="current_jpg"):
                    try:
                        from export_utils import mermaid_to_image
                        jpg_path = f"current_state_{result['session_id']}.jpg"
                        mermaid_to_image(result['current_state_map'], jpg_path, 'jpg')
                        with open(jpg_path, "rb") as f:
                            st.download_button(
                                "⬇️ Download JPG",
                                f,
                                file_name=jpg_path,
                                mime="image/jpeg"
                            )
                        os.remove(jpg_path)
                    except Exception as e:
                        st.error(f"Error: {e}")
        else:
            st.warning("No current state map available")
    
    with tab2:
        st.markdown("### Future State Process Map")
        if result.get('future_state_map'):
            st.code(result['future_state_map'], language='mermaid')
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.download_button(
                    "📥 Download Mermaid (.mermaid)",
                    result['future_state_map'],
                    file_name=f"future_state_{result['session_id']}.mermaid",
                    mime="text/plain"
                )
            with col2:
                if st.button("🖼️ Export as PNG", key="future_png"):
                    try:
                        from export_utils import mermaid_to_image
                        png_path = f"future_state_{result['session_id']}.png"
                        mermaid_to_image(result['future_state_map'], png_path, 'png')
                        with open(png_path, "rb") as f:
                            st.download_button(
                                "⬇️ Download PNG",
                                f,
                                file_name=png_path,
                                mime="image/png"
                            )
                        os.remove(png_path)
                    except Exception as e:
                        st.error(f"Error: {e}")
            with col3:
                if st.button("🖼️ Export as JPG", key="future_jpg"):
                    try:
                        from export_utils import mermaid_to_image
                        jpg_path = f"future_state_{result['session_id']}.jpg"
                        mermaid_to_image(result['future_state_map'], jpg_path, 'jpg')
                        with open(jpg_path, "rb") as f:
                            st.download_button(
                                "⬇️ Download JPG",
                                f,
                                file_name=jpg_path,
                                mime="image/jpeg"
                            )
                        os.remove(jpg_path)
                    except Exception as e:
                        st.error(f"Error: {e}")
        else:
            st.warning("No future state map available")
    
    with tab3:
        st.markdown("### Automation Opportunities")
        if result.get('automation_opportunities'):
            st.json(result['automation_opportunities'])
            st.download_button(
                "📥 Download Automation Opportunities",
                json.dumps(result['automation_opportunities'], indent=2),
                file_name=f"automation_opportunities_{result['session_id']}.json",
                mime="application/json"
            )
        else:
            st.warning("No automation opportunities available")
    
    with tab4:
        st.markdown("### Test Cases")
        if result.get('test_cases'):
            st.json(result['test_cases'])
            st.download_button(
                "📥 Download Test Cases",
                json.dumps(result['test_cases'], indent=2),
                file_name=f"test_cases_{result['session_id']}.json",
                mime="application/json"
            )
        else:
            st.warning("No test cases available")
    
    with tab5:
        st.markdown("### Generated Code")
        if result.get('generated_code', {}).get('code'):
            st.code(result['generated_code']['code'], language='python')
            st.download_button(
                "📥 Download Generated Code",
                result['generated_code']['code'],
                file_name=f"generated_code_{result['session_id']}.py",
                mime="text/plain"
            )
        else:
            st.warning("No generated code available")
    
    with tab6:
        st.markdown("### KPI/SLA Analysis")
        if result.get('kpi_analysis'):
            st.json(result['kpi_analysis'])
            st.download_button(
                "📥 Download KPI Analysis",
                json.dumps(result['kpi_analysis'], indent=2),
                file_name=f"kpi_analysis_{result['session_id']}.json",
                mime="application/json"
            )
        else:
            st.warning("No KPI analysis available")
    
    # Clear button
    st.markdown("---")
    if st.button("🔄 Process New SOP", type="secondary"):
        st.session_state.current_session = None
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
**Powered by:** LangGraph | Claude Sonnet 4.5 | GPT-4o | Azure OpenAI  
**Created by:** Sathya, Principal Architect, XYZ Consulting  
**Support:** kevin-ai@xyz-consulting.com
""")
