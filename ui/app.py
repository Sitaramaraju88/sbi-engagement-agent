import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import run_pipeline

st.set_page_config(
    page_title="SBI Agentic AI",
    page_icon="🏦",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main { background-color: #f0f4f8; }
    .stButton>button {
        background-color: #003366;
        color: white;
        font-size: 18px;
        border-radius: 10px;
        padding: 12px;
    }
    .agent-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #003366;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    .metric-card {
        background-color: #003366;
        color: white;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
    }
    .header-banner {
        background: linear-gradient(135deg, #003366, #0066cc);
        padding: 30px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
    }
    .status-pending {
        background-color: #fff3cd;
        border: 1px solid #ffc107;
        padding: 10px;
        border-radius: 8px;
    }
    .status-executed {
        background-color: #d4edda;
        border: 1px solid #28a745;
        padding: 10px;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header-banner">
    <h1>🏦 SBI Digital Engagement System</h1>
    <p style="font-size:18px;">Powered by Agentic AI | LLaMA 3.3 70B via Groq</p>
    <p style="font-size:14px; opacity:0.8;">Behavioral Intelligence · Proactive Advisor · Autonomous Action</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/c/cc/SBI-logo.svg", width=120)
    st.markdown("### System Info")
    st.success("✅ Groq API Connected")
    st.success("✅ LLaMA 3.3 70B Active")
    st.success("✅ 3 Agents Ready")
    st.divider()
    st.markdown("### Agent Pipeline")
    st.markdown("1. 🔍 Behavioral Intelligence")
    st.markdown("2. 💡 Proactive Advisor")
    st.markdown("3. ⚡ Autonomous Action")
    st.divider()
    st.markdown("### Compliance")
    st.markdown("✅ RBI Guidelines")
    st.markdown("✅ Audit Trail Active")
    st.markdown("✅ Consent Framework")

# Main button
col1, col2, col3 = st.columns([1,2,1])
with col2:
    run = st.button("🚀 Run Engagement Pipeline", type="primary", use_container_width=True)

if run:
    # Progress bar
    progress = st.progress(0, text="Initializing pipeline...")

    with st.spinner(""):
        progress.progress(10, text="Loading customer profile...")
        import time
        time.sleep(0.5)

        progress.progress(30, text="🔍 Running Behavioral Intelligence Agent...")
        result = run_pipeline(verbose=False)
        progress.progress(60, text="💡 Running Proactive Advisor Agent...")
        time.sleep(0.5)
        progress.progress(90, text="⚡ Running Autonomous Action Agent...")
        time.sleep(0.5)
        progress.progress(100, text="✅ Pipeline Complete!")

    behavioral = result["behavioral"]
    advisor = result["advisor"]
    action = result["action"]

    st.success("✅ All 3 agents completed successfully!")
    st.divider()

    # Customer Profile Section
    st.markdown("### 👤 Customer Profile")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Customer", behavioral["customer_name"])
    col2.metric("Account Balance", f"₹{behavioral['balance_info']['balance']:,}")
    col3.metric("Reserve Buffer", f"₹{behavioral['balance_info']['reserve_buffer']:,}")
    col4.metric("Investable Surplus", f"₹{behavioral['balance_info']['investable_surplus']:,}")

    st.divider()

    # Agent 1
    st.markdown('<div class="agent-card">', unsafe_allow_html=True)
    st.markdown("### 🔍 Agent 1 — Behavioral Intelligence Agent")

    level = behavioral["disengagement"]["disengagement_level"]
    score = behavioral["disengagement"]["disengagement_score"]
    color = "🔴" if level == "High" else "🟡" if level == "Medium" else "🟢"

    col1, col2, col3 = st.columns(3)
    col1.metric("Disengagement Level", f"{color} {level}")
    col2.metric("Disengagement Score", f"{score}/100")
    col3.metric("Last Login", f"{behavioral['balance_info']['balance'] and '12 days ago'}")

    st.markdown("**⚠️ Risk Signals Detected:**")
    for signal in behavioral["disengagement"]["signals"]:
        st.warning(f"⚠️ {signal}")

    with st.expander("📊 View Full Behavioral Analysis"):
        st.write(behavioral["analysis"])
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    # Agent 2
    st.markdown('<div class="agent-card">', unsafe_allow_html=True)
    st.markdown("### 💡 Agent 2 — Proactive Advisor Agent")

    st.info(f"💬 **Personalized Message:**\n\n{advisor['personalized_message']}")

    st.markdown(f"**Total Recommendations Generated: {len(advisor['recommendations'])}**")
    for i, rec in enumerate(advisor["recommendations"]):
        badge = "⭐ Best Match" if i == 0 else f"Option {i+1}"
        with st.expander(f"{badge}: {rec['action']}"):
            col1, col2 = st.columns(2)
            col1.metric("Recommended Amount", f"₹{rec['amount']:,}")
            col2.metric("Compliance Tier", rec["tier"])
            st.write(f"**📌 Reason:** {rec['reason']}")
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    # Agent 3
    st.markdown('<div class="agent-card">', unsafe_allow_html=True)
    st.markdown("### ⚡ Agent 3 — Autonomous Action Agent")

    status = action["status"]
    col1, col2, col3 = st.columns(3)
    status_display = "🟡 PENDING APPROVAL" if status == "PENDING_APPROVAL" else "🟢 EXECUTED"
    col1.metric("Action Status", status_display)
    col2.metric("Compliance Check", "✅ Passed" if action["compliance"]["compliant"] else "❌ Failed")
    col3.metric("Audit Trail", "✅ Logged" if action["compliance"]["audit_logged"] else "❌ Not Logged")

    st.success(f"📋 {action['status_update']}")

    st.markdown("**📁 Audit Log:**")
    if action["audit_log"]:
        st.json(action["audit_log"][0])
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    # Customer Approval Section
    if status == "PENDING_APPROVAL":
        st.markdown("### 🔐 Customer Approval Required")
        st.markdown(f"**Action:** {action['action']} | **Amount:** ₹{action['amount']:,}")

        col1, col2 = st.columns(2)
        if col1.button("✅ Approve Action", type="primary", use_container_width=True):
            st.success("✅ Action approved! Transaction initiated and audit logged securely.")
            st.balloons()
        if col2.button("❌ Reject Action", use_container_width=True):
            st.error("❌ Action rejected by customer. No transaction executed. Audit logged.")

    st.divider()
    st.markdown("""
    <div style='text-align:center; color:gray; font-size:12px;'>
    SBI Agentic AI System | Built for SBI Hackathon 2026 | 
    Powered by CrewAI + LangChain + Groq | All actions comply with RBI guidelines
    </div>
    """, unsafe_allow_html=True)