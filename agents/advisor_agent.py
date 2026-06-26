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

    # Use LLM-calculated risk appetite from behavioral agent
    risk_appetite = behavioral_output["risk_appetite"]
    recommendations = get_recommendation(customer, balance_info["investable_surplus"], risk_appetite)

    prompt = f"""
    You are SBI's Proactive Financial Advisor Agent.
    
    Behavioral Agent Report:
    {behavioral_output['analysis']}
    
    Customer Profile:
    - Name: {customer['name']}
    - Age: {customer['age']}
    - Occupation: {customer['occupation']}
    - AI Calculated Risk Appetite: {risk_appetite}
    - Financial Goals: {', '.join(customer['financial_goals'])}
    - Existing Products: {', '.join(customer['existing_products'])}
    
    Balance Analysis:
    - Total Balance: ₹{balance_info['balance']}
    - Reserve Buffer: ₹{balance_info['reserve_buffer']}
    - Investable Surplus: ₹{balance_info['investable_surplus']}
    
    Generated Recommendations:
    {json.dumps(recommendations, indent=2)}
    
    Your job:
    1. Review the recommendations above
    2. Prioritize the single best recommendation for this customer
    3. Write a friendly, personalized message to {customer['name']}
    4. Explain why this recommendation suits them specifically
    5. Mention the compliance tier clearly
    
    Rules:
    - Never recommend beyond the investable surplus
    - Be empathetic and human, not salesy
    - Keep the message under 100 words
    - Always mention approval requirement if Tier 2
    - If risk appetite is low, never suggest equity or high risk products
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