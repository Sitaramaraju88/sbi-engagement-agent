from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import json
import sys
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
            "status": "No action required",
            "audit_log": []
        }

    compliance = check_compliance(best_rec["action"])
    audit_log = []

    if compliance["requires_approval"]:
        status = "PENDING_APPROVAL"
        action_taken = f"Recommendation sent to {customer['name']} for approval"
    else:
        status = "EXECUTED"
        action_taken = f"Auto-executed: {best_rec['action']} of ₹{best_rec['amount']}"

    audit_log.append({
        "action": best_rec["action"],
        "amount": best_rec["amount"],
        "status": status,
        "compliant": compliance["compliant"],
        "requires_approval": compliance["requires_approval"],
        "audit_logged": compliance["audit_logged"],
        "timestamp": "2026-06-27 09:00:00"
    })

    prompt = f"""
    You are SBI's Autonomous Action Agent.
    
    Customer: {customer['name']}
    Action Requested: {best_rec['action']}
    Amount: ₹{best_rec['amount']}
    Reason: {best_rec['reason']}
    Compliance Status: {compliance}
    Action Status: {status}
    
    Your job:
    1. Confirm what action was taken or is pending
    2. Explain the compliance check result
    3. Write a short status update for the customer
    4. If pending approval, write a clear call-to-action
    
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
