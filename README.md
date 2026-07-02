🏦 SBI Agentic AI — Digital Engagement System

Built for SBI Hackathon 2026 · Topic: Agentic AI & Emerging Technologies

Show Image
Show Image
Show Image
Show Image


📑 Table of Contents


What is this project?
What is Agentic AI?
Project Structure
How Each Agent Works
Customer Dataset & Relational Database
Safety & Compliance
Tech Stack
How to Run This Project
Sample Pipeline Output
FAQ
Projected Impact
Built By
License



🤔 What is this project?

SBI has 500 million+ customers — but most of them only use the app to check their balance or do UPI transfers. They don't invest, don't save smartly, and don't manage their loans efficiently.

This project builds an Agentic AI system that:


👀 Detects when a customer is disengaged — from raw database tables, with no pre-labels
🧠 Uses an LLM to intelligently calculate their risk appetite
💳 Plans optimal loan repayment strategies based on salary and debt burden
💡 Recommends the right financial action at the right time
🌐 Communicates insights via a Multi-language Notification Engine (English, Hindi, Telugu, etc.)
✅ Takes action automatically — with the customer's approval


Think of it as a personal finance assistant that works quietly in the background and only speaks up when it has something genuinely useful to say.


🧠 What is Agentic AI?

Normal AIAgentic AIYou ask a question → AI answersAI has a goal → plans → delegates → acts → reports back

Our system has 4 AI agents that work together like a team:

Relational Database (SQLite3)
             ↓
  🔍 Behavioral Intelligence Agent   →  detects disengagement + calculates risk appetite via LLM
             ↓
  💳 Loan Optimizer Agent            →  plans optimal loan repayment strategy
             ↓
  💡 Proactive Advisor Agent         →  picks best recommendation + structures multi-language nudges
             ↓
  ⚡ Autonomous Action Agent         →  compliance check → execute or seek approval → audit log

Key distinction from a rule engine: rules can prioritize recommendations, but they can't write personalized human-sounding messages, dynamically translate notifications into a customer's regional language, reason across conflicting signals holistically, or explain decisions in plain language. The LLM handles all three.


🏗️ Project Structure

sbi-engagement-agent/
│
├── agents/
│   ├── behavioral_agent.py      # Agent 1 — detects disengagement, LLM calculates risk appetite
│   ├── loan_optimizer_agent.py  # Agent 2 — optimal loan repayment planning
│   ├── advisor_agent.py         # Agent 3 — personalized recommendations + multi-language messages
│   └── action_agent.py          # Agent 4 — compliance check, execute or seek approval
│
├── tools/
│   └── financial_tools.py       # Shared DB logic, balance analysis, disengagement detection,
│                                 # compliance check
│
├── ui/
│   └── app.py                   # Streamlit web interface with customer selector + filters
│
├── sbi_bank.db                  # SQLite3 database — relational customer & loan schemas
├── migrate.py                   # One-click data migration utility (JSON → SQLite3)
├── main.py                      # Orchestrator — connects all 4 agents, supports caching
├── .env                         # API keys (never commit this!)
├── .gitignore                   # Ignores sensitive files
└── requirements.txt             # Python dependencies


⚙️ How Each Agent Works

🔍 Agent 1 — Behavioral Intelligence Agent

Analyzes relational customer records dynamically and outputs two things:

Disengagement Score (0–100)

SignalScore AddedNo login for 60+ days+30No login for 30–60 days+15Balance idle for 90+ days+30Balance idle for 30–90 days+15Very low notification response (<10%)+20Low notification response (<30%)+10Using only 1 SBI service+20No investment/insurance products+10

Risk Appetite (via LLM — not hardcoded rules)

The LLM reasons across age, income, balance, loan burden, and occupation together:


Charan Dubey (Farmer, age 61, ₹13K salary, no loans) → LOW risk
Ananya Chauhan (Business Owner, age 28, ₹2.55L salary) → HIGH risk
Zara Jain (Sales Manager, EMI ratio 250%) → LOW risk despite age


