from langgraph.graph import StateGraph, END
from langgraph.types import RetryPolicy

from workflow.state import StartupState

from agents.ceo import ceo_agent
from agents.critic import critic_agent


def decide_next(state: StartupState):

    if state["approved"]:
        return END

    if state["iteration"] >= 3:
        return END

    return "ceo"


builder = StateGraph(StartupState)

builder.add_node(
    "ceo", 
    ceo_agent, 
    retry=RetryPolicy(
        initial_interval=5.0,
        max_interval=60.0,
        backoff_factor=2.0,
    )
)
builder.add_node(
    "critic",
    critic_agent,
    retry=RetryPolicy(
        initial_interval=5.0,
        max_interval=60.0,
        backoff_factor=2.0,
    )
)

builder.set_entry_point("ceo")

builder.add_edge("ceo", "critic")

builder.add_conditional_edges(
    "critic",
    decide_next
)

graph = builder.compile()