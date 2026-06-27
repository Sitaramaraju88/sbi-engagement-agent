from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import json
import sys
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.financial_tools import load_customer_data, check_compliance, analyze_balance

load_dotenv(override=True)

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)

def run_action_agent(advisor_output: dict, customer_id: str = None):
    customer = load_customer_data(customer_id)
    balance_info = analyze_balance(customer)
    best_rec = advisor_output["best_recommendation"]

    if not best_rec:
        return {
            "agent": "Autonomous Action Agent",
            "action": "No action required",
            "amount": 0,
            "status": "NO_ACTION",
            "compliance": {"compliant": True, "requires_approval": False, "audit_logged": True},
            "audit_log": [],
            "status_update": "No action required at this time. Customer profile is stable."
        }

    compliance = check_compliance(best_rec["action"])
    audit_log = []

    if compliance["requires_approval"]:
        status = "PENDING_APPROVAL"
        action_taken = f"Recommendation sent to {customer['name']} for approval"
    else:
        status = "EXECUTED"
        action_taken = f"Auto-executed: {best_rec['action']}"
        if best_rec["amount"] > 0:
            action_taken += f" of ₹{best_rec['amount']:,}"

    audit_log.append({
        "customer_id": customer["customer_id"],
        "customer_name": customer["name"],
        "action": best_rec["action"],
        "amount": best_rec["amount"],
        "status": status,
        "compliant": compliance["compliant"],
        "requires_approval": compliance["requires_approval"],
        "audit_logged": compliance["audit_logged"],
        "emi_to_salary_ratio": balance_info["emi_to_salary_ratio"],
        "investable_surplus": balance_info["investable_surplus"],
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    loans = customer.get("loans", [])
    loan_note = ""
    if loans:
        total_emi = balance_info["total_emi"]
        loan_note = f"Customer has {len(loans)} active loan(s) with total EMI of ₹{total_emi:,}/month."

    prompt = f"""
    You are SBI's Autonomous Action Agent.

    Customer: {customer['name']} ({customer['customer_id']})
    Action Requested: {best_rec['action']}
    Amount: ₹{best_rec['amount']:,}
    Reason: {best_rec['reason']}
    Compliance Tier: {best_rec['tier']}
    Action Status: {status}
    {loan_note}

    Financial Safety Check:
    - Investable Surplus: ₹{balance_info['investable_surplus']:,}
    - EMI to Salary Ratio: {balance_info['emi_to_salary_ratio']}
    - Reserve Buffer Protected: ₹{balance_info['reserve_buffer']:,}

    Your job:
    1. Confirm what action was taken or is pending
    2. Mention the compliance check result
    3. Write a clear status update for the customer
    4. If pending approval, write a clear call-to-action
    5. Reassure the customer their safety buffer is protected

    Rules:
    - Never execute without compliance check passing
    - Always mention audit trail is maintained
    - Be transparent about what happened and why
    - Keep response under 80 words
    """

    response = llm.invoke(prompt)

    return {
        "agent": "Autonomous Action Agent",
        "action": best_rec["action"],
        "amount": best_rec["amount"],
        "status": status,
        "compliance": compliance,
        "audit_log": audit_log,
        "status_update": response.content
    }

if __name__ == "__main__":
    from agents.behavioral_agent import run_behavioral_agent
    from agents.advisor_agent import run_advisor_agent
    behavioral_output = run_behavioral_agent()
    advisor_output = run_advisor_agent(behavioral_output)
    result = run_action_agent(advisor_output)
    print(json.dumps(result, indent=2))