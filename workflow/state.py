from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class StartupState(TypedDict):
    idea: str
    ceo_output: str
    critic_feedback: str
    retrieved_memory: str
    websearch:str
    needs_web_search: bool
    approved: bool
    score: float
    iteration: int
    messages: Annotated[Sequence[BaseMessage], add_messages]