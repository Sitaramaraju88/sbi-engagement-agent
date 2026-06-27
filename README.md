# 🏦 SBI Agentic AI — Digital Engagement System

> Built for **SBI Hackathon 2026** | Topic: Agentic AI & Emerging Technologies

---

## 🤔 What is this project?

SBI has **500 million+ customers** — but most of them only use the app to check their balance or do UPI transfers. They don't invest, don't save smartly, and don't manage their loans efficiently.

This project builds an **Agentic AI system** that:
- 👀 Detects when a customer is disengaged — from raw data, no pre-labels
- 🧠 Uses an LLM to calculate their risk appetite intelligently
- 💳 Plans optimal loan repayment strategies based on salary and debt burden
- 💡 Recommends the right financial action at the right time
- ✅ Takes action automatically — with the customer's approval

Think of it as a **personal finance assistant** that works quietly in the background and only speaks up when it has something genuinely useful to say.

---

## 🧠 What is Agentic AI?

Normal AI: You ask a question → AI answers.

**Agentic AI**: AI has a goal → AI plans → AI delegates → AI acts → AI reports back.

Our system has **4 AI agents** that work together like a team:

```
Customer Raw Data (no pre-labels)
           ↓
🔍 Behavioral Intelligence Agent   →   detects disengagement + calculates risk appetite via LLM
           ↓
💳 Loan Optimizer Agent            →   plans optimal loan repayment strategy
           ↓
💡 Proactive Advisor Agent         →   picks best recommendation based on AI-calculated risk
           ↓
⚡ Autonomous Action Agent         →   compliance check → execute or seek approval → audit log
```

> **Key distinction from a rule engine:** Rules can prioritize recommendations, but they cannot write personalized human-sounding messages, reason across conflicting signals holistically, or explain decisions in plain language. The LLM handles all three.

---

## 🏗️ Project Structure

```
sbi-engagement-agent/
│
├── agents/
│   ├── behavioral_agent.py       # Agent 1 — detects disengagement, LLM calculates risk appetite
│   ├── loan_optimizer_agent.py   # Agent 2 — optimal loan repayment planning
│   ├── advisor_agent.py          # Agent 3 — personalized recommendations + LLM message
│   └── action_agent.py           # Agent 4 — compliance check, execute or seek approval
│
├── tools/
│   └── financial_tools.py        # Shared tools: balance analysis, disengagement detection,
│                                 #               compliance check, engagement type detection
│
├── ui/
│   └── app.py                    # Streamlit web interface with customer selector + filter
│
├── data/
│   └── mock_customer.json        # 100 customer profiles — no pre-labels, AI detects everything
│
├── main.py                       # Orchestrator — connects all 4 agents, supports caching
├── .env                          # API keys (never commit this!)
├── .gitignore                    # Ignores sensitive files
└── requirements.txt              # Python dependencies
```

---

## ⚙️ How Each Agent Works

### 🔍 Agent 1 — Behavioral Intelligence Agent

Analyzes raw customer data and outputs two things:

**Disengagement Score (0–100):**

| Signal | Score Added |
|---|---|
| No login for 60+ days | +30 |
| No login for 30-60 days | +15 |
| Balance idle for 90+ days | +30 |
| Balance idle for 30-90 days | +15 |
| Very low notification response (<10%) | +20 |
| Low notification response (<30%) | +10 |
| Using only 1 SBI service | +20 |
| No investment/insurance products | +10 |

**Risk Appetite (via LLM — not hardcoded rules):**

The LLM reasons across age, income, balance, loan burden, and occupation together:
```
Charan Dubey (Farmer, age 61, ₹13K salary, no loans) → LOW risk
Ananya Chauhan (Business Owner, age 28, ₹2.55L salary) → HIGH risk
Zara Jain (Sales Manager, EMI ratio 250%) → LOW risk despite age
```
The LLM understands context — a high EMI burden always overrides age or occupation.

---

### 💳 Agent 2 — Loan Optimizer Agent

**Only activates for customers with active loans.** For others, it confirms full salary is available for savings.

