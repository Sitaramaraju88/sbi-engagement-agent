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

def calculate_risk_appetite(customer: dict, surplus: float) -> str:
    prompt = f"""
    You are a certified financial risk analyst at SBI.
    
    Analyze this customer profile and determine their risk appetite.
    
    Customer Data:
    - Age: {customer['age']}
    - Occupation: {customer['occupation']}
    - Monthly Salary: ₹{customer['monthly_salary']}
    - Account Balance: ₹{customer['account_balance']}
    - Investable Surplus: ₹{surplus}
    - Financial Goals: {', '.join(customer['financial_goals'])}
    - Existing Products: {', '.join(customer['existing_products'])}
    - Recent Transactions: {json.dumps(customer['transactions'])}
    
    Key principles to follow:
    - Zero or very low income = low risk regardless of age
    - Safety goals like emergency_fund or medical_fund = conservative
    - High surplus + wealth goals = can consider higher risk
    - Age is a minor factor only — financial stability matters more
    - A young person with no income must be rated low risk
    
    Respond with ONLY one word: low, moderate, or high
    No explanation. No punctuation. Just one word.
    """
    response = llm.invoke(prompt)
    result = response.content.strip().lower()
    if result not in ["low", "moderate", "high"]:
        return "moderate"
    return result

def run_behavioral_agent(customer_id: str = None):
    customer = load_customer_data(customer_id)
    disengagement = detect_disengagement(customer)
    balance_info = analyze_balance(customer)

    # LLM calculates risk appetite
    risk_appetite = calculate_risk_appetite(customer, balance_info["investable_surplus"])

    prompt = f"""
    You are SBI's Behavioral Intelligence Agent.
    
    Customer Profile:
    - Name: {customer['name']}
    - Age: {customer['age']}
    - Occupation: {customer['occupation']}
    - City: {customer['city']}
    - Last Login: {customer['last_login_days_ago']} days ago
    - Current Balance: ₹{customer['account_balance']}
    - Investable Surplus: ₹{balance_info['investable_surplus']}
    - Idle Balance Days: {customer['idle_balance_days']}
    - AI Calculated Risk Appetite: {risk_appetite}
    
    Disengagement Analysis:
    - Score: {disengagement['disengagement_score']}/100
    - Level: {disengagement['disengagement_level']}
    - Signals Detected: {', '.join(disengagement['signals'])}
    
    Your job:
    1. Summarize the customer's disengagement status in 2-3 lines
    2. Identify the top 2 risk factors
    3. Confirm the calculated risk appetite with reasoning
    4. Suggest what the Advisor Agent should focus on
    
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