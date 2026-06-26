# 🏦 SBI Agentic AI — Digital Engagement System

> Built for **SBI Hackathon 2026** | Topic: Agentic AI & Emerging Technologies
---

## 🤔 What is this project?

SBI has **500 million+ customers** — but most of them only use the app to check their balance or do UPI transfers. They don't invest, don't save smartly, and don't use most of the features SBI offers.

This project builds an **Agentic AI system** that:
- 👀 Detects when a customer is disengaged — from raw data, no pre-labels
- 🧠 Uses an LLM to calculate their risk appetite intelligently
- 💡 Recommends the right financial action at the right time
- ✅ Takes action automatically — with the customer's approval

Think of it as a **personal finance assistant** that works quietly in the background and only speaks up when it has something genuinely useful to say.

---

## 🧠 What is Agentic AI?

Normal AI: You ask a question → AI answers.

**Agentic AI**: AI has a goal → AI plans → AI delegates → AI acts → AI reports back.

Our system has **3 AI agents** that work together like a team:

```
Customer Raw Data (no pre-labels)
           ↓
🔍 Behavioral Intelligence Agent   →   detects disengagement + calculates risk appetite via LLM
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
│   ├── behavioral_agent.py      # Agent 1 — detects disengagement, LLM calculates risk appetite
│   ├── advisor_agent.py         # Agent 2 — personalized recommendations + LLM message
│   └── action_agent.py          # Agent 3 — compliance check, execute or seek approval
│
├── tools/
│   └── financial_tools.py       # Shared tools: balance analysis, disengagement detection,
│                                #               compliance check, engagement type detection
│
├── ui/
│   └── app.py                   # Streamlit web interface with customer selector + filter
│
├── data/
│   └── mock_customer.json       # 6 customer profiles — no pre-labels, AI detects everything
│
├── main.py                      # Orchestrator — connects all 3 agents, supports caching
├── .env                         # API keys (never commit this!)
├── .gitignore                   # Ignores sensitive files
└── requirements.txt             # Python dependencies
```

---

## ⚙️ How Each Agent Works

### 🔍 Agent 1 — Behavioral Intelligence Agent

Analyzes raw customer data and outputs two things:

**Disengagement Score (0–100):**

| Signal | Score Added |
|---|---|
| No login for 7+ days | +30 |
| Balance idle for 30+ days | +30 |
| Low notification response rate (<30%) | +20 |
| Using fewer than 3 SBI products | +20 |

**Risk Appetite (via LLM — not hardcoded rules):**

The LLM reasons across age, income, balance, goals, and transaction history together:
```
Rohan (Student, age 20, zero income, education goal) → LOW risk
Priya (Banker, age 34, ₹1.2L salary, wealth goals)  → HIGH risk
```
A 20-year-old gets LOW risk not because of a rule but because the LLM understands context.

---

### 💡 Agent 2 — Proactive Advisor Agent

Reads Agent 1's full report and:
- Calculates **investable surplus** = balance − (1.5× recurring expenses)
- Only recommends from the surplus — never touches the safety buffer
- Matches recommendations to the customer's **goals** and **AI-calculated risk**
- LLM writes a **personalized, human-sounding message** under 100 words

---

### ⚡ Agent 3 — Autonomous Action Agent

Runs a **3-tier compliance check** before any action:

| Tier | Example | What Happens |
|---|---|---|
| Tier 1 | Auto-sweep to FD | Executes automatically |
| Tier 2 | Start SIP, Open RD | Sent for customer approval |
| Tier 3 | Unknown action | Blocked entirely |

Every action generates an **immutable audit log** with timestamp, amount, compliance status, and approval status.

---

## 👥 Customer Dataset

6 diverse customer profiles — **no pre-labels anywhere**. The AI detects everything:

| Customer ID | Profile | AI Detected Engagement |
|---|---|---|
| SBI-HYD-2024-001 | Rahul Sharma, Software Engineer, 28 | 🔴 High Disengagement |
| SBI-MUM-2024-002 | Priya Patel, Investment Banker, 34 | 🟢 Low Disengagement |
| SBI-DEL-2024-003 | Amit Verma, Fresh Graduate, 22 | 🔵 Cold Start |
| SBI-CHN-2024-004 | Lakshmi Narayanan, Retired Teacher, 58 | 🟡 Medium Disengagement |
| SBI-BLR-2024-005 | Rohan Mehta, Student, 20 | 🔴 High Disengagement |
| SBI-KOL-2024-006 | Sunita Agarwal, Business Owner, 45 | 🟢 Low Disengagement |

---

## 🛡️ Safety & Compliance

Every concern a bank would have is addressed:

| Concern | Our Solution |
|---|---|
| Privacy surveillance | Consent dashboard — toggle per data type |
| Wrong recommendations | Reserve buffer = 1.5× recurring expenses |
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
git clone https://github.com/YOUR_USERNAME/sbi-engagement-agent.git
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

[1/3] Running Behavioral Intelligence Agent...
✅ Disengagement Level  : High
✅ Disengagement Score  : 100/100
✅ Investable Surplus   : ₹58,000
✅ AI Risk Appetite     : moderate

[2/3] Running Proactive Advisor Agent...
✅ Recommendations Found : 3
✅ Best Action           : Open Recurring Deposit
✅ Amount                : ₹5,000

[3/3] Running Autonomous Action Agent...
✅ Action Status  : PENDING_APPROVAL
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
2. Reason holistically across conflicting signals (e.g. young age + zero income = low risk, not high)
3. Explain decisions in plain language that customers trust

The LLM handles all three. Rules handle structured, clear-cut decisions like compliance tiers and audit logging.

**Q: Why does a 20-year-old student get LOW risk appetite?**

Because the LLM reasons across ALL signals together — not just age. Zero income + education goal + low balance = low risk, regardless of age. This is the key difference from a rule engine.

**Q: Is customer data safe?**

The LLM only receives anonymized behavioral signals, not raw transactions. All data stays within SBI's infrastructure. Customers can revoke access anytime from the consent dashboard.

**Q: Can the AI lose my money?**

No. The AI never touches the safety buffer (1.5× recurring expenses). It only works with the investable surplus. All investment actions require explicit customer approval before executing.

**Q: How does it scale to 500M customers?**

Event-driven architecture — agents only activate on financial triggers, not for every customer daily. A lightweight rule filter processes all events first. Only high-signal events (idle balance >30 days, salary credited) trigger the LLM pipeline, reducing LLM calls by ~95%.

---

## 📈 Projected Impact

Based on industry benchmarks (McKinsey Banking 2023, Bain Fintech Report):

| Metric | Projection | Basis |
|---|---|---|
| Feature Adoption | +40% | Personalized nudges lift engagement 35-45% |
| Customer Retention | +30% | Proactive engagement reduces churn 25-35% |
| Notification Response | 3× | Event-triggered beats generic alerts by 2-4× |
| Audit Compliance | 100% | Every action logged — measured, not projected |

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