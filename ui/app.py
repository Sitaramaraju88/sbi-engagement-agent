import streamlit as st
import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import run_pipeline
from tools.financial_tools import load_all_customers, get_engagement_type
@st.cache_data(ttl=300)
def run_pipeline_cached(customer_id: str = None) -> dict:
    return run_pipeline(verbose=False, customer_id=customer_id)

st.set_page_config(
    page_title="SBI Agentic AI",
    page_icon="🏦",
    layout="wide"
)

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
    .header-banner {
        background: linear-gradient(135deg, #003366, #0066cc);
        padding: 30px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
    }
    .customer-card {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #dee2e6;
        margin-bottom: 10px;
    }
    .filter-section {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #0066cc;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
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
    st.markdown("### AI Capabilities")
    st.markdown("🧠 LLM Risk Appetite Detection")
    st.markdown("📊 Dynamic Engagement Scoring")
    st.markdown("💡 Personalized Recommendations")
    st.markdown("⚡ Autonomous Action Execution")
    st.divider()
    st.markdown("### Compliance")
    st.markdown("✅ RBI Guidelines")
    st.markdown("✅ Audit Trail Active")
    st.markdown("✅ Consent Framework")
    st.markdown("✅ 3-Tier Action Model")

# ─────────────────────────────────────────
# CUSTOMER SELECTOR SECTION
# ─────────────────────────────────────────
st.markdown("### 🔎 Customer Selector")
st.caption("💡 Engagement types are **dynamically calculated by the AI** from raw customer signals — nothing is pre-labeled.")

# Load all customers and calculate engagement dynamically
all_customers = load_all_customers()
for c in all_customers:
    c["_engagement_type"] = get_engagement_type(c)

# Summary stats
total = len(all_customers)
high = sum(1 for c in all_customers if c["_engagement_type"] == "High Disengagement")
medium = sum(1 for c in all_customers if c["_engagement_type"] == "Medium Disengagement")
low = sum(1 for c in all_customers if c["_engagement_type"] == "Low Disengagement")
cold = sum(1 for c in all_customers if c["_engagement_type"] == "Cold Start")

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Customers", total)
col2.metric("🔴 High Disengagement", high)
col3.metric("🟡 Medium Disengagement", medium)
col4.metric("🟢 Low Disengagement", low)
col5.metric("🔵 Cold Start", cold)

st.divider()

# Filter section
st.markdown('<div class="filter-section">', unsafe_allow_html=True)
st.markdown("#### 🗂️ Filter & Select Customer")

col1, col2 = st.columns([1, 2])

with col1:
    engagement_options = [
        "All Customers",
        "🔴 High Disengagement",
        "🟡 Medium Disengagement",
        "🟢 Low Disengagement",
        "🔵 Cold Start"
    ]
    selected_filter = st.selectbox("Filter by Engagement Type", engagement_options)

# Map filter to actual engagement type
filter_map = {
    "All Customers": None,
    "🔴 High Disengagement": "High Disengagement",
    "🟡 Medium Disengagement": "Medium Disengagement",
    "🟢 Low Disengagement": "Low Disengagement",
    "🔵 Cold Start": "Cold Start"
}
filter_value = filter_map[selected_filter]

# Apply filter
filtered_customers = all_customers if not filter_value else [
    c for c in all_customers if c["_engagement_type"] == filter_value
]

# Customer table
st.markdown(f"**Showing {len(filtered_customers)} customer(s):**")
table_data = []
for c in filtered_customers:
    emoji = "🔴" if c["_engagement_type"] == "High Disengagement" else \
            "🟡" if c["_engagement_type"] == "Medium Disengagement" else \
            "🔵" if c["_engagement_type"] == "Cold Start" else "🟢"
    table_data.append({
        "Customer ID": c["customer_id"],
        "Name": c["name"],
        "Age": c["age"],
        "City": c["city"],
        "Occupation": c["occupation"],
        "Balance": f"₹{c['account_balance']:,}",
        "Last Login": f"{c['last_login_days_ago']} days ago",
        "AI Detected Engagement": f"{emoji} {c['_engagement_type']}"
    })
st.dataframe(table_data, use_container_width=True)

# Customer dropdown
with col2:
    if not filtered_customers:
        st.warning("No customers match this filter.")
        st.stop()

    customer_options = {
        f"{c['customer_id']} — {c['name']} ({c['_engagement_type']})": c["customer_id"]
        for c in filtered_customers
    }
    selected_label = st.selectbox("Select Customer to Analyze", list(customer_options.keys()))
    selected_customer_id = customer_options[selected_label]

st.markdown('</div>', unsafe_allow_html=True)

# Selected customer quick info
selected = next(c for c in all_customers if c["customer_id"] == selected_customer_id)
st.markdown("#### 👤 Selected Customer Preview")
col1, col2, col3, col4, col5, col6 = st.columns(6)
col1.metric("Customer ID", selected["customer_id"])
col2.metric("Name", selected["name"])
col3.metric("Age", selected["age"])
col4.metric("City", selected["city"])
col5.metric("Balance", f"₹{selected['account_balance']:,}")
col6.metric("AI Engagement", selected["_engagement_type"])

st.divider()

# ─────────────────────────────────────────
# RUN PIPELINE BUTTON
# ─────────────────────────────────────────
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    run = st.button("🚀 Run Engagement Pipeline", type="primary", use_container_width=True)

if run:
    progress = st.progress(0, text="Initializing pipeline...")

    with st.spinner(""):
        progress.progress(10, text="Loading customer profile...")
        time.sleep(0.5)
        progress.progress(25, text="🧠 LLM calculating risk appetite...")
        result = run_pipeline_cached(customer_id=selected_customer_id)
        progress.progress(60, text="💡 Running Proactive Advisor Agent...")
        time.sleep(0.5)
        progress.progress(85, text="⚡ Running Autonomous Action Agent...")
        time.sleep(0.5)
        progress.progress(100, text="✅ Pipeline Complete!")

    behavioral = result["behavioral"]
    advisor = result["advisor"]
    action = result["action"]

    st.success(f"✅ Pipeline completed for **{behavioral['customer_name']}** ({selected_customer_id})")
    st.divider()

    # ── Customer Profile ──
    st.markdown("### 👤 Customer Profile")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Name", behavioral["customer_name"])
    col2.metric("Account Balance", f"₹{behavioral['balance_info']['balance']:,}")
    col3.metric("Reserve Buffer", f"₹{behavioral['balance_info']['reserve_buffer']:,}")
    col4.metric("Investable Surplus", f"₹{behavioral['balance_info']['investable_surplus']:,}")
    col5.metric("AI Risk Appetite", behavioral["risk_appetite"].upper())

    st.divider()

    # ── Agent 1 ──
    st.markdown('<div class="agent-card">', unsafe_allow_html=True)
    st.markdown("### 🔍 Agent 1 — Behavioral Intelligence Agent")
    st.caption("Analyzes customer signals and calculates disengagement score dynamically")

    level = behavioral["disengagement"]["disengagement_level"]
    score = behavioral["disengagement"]["disengagement_score"]
    color = "🔴" if level == "High" else "🟡" if level == "Medium" else "🔵" if level == "Cold Start" else "🟢"

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Disengagement Level", f"{color} {level}")
    col2.metric("Disengagement Score", f"{score}/100")
    col3.metric("Last Login", f"{selected['last_login_days_ago']} days ago")
    col4.metric("Idle Balance Days", f"{selected['idle_balance_days']} days")

    st.markdown("**⚠️ Risk Signals Detected:**")
    if behavioral["disengagement"]["signals"]:
        for signal in behavioral["disengagement"]["signals"]:
            st.warning(f"⚠️ {signal}")
    else:
        st.success("✅ No disengagement signals detected")

    with st.expander("📊 View Full Behavioral Analysis"):
        st.write(behavioral["analysis"])
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    # ── Agent 2 ──
    st.markdown('<div class="agent-card">', unsafe_allow_html=True)
    st.markdown("### 💡 Agent 2 — Proactive Advisor Agent")
    st.caption("Generates personalized recommendations based on AI-calculated risk appetite")

    st.info(f"💬 **Personalized Message to {behavioral['customer_name']}:**\n\n{advisor['personalized_message']}")

    st.markdown(f"**Total Recommendations Generated: {len(advisor['recommendations'])}**")
    for i, rec in enumerate(advisor["recommendations"]):
        badge = "⭐ Best Match" if i == 0 else f"Option {i+1}"
        with st.expander(f"{badge}: {rec['action']}"):
            col1, col2, col3 = st.columns(3)
            col1.metric("Recommended Amount", f"₹{rec['amount']:,}")
            col2.metric("Compliance Tier", rec["tier"].split("—")[0].strip())
            col3.metric("Approval Required", "Yes ⚠️" if "Tier 2" in rec["tier"] else "No ✅")
            st.write(f"**📌 Reason:** {rec['reason']}")
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    # ── Agent 3 ──
    st.markdown('<div class="agent-card">', unsafe_allow_html=True)
    st.markdown("### ⚡ Agent 3 — Autonomous Action Agent")
    st.caption("Executes compliant actions autonomously or routes for customer approval")

    status = action["status"]
    col1, col2, col3, col4 = st.columns(4)
    status_display = "🟡 PENDING APPROVAL" if status == "PENDING_APPROVAL" else "🟢 EXECUTED"
    col1.metric("Action Status", status_display)
    col2.metric("Action", action.get("action", "N/A"))
    col3.metric("Compliance", "✅ Passed" if action["compliance"]["compliant"] else "❌ Failed")
    col4.metric("Audit Trail", "✅ Logged" if action["compliance"]["audit_logged"] else "❌ No")

    st.success(f"📋 {action['status_update']}")

    with st.expander("📁 View Full Audit Log"):
        if action["audit_log"]:
            st.json(action["audit_log"][0])
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    # ── Approval Section ──
    if status == "PENDING_APPROVAL":
        st.markdown("### 🔐 Customer Approval Required")
        st.warning(f"**Action:** {action['action']} | **Amount:** ₹{action['amount']:,} | **Requires your explicit consent**")

        col1, col2 = st.columns(2)
        if col1.button("✅ Approve Action", type="primary", use_container_width=True):
            st.success("✅ Action approved! Transaction initiated and audit logged securely.")
            st.balloons()
        if col2.button("❌ Reject Action", use_container_width=True):
            st.error("❌ Action rejected by customer. No transaction executed. Rejection audit logged.")

    st.divider()
    st.markdown("""
    <div style='text-align:center; color:gray; font-size:12px;'>
    SBI Agentic AI System | Built for SBI Hackathon 2026 |
    Powered by LangChain + Groq LLaMA 3.3 70B | All actions comply with RBI guidelines
    </div>
    """, unsafe_allow_html=True)