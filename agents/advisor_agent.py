from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import json
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.financial_tools import load_customer_data, get_recommendation, analyze_balance

load_dotenv(override=True)

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)

def run_advisor_agent(behavioral_output: dict, customer_id: str = None):
    customer = load_customer_data(customer_id)
    balance_info = analyze_balance(customer)
    risk_appetite = behavioral_output["risk_appetite"]
    recommendations = get_recommendation(customer, balance_info, risk_appetite)

    loans = customer.get("loans", [])
    loan_summary = ""
    if loans:
        loan_summary = "\n".join([
            f"- {l['loan_type']}: Outstanding ₹{l['outstanding_amount']:,}, EMI ₹{l['emi']:,}"
            for l in loans
        ])
    else:
        loan_summary = "No active loans"

    prompt = f"""
    You are SBI's Proactive Financial Advisor Agent.

    Behavioral Agent Report:
    {behavioral_output['analysis']}

    Customer Profile:
    - Name: {customer['name']}
    - Age: {customer['age']}
    - Occupation: {customer['occupation']}
    - Monthly Salary: ₹{customer['monthly_salary']:,}
    - Services in Use: {', '.join(customer['current_services_in_use'])}
    - AI Calculated Risk Appetite: {risk_appetite}

    Financial Position:
    - Account Balance: ₹{balance_info['balance']:,}
    - Idle Balance: ₹{balance_info['idle_balance']:,}
    - Total Monthly EMI: ₹{balance_info['total_emi']:,}
    - EMI to Salary Ratio: {balance_info['emi_to_salary_ratio']}
    - Reserve Buffer: ₹{balance_info['reserve_buffer']:,}
    - Investable Surplus: ₹{balance_info['investable_surplus']:,}

    Active Loans:
    {loan_summary}

    Generated Recommendations:
    {json.dumps(recommendations, indent=2)}

    Your job:
    1. The FIRST recommendation in the list is already the best one — use it
    2. Write a friendly personalized message to {customer['name']} about ONLY that first recommendation
    3. Do NOT mention any other recommendation
    4. Explain why this recommendation suits their specific situation
    5. Mention compliance tier clearly

    Rules:
    - Never recommend investing if EMI ratio > 0.5
    - Never recommend beyond the investable surplus
    - If customer has loans, acknowledge them empathetically
    - Be human and warm, not salesy
    - Keep message under 100 words
    - Always mention approval requirement if Tier 2
    """

    response = llm.invoke(prompt)

    return {
        "agent": "Proactive Advisor Agent",
        "recommendations": recommendations,
        "best_recommendation": recommendations[0] if recommendations else None,
        "risk_appetite": risk_appetite,
        "personalized_message": response.content
    }

if __name__ == "__main__":
    from agents.behavioral_agent import run_behavioral_agent
    behavioral_output = run_behavioral_agent()
    result = run_advisor_agent(behavioral_output)
    print(json.dumps(result, indent=2))