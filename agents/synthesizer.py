"""Optional node for merging parallel agent responses."""

from langchain_core.messages import HumanMessage, SystemMessage

from agents.prompts import SYNTHESIZER_PROMPT
from config import get_llm
from state import StackState


def synthesizer_node(state: StackState) -> dict[str, str]:
    """Combine specialist responses into one final answer."""
    specialist_outputs = []

    menu_response = state.get("menu_response")
    order_response = state.get("order_response")

    if menu_response:
        specialist_outputs.append(f"Menu Agent response:\n{menu_response}")

    if order_response:
        specialist_outputs.append(f"Order Agent response:\n{order_response}")

    if not specialist_outputs:
        return {
            "final_answer": ("I couldn't find a specialist response for this request.")
        }

    llm = get_llm()
    combined_outputs = "\n\n".join(specialist_outputs)
    response = llm.invoke(
        [
            SystemMessage(content=SYNTHESIZER_PROMPT),
            HumanMessage(
                content=(
                    "Customer request:\n"
                    f"{state['user_query']}\n\n"
                    "Specialist responses:\n"
                    f"{combined_outputs}"
                )
            ),
        ]
    )

    return {
        "final_answer": str(response.content),
    }
