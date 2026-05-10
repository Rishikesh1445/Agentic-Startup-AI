from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from workflow.state import StartupState


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0.7,
    max_retries=2,
    timeout=60
)


def ceo_agent(state: StartupState):

    prompt = f"""
    You are the CEO of an AI startup company.

    Startup Idea:
    {state['idea']}

    Previous Critic Feedback:
    {state.get('critic_feedback', '')}

    Your task:
    Create a startup strategy proposal.
    Improve the proposal based on criticism.

    Include:
    - target users
    - core product
    - pricing idea
    - unique value proposition

    Improve the proposal if critic feedback exists.
    """

    response = llm.invoke([
        HumanMessage(content=prompt)
    ])

    return {
        "ceo_output": response.content,
        "messages": [response]
    }