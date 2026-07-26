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

