"""Menu discovery agent node."""

from typing import Literal

from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.types import Command

from agents.prompts import MENU_AGENT_PROMPT
from config import get_llm
from state import StackState
from tools.menu_tools import search_menu_catalog

MENU_TOOLS = [search_menu_catalog]
MENU_TOOL_MAP = {tool.name: tool for tool in MENU_TOOLS}


def menu_agent_node(
    state: StackState,
) -> Command[Literal["synthesizer_node"]]:
    """Search the menu and route the grounded response to the synthesizer."""
    menu_llm = get_llm().bind_tools(MENU_TOOLS)
    messages = [
        SystemMessage(content=MENU_AGENT_PROMPT),
        HumanMessage(content=state["user_query"]),
    ]

    for _ in range(5):
        response = menu_llm.invoke(messages)
        messages.append(response)

        if not response.tool_calls:
            return Command(
                update={"menu_response": str(response.content)},
                goto="synthesizer_node",
            )

        for tool_call in response.tool_calls:
            selected_tool = MENU_TOOL_MAP[tool_call["name"]]
            tool_message = selected_tool.invoke(tool_call)
            messages.append(tool_message)

    return Command(
        update={
            "menu_response": (
                "I couldn't complete the menu search within the tool-call limit."
            )
        },
        goto="synthesizer_node",
    )
