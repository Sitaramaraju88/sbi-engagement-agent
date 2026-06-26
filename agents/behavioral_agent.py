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

def run_behavioral_agent():
    customer = load_customer_data()
    disengagement = detect_disengagement(customer)
    balance_info = analyze_balance(customer)

    prompt = f"""
    You are SBI's Behavioral Intelligence Agent.
    
    Customer Profile:
    - Name: {customer['name']}
    - Age: {customer['age']}
    - City: {customer['city']}
    - Last Login: {customer['last_login_days_ago']} days ago
    - Current Balance: ₹{customer['account_balance']}
    - Investable Surplus: ₹{balance_info['investable_surplus']}
    - Idle Balance Days: {customer['idle_balance_days']}
    
    Disengagement Analysis:
    - Score: {disengagement['disengagement_score']}/100
    - Level: {disengagement['disengagement_level']}
    - Signals Detected: {', '.join(disengagement['signals'])}
    
    Your job:
    1. Summarize the customer's disengagement status in 2-3 lines
    2. Identify the top 2 risk factors
    3. Suggest what the next agent should focus on
    
    Be concise, professional, and empathetic. Do not recommend products yet.
    """

    response = llm.invoke(prompt)
    return {
        "agent": "Behavioral Intelligence Agent",
        "customer_name": customer["name"],
        "disengagement": disengagement,
        "balance_info": balance_info,
        "analysis": response.content
    }

if __name__ == "__main__":
    result = run_behavioral_agent()
    print(json.dumps(result, indent=2))
