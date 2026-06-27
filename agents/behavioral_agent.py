from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import json
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.financial_tools import load_customer_data, detect_disengagement, analyze_balance

load_dotenv(override=True)

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)

def calculate_risk_appetite(customer: dict, balance_info: dict) -> str:
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
    You are a certified financial risk analyst at SBI.

    Analyze this customer profile and determine their risk appetite.

    Customer Data:
    - Name: {customer['name']}
    - Age: {customer['age']}
    - Occupation: {customer['occupation']}
    - Monthly Salary: ₹{customer['monthly_salary']:,}
    - Account Balance: ₹{customer['account_balance']:,}
    - Idle Balance: ₹{balance_info['idle_balance']:,}
    - Investable Surplus: ₹{balance_info['investable_surplus']:,}
    - Total Monthly EMI: ₹{balance_info['total_emi']:,}
    - EMI to Salary Ratio: {balance_info['emi_to_salary_ratio']}
    - Services in Use: {', '.join(customer['current_services_in_use'])}

    Active Loans:
    {loan_summary}

    Key principles:
    - If EMI ratio > 0.5 → always low risk regardless of income
    - Zero or very low income → low risk
    - High loan burden + low surplus → low risk
    - High surplus + high income + low loans → can be high risk
    - Age > 55 → lean conservative unless high surplus
    - Occupation like farmer, electrician, daily wage → lean low
    - Occupation like doctor, lawyer, business owner → can be moderate/high

    Respond with ONLY one word: low, moderate, or high
    No explanation. No punctuation. Just one word.
    """

    response = llm.invoke(prompt)
    result = response.content.strip().lower()
    if result not in ["low", "moderate", "high"]:
        return "low"
    return result

def run_behavioral_agent(customer_id: str = None):
    customer = load_customer_data(customer_id)
    disengagement = detect_disengagement(customer)
    balance_info = analyze_balance(customer)
    risk_appetite = calculate_risk_appetite(customer, balance_info)

    loans = customer.get("loans", [])
    loan_summary = ""
    if loans:
        loan_summary = "\n".join([
            f"- {l['loan_type']}: Outstanding ₹{l['outstanding_amount']:,}, EMI ₹{l['emi']:,}, {l['tenure_months']} months remaining"
            for l in loans
        ])
    else:
        loan_summary = "No active loans"

    prompt = f"""
    You are SBI's Behavioral Intelligence Agent.

    Customer Profile:
    - Name: {customer['name']}
    - Age: {customer['age']}
    - Occupation: {customer['occupation']}
    - City: {customer['city']}
    - Monthly Salary: ₹{customer['monthly_salary']:,}
    - Account Balance: ₹{customer['account_balance']:,}
    - Idle Balance: ₹{balance_info['idle_balance']:,}
    - Idle Balance Days: {customer['idle_balance_days']}
    - Last Login: {customer['last_login_days_ago']} days ago
    - Notification Response Rate: {customer['notification_response_rate']}
    - Services in Use: {', '.join(customer['current_services_in_use'])}

    Financial Position:
    - Total Monthly EMI: ₹{balance_info['total_emi']:,}
    - EMI to Salary Ratio: {balance_info['emi_to_salary_ratio']}
    - Investable Surplus: ₹{balance_info['investable_surplus']:,}
    - AI Calculated Risk Appetite: {risk_appetite}

    Active Loans:
    {loan_summary}

    Disengagement Analysis:
    - Score: {disengagement['disengagement_score']}/100
    - Level: {disengagement['disengagement_level']}
    - Signals: {', '.join(disengagement['signals']) if disengagement['signals'] else 'None'}

    Your job:
    1. Summarize the customer's financial health in 2-3 lines
    2. Identify top 2 disengagement risk factors
    3. Comment on loan burden if applicable
    4. Confirm risk appetite with brief reasoning
    5. Guide the Advisor Agent on what to focus on

    Be concise, professional, and empathetic. Do not recommend products yet.
    """

    response = llm.invoke(prompt)

    return {
        "agent": "Behavioral Intelligence Agent",
        "customer_name": customer["name"],
        "customer_id": customer["customer_id"],
        "disengagement": disengagement,
        "balance_info": balance_info,
        "risk_appetite": risk_appetite,
        "analysis": response.content
    }

if __name__ == "__main__":
    result = run_behavioral_agent()
    print(json.dumps(result, indent=2))