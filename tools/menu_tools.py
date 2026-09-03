"""Tools for searching the menu catalog."""

from typing import Any

from langchain.tools import tool

from tools.rag import get_retriever


@tool
def search_menu_catalog(query: str) -> list[dict[str, Any]]:
    """Search the menu for dishes matching the users preferences.

    Use this tool for requests involving cuisine, dietary preferences,
    ingredients, prices, ratings, or dish recommendations.

    Args:
        query: A natural-language description of the desired food.

    Returns:
        Matching menu items ordered by semantic relevance.
    """

    retriever = get_retriever()
    documents = retriever.invoke(query)

    return [
        {"description": document.page_content, **document.metadata}
        for document in documents
    ]
