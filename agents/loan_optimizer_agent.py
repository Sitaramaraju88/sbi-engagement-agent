from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import json
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.financial_tools import load_customer_data, analyze_balance

load_dotenv(override=True)

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)

def run_loan_optimizer_agent(behavioral_output: dict, customer_id: str = None):
    customer = load_customer_data(customer_id)
    balance_info = analyze_balance(customer)
    loans = customer.get("loans", [])

    # Skip if no loans
    if not loans:
        return {
            "agent": "Loan Optimizer Agent",
            "has_loans": False,
            "status": "NO_LOANS",
            "message": f"{customer['name']} has no active loans. Full salary available for savings and investments.",
            "loan_analysis": None,
            "repayment_plan": None,
            "optimization_tips": []
        }

    salary = customer["monthly_salary"]
    balance = customer["account_balance"]
    total_emi = balance_info["total_emi"]
    total_outstanding = balance_info["total_outstanding"]
    emi_ratio = balance_info["emi_to_salary_ratio"]
    surplus = balance_info["investable_surplus"]

    # Build loan details for LLM
    loan_details = "\n".join([
        f"- {l['loan_type'].replace('_', ' ').title()}: "
        f"Outstanding ₹{l['outstanding_amount']:,}, "
        f"EMI ₹{l['emi']:,}/month, "
        f"{l['tenure_months']} months remaining"
        for l in loans
    ])

    # Sort loans by outstanding amount (smallest first — snowball strategy)
    sorted_by_snowball = sorted(loans, key=lambda x: x["outstanding_amount"])

    # Sort loans by EMI burden (highest first — avalanche strategy)
    sorted_by_avalanche = sorted(loans, key=lambda x: x["emi"], reverse=True)

    snowball_order = " → ".join([
        f"{l['loan_type'].replace('_', ' ').title()} (₹{l['outstanding_amount']:,})"
        for l in sorted_by_snowball
    ])

    avalanche_order = " → ".join([
        f"{l['loan_type'].replace('_', ' ').title()} (EMI ₹{l['emi']:,})"
        for l in sorted_by_avalanche
    ])

    prompt = f"""
    You are SBI's Loan Optimizer Agent — a financial planning specialist.

    Customer Profile:
    - Name: {customer['name']}
    - Age: {customer['age']}
    - Occupation: {customer['occupation']}
    - Monthly Salary: ₹{salary:,}
    - Account Balance: ₹{balance:,}
    - Idle Balance: ₹{balance_info['idle_balance']:,}
    - Investable Surplus after EMIs: ₹{surplus:,}

    Active Loans:
    {loan_details}

    Financial Summary:
    - Total Monthly EMI: ₹{total_emi:,}
    - EMI to Salary Ratio: {emi_ratio} ({int(emi_ratio*100)}% of salary)
    - Total Outstanding Debt: ₹{total_outstanding:,}

    Repayment Strategies Available:
    - Snowball Strategy (pay smallest first for motivation): {snowball_order}
    - Avalanche Strategy (pay highest EMI first for savings): {avalanche_order}

    Your job:
    1. Assess the overall loan burden severity (mild/moderate/severe)
    2. Recommend the best repayment strategy (snowball or avalanche) with clear reasoning
    3. Suggest a specific monthly budget breakdown:
       - Fixed EMIs: ₹X
       - Extra loan payment: ₹X (which loan and why)
       - Emergency savings: ₹X
       - Daily expenses: ₹X
    4. Calculate approximately how many months to become debt-free if they follow your plan
    5. Give 2-3 specific actionable tips to reduce debt faster
    6. If EMI ratio > 50%, flag it as a financial emergency and suggest loan restructuring

    Be specific with numbers. Use the customer's actual salary and loan figures.
    Format your response clearly with sections.
    Keep total response under 250 words.
    """

    response = llm.invoke(prompt)

    # Calculate basic metrics for UI
    months_to_payoff = round(total_outstanding / total_emi) if total_emi > 0 else 0
    burden_level = "🔴 Severe" if emi_ratio > 0.5 else "🟡 Moderate" if emi_ratio > 0.3 else "🟢 Manageable"

    return {
        "agent": "Loan Optimizer Agent",
        "has_loans": True,
        "status": "PLAN_GENERATED",
        "customer_name": customer["name"],
        "loan_summary": {
            "total_loans": len(loans),
            "total_emi": total_emi,
            "total_outstanding": total_outstanding,
            "emi_to_salary_ratio": emi_ratio,
            "burden_level": burden_level,
            "estimated_months_to_payoff": months_to_payoff,
            "monthly_salary": salary,
            "investable_surplus": surplus
        },
        "loans": loans,
        "repayment_plan": response.content,
        "optimization_tips": [
            f"Total debt of ₹{total_outstanding:,} can be cleared in ~{months_to_payoff} months at current EMI pace",
            f"EMIs consume {int(emi_ratio*100)}% of salary — {'consider restructuring' if emi_ratio > 0.5 else 'within manageable range'}",
            f"Idle balance of ₹{balance_info['idle_balance']:,} could be used for partial loan prepayment"
        ]
    }

if __name__ == "__main__":
    from agents.behavioral_agent import run_behavioral_agent
    behavioral_output = run_behavioral_agent("SBI-HYD-2024-051")
    result = run_loan_optimizer_agent(behavioral_output, "SBI-HYD-2024-051")
    print(json.dumps(result, indent=2))