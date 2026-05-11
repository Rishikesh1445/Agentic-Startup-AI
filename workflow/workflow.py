from langgraph.graph import StateGraph, END
from langgraph.types import RetryPolicy

from workflow.state import StartupState

from agents.ceo import ceo_agent
from agents.critic import critic_agent
from agents.research_decision import research_decision_agent
from agents.web_search_agent import web_search_agent

from memory.chroma import store_startup_memory


def decide_next(state: StartupState):

    if state["approved"]:
        return "save_memory"

    if state["iteration"] >= 3:
        return "save_memory"

    return "ceo"

def route_research(state: StartupState):

    if state["needs_web_search"]:
        return "web_search"

    return "ceo"

def save_memory_node(state: StartupState):
    print("\n--- Saving in db... ---")
    store_startup_memory(
        idea=state["idea"],
        proposal=state["ceo_output"]
    )

    return state


builder = StateGraph(StartupState)

builder.add_node(
    "research_decision",
    research_decision_agent, 
    retry=RetryPolicy(
        initial_interval=5.0,
        max_interval=60.0,
        backoff_factor=2.0,
    )
)

builder.add_node(
    "web_search",
    web_search_agent,
    retry=RetryPolicy(
        initial_interval=5.0,
        max_interval=60.0,
        backoff_factor=2.0,
        max_attempts=2,
    )
)

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

builder.add_node("save_memory", save_memory_node)

builder.set_entry_point(
    "research_decision"
)

builder.add_conditional_edges(
    "research_decision",
    route_research
)

builder.add_edge(
    "web_search",
    "ceo"
)

builder.add_edge("ceo", "critic")

builder.add_conditional_edges(
    "critic",
    decide_next
)

builder.add_edge("save_memory", END)

graph = builder.compile()