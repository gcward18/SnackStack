"""SnackStack order database access."""
from langchain_core.documents import Document

orders = [
    {
        "Order ID": "ORD-201",
        "Item": "Butter Chicken",
        "Customer": "Priya Nair",
        "Status": "Out for Delivery",
        "Tracking": "SS201TRK",
        "Email": "priya@example.com",
    },
    {
        "Order ID": "ORD-202",
        "Item": "Margherita Pizza",
        "Customer": "Arjun Mehta",
        "Status": "Placed",
        "Tracking": "SS202TRK",
        "Email": "arjun@example.com",
    },
    {
        "Order ID": "ORD-203",
        "Item": "Cheeseburger",
        "Customer": "Sneha Roy",
        "Status": "Preparing",
        "Tracking": "SS203TRK",
        "Email": "sneha@example.com",
    },
    {
        "Order ID": "ORD-204",
        "Item": "Buddha Bowl",
        "Customer": "Rahul Das",
        "Status": "Delivered",
        "Tracking": "SS204TRK",
        "Email": "rahul@example.com",
    },
    {
        "Order ID": "ORD-205",
        "Item": "Paneer Tikka",
        "Customer": "Kavya Sharma",
        "Status": "Placed",
        "Tracking": "SS205TRK",
        "Email": "kavya@example.com",
    },
]

def get_order(order_id: str) -> list[dict[str, str]]:
    """Get orders into LangChain Documents."""
    return next(
        (order for order in orders if order["Order ID"] == order_id),
        None,
    )
