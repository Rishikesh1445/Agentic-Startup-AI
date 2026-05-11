from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from workflow.state import StartupState
from memory.chroma import retrieve_memories


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0.7,
    max_retries=2,
    timeout=60
)


def ceo_agent(state: StartupState):

    user_idea = state["idea"]

    retrieved_memory = state.get("retrieved_memory", "")

    if not retrieved_memory and "refer previous" in user_idea.lower():
        print("\n--- Fetching from db... ---")
        retrieved_memory = retrieve_memories(user_idea)

    prompt = f"""
    You are the CEO of an AI startup company.

    Startup Idea:
    {state['idea']}

    Latest Web Research:
    {state.get('websearch', '')}

    Previous Retrieved Memory:
    {retrieved_memory}

    Previous Critic Feedback:
    {state.get('critic_feedback', '')}

    Your task:
    Create a startup strategy proposal.
    Improve the proposal based on criticism.

    Requirements:
        - use retrieved memory if useful
        - use latest market research if available
        - address critic feedback
        - make realistic business decisions

    Include:
        - target users
        - competitors
        - pricing
        - business model
        - differentiation

    Improve the proposal if critic feedback exists and mention it specifically.

    Maximum 500-600 words.
    """

    response = llm.invoke([
        HumanMessage(content=prompt)
    ])

    return {
        "ceo_output": response.content,
        "retrieved_memory": retrieved_memory,
        "messages": [response]
    }