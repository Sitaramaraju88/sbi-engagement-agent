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
    idle_balance = customer["idle_balance_amount"]

    # Calculate total monthly EMI burden from loans
    loans = customer.get("loans", [])
    total_emi = sum(loan["emi"] for loan in loans)
    total_outstanding = sum(loan["outstanding_amount"] for loan in loans)

    # Reserve buffer = total EMI + 20% of salary for emergencies
    salary = customer["monthly_salary"]
    reserve_buffer = total_emi + (salary * 0.2)

    # Investable surplus = idle balance - reserve buffer
    investable_surplus = max(idle_balance - reserve_buffer, 0)

    # EMI to salary ratio — critical for recommendations
    emi_to_salary_ratio = round(total_emi / salary, 2) if salary > 0 else 0

    return {
        "balance": balance,
        "idle_balance": idle_balance,
        "total_emi": total_emi,
        "total_outstanding": total_outstanding,
        "reserve_buffer": round(reserve_buffer),
        "investable_surplus": round(investable_surplus),
        "emi_to_salary_ratio": emi_to_salary_ratio,
        "loan_count": len(loans)
    }

def detect_disengagement(customer: dict) -> dict:
    signals = []
    score = 0

    # Cold start — very new customer with minimal data
    if len(customer.get("current_services_in_use", [])) == 0:
        return {
            "disengagement_score": 0,
            "disengagement_level": "Cold Start",
            "signals": ["New customer — no services in use"]
        }

    # Login signal
    if customer["last_login_days_ago"] > 60:
        signals.append(f"No login for {customer['last_login_days_ago']} days")
        score += 30
    elif customer["last_login_days_ago"] > 30:
        signals.append(f"Inactive for {customer['last_login_days_ago']} days")
        score += 15

    # Idle balance signal
    if customer["idle_balance_days"] > 90:
        signals.append(f"Balance idle for {customer['idle_balance_days']} days")
        score += 30
    elif customer["idle_balance_days"] > 30:
        signals.append(f"Balance partially idle for {customer['idle_balance_days']} days")
        score += 15

    # Notification response signal
    if customer["notification_response_rate"] < 0.1:
        signals.append("Very low notification response rate")
        score += 20
    elif customer["notification_response_rate"] < 0.3:
        signals.append("Low notification response rate")
        score += 10

    # Services signal
    services = customer.get("current_services_in_use", [])
    core_services = ["savings_account", "net_banking", "mobile_banking", "debit_card"]
    advanced_services = ["mutual_fund", "fd", "sip", "health_insurance", "life_insurance"]
    has_advanced = any(s in advanced_services for s in services)

    if len(services) < 2:
        signals.append("Using only 1 SBI service")
        score += 20
    elif not has_advanced:
        signals.append("Not using any investment or insurance products")
        score += 10

    level = "High" if score >= 60 else "Medium" if score >= 30 else "Low"

    return {
        "disengagement_score": min(score, 100),
        "disengagement_level": level,
        "signals": signals
    }

def get_engagement_type(customer: dict) -> str:
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

def get_recommendation(customer: dict, balance_info: dict, risk_appetite: str) -> list:
    recommendations = []
    services = customer.get("current_services_in_use", [])
    surplus = balance_info["investable_surplus"]
    emi_ratio = balance_info["emi_to_salary_ratio"]
    salary = customer["monthly_salary"]

    # If EMI burden is too high — no investment recommendations
    if emi_ratio > 0.5:
        return [{
            "action": "Debt Consolidation Advisory",
            "amount": 0,
            "reason": f"Total EMIs consume {int(emi_ratio*100)}% of salary. Focus on reducing debt before investing.",
            "tier": "Tier 1 — informational only"
        }]

    # If no investable surplus
    if surplus <= 0:
        return [{
            "action": "Build Emergency Fund",
            "amount": 0,
            "reason": "After EMIs and reserve buffer, no surplus available. Focus on building savings first.",
            "tier": "Tier 1 — informational only"
        }]

    # Insurance recommendations
    if "health_insurance" not in services and salary > 20000:
        recommendations.append({
            "action": "Get SBI Health Insurance",
            "amount": round(salary * 0.02),
            "reason": "No health insurance detected. Medical emergencies can wipe out savings.",
            "tier": "Tier 2 — requires your approval"
        })

    # FD recommendation for low risk
    if surplus > 10000 and risk_appetite == "low":
        recommendations.append({
            "action": "Open Fixed Deposit",
            "amount": round(surplus * 0.6),
            "reason": f"₹{surplus:,} idle for {customer['idle_balance_days']} days. FD gives guaranteed returns.",
            "tier": "Tier 1 — informational only"
        })

    # SIP for moderate risk
    if surplus > 20000 and risk_appetite == "moderate":
        if "mutual_fund" not in services:
            recommendations.append({
                "action": "Start SIP in Balanced Mutual Fund",
                "amount": min(5000, round(surplus * 0.1)),
                "reason": "Idle surplus detected. Balanced SIP suits your moderate risk profile.",
                "tier": "Tier 2 — requires your approval"
            })

    # Equity for high risk
    if surplus > 50000 and risk_appetite == "high":
        recommendations.append({
            "action": "Invest in Equity Mutual Fund",
            "amount": round(surplus * 0.3),
            "reason": "High surplus + high risk appetite. Equity funds suit long-term wealth creation.",
            "tier": "Tier 2 — requires your approval"
        })

    # Auto sweep for large idle amounts
    if surplus > 30000:
        recommendations.append({
            "action": "Auto-sweep Idle Balance to FD",
            "amount": round(surplus * 0.5),
            "reason": f"₹{surplus:,} sitting idle. Auto-sweep to FD earns better returns automatically.",
            "tier": "Tier 1 — informational only"
        })

    return recommendations if recommendations else [{
        "action": "Monitor and Review",
        "amount": 0,
        "reason": "Customer profile is stable. No immediate action required.",
        "tier": "Tier 1 — informational only"
    }]

def check_compliance(action: str) -> dict:
    autonomous_allowed = [
        "Auto-sweep Idle Balance to FD",
        "Monitor and Review",
        "Build Emergency Fund",
        "Debt Consolidation Advisory"
    ]
    approval_required = [
        "Start SIP in Balanced Mutual Fund",
        "Invest in Equity Mutual Fund",
        "Get SBI Health Insurance",
        "Open Fixed Deposit"
    ]

    if action in autonomous_allowed:
        return {"compliant": True, "requires_approval": False, "audit_logged": True}
    elif action in approval_required:
        return {"compliant": True, "requires_approval": True, "audit_logged": True}
    else:
        return {"compliant": False, "requires_approval": True, "audit_logged": True}