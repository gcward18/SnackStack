"""Request routing and orchestration node."""

from typing import Literal

from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.types import Command
from pydantic import BaseModel, Field

from agents.prompts import ORCHESTRATOR_PROMPT
from config import get_llm
from state import StackState

AgentName = Literal["menu_agent_node", "order_agent_node"]


class RoutingDecision(BaseModel):
    """Validated routing decision produced by the orchestrator."""

    agents: list[AgentName] = Field(
        min_length=1,
        description="Every specialist agent needed for this request.",
    )
    reasoning: str = Field(description="A brief explanation of the routing decision.")


def orchestrator_node(
    state: StackState,
) -> Command[Literal["menu_agent_node", "order_agent_node"]]:
    """Choose the specialist nodes required for the user's request."""
    router_llm = get_llm().with_structured_output(RoutingDecision)
    decision = router_llm.invoke(
        [
            SystemMessage(content=ORCHESTRATOR_PROMPT),
            HumanMessage(content=state["user_query"]),
        ]
    )

    return Command(
        update={
            "route": decision.agents,
            "routing_reason": decision.reasoning,
        },
        goto=decision.agents,
    )
