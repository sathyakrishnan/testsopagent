"""Kevin AI - Automation Opportunities - Version 4.1"""
import streamlit as st

st.set_page_config(page_title="Kevin AI - Automation", page_icon="🤖", layout="wide")
st.html("<style>#MainMenu{visibility:hidden;}footer{visibility:hidden;}</style>")

st.markdown("### Step 3 of 6: Automation Opportunities")
st.progress(0.5)

st.title("🤖 Automation Opportunities")
st.markdown("**8 opportunities** | **$524K/year** | **8.7 mo payback**")

col1, col2, col3 = st.columns(3)
col1.selectbox("Priority", ["All", "P0", "P1", "P2"])
col2.selectbox("Type", ["All", "API", "RPA", "AI"])
col3.checkbox("Show Details", value=True)

st.markdown("---")

# Opportunity 1
with st.expander("**AUTO-001** 🔴 P0 - Inventory API ($47K/year)", expanded=True):
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("**Current State**")
        st.markdown("- Manual WMS lookup")
        st.markdown("- ⏱️ 60 sec/order")
        st.markdown("- ⚠️ 5% error rate")
    with col_b:
        st.markdown("**Future State**")
        st.markdown("- Real-time API")
        st.markdown("- ⚡ 2 sec/order")
        st.markdown("- ✅ 0.1% errors")
    
    st.metric("Annual Savings", "$47,112", "+6.4mo payback")

# Opportunity 2
with st.expander("**AUTO-002** 🔴 P0 - AI Order Routing ($89K/year)"):
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("**Current:** Manual, 8 min, 12% errors")
    with col_b:
        st.markdown("**Future:** AI Agent, 15 sec, 1% errors")

# Opportunity 3
with st.expander("**AUTO-003** 🟠 P1 - Email Automation ($28K/year)"):
    st.markdown("Template-based automation, 95% time reduction")

st.markdown("---")
st.subheader("💰 Total Impact")

col1, col2, col3 = st.columns(3)
col1.metric("Annual Savings", "$524K")
col2.metric("Opportunities", "8")
col3.metric("Avg Payback", "8.7 mo")

col1, col2, col3 = st.columns(3)
col1.metric("🤖 Agentic AI", "3", "$234K")
col2.metric("🔌 API Integration", "3", "$212K")
col3.metric("🔄 RPA", "2", "$78K")

st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1,2,1])
with col1:
    st.button("← Back", use_container_width=True, on_click=lambda: st.switch_page("pages/2_Current_State.py"))
with col3:
    st.button("Continue →", use_container_width=True, type="primary", on_click=lambda: st.switch_page("pages/4_Future_State.py"))
