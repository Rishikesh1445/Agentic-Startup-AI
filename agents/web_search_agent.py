from workflow.state import StartupState
from langchain_core.messages import AIMessage

from tools.web_search import search_web


def web_search_agent(state: StartupState):
    
    print("\n--- Initiating Web Search... ---")

    query = f"""
    Startup idea:
    {state['idea']}

    Find:
    - competitors
    - market trends
    - pricing models
    - industry insights
    """

    web_results = search_web(query)

    return {
        "websearch": web_results,
        "messages": [AIMessage(content=f"WEB SEARCH RESULTS:\n{web_results}")]
    }