The LLM understands context — a high EMI burden always overrides age or occupation.

💳 Agent 2 — Loan Optimizer Agent

Only activates for customers with active loans queried from the relational loans table. For others, it confirms full salary is available for savings.


Calculates EMI-to-salary ratio — flags it as a financial emergency if >50%
Compares Snowball strategy (pay smallest loan first) vs Avalanche strategy (pay highest-interest loan first)
Generates a month-by-month budget breakdown and estimates months to debt freedom at the current pace
Suggests whether idle balance can be used for loan prepayment


💡 Agent 3 — Proactive Advisor Agent

Reads Agent 1 and Agent 2's reports and constructs hyper-personalized strategies:


Calculates investable surplus = idle balance − (EMIs + 20% salary safety buffer)
If EMI ratio >50% → recommends debt consolidation only, no investments
Matches financial recommendations directly to the customer's AI-calculated risk appetite
Multi-language Notification Engine: the LLM localizes and drafts a friendly, human-sounding nudge under 100 words in the customer's native language (English, Hindi, Telugu, etc.) based on their demographic/regional profile


⚡ Agent 4 — Autonomous Action Agent

Runs a 3-tier compliance check before any action:

TierExampleWhat HappensTier 1Auto-sweep to FD, Debt AdvisoryExecutes automaticallyTier 2Start SIP, Open RD, Health InsuranceSent for customer approvalTier 3Unknown actionBlocked entirely

Every action generates an immutable audit log with customer ID, timestamp, amount, compliance status, EMI ratio, and investable surplus at time of action.


👥 Customer Dataset & Relational Database

The architecture is built on a relational SQLite3 engine that maps personal data tables to specialized loan tables via foreign keys. It handles 100 real-world customer profiles across diverse Indian cities, occupations, and financial situations — with no pre-labels anywhere.

Database Schema Map


customers table — demographic metrics, salaries, balances, activity tracking, and stringified service maps
loans table — independent loan records (loan_type, sanctioned_amount, outstanding_amount, emi, tenure_months), linked back via customer_id as a foreign key


Sample profiles in sbi_bank.db

Customer IDProfileHas LoansAI EngagementSBI-HYD-2024-001Bhargavi Mehta, Lawyer, 22No🟡 MediumSBI-HYD-2024-006Charan Dubey, Farmer, 61No🔴 HighSBI-HYD-2024-012Ananya Chauhan, Business Owner, 28No🟡 MediumSBI-HYD-2024-051Zara Jain, Sales Manager, 59Yes — 3 loans🔴 HighSBI-HYD-2024-081Priya Pandey, Business Owner, 33Yes — 2 loans🔴 High


🛡️ Safety & Compliance

ConcernMitigationPrivacy surveillanceConsent dashboard — toggle per data typeWrong recommendationsReserve buffer = EMIs + 20% salary safety marginHigh loan burdenAgent 2 detects EMI >50% of salary and blocks investmentsNotification fatigueMax 1 nudge/week, event-triggered onlyRegulatory compliance3-tier action model, audit trail on everythingAI hallucinationsDomain-constrained LLM, approved product whitelistFinancial liabilityExecution assistant only — customer always approvesCold start5-question onboarding + observe-only mode for 30 days


"The AI's job is to reduce the cognitive load of managing money — never to replace human judgment."




🧰 Tech Stack

ToolPurposeCostPython 3.11Core languageFreeSQLite3Lightweight relational database engineFree / IncludedLangChainAgent orchestrationFree / OSSGroq APILLM inferenceFree tierLLaMA 3.3 70BCore reasoning & multi-language translationFree via GroqStreamlitWeb UI engineFreepython-dotenvSecure key managementFree

Total infrastructure cost: ₹0


🚀 How to Run This Project

Step 1 — Clone the repo

