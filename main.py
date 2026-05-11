from dotenv import load_dotenv

load_dotenv()

from workflow.workflow import graph


initial_state = {
    "idea": "AI in bathroom",
    "ceo_output": "",
    "critic_feedback": "",
    "retrieved_memory": "",
    "websearch": "",
    "needs_web_search": False,
    "score": 0,
    "approved": False,
    "iteration": 0,
    "messages": []
}

print("Starting Startup AI Workflow...\n")

for event in graph.stream(initial_state):
    for node_name, state_update in event.items():
        print("\n" + "="*80)
        print(f"UPDATE FROM {node_name.upper()}")
        print("="*80)
        
        if "messages" in state_update and state_update["messages"]:
            # Print the newest message added by this node
            print(state_update["messages"][-1].content)

        if node_name == "critic" and "approved" in state_update:
            status = "APPROVED" if state_update["approved"] else "REJECTED (Needs improvement)"
            score = state_update.get("score", "N/A")
            print(f"\n--- Decision: {status} | Score: {score}/10 ---")
        

print("\n" + "="*80)
print("WORKFLOW COMPLETED")
print("="*80)