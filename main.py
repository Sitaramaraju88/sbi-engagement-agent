from dotenv import load_dotenv
import json
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.behavioral_agent import run_behavioral_agent
from agents.advisor_agent import run_advisor_agent
from agents.action_agent import run_action_agent

load_dotenv()

def run_pipeline(verbose: bool = True) -> dict:
    print("\n" + "="*60)
    print("   SBI AGENTIC AI - DIGITAL ENGAGEMENT SYSTEM")
    print("="*60)

    # Step 1 - Behavioral Agent
    print("\n[1/3] Running Behavioral Intelligence Agent...")
    behavioral_output = run_behavioral_agent()
    if verbose:
        print(f"✅ Disengagement Level : {behavioral_output['disengagement']['disengagement_level']}")
        print(f"✅ Disengagement Score : {behavioral_output['disengagement']['disengagement_score']}/100")
        print(f"✅ Investable Surplus  : ₹{behavioral_output['balance_info']['investable_surplus']}")
        print(f"\n📊 Behavioral Analysis:\n{behavioral_output['analysis']}")

    # Step 2 - Advisor Agent
    print("\n[2/3] Running Proactive Advisor Agent...")
    advisor_output = run_advisor_agent(behavioral_output)
    if verbose:
        print(f"✅ Recommendations Found : {len(advisor_output['recommendations'])}")
        if advisor_output['best_recommendation']:
            print(f"✅ Best Action           : {advisor_output['best_recommendation']['action']}")
            print(f"✅ Amount                : ₹{advisor_output['best_recommendation']['amount']}")
        print(f"\n💬 Personalized Message:\n{advisor_output['personalized_message']}")

    # Step 3 - Action Agent
    print("\n[3/3] Running Autonomous Action Agent...")
    action_output = run_action_agent(advisor_output)
    if verbose:
        print(f"✅ Action Status  : {action_output['status']}")
        print(f"✅ Compliant      : {action_output['compliance']['compliant']}")
        print(f"✅ Audit Logged   : {action_output['compliance']['audit_logged']}")
        print(f"\n📋 Status Update:\n{action_output['status_update']}")

    # Final output
    print("\n" + "="*60)
    print("   PIPELINE COMPLETE")
    print("="*60)

    final_output = {
        "behavioral": behavioral_output,
        "advisor": advisor_output,
        "action": action_output
    }

    return final_output

if __name__ == "__main__":
    result = run_pipeline(verbose=True)
    with open("output.json", "w") as f:
        json.dump(result, f, indent=2)
    print("\n✅ Full output saved to output.json")