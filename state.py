"""Shared graph state definitions."""

from typing import TypedDict


class StackState(TypedDict, total=False):
    """State shared by SnackStack graph nodes."""

    messages: list[str]
    user_query: str
    route: str
    menu_response: str
    order_response: str
    final_answer: str
