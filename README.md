🏦 SBI Agentic AI — Digital Engagement System


Built for SBI Hackathon 2026 | Topic: Agentic AI & Emerging Technologies




🤔 What is this project?

SBI has 500 million+ customers — but most of them only use the app to check their balance or do UPI transfers. They don't invest, don't save smartly, and don't use most of the features SBI offers.

This project builds an Agentic AI system that:


👀 Watches for signs that a customer is disengaged
💡 Recommends the right financial action at the right time
✅ Takes action automatically (with the customer's approval)


Think of it as a personal finance assistant that works quietly in the background and only speaks up when it has something genuinely useful to say.


🧠 What is Agentic AI?

Normal AI: You ask a question → AI answers.

Agentic AI: AI has a goal → AI plans → AI acts → AI reports back.

Our system has 3 AI agents that work together like a team:

Customer Data
     ↓
🔍 Behavioral Intelligence Agent   →   detects disengagement
     ↓
💡 Proactive Advisor Agent         →   picks the best recommendation
     ↓
⚡ Autonomous Action Agent         →   executes (with approval)


🏗️ Project Structure

sbi-engagement-agent/
│
├── agents/
│   ├── behavioral_agent.py      # Agent 1 - detects disengagement
│   ├── advisor_agent.py         # Agent 2 - recommends actions
│   └── action_agent.py          # Agent 3 - executes with compliance
│
├── tools/
│   └── financial_tools.py       # Shared tools used by all agents
│
├── ui/
│   └── app.py                   # Streamlit web interface
│
├── data/
│   └── mock_customer.json       # Sample customer data
│
├── main.py                      # Orchestrator - connects all 3 agents
├── .env                         # API keys (never commit this!)
├── .gitignore                   # Ignores sensitive files
└── requirements.txt             # Python dependencies


⚙️ How Each Agent Works

🔍 Agent 1 — Behavioral Intelligence Agent

Looks at the customer's data and calculates a disengagement score (0-100):

SignalScore AddedNo login for 7+ days+30Balance idle for 30+ days+30Low notification response rate+20Using fewer than 3 SBI products+20

Score ≥ 60 = High disengagement → system activates


💡 Agent 2 — Proactive Advisor Agent

Reads Agent 1's report and picks the best financial recommendation:


Only recommends from the investable surplus (never touches the safety buffer)
Matches recommendations to the customer's goals and risk appetite
Writes a personalized, human-sounding message using LLaMA 3.3 70B



⚡ Agent 3 — Autonomous Action Agent

Checks if the recommended action is compliant and either:


Executes it automatically (low-risk actions like FD sweep)
Sends it for customer approval (investments like SIP, RD)
Blocks it entirely (unknown or non-compliant actions)


Every action is audit logged with timestamp.


🛡️ Safety & Compliance

We take compliance seriously. Every action goes through a 3-tier system:

TierExampleWhat HappensTier 1Informational nudgeNo action neededTier 2Start SIP, Open RDCustomer approval requiredTier 3High-value transferBiometric + OTP required

No money ever moves without the customer's knowledge and consent.


🧰 Tech Stack

ToolPurposePythonCore programming languageLangChainAI agent frameworkGroq APIFree LLM inference (LLaMA 3.3 70B)StreamlitWeb UIFAISSVector store for RAGpython-dotenvSecure API key management


🚀 How to Run This Project

Step 1 — Clone the repo

bashgit clone https://github.com/YOUR_USERNAME/sbi-engagement-agent.git
cd sbi-engagement-agent

Step 2 — Install dependencies

bashpip install -r requirements.txt

Step 3 — Add your Groq API key

Create a .env file in the root folder:

GROQ_API_KEY=gsk_your_key_here

Get a free key at console.groq.com

Step 4 — Run the pipeline (terminal)

bashpython main.py

Step 5 — Run the web UI

bashstreamlit run ui/app.py

Then open http://localhost:8501 in your browser.


📊 Sample Output

============================================================
   SBI AGENTIC AI - DIGITAL ENGAGEMENT SYSTEM
============================================================

[1/3] Running Behavioral Intelligence Agent...
✅ Disengagement Level : High
✅ Disengagement Score : 100/100
✅ Investable Surplus  : ₹58,000

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


🙋 Frequently Asked Questions

Q: Why not just use IF-ELSE rules instead of AI?

A: Rules can prioritize, but they can't write personalized human-sounding messages, reason across conflicting signals (e.g. salary delayed + EMI due = don't suggest SIP right now), or explain recommendations in plain language. The LLM handles all three.

Q: Is customer data safe?

A: Yes. The LLM only receives anonymized behavioral signals, not raw transactions. All data stays within SBI's infrastructure. Customers can revoke access anytime.

Q: Can the AI lose my money?

A: No. The AI never touches your safety buffer. It only works with your investable surplus, and all investment actions require your explicit approval before executing.


👨‍💻 Built By

M V Sita Rama Raju
B.Tech Computer Science | KL University, Hyderabad

📄 License

MIT License — free to use, modify, and distribute.


Built with ❤️ for SBI Hackathon 2026