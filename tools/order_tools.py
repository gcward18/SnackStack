"""Tools for retrieving order status."""
from typing import Any
from langchain.tools import tool
from data.orders import get_order

@tool
def get_order_status(identifier: str) -> dict[str, Any]:
    """Retrieve an order using an order ID, tracking ID, or email address.

    Use this tool when a customer asks about an existing order and provides
    one of these identifiers.

    Args:
        identifier: An order ID, tracking ID, or customer email address.

    Returns:
        The matching order details or a not-found message.

    """
    order = get_order(identifier)

    if not order:
        return {
            "error": "No order found with that identifier"
        }

    return order