from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage

from workflow.state import StartupState


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    max_retries=2,
    timeout=60
)


def research_decision_agent(state: StartupState):

    print("\n--- Deciding Research Necessity... ---")
    
    prompt = f"""
    You are a research planning agent.

    User Startup Idea:
    {state['idea']}

    Decide whether latest internet data is NECESSARY.

    Web search is needed ONLY IF:
    - competitor analysis required
    - market trends required
    - latest pricing needed
    - latest startup landscape needed
    - recent technology/business trends matter

    Web search is NOT needed for:
    - generic brainstorming
    - simple startup ideas
    - timeless concepts

    Respond ONLY:

    YES

    or

    NO
    """

    response = llm.invoke([
        HumanMessage(content=prompt)
    ])

    answer = response.content.strip().upper()
    needs_search = "YES" in answer

    return {
        "needs_web_search": needs_search,
        "messages": [AIMessage(content=f"RESEARCH DECISION:\nWeb search needed? {needs_search}\nDetails: {answer}")]
    }