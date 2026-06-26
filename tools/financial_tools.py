import json
from pathlib import Path

def load_customer_data():
    path = Path("data/mock_customer.json")
    with open(path, "r") as f:
        return json.load(f)

def analyze_balance(customer: dict) -> dict:
    balance = customer["account_balance"]
    salary = customer["monthly_salary"]
    
    recurring_expenses = sum(
        t["amount"] for t in customer["transactions"]
        if t["type"] == "debit" and t["category"] in ["rent", "utilities"]
    )
    
    reserve_buffer = recurring_expenses * 1.5
    investable_surplus = balance - reserve_buffer
    
    return {
        "balance": balance,
        "recurring_expenses": recurring_expenses,
        "reserve_buffer": round(reserve_buffer),
        "investable_surplus": round(max(investable_surplus, 0))
    }

def detect_disengagement(customer: dict) -> dict:
    signals = []
    score = 0

    if customer["last_login_days_ago"] > 7:
        signals.append(f"No login for {customer['last_login_days_ago']} days")
        score += 30

    if customer["idle_balance_days"] > 30:
        signals.append(f"Balance idle for {customer['idle_balance_days']} days")
        score += 30

    if customer["notification_response_rate"] < 0.3:
        signals.append("Low notification response rate")
        score += 20

    if len(customer["existing_products"]) < 3:
        signals.append("Using fewer than 3 SBI products")
        score += 20

    level = "High" if score >= 60 else "Medium" if score >= 30 else "Low"

    return {
        "disengagement_score": score,
        "disengagement_level": level,
        "signals": signals
    }

def get_recommendation(customer: dict, surplus: float) -> list:
    recommendations = []
    goals = customer["financial_goals"]
    risk = customer["risk_appetite"]

    if "emergency_fund" in goals and surplus > 10000:
        recommendations.append({
            "action": "Open Recurring Deposit",
            "amount": 5000,
            "reason": "Build emergency fund — 3 months expenses target",
            "tier": "Tier 2 — requires your approval"
        })

    if risk == "moderate" and surplus > 20000:
        recommendations.append({
            "action": "Start SIP in Balanced Mutual Fund",
            "amount": 3000,
            "reason": "Idle surplus detected — moderate risk SIP suits your profile",
            "tier": "Tier 2 — requires your approval"
        })

    if surplus > 30000:
        recommendations.append({
            "action": "Auto-sweep excess to FD",
            "amount": round(surplus * 0.5),
            "reason": f"₹{surplus} idle for {customer['idle_balance_days']} days — FD gives better returns",
            "tier": "Tier 1 — informational only"
        })

    return recommendations

def check_compliance(action: str) -> dict:
    autonomous_allowed = ["Auto-sweep excess to FD"]
    approval_required = ["Start SIP in Balanced Mutual Fund", "Open Recurring Deposit"]

    if action in autonomous_allowed:
        return {"compliant": True, "requires_approval": False, "audit_logged": True}
    elif action in approval_required:
        return {"compliant": True, "requires_approval": True, "audit_logged": True}
    else:
        return {"compliant": False, "requires_approval": True, "audit_logged": True}