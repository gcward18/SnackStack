"""Shared graph state definitions."""

from typing import TypedDict
from langchain_core.messages import AnyMessage


class StackState(TypedDict, total=False):
    """State shared by SnackStack graph nodes."""

    messages: list[AnyMessage]
    user_query: str
    route: list[str]
    menu_response: str
    order_response: str
    final_answer: str
