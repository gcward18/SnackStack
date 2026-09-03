"""Order status agent node."""

import re
from langchain_core.messages import HumanMessage, SystemMessage
from typing import Literal
from agents.prompts import ORDER_AGENT_PROMPT
from langgraph.types import Command, interrupt
from config import get_llm
from state import StackState
from tools.order_tools import get_order_status

ORDER_ID_PATTERN = r"\bORD-\d+\b"
TRACKING_PATTERN = r"\bSS\d+TRK\b"
EMAIL_PATTERN = r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b"
ORDER_TOOLS = [get_order_status]

ORDER_TOOL_MAP = {tool.name: tool for tool in ORDER_TOOLS}


def extract_identifier(text: str) -> str | None:
    for pattern in (
        ORDER_ID_PATTERN,
        TRACKING_PATTERN,
        EMAIL_PATTERN,
    ):
        match = re.search(pattern, text, flags=re.IGNORECASE)

        if match:
            return match.group(0)

    return None


def order_agent_node(
    state: StackState,
) -> Command[str]:
    user_query = state["user_query"]
    identifier = extract_identifier(state["user_query"])

    if not identifier:
        resumed_value = interrupt(
            {
                "question": (
                    "Please provide your order ID, tracking ID, or customer email."
                )
            }
        )

    identifier = extract_identifier(str(resumed_value))

    if not identifier:
        return Command(
            update={
                "order_response": (
                    "I couldn't identify a valid order id, tracking id, email address."
                )
            },
            goto="synthesizer_node",
        )

    llm_with_tools = get_llm().bind_tools(ORDER_TOOLS)

    messages = [
        SystemMessage(content=ORDER_AGENT_PROMPT),
        HumanMessage(
            content=(f"Customer request: {user_query}\nOrder identifier: {identifier}")
        ),
    ]

    for _ in range(5):
        response = llm_with_tools.invoke(messages)
        messages.append(response)

        if not response.tool_calls:
            return Command(
                update={
                    "order_response": str(response.content),
                },
                goto="synthesizer_node",
            )

        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            selected_tool = ORDER_TOOL_MAP.get(tool_name)

            if selected_tool is None:
                return Command(
                    update={
                        "order_response": (
                            f"The model requested an unknown tool: {tool_name}."
                        )
                    },
                    goto="synthesizer_node",
                )

            tool_message = selected_tool.invoke(tool_call)
            messages.append(tool_message)

    return Command(
        update={
            "order_response": (
                "I couldn't complete the order lookup within the tool-call limit."
            )
        },
        goto="synthesizer_node",
    )
