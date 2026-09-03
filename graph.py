"""SnackStack StateGraph construction and compilation."""

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph

from agents.menu_agent import menu_agent_node
from agents.orchestrator import orchestrator_node
from agents.order_agent import order_agent_node
from agents.synthesizer import synthesizer_node
from state import StackState


def build_graph():
    """Build and compile the SnackStack workflow."""
    builder = StateGraph(StackState)
    builder.add_node("orchestrator_node", orchestrator_node)
    builder.add_node("menu_agent_node", menu_agent_node)
    builder.add_node("order_agent_node", order_agent_node)
    builder.add_node("synthesizer_node", synthesizer_node)

    builder.add_edge(START, "orchestrator_node")
    builder.add_edge("synthesizer_node", END)

    return builder.compile(checkpointer=InMemorySaver())


compiled_graph = build_graph()
