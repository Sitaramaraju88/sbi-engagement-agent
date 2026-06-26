import json
from pathlib import Path

def load_all_customers():
    path = Path("data/mock_customer.json")
    with open(path, "r") as f:
        return json.load(f)
    
def load_customer_data(customer_id: str = None):
    customers = load_all_customers()
    if customer_id:
        for c in customers:
            if c["customer_id"] == customer_id:
                return c
    return customers[0]

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

def get_recommendation(customer: dict, surplus: float, risk_appetite: str = "moderate") -> list:
    recommendations = []
    goals = customer["financial_goals"]

    if surplus <= 0:
        return [{
            "action": "Build Savings First",
            "amount": 0,
            "reason": "Insufficient surplus for investment. Focus on building emergency fund.",
            "tier": "Tier 1 — informational only"
        }]

    if "emergency_fund" in goals and surplus > 5000:
        recommendations.append({
            "action": "Open Recurring Deposit",
            "amount": min(5000, int(surplus * 0.1)),
            "reason": "Build emergency fund — 3 months expenses target",
            "tier": "Tier 2 — requires your approval"
        })

    if risk_appetite in ["moderate", "high"] and surplus > 20000:
        recommendations.append({
            "action": "Start SIP in Balanced Mutual Fund",
            "amount": min(3000, int(surplus * 0.05)),
            "reason": "Idle surplus detected — SIP suits your risk profile",
            "tier": "Tier 2 — requires your approval"
        })

    if surplus > 30000:
        recommendations.append({
            "action": "Auto-sweep excess to FD",
            "amount": round(surplus * 0.5),
            "reason": f"₹{surplus} idle for {customer['idle_balance_days']} days — FD gives better returns",
            "tier": "Tier 1 — informational only"
        })

    if risk_appetite == "high" and surplus > 50000:
        recommendations.append({
            "action": "Invest in Equity Mutual Fund",
            "amount": round(surplus * 0.3),
            "reason": "High risk appetite and large surplus — equity suits long-term wealth creation",
            "tier": "Tier 2 — requires your approval"
        })

    return recommendations if recommendations else [{
        "action": "Monitor and Review",
        "amount": 0,
        "reason": "Insufficient data or surplus for recommendation",
        "tier": "Tier 1 — informational only"
    }]

def check_compliance(action: str) -> dict:
    autonomous_allowed = ["Auto-sweep excess to FD"]
    approval_required = ["Start SIP in Balanced Mutual Fund", "Open Recurring Deposit"]

    if action in autonomous_allowed:
        return {"compliant": True, "requires_approval": False, "audit_logged": True}
    elif action in approval_required:
        return {"compliant": True, "requires_approval": True, "audit_logged": True}
    else:
        return {"compliant": False, "requires_approval": True, "audit_logged": True}

def get_engagement_type(customer: dict) -> str:
    """Dynamically calculate engagement type from raw customer data"""
    result = detect_disengagement(customer)
    level = result["disengagement_level"]
    if level == "Cold Start":
        return "Cold Start"
    elif level == "High":
        return "High Disengagement"
    elif level == "Medium":
        return "Medium Disengagement"
    else:
        return "Low Disengagement"