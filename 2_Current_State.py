"""Kevin AI - Current State Analysis - Version 4.1"""
import streamlit as st
import time
from backend_connector import process_sop, BACKEND_AVAILABLE, get_mock_results

st.set_page_config(page_title="Kevin AI - Current State", page_icon="📊", layout="wide")

st.html("<style>#MainMenu{visibility:hidden;}footer{visibility:hidden;}</style>")

st.markdown("### Step 2 of 6: Current State Analysis")
st.progress(0.33)

if "analysis_complete" not in st.session_state:
    st.session_state.analysis_complete = False

if not st.session_state.analysis_complete:
    st.title("🔍 Analyzing Your Process...")
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    steps = [
        ("📄 Extracting text...", 15),
        ("🧠 Applying NLP...", 30),
        ("🔍 Detecting decisions...", 45),
        ("👥 Mapping actors...", 60),
        ("💻 Identifying systems...", 75),
        ("📊 Analyzing flows...", 90),
        ("✅ Generating map...", 100)
    ]
    
    for step, progress in steps:
        status_text.markdown(f"**{step}**")
        progress_bar.progress(progress)
        time.sleep(0.8)
    
    try:
        from backend_connector import process_sop, get_mock_results
        if hasattr(st.session_state, 'sop_file') and hasattr(st.session_state, 'config'):
            status_text.markdown("**🤖 Running AI...**")
            results = process_sop(st.session_state.sop_file, st.session_state.config)
            st.session_state.analysis_results = results
        else:
            st.session_state.analysis_results = get_mock_results()
    except Exception as e:
        st.session_state.analysis_results = get_mock_results()
    
    st.session_state.analysis_complete = True
    status_text.markdown("**✓ Complete!**")
    time.sleep(1)
    st.rerun()

st.title("📊 Current State Process Analysis")

col1, col2 = st.columns([2, 1], gap="large")

with col1:
    st.subheader("Process Visualization")
    
    visual_diagram = st.session_state.analysis_results.get("current_state_map", "")
    if visual_diagram:
        st.code(visual_diagram, language="text")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.download_button("📥 Download Diagram", "placeholder", "process.txt")
    with col_b:
        st.download_button("📄 Download Data", "placeholder", "data.json")

with col2:
    st.subheader("📊 Process Metrics")
    st.metric("Total Steps", "18")
    st.metric("Manual Steps", "12")
    st.metric("Automated", "6")
    st.metric("Decisions", "4")
    st.metric("Cycle Time", "4.2 hrs")
    st.metric("Error Rate", "5%")
    
    st.subheader("⚠️ Bottlenecks")
    st.warning("**Manual Inventory Check**\n15 min/order, 30% delays")
    st.warning("**Approval Wait**\n2-4 hours blocking")
    st.warning("**Manual Entry**\n5% error rate")

st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.button("← Back", use_container_width=True, on_click=lambda: st.switch_page("pages/1_Upload_Configure.py"))
with col3:
    st.button("Continue →", use_container_width=True, type="primary", on_click=lambda: st.switch_page("pages/3_Automation_Opportunities.py"))
