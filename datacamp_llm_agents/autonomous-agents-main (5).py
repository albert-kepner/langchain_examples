from dotenv import load_dotenv

from typing import Annotated

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage
from tools import (
    query_hotels,
    get_weather,
    calculate_total_cost,
    book_room,
    claude_websearch,
)
from utils import print_conversation

load_dotenv()


# SETUP

# Tool definitions (custom, provider, and MCP)
custom_tools = [
    query_hotels,
    calculate_total_cost,
    get_weather,
    book_room,
]
provider_tools = [claude_websearch]
mcp_toolset = {
    "type": "mcp_toolset",
    "mcp_server_name": "time-mcp",
}
all_tools = custom_tools + provider_tools + [mcp_toolset]
mcp_servers = [
    {
        "type": "url",
        "url": "https://time-mcp-optima-teams-projects-bcf90879.vercel.app/mcp",
        "name": "time-mcp",
    }
]

# LLM configuration
llm = init_chat_model(
    model="claude-sonnet-4-5-20250929",
    betas=["mcp-client-2025-04-04"],
    mcp_servers=mcp_servers,
)
llm_with_tools = llm.bind_tools(all_tools)

# Load system message once at setup time
with open("prompt.md", "r") as f:
    system_prompt = f.read()
system_message = SystemMessage(content=system_prompt)


# STATE DEFINITION

from langgraph.graph.message import AnyMessage, add_messages
from typing_extensions import TypedDict


# Define state schema with messages using add_messages reducer
class State(TypedDict):
    """Define the state schema for our hotel assistant.""" ""

    messages: Annotated[list[AnyMessage], add_messages]


# NODE DEFINITIONS


# Reasoning node that processes messages and makes decisions
def reason(state: State) -> dict:
    """Reasoning node: LLM analyzes the current context and decides what to do next."""
    # Combine system message with conversation messages
    messages = [system_message] + state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}


# ACTION NODE

from langgraph.prebuilt import ToolNode

# Action node that executes tool calls
act = ToolNode(custom_tools)

# -----NEW CODE-----#
# CONDITIONAL EDGES (FINAL IMPLEMENTATION)

from langgraph.graph import StateGraph, START, END

from langgraph.prebuilt import tools_condition

# Using prebuilt tools_condition from LangGraph
# Build graph with nodes
hotel_assistant_builder = StateGraph(State)
hotel_assistant_builder.add_node("reason", reason)
hotel_assistant_builder.add_node("act", act)

# Define edges for the ReAct cycle with prebuilt conditional routing
hotel_assistant_builder.add_edge(START, "reason")  # Start with reasoning
hotel_assistant_builder.add_conditional_edges(
    "reason",
    tools_condition,  # Conditionally route to tools if needed
    {"tools": "act", END: END},  # Map tool calls to "act" node
)
hotel_assistant_builder.add_edge("act", "reason")  # After acting, reason again

