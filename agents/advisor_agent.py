from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.financial_tools import load_customer_data, get_recommendation, analyze_balance, fetch_live_sbi_rates

load_dotenv(override=True)

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)

def run_advisor_agent(behavioral_output: dict, customer_id: str = None, target_lang: str = "English"):
    customer = load_customer_data(customer_id)
    balance_info = analyze_balance(customer)
    risk_appetite = behavioral_output["risk_appetite"]
    
    # 1. Fetch our newly added live multi-path debt/investment strategy registry
    sbi_strategies = fetch_live_sbi_rates()
    debt_strategies = sbi_strategies.get("debt_strategies", {})
    fixed_deposits = sbi_strategies.get("fixed_deposits", [])

    # 2. Match customer signals to extract the most efficient payoff or investment strategy
    loans = customer.get("loans", [])
    emi_ratio = balance_info.get("emi_to_salary_ratio", 0)
    idle_balance = balance_info.get("idle_balance", 0)
    
    selected_strategy_context = {}
    
    if loans:
        if emi_ratio > 0.50:
            # Path A: Severe burden -> Consolidate
            selected_strategy_context = debt_strategies.get("consolidation", {})
        elif idle_balance > 50000:  # Threshold checking for major idle cash
            # Path B: High idle money + active loans -> Prepay principal to save tenure
            selected_strategy_context = debt_strategies.get("prepayment", {})
        else:
            # Path C: Normal active debt management -> Smart Paydown Track (Defaulting to Avalanche efficiency)
            selected_strategy_context = debt_strategies.get("avalanche", {})
    else:
        # Path D: Clean state -> Growth via Amrit Vrishti Scheme
        selected_strategy_context = fixed_deposits[1] if len(fixed_deposits) > 1 else fixed_deposits[0]

    # Generate old rules engine output for backwards compatibility
    recommendations = get_recommendation(customer, balance_info, risk_appetite)
    
    loan_summary = ""
    if loans:
        loan_summary = "\n".join([
            f"- {l['loan_type']}: Outstanding ₹{l['outstanding_amount']:,}, EMI ₹{l['emi']:,}"
            for l in loans
        ])
    else:
        loan_summary = "No active loans"

    # 3. Enhanced dynamic system prompt supporting targeted strategies & localization
    prompt = f"""
    You are SBI's Proactive Financial Advisor Agent. Your task is to write a warm, personalized financial nudge.

    Behavioral Agent Report:
    {behavioral_output['analysis']}

    Customer Profile:
    - Name: {customer['name']}
    - Age: {customer['age']}
    - Occupation: {customer['occupation']}
    - Monthly Salary: ₹{customer['monthly_salary']:,}
    - AI Calculated Risk Appetite: {risk_appetite}

    Financial Position:
    - Account Balance: ₹{balance_info['balance']:,}
    - Idle Balance: ₹{balance_info['idle_balance']:,}
    - Total Monthly EMI: ₹{balance_info['total_emi']:,}
    - EMI to Salary Ratio: {emi_ratio}
    - Investable Surplus: ₹{balance_info['investable_surplus']:,}

    Active Loans:
    {loan_summary}

    TARGET OPTIMIZED FINANCIAL STRATEGY FOR THIS SYSTEM CYCLE:
    {json.dumps(selected_strategy_context, indent=2)}

    Your job:
    1. Focus entirely on explaining the optimization path highlighted in the 'TARGET OPTIMIZED FINANCIAL STRATEGY' block above.
    2. Write a warm personalized notification text to {customer['name']} explaining how this strategy efficiently improves their financial freedom.
    3. Quote exact interest rates or strategy names mentioned in the target context block. Do not hallucinate external bank variables.

    STRICT LOCALIZATION & COMPLIANCE RULES:
    1. Write the ENTIRE message completely and fluently in this script/language: {target_lang}.
    2. Keep the message human-sounding, relatable, and under 90 words.
    3. Never recommend investing if the EMI ratio > 0.5.
    """

    response = llm.invoke(prompt)

    return {
        "agent": "Proactive Advisor Agent",
        "recommendations": recommendations,
        "best_recommendation": selected_strategy_context.get("strategy_name", selected_strategy_context.get("scheme_name", "SBI Wealth Management")),
        "risk_appetite": risk_appetite,
        "target_language": target_lang,
        "personalized_message": response.content
    }

if __name__ == "__main__":
    from agents.behavioral_agent import run_behavioral_agent
    behavioral_output = run_behavioral_agent()
    # Test execution defaulting to Hindi to verify language synthesis logic
    result = run_advisor_agent(behavioral_output, target_lang="Hindi")
    print(json.dumps(result, indent=2))