import sys
import os

# Add the parent directory to the Python path so we can import the workflow
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
# Load environment variables BEFORE importing workflow modules which instantiate models
load_dotenv()

import streamlit as st
from workflow.workflow import graph

# Set up the page layout
st.set_page_config(
    page_title="AI Startup Builder",
    page_icon="🚀",
    layout="centered"
)

# App header
st.title("🚀 AI Startup Builder")
st.markdown("Enter your startup idea below, and our AI agents will research, propose, and critique a business strategy for you.")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Custom CSS for the helper text
st.markdown(
    """
    <style>
    .helper-text {
        font-size: 0.8rem;
        color: gray;
        text-align: center;
        margin-bottom: 10px;
    }
    </style>
    <div class="helper-text">
        💡 Use the "refer previous" keyword in your prompt to look up past ideas from memory!
    </div>
    """,
    unsafe_allow_html=True
)

# Chat input - automatically disables while the code inside the if block is running
if prompt := st.chat_input("E.g., An AI fitness startup for college students"):
    
    # Display user prompt in chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # Setup the initial state for LangGraph
    initial_state = {
        "idea": prompt,
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
    
    # Run the graph and stream results
    with st.spinner("Agents are analyzing your idea..."):
        
        # We will use this placeholder to smoothly add new messages
        status_container = st.container()
        
        for event in graph.stream(initial_state):
            for node_name, state_update in event.items():
                
                # Fetch the latest message added to the state by the agent
                if "messages" in state_update and state_update["messages"]:
                    latest_msg = state_update["messages"][-1].content
                    
                    st.session_state.messages.append({"role": "assistant", "content": f"**[{node_name.upper()}]**\n\n{latest_msg}"})
                    
                    with status_container.chat_message("assistant"):
                        # Streamlit automatically renders Markdown cleanly
                        st.markdown(f"**[{node_name.upper()}]**\n\n{latest_msg}")
                        
                # If the critic provides a final decision score
                if node_name == "critic" and "approved" in state_update:
                    status = "✅ APPROVED" if state_update["approved"] else "❌ REJECTED (Needs improvement)"
                    score = state_update.get("score", "N/A")
                    decision_msg = f"**Decision:** {status} | **Score:** {score}/10"
                    
                    st.session_state.messages.append({"role": "assistant", "content": decision_msg})
                    with status_container.chat_message("assistant"):
                        st.markdown(decision_msg)
                        
    st.success("Workflow Complete!")