- Calculates **EMI to salary ratio** — flags if >50% as financial emergency
- Compares **Snowball strategy** (pay smallest loan first) vs **Avalanche strategy** (pay highest EMI first)
- Generates a **month-by-month budget breakdown**
- Estimates **months to debt freedom** at current pace
- Suggests if **idle balance** can be used for loan prepayment

---

### 💡 Agent 3 — Proactive Advisor Agent

Reads Agent 1 and Agent 2's reports and:
- Calculates **investable surplus** = idle balance − (EMIs + 20% salary safety buffer)
- If EMI ratio >50% → recommends debt consolidation only, no investments
- Matches recommendations to the customer's **AI-calculated risk appetite**
- LLM writes a **personalized, human-sounding message** under 100 words

---

### ⚡ Agent 4 — Autonomous Action Agent

Runs a **3-tier compliance check** before any action:

| Tier | Example | What Happens |
|---|---|---|
| Tier 1 | Auto-sweep to FD, Debt Advisory | Executes automatically |
| Tier 2 | Start SIP, Open RD, Health Insurance | Sent for customer approval |
| Tier 3 | Unknown action | Blocked entirely |

Every action generates an **immutable audit log** with customer ID, timestamp, amount, compliance status, EMI ratio, and investable surplus at time of action.

---

## 👥 Customer Dataset

**100 real-world customer profiles** across diverse Indian cities, occupations, and financial situations — **no pre-labels anywhere**. The AI detects everything dynamically.

Dataset covers:
- Customers with no loans (simple savings/investment focus)
- Customers with single loans (home, education, car)
- Customers with multiple loans (gold + home + personal)
- High income professionals (doctors, lawyers, business owners)
- Low income earners (farmers, electricians, daily wage)
- Retired and senior citizens
- Young professionals just starting out

**Sample profiles:**

| Customer ID | Profile | Has Loans | AI Engagement |
|---|---|---|---|
| SBI-HYD-2024-001 | Bhargavi Mehta, Lawyer, 22 | No | 🟡 Medium |
| SBI-HYD-2024-006 | Charan Dubey, Farmer, 61 | No | 🔴 High |
| SBI-HYD-2024-012 | Ananya Chauhan, Business Owner, 28 | No | 🟡 Medium |
| SBI-HYD-2024-051 | Zara Jain, Sales Manager, 59 | Yes — 3 loans | 🔴 High |
| SBI-HYD-2024-081 | Priya Pandey, Business Owner, 33 | Yes — 2 loans | 🔴 High |

---

## 🛡️ Safety & Compliance

Every concern a bank would have is addressed:

| Concern | Our Solution |
|---|---|
| Privacy surveillance | Consent dashboard — toggle per data type |
| Wrong recommendations | Reserve buffer = EMIs + 20% salary safety margin |
| High loan burden | Agent 2 detects EMI >50% salary and blocks investments |
| Notification fatigue | Max 1 nudge/week, event-triggered only |
| Regulatory compliance | 3-tier action model, audit trail on everything |
| AI hallucinations | Domain-constrained LLM, approved product whitelist |
| Financial liability | Execution assistant only — customer always approves |
| Cold start | 5-question onboarding + observe-only mode for 30 days |

> *"The AI's job is to reduce the cognitive load of managing money — never to replace human judgment."*

---

## 🧰 Tech Stack

| Tool | Purpose | Cost |
|---|---|---|
| **Python 3.11** | Core language | Free |
| **LangChain** | Agent orchestration | Free / OSS |
| **Groq API** | LLM inference | Free tier |
| **LLaMA 3.3 70B** | Core reasoning model | Free via Groq |
| **Streamlit** | Web UI | Free |
| **FAISS** | Vector store for RAG | Free / OSS |
| **python-dotenv** | Secure key management | Free |

**Total infrastructure cost: ₹0**

---

## 🚀 How to Run This Project

### Step 1 — Clone the repo
```bash
git clone https://github.com/Sitaramaraju88/sbi-engagement-agent.git
cd sbi-engagement-agent
```