bashgit clone https://github.com/Sitaramaraju88/sbi-engagement-agent.git
cd sbi-engagement-agent

Step 2 — Install dependencies

bashpip install -r requirements.txt

Step 3 — Seed/populate your SQLite3 database

Run the migration script to extract the original customer profiles and build the relational database layout:

bashpython migrate.py

Step 4 — Add your Groq API key

Create a .env file in the root folder:

GROQ_API_KEY=gsk_your_key_here


Windows users: if .env isn't loading, set the key directly in PowerShell:

powershell$env:GROQ_API_KEY = "gsk_your_key_here"



Step 5 — Run the pipeline (terminal)

bashpython main.py

Step 6 — Run the web UI

bashstreamlit run ui/app.py

Then open http://localhost:8501 in your browser.


📊 Sample Pipeline Output

============================================================
   SBI AGENTIC AI - DIGITAL ENGAGEMENT SYSTEM
============================================================

[1/5] Connecting to SQLite3 Database Schema... Connected.
[2/5] Running Behavioral Intelligence Agent...
✅ Disengagement Level  : High
✅ Disengagement Score  : 80/100
✅ Investable Surplus   : ₹0
✅ AI Risk Appetite     : Low

[3/5] Running Loan Optimizer Agent...
✅ Loans Found from DB  : 3
✅ Total EMI            : ₹97,000
✅ Burden Level         : 🔴 Severe

[4/5] Running Proactive Advisor Agent...
✅ Recommendations Found : 1
✅ Best Action           : Debt Consolidation Advisory
✅ Multi-language Nudge  : Generated successfully (Hindi/Telugu localized)

[5/5] Running Autonomous Action Agent...
✅ Action Status  : EXECUTED
✅ Compliant      : True
✅ Audit Logged   : True

============================================================
   PIPELINE COMPLETE
============================================================


🙋 Frequently Asked Questions

Q: Why migrate from JSON files to SQLite3?
JSON scales terribly for 500M customers. SQLite3 gives relational stability, unlocks real SQL filtering (WHERE customer_id = ?), enforces loan-to-customer constraints securely via foreign keys, and demonstrates production intent to the judges.

Q: How does the Multi-language Notification Engine work?
The Proactive Advisor Agent reads the customer's geographic and cultural profile from the database (city, occupation). The LLM uses its natural multilingual ability to translate financial advice directly into regional languages, bypassing robotic translation software for a more personal connection.

Q: What if a customer has too many loans?
If the EMI burden exceeds 50% of salary, the system immediately flags a financial emergency, blocks any investment recommendations, and instead suggests debt consolidation. The Loan Optimizer Agent takes priority over the Advisor Agent in this case.

Q: Can the AI lose my money?
No. The AI never recommends investments when EMIs are too high. It only works with the investable surplus left after all EMIs and a 20% salary safety buffer are accounted for. All investment actions require explicit customer approval.

Q: How does it scale to 500M customers?
Event-driven architecture — agents only activate on financial triggers. A lightweight database index handles query lookups, and only high-signal changes (idle balance >30 days, salary credited, EMI due) trigger the LLM pipeline, keeping compute overhead low.


📈 Projected Impact

Based on industry benchmarks (McKinsey Banking 2023, Bain Fintech Report):

MetricProjected ChangeFeature Adoption+40% — personalized, localized nudges lift product explorationCustomer Retention+30% — proactive, localized interventions reduce churnNotification Response3× — localized, context-driven notifications outperform generic English alertsLoan Default Reduction-20% — direct strategy intervention prevents loan cycle dropsAudit Compliance100% — structured logs capture every action


👨‍💻 Built By

M V Sita Rama Raju
B.Tech Computer Science · KL University, Hyderabad (2023–2027)
DSA Mentor & Technical Team Member, Avinya Club
🏆 First Place — OpenSourceX Hackathon 2025


📄 License

MIT License — free to use, modify, and distribute.


Built with ❤️ for SBI Hackathon 2026