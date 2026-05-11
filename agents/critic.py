from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
from pydantic import BaseModel, Field
from workflow.state import StartupState


class CriticResponse(BaseModel):
    feedback: str = Field(description="Detailed feedback explaining weaknesses and required improvements")
    score: int = Field(description="Score between 0 and 10") 


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0,
    max_retries=2,
    timeout=60
)


def critic_agent(state: StartupState):

    prompt = f"""
    Maximum around 200 words.

    You are a startup critic and evaluator.

    Evaluate this startup proposal carefully.

    Proposal:
    {state['ceo_output']}

    Previous Score:
    {state['score']}

    Previous Feedback:
    {state['critic_feedback']}

    Give:
    1. major failure or critical issues like for example:
    Main Problem 1:
    Main Problem 2:....etc
    2. score out of 10. Reduce score by 2 for each critical issue.

    Dont try to find failure deliberatly. Reasonably and Practically check for issues.
    Dont have a fixed amount of failures to be listed. it can be 0 or more anything. Its okay to give no failure if not found.

    Important:
    - Be practical.
    """

    structured_llm = llm.with_structured_output(CriticResponse)
    
    response = structured_llm.invoke([
        HumanMessage(content=prompt)
    ])

    approve = response.score >= 8

    return {
        "critic_feedback": response.feedback,
        "approved": approve,
        "iteration": state["iteration"] + 1,
        "score": response.score,
        "messages": [AIMessage(content=f"CRITIC FEEDBACK:\n{response.feedback}\n\nSCORE: {response.score}/10\nAPPROVED: {approve}")]
    }