### Step 2 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3 — Add your Groq API key
Create a `.env` file in the root folder:
```
GROQ_API_KEY=gsk_your_key_here
```
Get a free key at [console.groq.com](https://console.groq.com)

> **Note for Windows users:** If `.env` is not loading, set the key directly:
> ```powershell
> $env:GROQ_API_KEY = "gsk_your_key_here"
> ```

### Step 4 — Run the pipeline (terminal)
```bash
python main.py
```

### Step 5 — Run the web UI
```bash
streamlit run ui/app.py
```
Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 📊 Sample Output

```
============================================================
   SBI AGENTIC AI - DIGITAL ENGAGEMENT SYSTEM
============================================================

[1/4] Running Behavioral Intelligence Agent...
✅ Disengagement Level  : High
✅ Disengagement Score  : 80/100
✅ Investable Surplus   : ₹0
✅ AI Risk Appetite     : low

[2/4] Running Loan Optimizer Agent...
✅ Loans Found          : 3
✅ Total EMI            : ₹97,000
✅ Burden Level         : 🔴 Severe

[3/4] Running Proactive Advisor Agent...
✅ Recommendations Found : 1
✅ Best Action           : Debt Consolidation Advisory

[4/4] Running Autonomous Action Agent...
✅ Action Status  : EXECUTED
✅ Compliant      : True
✅ Audit Logged   : True

============================================================
   PIPELINE COMPLETE
============================================================
```

---

## 🙋 Frequently Asked Questions

**Q: Why not just use IF-ELSE rules instead of AI?**

Rules can prioritize recommendations. But they cannot:
1. Write personalized human-sounding messages that drive engagement
2. Reason holistically across conflicting signals (e.g. high salary + high EMI burden = low risk)
3. Explain loan repayment strategies in plain language customers trust

The LLM handles all three. Rules handle structured decisions like compliance tiers and audit logging.

**Q: How does the Loan Optimizer Agent work?**

It compares two strategies — Snowball (pay smallest loan first for motivation) and Avalanche (pay highest EMI first for maximum savings). The LLM picks the best one based on the customer's salary, outstanding amounts, and financial stress level, then generates a month-by-month budget breakdown.

**Q: What if a customer has too many loans?**

If EMI burden exceeds 50% of salary, the system immediately flags it as a financial emergency, blocks any investment recommendations, and instead suggests debt consolidation. The Loan Optimizer Agent takes priority over the Advisor Agent in this case.

**Q: Is customer data safe?**

The LLM only receives anonymized behavioral signals — no raw account numbers or personal identifiers. All data stays within SBI's infrastructure. Customers can revoke access anytime from the consent dashboard.

**Q: Can the AI lose my money?**

No. The AI never recommends investments when EMIs are too high. It only works with the investable surplus after all EMIs and a 20% salary safety buffer are accounted for. All investment actions require explicit customer approval.

**Q: How does it scale to 500M customers?**

Event-driven architecture — agents only activate on financial triggers. A lightweight rule filter processes all events first. Only high-signal events (idle balance >30 days, salary credited, EMI due) trigger the LLM pipeline, reducing LLM calls by ~95%.

---

## 📈 Projected Impact

Based on industry benchmarks (McKinsey Banking 2023, Bain Fintech Report):

| Metric | Projection | Basis |
|---|---|---|
| Feature Adoption | +40% | Personalized nudges lift engagement 35-45%* |
| Customer Retention | +30% | Proactive engagement reduces churn 25-35%* |
| Notification Response | 3× | Event-triggered beats generic alerts by 2-4×* |
| Loan Default Reduction | -20% | Proactive repayment planning reduces defaults* |
| Audit Compliance | 100% | Every action logged — measured, not projected ✅ |

*Based on McKinsey Banking 2023 & Bain Fintech Report

---

## 👨‍💻 Built By

**M V Sita Rama Raju**
B.Tech Computer Science | KL University, Hyderabad (2023–2027)
DSA Mentor & Technical Team Member, Avinya Club
🏆 First Place — OpenSourceX Hackathon 2025

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

*Built with ❤️ for SBI Hackathon 2026*